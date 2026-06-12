# GUI Quick Start Guide

Get started with the AI Call Assistant GUI in 3 minutes!

## Prerequisites

1. Python 3.8+ installed
2. OpenRouter API Key ([Get one here](https://openrouter.ai/))
3. Working microphone and speakers

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Launch

```bash
python CallAssistantGUI.py
```

## First-Time Setup

### 1. API Configuration

![API Configuration Section]

- **OpenRouter API Key**: Paste your API key
  - Get your key from https://openrouter.ai/keys
  - The key will be hidden for security
- **LLM Model**: Keep default or choose:
  - `qwen/qwen3-vl-30b-a3b-instruct` (recommended - cheap)
  - `anthropic/claude-3-opus` (premium - best quality)
  - `openai/gpt-4-turbo` (premium - fast)
- **Audio Model**: Keep default `openai/whisper-large-v3-turbo`

### 2. Session Configuration

- **Participants**: Enter names separated by commas
  - Example: `Alice, Bob, Charlie`
- **Session Number**: Set to `1` for first session
- **Output File**: Name for your report
  - Example: `Meeting_Notes.md` or `Session_1_Report.md`
- **Speaker Label**: Your microphone source
  - Examples: `Moderator`, `Tutor`, `Me`, `Host`
- **Listener Label**: The other audio source (loopback)
  - Examples: `Participants`, `Students`, `Guest`, `Team`

### 3. Create Session File

Create a file named `sessions/session_1.txt` with your session objectives:

```
Session 1 - Team Meeting
========================

OBJECTIVES:
Discuss project progress and next steps

KEY GOALS:
1. Review completed tasks
2. Identify blockers
3. Plan next sprint

SUCCESS CRITERIA:
- All tasks reviewed
- Blockers documented
- Sprint plan agreed
```

### 4. (Optional) Customize AI Prompts

Want to change how the AI behaves? Click **Edit Prompts** at the bottom:

1. Select a prompt type (Live Analysis or Final Report)
2. Click **Load** to view the current prompt
3. Edit the text to customize AI behavior
4. Click **Save Changes** when done

**What you can customize:**
- Tone and style of feedback
- Report structure and sections
- Level of detail
- Focus areas (technical, general, specific topics)

### 5. Save and Start

1. Click **Save Configuration**
2. Click **Start Recording**
3. Have your meeting/call
4. Click **Stop & Generate Report** when done
5. Open your report file (e.g., `Meeting_Notes.md`)

## Quick Tips

### API Key Management

**Option 1: Enter in GUI** (easiest)
- Just paste it in the GUI
- Will be saved for next time

**Option 2: .env file** (recommended)
```bash
# Create .env file
echo OPENROUTER_API_KEY=sk-or-v1-your-key-here > .env
```

### Model Selection Guide

**For daily use (cheap):**
- LLM: `qwen/qwen3-vl-30b-a3b-instruct`
- Cost: ~$0.30/hour

**For important meetings (premium):**
- LLM: `anthropic/claude-3-opus`
- Cost: ~$2-3/hour
- Better analysis quality

**For transcription only:**
- Keep default Whisper model
- Very accurate, good price

### Troubleshooting

**"OPENROUTER_API_KEY not set"**
- Enter your API key in the GUI
- Or create a `.env` file with your key

**"Session file not found"**
- Create `sessions/session_1.txt` (or the number you set)
- Or change Session Number to an existing session

**No transcription appearing**
- Check your internet connection
- Ensure your microphone is working
- Check audio device settings in your OS

**GUI won't start**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check if Tkinter is available: `python -m tkinter`

### Use Case Examples

**Team Meeting:**
```
Participants: Alice, Bob, Charlie
Session Number: 1
Speaker Label: Moderator
Listener Label: Team
Output File: Team_Meeting_2026_06_12.md
```

**1-on-1 Interview:**
```
Participants: Candidate, Interviewer
Session Number: 1
Speaker Label: Interviewer
Listener Label: Candidate
Output File: Interview_Candidate_Name.md
```

**Tutoring Session:**
```
Participants: Student1, Student2, Student3
Session Number: 2
Speaker Label: Tutor
Listener Label: Students
Output File: Milestone_2_Report.md
```

**Podcast Recording:**
```
Participants: Host, Guest
Session Number: 1
Speaker Label: Host
Listener Label: Guest
Output File: Podcast_Episode_5.md
```

## Live Display

While recording, the GUI shows:
- Real-time transcripts with speaker labels
- AI insights and suggestions (every ~250 characters)
- Status messages
- Any errors or warnings

**Colors:**
- Blue = Information
- Red = Errors
- Green = Success

## After Recording

Your report will contain:
- Session overview table
- Participant contributions
- Key discussions
- AI insights
- Action items (if mentioned)

Open the file in any markdown viewer or editor:
- VS Code
- Typora
- Obsidian
- GitHub (if you push it)

## Cost Optimization

To reduce API costs:

1. **Use cheaper models:**
   - Qwen instead of Claude/GPT-4

2. **Shorter sessions:**
   - Only record important parts

3. **Disable live analysis** (advanced):
   - Edit `CallAssistant.py`
   - Comment out the live analysis worker

4. **Longer audio chunks** (advanced):
   - Edit `CallAssistant.py`
   - Increase `CHUNK_DURATION` from 5 to 10 seconds

## Need Help?

- **Documentation**: See full [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/FarshadAhmadi089/Multiplattform-KI-Call-Assistant/issues)
- **Configuration**: See [Configuration Guide](README.md#-configuration-guide)

## Happy Recording!

You're all set! Launch the GUI and start your first session.

```bash
python CallAssistantGUI.py
```

Questions? Check the full documentation in README.md
