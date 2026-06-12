"""
AI Call Assistant - Generalized Version
========================================
A multi-platform AI assistant that records conversations, transcribes them in real-time,
provides live feedback, and generates structured session reports.

Perfect for: tutoring sessions, team meetings, interviews, project reviews, etc.

Configuration: Edit config.json to customize participants, session numbers, and prompts.
"""

import soundcard as sc
import numpy as np
import requests
import json
import threading
import queue
import time
import io
import wave
import base64
import sys
import os
import logging
from pathlib import Path

# Optional: Load .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, environment variables must be set manually

# =================================================
# LOGGING CONFIGURATION
# =================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# =================================================
# API CONFIGURATION
# =================================================
# Load API key from environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    logger.error("OPENROUTER_API_KEY environment variable not set!")
    logger.info("Please create a .env file or set the variable: export OPENROUTER_API_KEY='your-key'")
    sys.exit(1)

# Model Configuration - Can be overridden via environment variables
LLM_MODEL = os.getenv("LLM_MODEL", "qwen/qwen3-vl-30b-a3b-instruct")
AUDIO_MODEL = os.getenv("AUDIO_MODEL", "openai/whisper-large-v3-turbo")

# =================================================
# AUDIO CONFIGURATION
# =================================================
SAMPLE_RATE = 16000  # Audio sample rate in Hz
CHUNK_DURATION = 5   # Duration of each audio chunk in seconds
AUDIO_CHANNELS = 1   # Mono audio
AUDIO_SAMPLE_WIDTH = 2  # 16-bit audio

# =================================================
# TRANSCRIPTION CONFIGURATION
# =================================================
LIVE_BUFFER_THRESHOLD = 250  # Characters before triggering live analysis
MIN_TEXT_LENGTH = 3  # Minimum text length to consider valid transcription

# =================================================
# CONFIGURATION AND FILE LOADER
# =================================================

def load_config():
    """
    Loads configuration from config.json

    Expected structure:
    {
      "participants": ["Name1", "Name2", ...],
      "current_session": 1,
      "output_file": "Report.md",
      "whisper_keywords": ["keyword1", "keyword2", ...],
      "hallucination_filter": ["phrase1", "phrase2", ...],
      "speaker_label": "Speaker",
      "listener_label": "Listeners"
    }
    """
    config_path = Path(__file__).parent / "config.json"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"config.json not found at {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing config.json: {e}")
        sys.exit(1)

def load_text_file(filepath):
    """Loads a text file and returns its content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        sys.exit(1)

def get_session_content(session_number):
    """
    Loads the content/task description for a specific session.
    Looks for: sessions/session_X.txt
    """
    session_path = Path(__file__).parent / "sessions" / f"session_{session_number}.txt"
    return load_text_file(session_path)

def get_prompt(prompt_name):
    """
    Loads a prompt from the prompts/ folder.
    New structure: prompts/live_analysis/default.txt or prompts/final_report/default.txt
    Falls back to old structure if new folders don't exist.
    """
    # Try new structure first (from config if specified)
    config_key = f"active_{prompt_name}_prompt"
    active_prompt = CONFIG.get(config_key, "default")

    new_prompt_path = Path(__file__).parent / "prompts" / prompt_name / f"{active_prompt}.txt"
    if new_prompt_path.exists():
        return load_text_file(new_prompt_path)

    # Fallback to default if specified prompt doesn't exist
    default_prompt_path = Path(__file__).parent / "prompts" / prompt_name / "default.txt"
    if default_prompt_path.exists():
        return load_text_file(default_prompt_path)

    # Fallback to old structure for backward compatibility
    old_prompt_path = Path(__file__).parent / "prompts" / f"{prompt_name}.txt"
    return load_text_file(old_prompt_path)

# =================================================
# LOAD CONFIGURATION
# =================================================
CONFIG = load_config()

# Extract configuration values
PARTICIPANTS = CONFIG["participants"]
CURRENT_SESSION = CONFIG["current_session"]
OUTPUT_FILE = CONFIG["output_file"]
WHISPER_KEYWORDS = CONFIG["whisper_keywords"]
HALLUCINATION_FILTER = CONFIG["hallucination_filter"]
SPEAKER_LABEL = CONFIG.get("speaker_label", "Speaker")  # Default: "Speaker"
LISTENER_LABEL = CONFIG.get("listener_label", "Listeners")  # Default: "Listeners"

logger.info(f"Configuration loaded: Session {CURRENT_SESSION}, {len(PARTICIPANTS)} participants")

# =================================================
# QUEUES FOR DATA EXCHANGE
# =================================================
audio_queue = queue.Queue()  # Queue for audio chunks
live_text_queue = queue.Queue()  # Queue for live feedback during call
full_transcript = []  # Storage for final report at the end

# =================================================
# AUDIO PROCESSING
# =================================================

def numpy_to_wav_buffer(audio_data, sample_rate=SAMPLE_RATE):
    """
    Converts raw audio stream from memory to playable .wav format.

    Args:
        audio_data: NumPy array with audio samples
        sample_rate: Sample rate in Hz

    Returns:
        BytesIO buffer containing WAV file, or None on error
    """
    if audio_data is None or len(audio_data) == 0:
        logger.warning("Received empty audio data")
        return None

    try:
        # Convert float32 to int16
        audio_data_int = np.int16(audio_data * 32767)
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wf:
            wf.setnchannels(AUDIO_CHANNELS)
            wf.setsampwidth(AUDIO_SAMPLE_WIDTH)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data_int.tobytes())
        buffer.seek(0)
        return buffer
    except Exception as e:
        logger.error(f"Error converting audio: {e}")
        return None

# =================================================
# LIVE ANALYSIS WORKER
# =================================================

def live_analysis_worker():
    """
    Thread 3: Provides short, constructive live feedback DURING the call.

    This worker continuously monitors the conversation and provides
    real-time insights based on the live_analysis prompt.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Load prompt once at startup
    system_prompt = get_prompt("live_analysis")

    while True:
        live_chunk = live_text_queue.get()
        if live_chunk is None:
            break

        data = {
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Current conversation:\n{live_chunk}"}
            ]
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
            if response.status_code == 200:
                ai_message = response.json()['choices'][0]['message']['content']
                logger.info(f"\n✨ LIVE ASSISTANT:\n{ai_message}\n" + "-"*30)
            else:
                logger.warning(f"Live analysis failed: {response.status_code}")
        except requests.exceptions.Timeout:
            logger.warning("Live analysis timeout")
        except Exception as e:
            logger.error(f"Error in live analysis: {e}")

        live_text_queue.task_done()

# =================================================
# REPORT GENERATION
# =================================================

def generate_participants_table(participants_list):
    """
    Generates HTML table rows for participants dynamically.

    Args:
        participants_list: List of participant names

    Returns:
        String containing HTML table rows
    """
    rows = []
    for participant in participants_list:
        row = f"""
<tr>
<td>

**{participant}**
</td>
<td>

**Contribution [X]%**
<br>
[Area/Role]

</td>
<td>
<i>

[Notes]

</i>
</td>
</tr>"""
        rows.append(row)
    return '\n'.join(rows)

def generate_final_report():
    """
    Called at the end of the call (via Ctrl+C) to generate the final report.

    This function:
    1. Processes the full transcript
    2. Sends it to the LLM with the final_report prompt
    3. Generates a structured report
    4. Saves it to the configured output file
    """
    if not full_transcript:
        logger.warning("No text collected. Aborting report generation.")
        return

    logger.info("\n" + "="*50)
    logger.info("🎙️ CALL ENDED. GENERATING FINAL REPORT... PLEASE WAIT.")
    logger.info("="*50 + "\n")

    transcript_text = "\n".join(full_transcript)
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Load prompt template and session content
    prompt_template = get_prompt("final_report")
    session_content = get_session_content(CURRENT_SESSION)

    # Replace placeholders
    participants_list_text = ", ".join(PARTICIPANTS)
    participants_table_html = generate_participants_table(PARTICIPANTS)

    system_prompt = prompt_template.replace("{participants_list}", participants_list_text)
    system_prompt = system_prompt.replace("{session_content}", session_content)
    system_prompt = system_prompt.replace("{session_number}", str(CURRENT_SESSION))
    system_prompt = system_prompt.replace("{participants_table}", participants_table_html)

    data = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Transcript:\n{transcript_text}"}
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
        response.raise_for_status()
        ai_message = response.json()['choices'][0]['message']['content']

        logger.info(f"\n{ai_message}\n")

        # Clean up markdown code blocks if present
        clean_text = ai_message.strip()
        if clean_text.startswith("```markdown"):
            clean_text = clean_text[11:].strip()
        elif clean_text.startswith("```"):
            clean_text = clean_text[3:].strip()

        if clean_text.endswith("```"):
            clean_text = clean_text[:-3].strip()

        # Save to file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(clean_text)

        logger.info("="*50)
        logger.info(f"✅ SUCCESS: Report saved as '{OUTPUT_FILE}'!")
        logger.info("="*50)

    except requests.exceptions.Timeout:
        logger.error("Timeout during report generation (>60s)")
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during report generation: {e}")
    except Exception as e:
        logger.error(f"Error during report generation: {e}")

# =================================================
# TRANSCRIPTION WORKER
# =================================================

def transcription_worker():
    """
    Thread 2: Sends audio to Whisper and distributes text to live AI and final storage.

    This worker:
    1. Receives audio chunks from the audio queue
    2. Sends them to Whisper API for transcription
    3. Filters out hallucinations
    4. Adds transcripts to full_transcript for final report
    5. Sends chunks to live_text_queue for real-time analysis
    """
    logger.info(f"OpenRouter API ready for cloud transcription ({AUDIO_MODEL})")

    url = "https://openrouter.ai/api/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    live_buffer = ""

    while True:
        label, audio_data = audio_queue.get()
        if audio_data is None:
            logger.info("Transcription worker stopped")
            break

        # Convert audio to WAV format
        wav_buffer = numpy_to_wav_buffer(audio_data)
        if wav_buffer is None:
            audio_queue.task_done()
            continue

        # Encode as base64
        wav_bytes = wav_buffer.read()
        base64_audio = base64.b64encode(wav_bytes).decode('utf-8')

        data = {
            "model": AUDIO_MODEL,
            "language": "de",  # Change to "en" for English or remove for auto-detection
            "input_audio": {
                "data": base64_audio,
                "format": "wav"
            },
            # Keywords from config for better recognition
            "prompt": ", ".join(WHISPER_KEYWORDS)
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)

            if response.status_code == 200:
                chunk_text = response.json().get("text", "").strip()
                text_lower = chunk_text.lower()

                # Filter hallucinations
                is_ghost = any(h in text_lower for h in HALLUCINATION_FILTER)

                if chunk_text and not is_ghost and len(chunk_text) > MIN_TEXT_LENGTH:
                    labeled_text = f"[{label}]: {chunk_text}"
                    logger.info(labeled_text)

                    # 1. Store for final report
                    full_transcript.append(labeled_text)

                    # 2. Collect for live analysis
                    live_buffer += " " + labeled_text
                    if len(live_buffer) > LIVE_BUFFER_THRESHOLD:
                        live_text_queue.put(live_buffer.strip())
                        live_buffer = ""
            else:
                logger.warning(f"OpenRouter Audio API error: {response.status_code}")

        except requests.exceptions.Timeout:
            logger.warning("Whisper API timeout")
        except Exception as e:
            logger.error(f"Network error with Whisper API: {e}")

        audio_queue.task_done()

# =================================================
# AUDIO RECORDING
# =================================================

def record_audio(device, label, sample_rate=SAMPLE_RATE, chunk_duration=CHUNK_DURATION):
    """
    Records audio from device and puts it in the queue.

    Args:
        device: soundcard device object
        label: Label for this audio source (appears in transcript)
        sample_rate: Sample rate in Hz
        chunk_duration: Duration of each chunk in seconds
    """
    try:
        logger.info(f"Audio recording started for: {label}")
        with device.recorder(samplerate=sample_rate) as recorder:
            while True:
                data = recorder.record(numframes=sample_rate * chunk_duration)
                mono_data = np.mean(data, axis=1)
                audio_queue.put((label, mono_data))
    except Exception as e:
        logger.error(f"Error recording from {label}: {e}")

# =================================================
# MAIN FUNCTION
# =================================================

def main():
    """
    Main function - starts all worker threads and coordinates the workflow.

    Process:
    1. Start transcription and analysis workers
    2. Initialize audio devices (loopback + microphone)
    3. Start recording threads
    4. Wait for Ctrl+C to stop
    5. Generate final report
    """
    logger.info("Starting worker threads...")
    transcription_thread = threading.Thread(target=transcription_worker, daemon=True)
    analysis_thread = threading.Thread(target=live_analysis_worker, daemon=True)
    transcription_thread.start()
    analysis_thread.start()

    try:
        # Initialize audio devices
        speaker = sc.default_speaker()
        listener_device = sc.get_microphone(id=str(speaker.name), include_loopback=True)
        speaker_device = sc.default_microphone()
    except Exception as e:
        logger.error(f"Error initializing audio devices: {e}")
        sys.exit(1)

    logger.info("="*50)
    logger.info("🚀 AI CALL ASSISTANT STARTED")
    logger.info(f"- Listening to {LISTENER_LABEL} (Loopback): {speaker.name}")
    logger.info(f"- Listening to {SPEAKER_LABEL} (Microphone): {speaker_device.name}")
    logger.info("\nFeatures:")
    logger.info("1. Provides real-time feedback during the call")
    logger.info("2. Generates structured session report when finished")
    logger.info(f"\nPress Ctrl+C to end the call and generate '{OUTPUT_FILE}'!")
    logger.info("="*50 + "\n")

    # Start recording threads
    listener_thread = threading.Thread(target=record_audio, args=(listener_device, LISTENER_LABEL), daemon=True)
    speaker_thread = threading.Thread(target=record_audio, args=(speaker_device, SPEAKER_LABEL), daemon=True)
    listener_thread.start()
    speaker_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\n🛑 Stopping recording and generating report...")

        # Clean shutdown of workers
        audio_queue.put(("shutdown", None))
        live_text_queue.put(None)

        # Wait briefly for queues to empty
        time.sleep(2)

        # Generate final report
        generate_final_report()

        logger.info("Program terminated.")
        sys.exit(0)

if __name__ == "__main__":
    main()
