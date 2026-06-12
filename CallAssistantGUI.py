"""
AI Call Assistant - Modern Graphical User Interface
===================================================
A beautiful, user-friendly GUI with modern styling
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import json
import os
import sys
from pathlib import Path

# Import the ConfigurationWindow
from ConfigurationWindow import StyledConfigurationWindow as ConfigurationWindow


class CallAssistantGUI:
    # Modern Color Scheme
    COLORS = {
        'primary': '#2563EB',      # Blue
        'primary_dark': '#1E40AF',
        'primary_light': '#DBEAFE',
        'secondary': '#10B981',    # Green
        'danger': '#EF4444',       # Red
        'warning': '#F59E0B',      # Orange
        'bg_main': '#F9FAFB',      # Light gray
        'bg_card': '#FFFFFF',
        'bg_dark': '#1F2937',
        'text_primary': '#111827',
        'text_secondary': '#6B7280',
        'border': '#E5E7EB',
        'success': '#10B981'
    }

    # Class variable for singleton Configuration Window
    _config_window = None

    def __init__(self, root):
        self.root = root
        self.root.title("🎙️ AI Call Assistant")
        self.root.geometry("1000x750")
        self.root.configure(bg=self.COLORS['bg_main'])

        # State variables
        self.is_running = False
        self.recording_thread = None
        self.transcript_queue = queue.Queue()

        # Configure style
        self.setup_styles()

        # Create UI
        self.create_widgets()
        self.load_config()

    def setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure frames
        style.configure('Card.TFrame', background=self.COLORS['bg_card'], relief='flat')
        style.configure('Main.TFrame', background=self.COLORS['bg_main'])
        style.configure('Header.TFrame', background=self.COLORS['primary'])

        # Configure labels
        style.configure('Header.TLabel',
                       background=self.COLORS['primary'],
                       foreground='white',
                       font=('Segoe UI', 20, 'bold'))
        style.configure('Subtitle.TLabel',
                       background=self.COLORS['primary'],
                       foreground='white',
                       font=('Segoe UI', 10))
        style.configure('SectionTitle.TLabel',
                       background=self.COLORS['bg_card'],
                       foreground=self.COLORS['text_primary'],
                       font=('Segoe UI', 11, 'bold'))
        style.configure('CardLabel.TLabel',
                       background=self.COLORS['bg_card'],
                       foreground=self.COLORS['text_primary'])
        style.configure('Status.TLabel',
                       background=self.COLORS['bg_card'],
                       foreground=self.COLORS['text_secondary'],
                       font=('Segoe UI', 9))

        # Configure buttons
        style.configure('Primary.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10))
        style.configure('Success.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10))
        style.configure('Danger.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10))

        # Configure LabelFrames
        style.configure('Card.TLabelframe',
                       background=self.COLORS['bg_card'],
                       borderwidth=0)
        style.configure('Card.TLabelframe.Label',
                       background=self.COLORS['bg_card'],
                       foreground=self.COLORS['text_primary'],
                       font=('Segoe UI', 11, 'bold'))

    def create_widgets(self):
        # ============================================
        # HEADER
        # ============================================
        header_frame = ttk.Frame(self.root, style='Header.TFrame', height=100)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=0, pady=0)
        header_frame.grid_propagate(False)

        header_content = ttk.Frame(header_frame, style='Header.TFrame')
        header_content.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Label(header_content, text="🎙️  AI Call Assistant", style='Header.TLabel').pack()
        ttk.Label(header_content, text="Record, Transcribe, and Analyze Conversations with AI",
                 style='Subtitle.TLabel').pack(pady=(5, 0))

        # ============================================
        # MAIN CONTAINER
        # ============================================
        main_container = ttk.Frame(self.root, style='Main.TFrame', padding="20")
        main_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(2, weight=1)

        # ============================================
        # API CONFIGURATION CARD
        # ============================================
        api_card = self.create_card(main_container, "⚙️ API Configuration")
        api_card.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

        api_content = ttk.Frame(api_card, style='Card.TFrame')
        api_content.pack(fill='both', expand=True, padx=15, pady=15)

        # API Key Row
        api_row1 = ttk.Frame(api_content, style='Card.TFrame')
        api_row1.pack(fill='x', pady=(0, 10))

        ttk.Label(api_row1, text="OpenRouter API Key", style='CardLabel.TLabel', width=18).pack(side='left')
        self.api_key_var = tk.StringVar(value=os.getenv("OPENROUTER_API_KEY", ""))
        api_entry = ttk.Entry(api_row1, textvariable=self.api_key_var, show="●", width=40)
        api_entry.pack(side='left', padx=(10, 5), fill='x', expand=True)

        self.show_key_var = tk.BooleanVar()
        ttk.Checkbutton(api_row1, text="Show", variable=self.show_key_var,
                       command=lambda: api_entry.config(show="" if self.show_key_var.get() else "●")
                       ).pack(side='left')

        # Models Row
        models_row = ttk.Frame(api_content, style='Card.TFrame')
        models_row.pack(fill='x')

        # LLM Model
        llm_frame = ttk.Frame(models_row, style='Card.TFrame')
        llm_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))

        ttk.Label(llm_frame, text="LLM Model", style='CardLabel.TLabel').pack(anchor='w')
        self.llm_model_var = tk.StringVar()
        llm_models = [
            "qwen/qwen3-vl-30b-a3b-instruct",
            "anthropic/claude-3-opus",
            "anthropic/claude-3-sonnet",
            "openai/gpt-4-turbo",
        ]
        llm_combo = ttk.Combobox(llm_frame, textvariable=self.llm_model_var, values=llm_models)
        llm_combo.pack(fill='x', pady=(5, 0))
        llm_combo.set("qwen/qwen3-vl-30b-a3b-instruct")

        # Audio Model
        audio_frame = ttk.Frame(models_row, style='Card.TFrame')
        audio_frame.pack(side='left', fill='x', expand=True)

        ttk.Label(audio_frame, text="Audio Model", style='CardLabel.TLabel').pack(anchor='w')
        self.audio_model_var = tk.StringVar()
        audio_models = [
            "openai/whisper-large-v3-turbo",
            "openai/whisper-large-v3",
        ]
        audio_combo = ttk.Combobox(audio_frame, textvariable=self.audio_model_var, values=audio_models)
        audio_combo.pack(fill='x', pady=(5, 0))
        audio_combo.set("openai/whisper-large-v3-turbo")

        # ============================================
        # SESSION CONFIGURATION CARD
        # ============================================
        session_card = self.create_card(main_container, "📝 Session Configuration")
        session_card.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

        session_content = ttk.Frame(session_card, style='Card.TFrame')
        session_content.pack(fill='both', expand=True, padx=15, pady=15)

        # Row 1
        row1 = ttk.Frame(session_content, style='Card.TFrame')
        row1.pack(fill='x', pady=(0, 10))

        # Participants
        part_frame = ttk.Frame(row1, style='Card.TFrame')
        part_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        ttk.Label(part_frame, text="Participants (comma-separated)", style='CardLabel.TLabel').pack(anchor='w')
        self.participants_var = tk.StringVar()
        ttk.Entry(part_frame, textvariable=self.participants_var).pack(fill='x', pady=(5, 0))

        # Session Number
        session_frame = ttk.Frame(row1, style='Card.TFrame')
        session_frame.pack(side='left')
        ttk.Label(session_frame, text="Session #", style='CardLabel.TLabel').pack(anchor='w')
        self.session_num_var = tk.StringVar()
        ttk.Spinbox(session_frame, from_=1, to=100, textvariable=self.session_num_var, width=10).pack(pady=(5, 0))

        # Row 2
        row2 = ttk.Frame(session_content, style='Card.TFrame')
        row2.pack(fill='x', pady=(0, 10))

        # Output File
        output_frame = ttk.Frame(row2, style='Card.TFrame')
        output_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        ttk.Label(output_frame, text="Output File", style='CardLabel.TLabel').pack(anchor='w')
        self.output_file_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_file_var).pack(fill='x', pady=(5, 0))

        # Labels
        labels_container = ttk.Frame(row2, style='Card.TFrame')
        labels_container.pack(side='left', fill='x', expand=True)

        speaker_frame = ttk.Frame(labels_container, style='Card.TFrame')
        speaker_frame.pack(side='left', fill='x', expand=True, padx=(0, 5))
        ttk.Label(speaker_frame, text="Speaker Label", style='CardLabel.TLabel').pack(anchor='w')
        self.speaker_label_var = tk.StringVar()
        ttk.Entry(speaker_frame, textvariable=self.speaker_label_var, width=15).pack(pady=(5, 0))

        listener_frame = ttk.Frame(labels_container, style='Card.TFrame')
        listener_frame.pack(side='left', fill='x', expand=True, padx=(5, 0))
        ttk.Label(listener_frame, text="Listener Label", style='CardLabel.TLabel').pack(anchor='w')
        self.listener_label_var = tk.StringVar()
        ttk.Entry(listener_frame, textvariable=self.listener_label_var, width=15).pack(pady=(5, 0))

        # ============================================
        # CONTROL PANEL
        # ============================================
        control_card = ttk.Frame(main_container, style='Card.TFrame',
                                relief='solid', borderwidth=1)
        control_card.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

        control_content = ttk.Frame(control_card, style='Card.TFrame')
        control_content.pack(fill='both', expand=True, padx=20, pady=20)

        # Buttons Row
        button_container = ttk.Frame(control_content, style='Card.TFrame')
        button_container.pack(fill='x', pady=(0, 15))

        self.start_button = tk.Button(button_container, text="▶ Start Recording",
                                      command=self.start_recording,
                                      bg=self.COLORS['success'], fg='white',
                                      font=('Segoe UI', 11, 'bold'),
                                      relief='flat', padx=30, pady=12,
                                      cursor='hand2')
        self.start_button.pack(side='left', padx=(0, 10))

        self.stop_button = tk.Button(button_container, text="■ Stop & Generate Report",
                                     command=self.stop_recording,
                                     bg=self.COLORS['danger'], fg='white',
                                     font=('Segoe UI', 11, 'bold'),
                                     relief='flat', padx=30, pady=12,
                                     state='disabled', cursor='hand2')
        self.stop_button.pack(side='left')

        # Status Row
        status_container = ttk.Frame(control_content, style='Card.TFrame')
        status_container.pack(fill='x')

        ttk.Label(status_container, text="Status:", style='CardLabel.TLabel').pack(side='left', padx=(0, 10))
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(status_container, textvariable=self.status_var,
                                     bg=self.COLORS['bg_card'],
                                     fg=self.COLORS['text_secondary'],
                                     font=('Segoe UI', 10, 'bold'))
        self.status_label.pack(side='left')

        # ============================================
        # LIVE DISPLAY CARD
        # ============================================
        display_card = self.create_card(main_container, "💬 Live Transcript & AI Feedback")
        display_card.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        main_container.rowconfigure(3, weight=1)

        display_content = ttk.Frame(display_card, style='Card.TFrame')
        display_content.pack(fill='both', expand=True, padx=15, pady=15)

        # Text display
        self.transcript_display = scrolledtext.ScrolledText(display_content, wrap=tk.WORD,
                                                             height=12, font=('Consolas', 9),
                                                             bg='#FAFAFA', relief='flat',
                                                             borderwidth=1)
        self.transcript_display.pack(fill='both', expand=True)
        self.transcript_display.config(state="disabled")

        # Configure tags for colors
        self.transcript_display.tag_config("info", foreground=self.COLORS['primary'])
        self.transcript_display.tag_config("error", foreground=self.COLORS['danger'])
        self.transcript_display.tag_config("success", foreground=self.COLORS['success'])

        # Clear button
        clear_btn_container = ttk.Frame(display_content, style='Card.TFrame')
        clear_btn_container.pack(fill='x', pady=(10, 0))

        tk.Button(clear_btn_container, text="Clear Display",
                 command=self.clear_display,
                 bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary'],
                 font=('Segoe UI', 9),
                 relief='flat', padx=15, pady=5,
                 cursor='hand2').pack(side='right')

        # ============================================
        # BOTTOM TOOLBAR
        # ============================================
        toolbar = ttk.Frame(main_container, style='Main.TFrame')
        toolbar.grid(row=4, column=0, sticky=(tk.W, tk.E))

        tk.Button(toolbar, text="💾 Save Configuration",
                 command=self.save_config,
                 bg=self.COLORS['primary'], fg='white',
                 font=('Segoe UI', 9, 'bold'),
                 relief='flat', padx=15, pady=8,
                 cursor='hand2').pack(side='left', padx=(0, 10))

        tk.Button(toolbar, text="⚙️ Configuration Manager",
                 command=self.open_configuration_window,
                 bg=self.COLORS['bg_card'], fg=self.COLORS['text_primary'],
                 font=('Segoe UI', 9, 'bold'),
                 relief='solid', borderwidth=1,
                 padx=15, pady=8,
                 cursor='hand2').pack(side='left')

        ttk.Label(toolbar, text="AI Call Assistant v2.0 | Modern Edition",
                 style='Status.TLabel').pack(side='right')

    def create_card(self, parent, title):
        """Create a styled card with title"""
        card = ttk.LabelFrame(parent, text=title, style='Card.TLabelframe',
                             relief='solid', borderwidth=1)
        return card

    # ============================================
    # REMAINING METHODS (unchanged logic, only UI)
    # ============================================

    def load_config(self):
        """Load existing configuration from config.json"""
        try:
            config_path = Path(__file__).parent / "config.json"
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                self.participants_var.set(", ".join(config.get("participants", [])))
                self.session_num_var.set(str(config.get("current_session", 1)))
                self.output_file_var.set(config.get("output_file", "Session_Report.md"))
                self.speaker_label_var.set(config.get("speaker_label", "Speaker"))
                self.listener_label_var.set(config.get("listener_label", "Listeners"))

                # Load API key if saved
                if config.get("api_key"):
                    self.api_key_var.set(config.get("api_key"))

                # Load models if saved
                if config.get("llm_model"):
                    self.llm_model_var.set(config.get("llm_model"))
                if config.get("audio_model"):
                    self.audio_model_var.set(config.get("audio_model"))

                self.append_to_display("Configuration loaded successfully.\n", "info")
        except Exception as e:
            self.append_to_display(f"Error loading config: {e}\n", "error")

    def save_config(self):
        """Save current configuration to config.json"""
        try:
            participants = [p.strip() for p in self.participants_var.get().split(",") if p.strip()]

            config = {
                "participants": participants,
                "current_session": int(self.session_num_var.get()),
                "output_file": self.output_file_var.get(),
                "whisper_keywords": participants,
                "hallucination_filter": [
                    "untertitel", "vielen dank", "danke fürs zuschauen",
                    "abonniert den kanal", "tschüss",
                    "like and subscribe", "thanks for watching"
                ],
                "speaker_label": self.speaker_label_var.get(),
                "listener_label": self.listener_label_var.get(),
                "active_live_analysis_prompt": "default",
                "active_final_report_prompt": "default",
                "api_key": self.api_key_var.get(),
                "llm_model": self.llm_model_var.get(),
                "audio_model": self.audio_model_var.get()
            }

            config_path = Path(__file__).parent / "config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            messagebox.showinfo("Success", "Configuration saved successfully!")
            self.append_to_display("Configuration saved.\n", "success")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            self.append_to_display(f"Error saving config: {e}\n", "error")

    def validate_inputs(self):
        """Validate all required inputs before starting"""
        if not self.api_key_var.get():
            messagebox.showerror("Error", "Please enter your OpenRouter API Key")
            return False

        if not self.participants_var.get():
            messagebox.showerror("Error", "Please enter at least one participant")
            return False

        if not self.output_file_var.get():
            messagebox.showerror("Error", "Please enter an output filename")
            return False

        try:
            int(self.session_num_var.get())
        except ValueError:
            messagebox.showerror("Error", "Session number must be a valid number")
            return False

        session_path = Path(__file__).parent / "sessions" / f"session_{self.session_num_var.get()}.txt"
        if not session_path.exists():
            response = messagebox.askyesno("Warning",
                f"Session file '{session_path.name}' does not exist.\n\n"
                "The program may fail when generating the report.\n\n"
                "Continue anyway?")
            if not response:
                return False

        return True

    def start_recording(self):
        """Start the recording session"""
        if not self.validate_inputs():
            return

        self.save_config()

        os.environ["OPENROUTER_API_KEY"] = self.api_key_var.get()
        os.environ["LLM_MODEL"] = self.llm_model_var.get()
        os.environ["AUDIO_MODEL"] = self.audio_model_var.get()

        self.is_running = True
        self.start_button.config(state='disabled', bg='#9CA3AF')
        self.stop_button.config(state='normal', bg=self.COLORS['danger'])
        self.status_var.set("🔴 Recording...")
        self.status_label.config(fg=self.COLORS['danger'])

        self.append_to_display("="*50 + "\n", "info")
        self.append_to_display("🎙️ Starting AI Call Assistant...\n", "success")
        self.append_to_display(f"LLM: {self.llm_model_var.get()}\n", "info")
        self.append_to_display(f"Audio: {self.audio_model_var.get()}\n", "info")
        self.append_to_display("="*50 + "\n\n", "info")

        self.recording_thread = threading.Thread(target=self.run_assistant, daemon=True)
        self.recording_thread.start()

        self.update_display()

    def run_assistant(self):
        """Run the CallAssistant in a separate thread"""
        try:
            import CallAssistant
            import importlib
            importlib.reload(CallAssistant)

            self.CallAssistant = CallAssistant
            self.setup_logging_redirect()
            self.CallAssistant.main()

        except KeyboardInterrupt:
            pass
        except Exception as e:
            self.transcript_queue.put(("error", f"Error: {e}\n"))
        finally:
            self.transcript_queue.put(("done", "Recording stopped.\n"))

    def setup_logging_redirect(self):
        """Redirect CallAssistant logging to GUI"""
        import logging

        class GUIHandler(logging.Handler):
            def __init__(self, queue):
                super().__init__()
                self.queue = queue

            def emit(self, record):
                msg = self.format(record)
                level = record.levelname.lower()
                tag = "info" if level == "info" else "error"
                self.queue.put((tag, msg + "\n"))

        gui_handler = GUIHandler(self.transcript_queue)
        gui_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S'))
        self.CallAssistant.logger.addHandler(gui_handler)

    def stop_recording(self):
        """Stop the recording and generate report"""
        if self.is_running:
            self.append_to_display("\n🛑 Stopping recording and generating report...\n", "info")

            if self.recording_thread and self.recording_thread.is_alive() and hasattr(self, 'CallAssistant'):
                self.CallAssistant.audio_queue.put(("shutdown", None))
                self.CallAssistant.live_text_queue.put(None)
                threading.Thread(target=self.CallAssistant.generate_final_report, daemon=True).start()

            self.is_running = False
            self.start_button.config(state='normal', bg=self.COLORS['success'])
            self.stop_button.config(state='disabled', bg='#9CA3AF')
            self.status_var.set("Ready")
            self.status_label.config(fg=self.COLORS['text_secondary'])

            self.append_to_display("\n✅ Recording stopped. Report generation in progress...\n", "success")

    def update_display(self):
        """Update the transcript display with queued messages"""
        try:
            while True:
                tag, message = self.transcript_queue.get_nowait()
                self.append_to_display(message, tag)

                if tag == "done":
                    self.is_running = False
                    self.start_button.config(state='normal', bg=self.COLORS['success'])
                    self.stop_button.config(state='disabled', bg='#9CA3AF')
                    self.status_var.set("Ready")
                    self.status_label.config(fg=self.COLORS['text_secondary'])
        except queue.Empty:
            pass

        if self.is_running or not self.transcript_queue.empty():
            self.root.after(100, self.update_display)

    def append_to_display(self, message, tag="normal"):
        """Append message to transcript display with color coding"""
        self.transcript_display.config(state="normal")
        self.transcript_display.insert(tk.END, message, tag)
        self.transcript_display.see(tk.END)
        self.transcript_display.config(state="disabled")

    def clear_display(self):
        """Clear the transcript display"""
        self.transcript_display.config(state="normal")
        self.transcript_display.delete(1.0, tk.END)
        self.transcript_display.config(state="disabled")

    def open_configuration_window(self):
        """Open the configuration window for prompts and sessions"""
        # Singleton pattern - only one configuration window at a time
        if CallAssistantGUI._config_window is None or not CallAssistantGUI._config_window.window.winfo_exists():
            CallAssistantGUI._config_window = ConfigurationWindow(self.root)
        else:
            # Bring existing window to front
            CallAssistantGUI._config_window.window.lift()
            CallAssistantGUI._config_window.window.focus_force()


def main():
    root = tk.Tk()
    app = CallAssistantGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
