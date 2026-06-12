"""
AI Call Assistant - Graphical User Interface
=============================================
A user-friendly GUI for the AI Call Assistant that allows easy configuration
and control of recording sessions without editing config files.

Features:
- Configure API keys and models
- Set up participants and session details
- Start/Stop recording with buttons
- View live transcripts and AI feedback
- Automatic config saving
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import json
import os
import sys
from pathlib import Path

# CallAssistant will be imported dynamically when needed
# This prevents API key validation on GUI startup

# Import the ConfigurationWindow
from ConfigurationWindow import ConfigurationWindow


class CallAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Call Assistant - Control Panel")
        self.root.geometry("900x700")

        # State variables
        self.is_running = False
        self.recording_thread = None
        self.transcript_queue = queue.Queue()

        # Create UI
        self.create_widgets()
        self.load_config()

    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # ============================================
        # API CONFIGURATION SECTION
        # ============================================
        api_frame = ttk.LabelFrame(main_frame, text="API Configuration", padding="10")
        api_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        api_frame.columnconfigure(1, weight=1)

        # API Key
        ttk.Label(api_frame, text="OpenRouter API Key:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.api_key_var = tk.StringVar(value=os.getenv("OPENROUTER_API_KEY", ""))
        self.api_key_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, show="*", width=50)
        self.api_key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))

        self.show_key_var = tk.BooleanVar()
        show_key_check = ttk.Checkbutton(api_frame, text="Show", variable=self.show_key_var,
                                         command=self.toggle_api_key_visibility)
        show_key_check.grid(row=0, column=2)

        # LLM Model
        ttk.Label(api_frame, text="LLM Model:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.llm_model_var = tk.StringVar()
        llm_models = [
            "qwen/qwen3-vl-30b-a3b-instruct",
            "anthropic/claude-3-opus",
            "anthropic/claude-3-sonnet",
            "openai/gpt-4-turbo",
            "openai/gpt-3.5-turbo",
            "meta-llama/llama-3-70b-instruct"
        ]
        llm_combo = ttk.Combobox(api_frame, textvariable=self.llm_model_var, values=llm_models, width=47)
        llm_combo.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        llm_combo.set("qwen/qwen3-vl-30b-a3b-instruct")

        # Audio Model
        ttk.Label(api_frame, text="Audio Model:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.audio_model_var = tk.StringVar()
        audio_models = [
            "openai/whisper-large-v3-turbo",
            "openai/whisper-large-v3",
            "openai/whisper-medium",
            "openai/whisper-small"
        ]
        audio_combo = ttk.Combobox(api_frame, textvariable=self.audio_model_var, values=audio_models, width=47)
        audio_combo.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        audio_combo.set("openai/whisper-large-v3-turbo")

        # ============================================
        # SESSION CONFIGURATION SECTION
        # ============================================
        session_frame = ttk.LabelFrame(main_frame, text="Session Configuration", padding="10")
        session_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        session_frame.columnconfigure(1, weight=1)

        # Participants
        ttk.Label(session_frame, text="Participants:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.participants_var = tk.StringVar()
        ttk.Entry(session_frame, textvariable=self.participants_var).grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Label(session_frame, text="(comma-separated)", font=("", 8)).grid(row=0, column=2, sticky=tk.W, padx=(5, 0))

        # Session Number
        ttk.Label(session_frame, text="Session Number:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.session_num_var = tk.StringVar()
        session_spin = ttk.Spinbox(session_frame, from_=1, to=100, textvariable=self.session_num_var, width=10)
        session_spin.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))

        # Output File
        ttk.Label(session_frame, text="Output File:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.output_file_var = tk.StringVar()
        ttk.Entry(session_frame, textvariable=self.output_file_var).grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))

        # Speaker Label
        ttk.Label(session_frame, text="Speaker Label:").grid(row=3, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.speaker_label_var = tk.StringVar()
        ttk.Entry(session_frame, textvariable=self.speaker_label_var, width=20).grid(row=3, column=1, sticky=tk.W, pady=(5, 0))

        # Listener Label
        ttk.Label(session_frame, text="Listener Label:").grid(row=4, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.listener_label_var = tk.StringVar()
        ttk.Entry(session_frame, textvariable=self.listener_label_var, width=20).grid(row=4, column=1, sticky=tk.W, pady=(5, 0))

        # ============================================
        # CONTROL SECTION
        # ============================================
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Button frame
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=0, columnspan=2)

        self.start_button = ttk.Button(button_frame, text="Start Recording", command=self.start_recording, width=20)
        self.start_button.grid(row=0, column=0, padx=(0, 5))

        self.stop_button = ttk.Button(button_frame, text="Stop & Generate Report", command=self.stop_recording,
                                      state="disabled", width=20)
        self.stop_button.grid(row=0, column=1, padx=(5, 0))

        # Status
        ttk.Label(control_frame, text="Status:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, font=("", 10, "bold"))
        status_label.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))

        # ============================================
        # LIVE DISPLAY SECTION
        # ============================================
        display_frame = ttk.LabelFrame(main_frame, text="Live Transcript & AI Feedback", padding="10")
        display_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

        self.transcript_display = scrolledtext.ScrolledText(display_frame, wrap=tk.WORD, height=15)
        self.transcript_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.transcript_display.config(state="disabled")

        # Clear button
        clear_button = ttk.Button(display_frame, text="Clear Display", command=self.clear_display)
        clear_button.grid(row=1, column=0, sticky=tk.E, pady=(5, 0))

        # ============================================
        # BOTTOM BUTTONS
        # ============================================
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=4, column=0, sticky=(tk.W, tk.E))

        save_config_button = ttk.Button(bottom_frame, text="Save Configuration", command=self.save_config)
        save_config_button.grid(row=0, column=0, sticky=tk.W)

        config_button = ttk.Button(bottom_frame, text="Configuration", command=self.open_configuration_window)
        config_button.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))

        ttk.Label(bottom_frame, text="AI Call Assistant v1.0", font=("", 8)).grid(row=0, column=2, sticky=tk.E)
        bottom_frame.columnconfigure(2, weight=1)

    def toggle_api_key_visibility(self):
        """Toggle API key visibility"""
        if self.show_key_var.get():
            self.api_key_entry.config(show="")
        else:
            self.api_key_entry.config(show="*")

    def load_config(self):
        """Load existing configuration from config.json"""
        try:
            config_path = Path(__file__).parent / "config.json"
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                # Load values into UI
                self.participants_var.set(", ".join(config.get("participants", [])))
                self.session_num_var.set(str(config.get("current_session", 1)))
                self.output_file_var.set(config.get("output_file", "Session_Report.md"))
                self.speaker_label_var.set(config.get("speaker_label", "Speaker"))
                self.listener_label_var.set(config.get("listener_label", "Listeners"))

                self.append_to_display("Configuration loaded successfully.\n", "info")
        except Exception as e:
            self.append_to_display(f"Error loading config: {e}\n", "error")

    def save_config(self):
        """Save current configuration to config.json"""
        try:
            # Parse participants
            participants = [p.strip() for p in self.participants_var.get().split(",") if p.strip()]

            config = {
                "participants": participants,
                "current_session": int(self.session_num_var.get()),
                "output_file": self.output_file_var.get(),
                "whisper_keywords": participants,  # Use participants as keywords
                "hallucination_filter": [
                    "untertitel",
                    "vielen dank",
                    "danke fürs zuschauen",
                    "abonniert den kanal",
                    "tschüss",
                    "like and subscribe",
                    "thanks for watching"
                ],
                "speaker_label": self.speaker_label_var.get(),
                "listener_label": self.listener_label_var.get()
            }

            config_path = Path(__file__).parent / "config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            messagebox.showinfo("Success", "Configuration saved successfully!")
            self.append_to_display("Configuration saved.\n", "info")

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

        # Check if session file exists
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

        # Save configuration first
        self.save_config()

        # Set environment variables
        os.environ["OPENROUTER_API_KEY"] = self.api_key_var.get()
        os.environ["LLM_MODEL"] = self.llm_model_var.get()
        os.environ["AUDIO_MODEL"] = self.audio_model_var.get()

        # Update UI
        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_var.set("Recording...")

        self.append_to_display("="*50 + "\n", "info")
        self.append_to_display("Starting AI Call Assistant...\n", "info")
        self.append_to_display(f"LLM Model: {self.llm_model_var.get()}\n", "info")
        self.append_to_display(f"Audio Model: {self.audio_model_var.get()}\n", "info")
        self.append_to_display("="*50 + "\n\n", "info")

        # Start recording in separate thread
        self.recording_thread = threading.Thread(target=self.run_assistant, daemon=True)
        self.recording_thread.start()

        # Start UI update loop
        self.update_display()

    def run_assistant(self):
        """Run the CallAssistant in a separate thread"""
        try:
            # Import CallAssistant module now (after API key is set)
            import CallAssistant
            import importlib

            # Reload to pick up new environment variables
            importlib.reload(CallAssistant)

            # Store reference for later use
            self.CallAssistant = CallAssistant

            # Redirect logging to GUI
            self.setup_logging_redirect()

            # Run the main assistant
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

        # Add GUI handler to CallAssistant logger
        gui_handler = GUIHandler(self.transcript_queue)
        gui_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S'))
        self.CallAssistant.logger.addHandler(gui_handler)

    def stop_recording(self):
        """Stop the recording and generate report"""
        if self.is_running:
            self.append_to_display("\nStopping recording and generating report...\n", "info")

            # Trigger the same behavior as Ctrl+C in the original script
            if self.recording_thread and self.recording_thread.is_alive() and hasattr(self, 'CallAssistant'):
                # Send shutdown signals to queues
                self.CallAssistant.audio_queue.put(("shutdown", None))
                self.CallAssistant.live_text_queue.put(None)

                # Generate report
                threading.Thread(target=self.CallAssistant.generate_final_report, daemon=True).start()

            # Update UI
            self.is_running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.status_var.set("Ready")

            self.append_to_display("\nRecording stopped. Report generation in progress...\n", "info")

    def update_display(self):
        """Update the transcript display with queued messages"""
        try:
            while True:
                tag, message = self.transcript_queue.get_nowait()
                self.append_to_display(message, tag)

                if tag == "done":
                    self.is_running = False
                    self.start_button.config(state="normal")
                    self.stop_button.config(state="disabled")
                    self.status_var.set("Ready")
        except queue.Empty:
            pass

        # Schedule next update if still running
        if self.is_running or not self.transcript_queue.empty():
            self.root.after(100, self.update_display)

    def append_to_display(self, message, tag="normal"):
        """Append message to transcript display with color coding"""
        self.transcript_display.config(state="normal")

        # Configure tags for color coding
        self.transcript_display.tag_config("info", foreground="blue")
        self.transcript_display.tag_config("error", foreground="red")
        self.transcript_display.tag_config("success", foreground="green")

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
        ConfigurationWindow(self.root)


def main():
    root = tk.Tk()
    app = CallAssistantGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
