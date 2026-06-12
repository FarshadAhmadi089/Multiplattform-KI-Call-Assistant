# AI Call Assistant - Multi-Platform Edition

An intelligent AI assistant that automatically records conversations, transcribes them in real-time, provides live feedback, and generates structured session reports.

Perfect for: team meetings, code reviews, interviews, project check-ins, and any scenario where you need AI-powered conversation analysis and documentation.

---

## ✨ Features

- 🎤 **Dual-Audio Recording**: Captures both speaker and listener audio streams simultaneously
- 🗣️ **Real-Time Transcription**: Uses OpenRouter Whisper API for accurate speech-to-text
- 💡 **Live Analysis**: Provides constructive feedback and insights during the conversation
- 📊 **Automatic Report Generation**: Creates structured markdown reports with participant breakdown
- ⚙️ **Highly Configurable**: All prompts, participants, and settings externally manageable
- 🌍 **Multi-Language Support**: Works with German, English, and other languages supported by Whisper
- 🖥️ **Graphical User Interface**: Easy-to-use GUI for configuration and control
- ✏️ **Visual Prompt Editor**: Customize AI behavior directly in the GUI without editing files

---

## 🎛️ Two Ways to Use

### Option 1: Graphical User Interface (Recommended for Beginners)

The easiest way to use the AI Call Assistant is through the graphical interface:

```bash
python CallAssistantGUI.py
```

**Features of the GUI:**
- Visual configuration of all settings (no config file editing needed)
- API key and model selection with dropdowns
- Real-time transcript and AI feedback display
- One-click Start/Stop recording
- Automatic configuration saving
- Status indicators and error messages
- Built-in prompt editor for customizing AI behavior

**Perfect for:**
- First-time users
- Quick configuration changes
- Visual feedback during recording
- Users who prefer graphical interfaces

### Option 2: Command Line (Advanced Users)

For advanced users who prefer terminal-based workflows:

```bash
python CallAssistant.py
```

**Perfect for:**
- Automation and scripting
- Server deployments
- Minimal resource usage
- Integration with other tools

---

## 📁 Project Structure

```
Multiplattform-KI-Call-Assistant/
├── CallAssistant.py             # Main program (command-line)
├── CallAssistantGUI.py          # Graphical User Interface
├── config.json                  # Configuration (participants, session, etc.)
├── config.example.json          # Configuration template with detailed comments
├── requirements.txt             # Python dependencies
├── .env.example                 # Template for environment variables
├── .env                         # Your local secrets (DO NOT commit!)
├── .gitignore                   # Git ignore rules
│
├── prompts/                     # AI prompts (customizable)
│   ├── live_analysis.txt        # Real-time feedback prompt
│   └── final_report.txt         # Session report template
│
└── sessions/                    # Session objectives/requirements
    ├── session_1.txt            # Session 1 objectives
    ├── session_2.txt            # Session 2 objectives
    └── session_3.txt            # Session 3 objectives
```

---

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.8+** installed
- **OpenRouter API Key** ([Get one here](https://openrouter.ai/))
- **Audio devices**: Microphone + speakers/headphones for loopback recording

### 2. Clone Repository

```bash
git clone https://github.com/FarshadAhmadi089/Multiplattform-KI-Call-Assistant.git
cd Multiplattform-KI-Call-Assistant
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `soundcard` - Cross-platform audio capture
- `numpy` - Audio processing
- `requests` - API communication
- `python-dotenv` - Environment variable management (optional)

### 4. Configure API Key

**Option A: Using .env file (recommended)**

```bash
# Copy template
cp .env.example .env

# Edit .env and add your API key
# OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

**Option B: Set environment variable manually**

```powershell
# Windows PowerShell
$env:OPENROUTER_API_KEY="sk-or-v1-your-key-here"

# Windows CMD
set OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Linux/Mac
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

### 5. Customize Configuration

Edit `config.json` to match your use case:

```json
{
  "participants": ["Alice", "Bob", "Charlie"],
  "current_session": 1,
  "output_file": "Session_Report.md",
  "whisper_keywords": ["Alice", "Bob", "Charlie"],
  "hallucination_filter": ["untertitel", "thanks for watching"],
  "speaker_label": "Moderator",
  "listener_label": "Participants"
}
```

**See [Configuration Guide](#-configuration-guide) below for detailed explanations.**

### 6. Customize Session Objectives

Edit the session file corresponding to your `current_session`:

```bash
# For session 1, edit:
sessions/session_1.txt
```

Add your session objectives, goals, and success criteria. This helps the AI generate accurate reports.

### 7. Run the Assistant

```bash
python CallAssistant.py
```

**Expected output:**
```
14:30:15 - INFO - Configuration loaded: Session 1, 3 participants
14:30:15 - INFO - OpenRouter API ready for cloud transcription
==================================================
🚀 AI CALL ASSISTANT STARTED
- Listening to Participants (Loopback): Speakers (Realtek Audio)
- Listening to Moderator (Microphone): Microphone Array

Features:
1. Provides real-time feedback during the call
2. Generates structured session report when finished

Press Ctrl+C to end the call and generate 'Session_Report.md'!
==================================================
```

### 8. During the Call

The assistant will:
- Transcribe both audio streams in real-time
- Display transcripts: `[Participants]: "We've implemented the frontend..."`
- Provide live insights every ~250 characters: `💡 [Insight] ❓ [Question]`

### 9. End the Call

Press **Ctrl+C** to stop recording.

The assistant will:
1. Stop recording
2. Analyze the complete transcript
3. Generate the session report
4. Save it as `Session_Report.md` (or your configured filename)

---

## 🖥️ Using the Graphical Interface

For a more user-friendly experience, use the GUI version:

### 1. Launch the GUI

```bash
python CallAssistantGUI.py
```

A window will open with the AI Call Assistant Control Panel.

### 2. Configure API Settings

In the **API Configuration** section:
- **OpenRouter API Key**: Enter your API key (will be hidden by default)
  - Check "Show" to reveal the key
  - Or load from `.env` file (recommended)
- **LLM Model**: Select the AI model for analysis from the dropdown
  - Default: `qwen/qwen3-vl-30b-a3b-instruct` (cost-effective)
  - Premium: `anthropic/claude-3-opus` or `openai/gpt-4-turbo`
- **Audio Model**: Select the Whisper model for transcription
  - Default: `openai/whisper-large-v3-turbo` (fast and accurate)

### 3. Configure Session Settings

In the **Session Configuration** section:
- **Participants**: Enter names separated by commas (e.g., `Alice, Bob, Charlie`)
- **Session Number**: Set the session/milestone number
- **Output File**: Specify the report filename (e.g., `Meeting_Report.md`)
- **Speaker Label**: Label for your microphone audio (e.g., `Moderator`, `Tutor`)
- **Listener Label**: Label for loopback audio (e.g., `Participants`, `Students`)

### 4. Save Configuration

Click **Save Configuration** to save settings to `config.json`. This ensures your preferences are preserved.

### 5. Start Recording

Click **Start Recording** to begin:
- Status will change to "Recording..."
- Live transcripts will appear in the display area
- AI feedback will be shown in real-time

### 6. Monitor Live Output

The **Live Transcript & AI Feedback** section shows:
- Real-time transcriptions with speaker labels
- AI insights and suggestions
- System messages and status updates
- Color-coded messages (blue: info, red: errors)

### 7. Stop Recording

Click **Stop & Generate Report** to:
- Stop the recording
- Generate the final session report
- Save the report to your specified output file

### 8. Review Report

Open the generated markdown file (e.g., `Session_Report.md`) in your preferred editor or viewer.

### GUI Features

- **Automatic Validation**: Checks for missing required fields before starting
- **Session File Warning**: Alerts if the session file doesn't exist
- **Configuration Persistence**: Saves settings automatically
- **Visual Feedback**: Color-coded status messages
- **Clear Display**: Button to clear the transcript view
- **API Key Security**: Password field for API key (can be toggled)
- **Prompt Editor**: Built-in editor to customize AI prompts without editing files manually
  - Switch between Live Analysis and Final Report prompts
  - Edit prompts with syntax highlighting
  - Save changes with confirmation
  - Reset to original content

---

## ✏️ Customizing AI Prompts with the GUI

The GUI includes a built-in prompt editor that makes it easy to customize how the AI behaves without manually editing files.

### Opening the Prompt Editor

1. Launch the GUI: `python CallAssistantGUI.py`
2. Click the **Edit Prompts** button at the bottom of the main window
3. A new window will open with the Prompt Editor

### Using the Prompt Editor

**Select a Prompt:**
- Use the dropdown to choose between:
  - **Live Analysis**: Controls real-time feedback during calls
  - **Final Report**: Defines the structure of session reports

**Load the Prompt:**
- Click **Load** to view the current prompt content
- The description below shows what this prompt does

**Edit the Content:**
- Modify the text in the editor as needed
- Use placeholders like `{participants_list}`, `{session_number}`, `{session_content}`
- The editor uses a monospace font for better readability

**Save Changes:**
- Click **Save Changes** to write your modifications
- You'll be asked to confirm before saving
- Original files are overwritten (backup recommended)

**Reset to Original:**
- Click **Reset to Original** to discard unsaved changes
- This restores the content to what was last loaded

### Tips for Prompt Editing

**Live Analysis Prompt:**
- Controls the tone and style of real-time feedback
- Adjust to be more/less technical
- Change focus areas (e.g., only code review, only questions)
- Modify output format

**Final Report Prompt:**
- Customize report structure and sections
- Add or remove table columns
- Change formatting style
- Adjust level of detail

**Using Placeholders:**
The prompts support these dynamic placeholders:
- `{participants_list}`: Comma-separated list of participant names
- `{session_number}`: Current session number
- `{session_content}`: Content from `sessions/session_X.txt`
- `{participants_table}`: Auto-generated HTML table for participants

**Example Customizations:**

*Making Live Analysis More Technical:*
```
Original: "Provide constructive feedback..."
Modified: "Provide technical code review feedback focusing on best practices..."
```

*Adding a New Report Section:*
```
## Code Quality Metrics

- Lines of code reviewed: [X]
- Issues found: [Y]
- Suggestions implemented: [Z]
```

---

## ⚙️ Configuration Guide

### config.json Breakdown

| Field | Description | Example |
|-------|-------------|---------|
| `participants` | List of all conversation participants | `["Alice", "Bob", "Charlie"]` |
| `current_session` | Current session/meeting number | `1` |
| `output_file` | Filename for generated report | `"Session_Report.md"` |
| `whisper_keywords` | Important terms for better transcription accuracy | `["ProjectName", "TechTerm1"]` |
| `hallucination_filter` | Phrases to filter out (common Whisper hallucinations) | `["thanks for watching"]` |
| `speaker_label` | Label for main speaker audio | `"Moderator"` |
| `listener_label` | Label for other participants audio | `"Participants"` |

### Detailed Field Explanations

#### `participants`
List all people who will be in the conversation. These names appear in the final report table.

**Example use cases:**
- **Tutoring**: `["Student1", "Student2", "Student3"]`
- **Team meeting**: `["Alice", "Bob", "Charlie"]`
- **Interview**: `["Candidate", "Interviewer1", "Interviewer2"]`

#### `current_session`
Session/meeting/milestone number. The program loads `sessions/session_X.txt` to understand the objectives.

**How to use:**
1. Set `"current_session": 1` for your first session
2. Create/edit `sessions/session_1.txt` with your objectives
3. For the next session, change to `"current_session": 2` and edit `sessions/session_2.txt`

#### `whisper_keywords`
Helps Whisper recognize specific terms more accurately.

**What to include:**
- Participant names (especially non-English names)
- Technical jargon specific to your domain
- Project names, code names, company names
- Acronyms that might be misheard

**Example for software project:**
```json
"whisper_keywords": [
  "Alice", "Bob",
  "React", "TypeScript", "API",
  "ProjectX", "Backend", "Frontend"
]
```

#### `hallucination_filter`
Common phrases Whisper sometimes "hears" that aren't actually spoken.

**Default filters:**
- `"untertitel"` (German subtitles)
- `"thanks for watching"` (YouTube outro)
- `"like and subscribe"` (Social media phrases)

**Add your own** if you notice recurring false transcriptions.

#### `speaker_label` and `listener_label`
Customize how audio sources are labeled in transcripts.

**Examples:**
- **University tutoring**: `"Tutor"` and `"Students"`
- **Interview**: `"Interviewer"` and `"Candidate"`
- **Meeting**: `"Moderator"` and `"Team"`
- **Podcast**: `"Host"` and `"Guest"`

---

## 🎨 Customizing Prompts

### Live Analysis Prompt (`prompts/live_analysis.txt`)

Controls real-time feedback behavior during the call.

**Current behavior:**
- Provides constructive observations
- Asks helpful follow-up questions
- Format: `💡 [Insight] ❓ [Question]`

**To customize:**
1. Edit `prompts/live_analysis.txt`
2. Change tone, format, or focus areas
3. Restart the program

**Example customizations:**
- Make it more technical/less technical
- Focus on specific topics (e.g., only code review)
- Change output format
- Add emoji preferences

### Final Report Prompt (`prompts/final_report.txt`)

Controls the structure and content of the final report.

**Current behavior:**
- Generates markdown table with session overview
- Creates participant breakdown with contributions
- Uses placeholders: `{participants_list}`, `{session_content}`, `{session_number}`

**To customize:**
1. Edit `prompts/final_report.txt`
2. Modify table structure, sections, or formatting
3. Restart the program

**Example customizations:**
- Add additional report sections
- Change table format
- Include specific metrics or KPIs
- Adjust tone (formal vs. casual)

---

## 📝 Session Files

Session files (`sessions/session_X.txt`) define the objectives and context for each session.

### Why Session Files?

The AI uses this information to:
- Evaluate progress against goals
- Identify what's missing or incomplete
- Generate accurate, context-aware reports

### How to Create Session Files

1. **Copy a template:**
   ```bash
   cp sessions/session_1.txt sessions/session_4.txt
   ```

2. **Edit the content:**
   ```
   SESSION 4 - Sprint Review
   =========================

   OBJECTIVES:
   Review completed features from Sprint 4

   KEY GOALS:
   1. Demo new authentication system
   2. Review API performance improvements
   3. Discuss deployment strategy

   SUCCESS CRITERIA:
   - All features demonstrated successfully
   - Performance targets met
   - Deployment plan approved
   ```

3. **Update config.json:**
   ```json
   "current_session": 4
   ```

### Session File Examples

**Example 1: Code Review Session**
```
SESSION 2 - Code Review
=======================

OBJECTIVES:
Review pull requests and ensure code quality standards

KEY GOALS:
1. Review 5 open pull requests
2. Discuss architectural decisions
3. Identify technical debt
4. Plan refactoring priorities

SUCCESS CRITERIA:
- All PRs reviewed with feedback
- Technical debt documented
- Refactoring tasks assigned
```

**Example 2: Project Planning**
```
SESSION 1 - Q2 Planning
=======================

OBJECTIVES:
Plan project roadmap for Q2

KEY GOALS:
1. Define Q2 objectives
2. Break down into epics and stories
3. Assign ownership
4. Estimate effort

SUCCESS CRITERIA:
- Roadmap agreed upon
- All stories estimated
- Owners assigned
```

---

## 🔧 Advanced Configuration

### Environment Variables

You can override default models via environment variables:

```bash
# Use a different LLM for analysis
export LLM_MODEL="anthropic/claude-3-opus"

# Use a different Whisper model
export AUDIO_MODEL="openai/whisper-large-v3"
```

**Available on OpenRouter:**
- LLM Models: Claude, GPT-4, Qwen, Llama, etc.
- Audio Models: Whisper variants

### Audio Configuration

Edit constants in `CallAssistant.py`:

```python
SAMPLE_RATE = 16000          # Audio sample rate (Hz)
CHUNK_DURATION = 5           # Seconds per audio chunk
LIVE_BUFFER_THRESHOLD = 250  # Characters before live analysis
MIN_TEXT_LENGTH = 3          # Minimum valid transcription length
```

### Language Configuration

Change transcription language in `CallAssistant.py`:

```python
data = {
    "model": AUDIO_MODEL,
    "language": "en",  # Change to "de", "fr", "es", etc.
    ...
}
```

Or remove `"language"` entirely for auto-detection.

---

## 🐛 Troubleshooting

### "OPENROUTER_API_KEY environment variable not set!"

**Solution:** Set the API key using one of the methods in [Quick Start Step 4](#4-configure-api-key).

### "config.json not found"

**Solution:** Make sure you're in the correct directory:
```bash
cd Multiplattform-KI-Call-Assistant
ls config.json  # Should exist
```

### "File not found: sessions/session_X.txt"

**Solution:** Create the session file:
```bash
cp sessions/session_1.txt sessions/session_X.txt
# Edit with your session objectives
```

Or change `current_session` in `config.json` to a session that exists.

### No Audio Recording

**Solution:** Check if soundcard detects your devices:

```python
import soundcard as sc
print(sc.all_speakers())
print(sc.all_microphones())
```

If devices aren't listed:
- Check audio drivers
- Try restarting the program
- On Linux: Install ALSA/PulseAudio dependencies

### Transcription Not Working

**Possible causes:**
1. **No internet connection** - Whisper API requires internet
2. **Invalid API key** - Check OpenRouter dashboard
3. **Audio too quiet** - Adjust microphone volume
4. **Wrong language setting** - Change or remove language parameter

### Live Analysis Not Appearing

**Possible causes:**
1. **Buffer threshold not reached** - Wait for ~250 characters of transcript
2. **API timeout** - Check internet connection
3. **API rate limits** - Check OpenRouter usage

---

## 💡 Use Case Examples

### 1. University Tutoring Sessions

**config.json:**
```json
{
  "participants": ["Student1", "Student2", "Student3"],
  "current_session": 2,
  "speaker_label": "Tutor",
  "listener_label": "Students",
  "output_file": "Milestone_2_Report.md"
}
```

**sessions/session_2.txt:**
```
Milestone 2 - Backend Implementation

OBJECTIVES:
Implement REST API endpoints and database integration

KEY GOALS:
1. User authentication endpoints
2. CRUD operations for main entities
3. Database migrations
4. API documentation
```

### 2. Team Code Review

**config.json:**
```json
{
  "participants": ["Alice", "Bob", "Charlie"],
  "current_session": 1,
  "speaker_label": "Reviewer",
  "listener_label": "Team",
  "output_file": "Code_Review_Sprint_14.md"
}
```

### 3. Client Interview

**config.json:**
```json
{
  "participants": ["Client", "ProjectManager"],
  "current_session": 1,
  "speaker_label": "Interviewer",
  "listener_label": "Client",
  "output_file": "Requirements_Interview.md"
}
```

---

## 🔒 Security & Privacy

⚠️ **IMPORTANT:**

- **Never commit API keys** to version control
- `.env` is already in `.gitignore`
- If you accidentally commit secrets:
  1. Rotate API key immediately on [OpenRouter](https://openrouter.ai/)
  2. Remove from git history using `git filter-branch` or BFG Repo-Cleaner

- **Audio recordings** are processed in memory and not saved to disk
- **Transcripts** are sent to OpenRouter API - review their privacy policy
- **Final reports** are saved locally only

---

## 💰 API Costs

**Estimated cost with default models: ~€0.30 per hour** (as of May 2026)

This includes:
- **Whisper API**: Real-time transcription (~5-second audio chunks)
- **LLM API**: Live analysis (~every 250 characters) + final report generation

**Cost factors:**
- Transcription frequency (every 5 seconds by default)
- Live analysis frequency (depends on conversation speed)
- LLM model choice (Qwen is cost-effective, Claude/GPT-4 costs more)
- Session duration

**Cost optimization tips:**
1. **Increase `CHUNK_DURATION`** in code (5s → 10s) to reduce API calls
2. **Increase `LIVE_BUFFER_THRESHOLD`** (250 → 500 characters) for less frequent live analysis
3. **Use cheaper models** via environment variables:
   ```bash
   export LLM_MODEL="qwen/qwen3-vl-30b-a3b-instruct"  # Default, cost-effective
   export AUDIO_MODEL="openai/whisper-large-v3-turbo"  # Default
   ```
4. **Disable live analysis** if you only need the final report (comment out live analysis worker)

**Example calculation (1 hour session):**
- Transcription: 720 chunks (1h ÷ 5s) × 2 audio sources = 1,440 API calls
- Live analysis: ~15-20 calls (depends on conversation)
- Final report: 1 call

Check your actual costs on the [OpenRouter dashboard](https://openrouter.ai/usage).

---

## 🧪 Technical Details

- **Language**: Python 3.8+
- **Audio Library**: soundcard (cross-platform)
- **Transcription**: OpenRouter Whisper API (cloud-based)
- **LLM**: Qwen 3 VL (configurable via environment variables)
- **Architecture**: Multi-threaded (transcription, live analysis, audio recording x2)
- **Audio Format**: 16kHz, mono, 16-bit PCM WAV

---

## 🤝 Contributing

This is currently a personal/educational project, but contributions are welcome!

**To contribute:**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

**Ideas for contributions:**
- Add support for more languages
- Implement local Whisper (no API needed)
- Create web UI
- Add more report templates
- Improve audio device selection

---

## 📄 License

This project is for educational and personal use.

---

## 🙏 Credits

Originally developed for university tutoring documentation, now generalized for broader use.

Built with:
- [OpenRouter](https://openrouter.ai/) - Unified LLM API
- [soundcard](https://github.com/bastibe/SoundCard) - Python audio library
- [Whisper](https://openai.com/research/whisper) - Speech recognition model

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/FarshadAhmadi089/Multiplattform-KI-Call-Assistant/issues)
- **Questions**: Open a GitHub Discussion

---

## 🗺️ Roadmap

Completed features:
- [✅] Desktop GUI with Tkinter (configuration, control, live display)
- [✅] Custom prompt editor in GUI (edit prompts visually)

Future improvements:
- [ ] Web-based UI (Flask/FastAPI)
- [ ] Local Whisper support (no API required)
- [ ] Multi-language live analysis
- [ ] Export to PDF/Word
- [ ] Integration with calendar apps
- [ ] Automatic meeting scheduling detection
- [ ] Speaker diarization (identify who said what)
- [ ] Audio device selection in GUI
- [ ] Session file editor in GUI

---

**Happy documenting! 🎉**
