# AI Call Assistant - Multi-Platform Edition

An intelligent AI assistant that automatically records conversations, transcribes them in real-time, provides live feedback, and generates structured session reports.

Perfect for: team meetings, code reviews, interviews, project check-ins, and any scenario where you need AI-powered conversation analysis and documentation.

---

## ✨ Features

### 🎙️ Core Features
- **Dual-Audio Recording**: Captures both speaker and listener audio streams simultaneously
- **Real-Time Transcription**: Uses OpenRouter Whisper API for accurate speech-to-text
- **Live Analysis Window**: Separate window showing only AI feedback - perfect for screensharing
- **Automatic Report Generation**: Creates structured markdown reports with participant breakdown
- **Multi-Language Support**: Works with German, English, and other languages supported by Whisper

### 🖥️ Modern GUI Features
- **Beautiful Interface**: Modern, card-based design with scrollable layout
- **Configuration Manager**: Visual editor for prompts and sessions
- **Active Prompt Selection**: Choose which prompts to use with visual indicators (⭐)
- **Screen Capture Protection**: Hide GUI from screenshots and screensharing
- **Keyboard Shortcuts**: Hotkeys for Start (F9) and Stop (F10) recording
- **Session Management**: Create, rename, and delete session files directly in GUI

### 🔒 Privacy & Security
- **Screen Protection**: Hide all windows from screen capture and screensharing
- **API Key Security**: Secure password field with show/hide toggle
- **Local Storage**: Recordings processed in memory, not saved to disk

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

### 4. Launch the GUI

```bash
python CallAssistantGUI.py
```

A beautiful, modern interface will open with the AI Call Assistant Control Panel.

---

## 🎛️ Using the GUI

### Main Window Overview

The GUI is organized into clear sections:

1. **Control Panel** (Top) - Start/Stop buttons with hotkey indicators
2. **API Configuration** - OpenRouter API key and model selection
3. **Session Configuration** - Participants, session number, labels
4. **Live Transcript** - Real-time transcription and AI feedback
5. **Toolbar** - Save configuration, open Configuration Manager, screen protection

### Quick Usage

1. **Enter API Key**: Paste your OpenRouter API key in the API Configuration section
2. **Configure Session**: Add participant names, set session number
3. **Start Recording**: Click "▶ Start Recording" (or press F9)
4. **Live Analysis Window Opens**: Shows only AI feedback - perfect for screensharing
5. **Stop Recording**: Click "■ Stop & Generate Report" (or press F10)
6. **Review Report**: Open the generated markdown file

---

## 🤖 Live Analysis Window

When you start recording, a **separate Live Analysis Window** automatically opens.

### Features:
- **Always on Top**: Stays visible above other windows
- **Clean Display**: Shows only AI feedback and insights
- **Perfect for Screensharing**: Share this window during meetings while keeping your main GUI private
- **Real-Time Updates**: AI analysis appears instantly with color-coded messages

### Use Cases:
- **Team Meetings**: Share Live Analysis Window via Zoom/Teams to show AI insights to your team
- **Code Reviews**: Display AI suggestions while keeping your API keys hidden
- **Presentations**: Professional display of AI-generated insights

---

## 🔒 Screen Capture Protection

### What It Does:
Hide **all windows** from screenshots, screen recording, and screensharing applications.

### How to Enable:
1. Check the box: **"🔒 Hide from screen capture"** in the toolbar
2. All windows become invisible to:
   - Screenshots (Windows Snipping Tool, PrtScn)
   - Screen recording software (OBS, etc.)
   - Screensharing (Zoom, Teams, Discord)

### Protected Windows:
- ✅ Main GUI (API keys, configuration)
- ✅ Configuration Manager (prompts, sessions)
- ✅ Live Analysis Window (AI feedback)

### Why Use It:
- **Privacy**: Keep API keys and sensitive information hidden during screenshares
- **Professionalism**: Share only what's relevant (Live Analysis Window) during meetings
- **Security**: Prevent accidental exposure in screenshots or recordings

**Note**: This feature uses Windows API and works on Windows 10/11.

---

## ⌨️ Keyboard Shortcuts

### Default Hotkeys:
- **F9**: Start Recording
- **F10**: Stop & Generate Report

### Customizing Hotkeys:
Hotkeys are stored in `config.json` and can be customized:

```json
{
  "start_hotkey": "<F9>",
  "stop_hotkey": "<F10>"
}
```

Supported keys: F1-F12, Control-*, Alt-*, Shift-*

Example: `"<Control-r>"` for Ctrl+R

---

## ⚙️ Configuration Manager

Access via the **"⚙️ Configuration Manager"** button in the toolbar.

### Prompts Tab

**Manage AI Prompts:**
- **Live Analysis**: Real-time feedback during calls
- **Final Report**: Structure of session reports

**Available Prompts:**
- `default` - General purpose
- `technical` - Code review focused
- `meeting` - Meeting facilitation
- Custom prompts you create

**Actions:**
- **➕ New**: Create a new prompt variation
- **✏️ Rename**: Rename existing prompts
- **🗑️ Delete**: Remove unused prompts
- **⭐ Set as Active**: Mark a prompt as active (visual star indicator)

**Active Prompt Selection:**
The active prompt is marked with a ⭐ star in the list. Click "⭐ Set as Active" to change which prompt is used during recording.

### Sessions Tab

**Manage Session Files:**
- Create new session objectives
- Edit existing session files
- Rename or delete sessions
- Define goals and success criteria for each session

---

## 📝 Session Configuration

### Participants
Enter names separated by commas:
```
Alice, Bob, Charlie
```

These names appear in the final report and help with transcription accuracy.

### Session Number
The session number corresponds to `sessions/session_X.txt` file:
- Session 1 → `sessions/session_1.txt`
- Session 2 → `sessions/session_2.txt`

### Speaker & Listener Labels
Customize how audio sources are labeled:
- **University tutoring**: `Tutor` and `Students`
- **Interview**: `Interviewer` and `Candidate`
- **Meeting**: `Moderator` and `Team`
- **Podcast**: `Host` and `Guest`

---

## 🎨 Customizing Prompts

### Via Configuration Manager (Recommended)

1. Click **"⚙️ Configuration Manager"**
2. Go to **"📝 Prompts"** tab
3. Select prompt type: "Live Analysis" or "Final Report"
4. Choose a prompt from the list or create a new one
5. Edit the content in the editor
6. Click **"💾 Save Changes"**
7. Click **"⭐ Set as Active"** to use this prompt

### Prompt Types Explained

**Live Analysis Prompts:**
- Control the AI's real-time feedback during calls
- Options:
  - `default`: General constructive feedback
  - `technical`: Code review focused with technical observations
  - `meeting`: Meeting facilitation with action items

**Final Report Prompts:**
- Control the structure of generated reports
- Options:
  - `default`: Standard session report
  - `detailed`: Comprehensive report with extra sections
  - `brief`: Concise summary report

### Placeholders

Use these in your prompts:
- `{participants_list}`: Comma-separated participant names
- `{session_number}`: Current session number
- `{session_content}`: Content from session file
- `{participants_table}`: Auto-generated HTML table

---

## 📁 Project Structure

```
Multiplattform-KI-Call-Assistant/
├── CallAssistant.py             # Core logic (command-line version)
├── CallAssistantGUI.py          # Modern GUI application
├── ConfigurationWindow.py       # Configuration Manager window
├── config.json                  # User configuration
├── requirements.txt             # Python dependencies
│
├── prompts/                     # AI prompts
│   ├── live_analysis/           # Live analysis prompts
│   │   ├── default.txt
│   │   ├── technical.txt
│   │   └── meeting.txt
│   └── final_report/            # Final report prompts
│       ├── default.txt
│       ├── detailed.txt
│       └── brief.txt
│
└── sessions/                    # Session objectives
    ├── session_1.txt
    ├── session_2.txt
    └── session_3.txt
```

---

## 🔧 Advanced Configuration

### config.json Structure

```json
{
  "participants": ["Alice", "Bob", "Charlie"],
  "current_session": 1,
  "output_file": "Session_Report.md",
  "whisper_keywords": ["Alice", "Bob", "Charlie"],
  "hallucination_filter": ["untertitel", "thanks for watching"],
  "speaker_label": "Moderator",
  "listener_label": "Participants",
  "active_live_analysis_prompt": "default",
  "active_final_report_prompt": "default",
  "api_key": "sk-or-v1-...",
  "llm_model": "qwen/qwen3-vl-30b-a3b-instruct",
  "audio_model": "openai/whisper-large-v3-turbo",
  "hide_from_capture": false,
  "start_hotkey": "<F9>",
  "stop_hotkey": "<F10>"
}
```

### Field Explanations

| Field | Description | Example |
|-------|-------------|---------|
| `participants` | List of conversation participants | `["Alice", "Bob"]` |
| `current_session` | Session/meeting number | `1` |
| `output_file` | Report filename | `"Session_Report.md"` |
| `whisper_keywords` | Terms for better transcription | `["ProjectName", "API"]` |
| `hallucination_filter` | False transcriptions to filter | `["thanks for watching"]` |
| `speaker_label` | Main speaker label | `"Moderator"` |
| `listener_label` | Other participants label | `"Participants"` |
| `active_live_analysis_prompt` | Active live prompt | `"technical"` |
| `active_final_report_prompt` | Active report prompt | `"detailed"` |
| `api_key` | OpenRouter API key | `"sk-or-v1-..."` |
| `llm_model` | LLM model for analysis | `"qwen/qwen3-vl-30b-a3b-instruct"` |
| `audio_model` | Whisper model | `"openai/whisper-large-v3-turbo"` |
| `hide_from_capture` | Screen protection enabled | `false` |
| `start_hotkey` | Start recording hotkey | `"<F9>"` |
| `stop_hotkey` | Stop recording hotkey | `"<F10>"` |

---

## 💡 Use Case Examples

### 1. University Tutoring Sessions

**Configuration:**
```json
{
  "participants": ["Student1", "Student2", "Student3"],
  "current_session": 2,
  "speaker_label": "Tutor",
  "listener_label": "Students",
  "output_file": "Milestone_2_Report.md",
  "active_live_analysis_prompt": "default"
}
```

**Workflow:**
1. Start recording at beginning of tutoring session
2. Live Analysis Window shows AI feedback in real-time
3. Students can see AI suggestions on shared screen
4. Stop at end of session to generate report

### 2. Team Code Review

**Configuration:**
```json
{
  "participants": ["Alice", "Bob", "Charlie"],
  "speaker_label": "Reviewer",
  "listener_label": "Team",
  "active_live_analysis_prompt": "technical"
}
```

**Workflow:**
1. Enable screen capture protection
2. Start recording
3. Share Live Analysis Window during review
4. AI provides technical observations in real-time

### 3. Client Meeting

**Configuration:**
```json
{
  "participants": ["Client", "ProjectManager", "TechLead"],
  "speaker_label": "Team",
  "listener_label": "Client",
  "active_live_analysis_prompt": "meeting",
  "active_final_report_prompt": "brief"
}
```

**Workflow:**
1. Hide GUI from screen capture
2. Share Live Analysis Window to show AI insights
3. AI tracks action items and decisions
4. Generate brief summary report at end

---

## 🐛 Troubleshooting

### GUI doesn't start
**Solution:** Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### "OPENROUTER_API_KEY environment variable not set!"
**Solution:** Enter your API key in the GUI's API Configuration section, or set it in `.env` file.

### Live Analysis Window doesn't open
**Solution:** Check that recording started successfully. Look for error messages in the main GUI's live transcript area.

### Hotkeys don't work
**Solution:** Make sure the main GUI window has focus. Hotkeys only work when the application is active.

### Screen Capture Protection doesn't work
**Solution:** This feature requires Windows 10/11. It may not work on older systems or non-Windows platforms.

### No Audio Recording
**Solution:** Check audio device selection. Run this to see available devices:
```python
import soundcard as sc
print(sc.all_speakers())
print(sc.all_microphones())
```

---

## 💰 API Costs

**Estimated cost with default models: ~€0.30 per hour** (as of 2026)

### Cost Breakdown:
- **Whisper API**: Real-time transcription (~5-second chunks)
- **LLM API**: Live analysis + final report

### Cost Optimization:
1. Use cost-effective models (Qwen is default and affordable)
2. Increase chunk duration to reduce API calls
3. Disable live analysis if only final report is needed

Check actual costs on [OpenRouter dashboard](https://openrouter.ai/usage).

---

## 🧪 Technical Details

- **Language**: Python 3.8+
- **GUI Framework**: Tkinter with modern styling
- **Audio Library**: soundcard (cross-platform)
- **Transcription**: OpenRouter Whisper API
- **LLM**: Configurable (default: Qwen 3 VL)
- **Architecture**: Multi-threaded design
- **Screen Protection**: Windows SetWindowDisplayAffinity API

---

## 🤝 Contributing

Contributions welcome!

**Ideas for contributions:**
- Add support for more languages
- Implement local Whisper (no API needed)
- Linux/Mac screen capture protection
- Global hotkey support (works when app not in focus)
- Audio device selection in GUI
- Export reports to PDF/Word

---

## 🗺️ Roadmap

### Completed ✅
- Modern GUI with Tkinter
- Configuration Manager (prompts & sessions)
- Live Analysis Window
- Screen Capture Protection
- Keyboard shortcuts (F9/F10)
- Active prompt selection with visual indicators
- Scrollable layout
- Multi-prompt support

### Planned 📋
- [ ] Web-based UI (Flask/FastAPI)
- [ ] Local Whisper support (offline mode)
- [ ] Global hotkeys (work system-wide)
- [ ] Audio device selection in GUI
- [ ] Export to PDF/Word
- [ ] Speaker diarization
- [ ] Multi-language live analysis
- [ ] Calendar integration

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

**Happy documenting! 🎉**
