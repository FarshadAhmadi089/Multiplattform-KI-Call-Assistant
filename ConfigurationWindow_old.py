"""
Configuration Window for AI Call Assistant
Manages Prompts and Sessions with file operations
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
from pathlib import Path
import os
import shutil


class ConfigurationWindow:
    """
    Unified configuration window for managing Prompts and Sessions
    """
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Configuration Manager")
        self.window.geometry("950x700")

        # State variables
        self.current_file = None
        self.original_content = ""
        self.current_category = None  # "live_analysis", "final_report", or "sessions"

        # Paths
        self.base_path = Path(__file__).parent
        self.prompt_paths = {
            "Live Analysis": self.base_path / "prompts" / "live_analysis",
            "Final Report": self.base_path / "prompts" / "final_report"
        }
        self.session_path = self.base_path / "sessions"

        # Create UI
        self.create_widgets()

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create tabs
        self.prompt_tab = ttk.Frame(self.notebook, padding="10")
        self.session_tab = ttk.Frame(self.notebook, padding="10")

        self.notebook.add(self.prompt_tab, text="Prompts")
        self.notebook.add(self.session_tab, text="Sessions")

        # Configure tab frames
        self.prompt_tab.columnconfigure(1, weight=1)
        self.prompt_tab.rowconfigure(1, weight=1)
        self.session_tab.columnconfigure(1, weight=1)
        self.session_tab.rowconfigure(1, weight=1)

        # Build prompt tab
        self.create_prompt_tab()

        # Build session tab
        self.create_session_tab()

    def create_prompt_tab(self):
        """Create the Prompts management tab"""
        # ============================================
        # LEFT PANEL - File Browser
        # ============================================
        left_frame = ttk.Frame(self.prompt_tab)
        left_frame.grid(row=0, column=0, rowspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # Category selection
        ttk.Label(left_frame, text="Prompt Type:", font=("", 9, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        self.prompt_category_var = tk.StringVar()
        category_combo = ttk.Combobox(left_frame, textvariable=self.prompt_category_var,
                                      values=list(self.prompt_paths.keys()), state="readonly", width=20)
        category_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        category_combo.bind("<<ComboboxSelected>>", self.on_prompt_category_change)

        # File list
        ttk.Label(left_frame, text="Available Prompts:", font=("", 9, "bold")).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))

        list_frame = ttk.Frame(left_frame)
        list_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.prompt_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=15)
        self.prompt_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.prompt_listbox.bind("<<ListboxSelect>>", self.on_prompt_select)
        scrollbar.config(command=self.prompt_listbox.yview)

        left_frame.rowconfigure(3, weight=1)

        # File management buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(5, 0))

        ttk.Button(button_frame, text="New", command=self.new_prompt, width=10).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="Rename", command=self.rename_prompt, width=10).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="Delete", command=self.delete_prompt, width=10).grid(row=0, column=2)

        # ============================================
        # RIGHT PANEL - Editor
        # ============================================
        right_frame = ttk.LabelFrame(self.prompt_tab, text="Prompt Content", padding="10")
        right_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        # Text editor
        self.prompt_editor = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=60, height=25, font=("Consolas", 10))
        self.prompt_editor.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Info label
        info_label = ttk.Label(right_frame,
                              text="💡 Placeholders: {participants_list}, {session_number}, {session_content}, {participants_table}",
                              foreground="blue", font=("", 8))
        info_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))

        # ============================================
        # BOTTOM BUTTONS
        # ============================================
        prompt_button_frame = ttk.Frame(self.prompt_tab)
        prompt_button_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(10, 0))

        self.prompt_save_btn = ttk.Button(prompt_button_frame, text="Save Changes", command=self.save_prompt)
        self.prompt_save_btn.grid(row=0, column=0, padx=(0, 5))

        self.prompt_reset_btn = ttk.Button(prompt_button_frame, text="Reset", command=self.reset_prompt)
        self.prompt_reset_btn.grid(row=0, column=1)

        # Spacer
        prompt_button_frame.columnconfigure(2, weight=1)

        # Status
        self.prompt_status_label = ttk.Label(prompt_button_frame, text="Select a prompt to begin", foreground="gray")
        self.prompt_status_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))

    def create_session_tab(self):
        """Create the Sessions management tab"""
        # ============================================
        # LEFT PANEL - File Browser
        # ============================================
        left_frame = ttk.Frame(self.session_tab)
        left_frame.grid(row=0, column=0, rowspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # File list
        ttk.Label(left_frame, text="Available Sessions:", font=("", 9, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        list_frame = ttk.Frame(left_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.session_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=15)
        self.session_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.session_listbox.bind("<<ListboxSelect>>", self.on_session_select)
        scrollbar.config(command=self.session_listbox.yview)

        left_frame.rowconfigure(1, weight=1)

        # File management buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))

        ttk.Button(button_frame, text="New", command=self.new_session, width=10).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="Rename", command=self.rename_session, width=10).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="Delete", command=self.delete_session, width=10).grid(row=0, column=2)

        # Refresh button
        ttk.Button(left_frame, text="Refresh List", command=self.refresh_sessions, width=25).grid(row=3, column=0, pady=(10, 0))

        # ============================================
        # RIGHT PANEL - Editor
        # ============================================
        right_frame = ttk.LabelFrame(self.session_tab, text="Session Content", padding="10")
        right_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        # Text editor
        self.session_editor = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=60, height=25, font=("Consolas", 10))
        self.session_editor.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Info label
        info_label = ttk.Label(right_frame,
                              text="💡 Define session objectives, goals, and success criteria here",
                              foreground="blue", font=("", 8))
        info_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))

        # ============================================
        # BOTTOM BUTTONS
        # ============================================
        session_button_frame = ttk.Frame(self.session_tab)
        session_button_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(10, 0))

        self.session_save_btn = ttk.Button(session_button_frame, text="Save Changes", command=self.save_session)
        self.session_save_btn.grid(row=0, column=0, padx=(0, 5))

        self.session_reset_btn = ttk.Button(session_button_frame, text="Reset", command=self.reset_session)
        self.session_reset_btn.grid(row=0, column=1)

        # Spacer
        session_button_frame.columnconfigure(2, weight=1)

        # Status
        self.session_status_label = ttk.Label(session_button_frame, text="Select a session to begin", foreground="gray")
        self.session_status_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))

        # Load sessions on init
        self.refresh_sessions()

    # ============================================
    # PROMPT TAB METHODS
    # ============================================

    def on_prompt_category_change(self, event=None):
        """When prompt category changes, refresh the file list"""
        category = self.prompt_category_var.get()
        if not category:
            return

        self.current_category = category
        self.refresh_prompts()

    def refresh_prompts(self):
        """Refresh the list of available prompts"""
        category = self.prompt_category_var.get()
        if not category or category not in self.prompt_paths:
            return

        self.prompt_listbox.delete(0, tk.END)

        prompt_dir = self.prompt_paths[category]
        if not prompt_dir.exists():
            prompt_dir.mkdir(parents=True, exist_ok=True)
            return

        # List all .txt files
        for file in sorted(prompt_dir.glob("*.txt")):
            self.prompt_listbox.insert(tk.END, file.stem)

    def on_prompt_select(self, event=None):
        """When a prompt is selected from the list"""
        selection = self.prompt_listbox.curselection()
        if not selection:
            return

        filename = self.prompt_listbox.get(selection[0])
        self.load_prompt_file(filename)

    def load_prompt_file(self, filename):
        """Load a specific prompt file"""
        category = self.prompt_category_var.get()
        if not category:
            return

        file_path = self.prompt_paths[category] / f"{filename}.txt"

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            self.current_file = file_path
            self.original_content = content

            # Load into editor
            self.prompt_editor.delete(1.0, tk.END)
            self.prompt_editor.insert(1.0, content)

            self.prompt_status_label.config(text=f"Loaded: {file_path.name}", foreground="green")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load prompt:\n{e}")
            self.prompt_status_label.config(text=f"Error: {e}", foreground="red")

    def save_prompt(self):
        """Save changes to the current prompt"""
        if not self.current_file:
            messagebox.showwarning("No File", "No prompt file is currently loaded.")
            return

        content = self.prompt_editor.get(1.0, tk.END).rstrip()

        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(content)

            self.original_content = content
            self.prompt_status_label.config(text="✓ Saved successfully", foreground="green")
            messagebox.showinfo("Success", f"Saved: {self.current_file.name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save:\n{e}")
            self.prompt_status_label.config(text=f"Error: {e}", foreground="red")

    def reset_prompt(self):
        """Reset prompt editor to original content"""
        if not self.current_file:
            return

        self.prompt_editor.delete(1.0, tk.END)
        self.prompt_editor.insert(1.0, self.original_content)
        self.prompt_status_label.config(text="Reset to original", foreground="blue")

    def new_prompt(self):
        """Create a new prompt file"""
        category = self.prompt_category_var.get()
        if not category:
            messagebox.showwarning("No Category", "Please select a prompt type first.")
            return

        filename = simpledialog.askstring("New Prompt", "Enter filename (without .txt):")
        if not filename:
            return

        # Sanitize filename
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()
        if not filename:
            messagebox.showerror("Invalid Name", "Filename cannot be empty.")
            return

        file_path = self.prompt_paths[category] / f"{filename}.txt"

        if file_path.exists():
            messagebox.showerror("File Exists", f"A prompt named '{filename}' already exists.")
            return

        # Create with template
        template = f"# {filename}\n\nYour prompt content here...\n"

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(template)

            self.refresh_prompts()
            self.prompt_status_label.config(text=f"Created: {filename}.txt", foreground="green")
            messagebox.showinfo("Success", f"Created new prompt: {filename}.txt")

            # Select the new file
            for i in range(self.prompt_listbox.size()):
                if self.prompt_listbox.get(i) == filename:
                    self.prompt_listbox.selection_clear(0, tk.END)
                    self.prompt_listbox.selection_set(i)
                    self.load_prompt_file(filename)
                    break

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create prompt:\n{e}")

    def rename_prompt(self):
        """Rename the selected prompt"""
        selection = self.prompt_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a prompt to rename.")
            return

        old_name = self.prompt_listbox.get(selection[0])
        category = self.prompt_category_var.get()

        new_name = simpledialog.askstring("Rename Prompt", f"Rename '{old_name}' to:", initialvalue=old_name)
        if not new_name or new_name == old_name:
            return

        # Sanitize
        new_name = "".join(c for c in new_name if c.isalnum() or c in (' ', '-', '_')).strip()
        if not new_name:
            messagebox.showerror("Invalid Name", "Filename cannot be empty.")
            return

        old_path = self.prompt_paths[category] / f"{old_name}.txt"
        new_path = self.prompt_paths[category] / f"{new_name}.txt"

        if new_path.exists():
            messagebox.showerror("File Exists", f"A prompt named '{new_name}' already exists.")
            return

        try:
            old_path.rename(new_path)
            self.refresh_prompts()
            self.prompt_status_label.config(text=f"Renamed to: {new_name}.txt", foreground="green")

            # Select the renamed file
            for i in range(self.prompt_listbox.size()):
                if self.prompt_listbox.get(i) == new_name:
                    self.prompt_listbox.selection_clear(0, tk.END)
                    self.prompt_listbox.selection_set(i)
                    self.load_prompt_file(new_name)
                    break

        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename:\n{e}")

    def delete_prompt(self):
        """Delete the selected prompt"""
        selection = self.prompt_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a prompt to delete.")
            return

        filename = self.prompt_listbox.get(selection[0])
        category = self.prompt_category_var.get()

        response = messagebox.askyesno("Confirm Delete",
                                       f"Are you sure you want to delete '{filename}.txt'?\n\nThis cannot be undone.")
        if not response:
            return

        file_path = self.prompt_paths[category] / f"{filename}.txt"

        try:
            file_path.unlink()
            self.prompt_editor.delete(1.0, tk.END)
            self.current_file = None
            self.refresh_prompts()
            self.prompt_status_label.config(text=f"Deleted: {filename}.txt", foreground="orange")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete:\n{e}")

    # ============================================
    # SESSION TAB METHODS
    # ============================================

    def refresh_sessions(self):
        """Refresh the list of available sessions"""
        self.session_listbox.delete(0, tk.END)

        if not self.session_path.exists():
            self.session_path.mkdir(parents=True, exist_ok=True)
            return

        # List all .txt files
        for file in sorted(self.session_path.glob("*.txt")):
            self.session_listbox.insert(tk.END, file.stem)

    def on_session_select(self, event=None):
        """When a session is selected from the list"""
        selection = self.session_listbox.curselection()
        if not selection:
            return

        filename = self.session_listbox.get(selection[0])
        self.load_session_file(filename)

    def load_session_file(self, filename):
        """Load a specific session file"""
        file_path = self.session_path / f"{filename}.txt"

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            self.current_file = file_path
            self.original_content = content

            # Load into editor
            self.session_editor.delete(1.0, tk.END)
            self.session_editor.insert(1.0, content)

            self.session_status_label.config(text=f"Loaded: {file_path.name}", foreground="green")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load session:\n{e}")
            self.session_status_label.config(text=f"Error: {e}", foreground="red")

    def save_session(self):
        """Save changes to the current session"""
        if not self.current_file:
            messagebox.showwarning("No File", "No session file is currently loaded.")
            return

        content = self.session_editor.get(1.0, tk.END).rstrip()

        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(content)

            self.original_content = content
            self.session_status_label.config(text="✓ Saved successfully", foreground="green")
            messagebox.showinfo("Success", f"Saved: {self.current_file.name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save:\n{e}")
            self.session_status_label.config(text=f"Error: {e}", foreground="red")

    def reset_session(self):
        """Reset session editor to original content"""
        if not self.current_file:
            return

        self.session_editor.delete(1.0, tk.END)
        self.session_editor.insert(1.0, self.original_content)
        self.session_status_label.config(text="Reset to original", foreground="blue")

    def new_session(self):
        """Create a new session file"""
        filename = simpledialog.askstring("New Session", "Enter session filename (e.g., session_4):")
        if not filename:
            return

        # Sanitize filename
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()
        if not filename:
            messagebox.showerror("Invalid Name", "Filename cannot be empty.")
            return

        file_path = self.session_path / f"{filename}.txt"

        if file_path.exists():
            messagebox.showerror("File Exists", f"A session named '{filename}' already exists.")
            return

        # Create with template
        template = f"""Session - {filename}
{'='*50}

OBJECTIVES:
[Describe the main objectives of this session]

KEY GOALS:
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

SUCCESS CRITERIA:
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]
"""

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(template)

            self.refresh_sessions()
            self.session_status_label.config(text=f"Created: {filename}.txt", foreground="green")
            messagebox.showinfo("Success", f"Created new session: {filename}.txt")

            # Select the new file
            for i in range(self.session_listbox.size()):
                if self.session_listbox.get(i) == filename:
                    self.session_listbox.selection_clear(0, tk.END)
                    self.session_listbox.selection_set(i)
                    self.load_session_file(filename)
                    break

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create session:\n{e}")

    def rename_session(self):
        """Rename the selected session"""
        selection = self.session_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a session to rename.")
            return

        old_name = self.session_listbox.get(selection[0])

        new_name = simpledialog.askstring("Rename Session", f"Rename '{old_name}' to:", initialvalue=old_name)
        if not new_name or new_name == old_name:
            return

        # Sanitize
        new_name = "".join(c for c in new_name if c.isalnum() or c in (' ', '-', '_')).strip()
        if not new_name:
            messagebox.showerror("Invalid Name", "Filename cannot be empty.")
            return

        old_path = self.session_path / f"{old_name}.txt"
        new_path = self.session_path / f"{new_name}.txt"

        if new_path.exists():
            messagebox.showerror("File Exists", f"A session named '{new_name}' already exists.")
            return

        try:
            old_path.rename(new_path)
            self.refresh_sessions()
            self.session_status_label.config(text=f"Renamed to: {new_name}.txt", foreground="green")

            # Select the renamed file
            for i in range(self.session_listbox.size()):
                if self.session_listbox.get(i) == new_name:
                    self.session_listbox.selection_clear(0, tk.END)
                    self.session_listbox.selection_set(i)
                    self.load_session_file(new_name)
                    break

        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename:\n{e}")

    def delete_session(self):
        """Delete the selected session"""
        selection = self.session_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a session to delete.")
            return

        filename = self.session_listbox.get(selection[0])

        response = messagebox.askyesno("Confirm Delete",
                                       f"Are you sure you want to delete '{filename}.txt'?\n\nThis cannot be undone.")
        if not response:
            return

        file_path = self.session_path / f"{filename}.txt"

        try:
            file_path.unlink()
            self.session_editor.delete(1.0, tk.END)
            self.current_file = None
            self.refresh_sessions()
            self.session_status_label.config(text=f"Deleted: {filename}.txt", foreground="orange")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete:\n{e}")
