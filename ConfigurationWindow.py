"""
Configuration Window for AI Call Assistant - Modern Design
Manages Prompts and Sessions with beautiful styling
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
from pathlib import Path
import os
import json
import sys
import ctypes


class StyledConfigurationWindow:
    # Modern Color Scheme (same as main GUI)
    COLORS = {
        'primary': '#2563EB',
        'primary_dark': '#1E40AF',
        'primary_light': '#DBEAFE',
        'secondary': '#10B981',
        'danger': '#EF4444',
        'warning': '#F59E0B',
        'bg_main': '#F9FAFB',
        'bg_card': '#FFFFFF',
        'bg_sidebar': '#F3F4F6',
        'text_primary': '#111827',
        'text_secondary': '#6B7280',
        'border': '#E5E7EB',
        'success': '#10B981'
    }

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("⚙️ Configuration Manager")
        self.window.geometry("1100x750")
        self.window.configure(bg=self.COLORS['bg_main'])

        # State variables
        self.current_file = None
        self.original_content = ""
        self.current_category = None

        # Paths
        self.base_path = Path(__file__).parent
        self.prompt_paths = {
            "Live Analysis": self.base_path / "prompts" / "live_analysis",
            "Final Report": self.base_path / "prompts" / "final_report"
        }
        self.session_path = self.base_path / "sessions"

        # Load config to get active prompts
        self.config = self.load_config()
        self.active_prompts = {
            "Live Analysis": self.config.get("active_live_analysis_prompt", "default"),
            "Final Report": self.config.get("active_final_report_prompt", "default")
        }

        # Setup styles
        self.setup_styles()

        # Create UI
        self.create_widgets()

    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')

        # Frames
        style.configure('Main.TFrame', background=self.COLORS['bg_main'])
        style.configure('Card.TFrame', background=self.COLORS['bg_card'])
        style.configure('Sidebar.TFrame', background=self.COLORS['bg_sidebar'])
        style.configure('Header.TFrame', background=self.COLORS['primary'])

        # Labels
        style.configure('Header.TLabel',
                       background=self.COLORS['primary'],
                       foreground='white',
                       font=('Segoe UI', 16, 'bold'))
        style.configure('SectionTitle.TLabel',
                       background=self.COLORS['bg_card'],
                       foreground=self.COLORS['text_primary'],
                       font=('Segoe UI', 11, 'bold'))
        style.configure('SidebarLabel.TLabel',
                       background=self.COLORS['bg_sidebar'],
                       foreground=self.COLORS['text_primary'],
                       font=('Segoe UI', 9, 'bold'))
        style.configure('CardLabel.TLabel',
                       background=self.COLORS['bg_card'],
                       foreground=self.COLORS['text_primary'])
        style.configure('Info.TLabel',
                       background=self.COLORS['bg_card'],
                       foreground=self.COLORS['text_secondary'],
                       font=('Segoe UI', 8))

        # Notebook
        style.configure('TNotebook', background=self.COLORS['bg_main'], borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Segoe UI', 10, 'bold'))

    def create_widgets(self):
        # ============================================
        # HEADER
        # ============================================
        header = ttk.Frame(self.window, style='Header.TFrame', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)

        header_content = ttk.Frame(header, style='Header.TFrame')
        header_content.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Label(header_content, text="⚙️  Configuration Manager", style='Header.TLabel').pack()

        # ============================================
        # MAIN CONTENT
        # ============================================
        content = ttk.Frame(self.window, style='Main.TFrame', padding="20")
        content.pack(fill='both', expand=True)

        # Create notebook with tabs
        self.notebook = ttk.Notebook(content)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.create_prompts_tab()
        self.create_sessions_tab()

    def create_prompts_tab(self):
        """Create the Prompts management tab"""
        tab = ttk.Frame(self.notebook, style='Main.TFrame', padding="15")
        self.notebook.add(tab, text="  📝 Prompts  ")

        # Main container
        container = ttk.Frame(tab, style='Main.TFrame')
        container.pack(fill='both', expand=True)

        # ============================================
        # LEFT SIDEBAR
        # ============================================
        sidebar = ttk.Frame(container, style='Sidebar.TFrame', width=280)
        sidebar.pack(side='left', fill='y', padx=(0, 15))
        sidebar.pack_propagate(False)

        sidebar_content = ttk.Frame(sidebar, style='Sidebar.TFrame', padding="15")
        sidebar_content.pack(fill='both', expand=True)

        # Category selection
        ttk.Label(sidebar_content, text="Prompt Type", style='SidebarLabel.TLabel').pack(anchor='w', pady=(0, 5))

        self.prompt_category_var = tk.StringVar()
        category_combo = ttk.Combobox(sidebar_content, textvariable=self.prompt_category_var,
                                      values=list(self.prompt_paths.keys()), state="readonly")
        category_combo.pack(fill='x', pady=(0, 15))
        category_combo.bind("<<ComboboxSelected>>", self.on_prompt_category_change)

        # File list
        ttk.Label(sidebar_content, text="Available Prompts", style='SidebarLabel.TLabel').pack(anchor='w', pady=(0, 5))

        list_container = ttk.Frame(sidebar_content, style='Sidebar.TFrame')
        list_container.pack(fill='both', expand=True, pady=(0, 15))

        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side='right', fill='y')

        self.prompt_listbox = tk.Listbox(list_container, yscrollcommand=scrollbar.set,
                                         font=('Segoe UI', 9), relief='flat',
                                         borderwidth=1, highlightthickness=1,
                                         highlightcolor=self.COLORS['primary'],
                                         selectbackground=self.COLORS['primary_light'],
                                         selectforeground=self.COLORS['primary_dark'])
        self.prompt_listbox.pack(side='left', fill='both', expand=True)
        self.prompt_listbox.bind("<<ListboxSelect>>", self.on_prompt_select)
        scrollbar.config(command=self.prompt_listbox.yview)

        # Action buttons
        button_container = ttk.Frame(sidebar_content, style='Sidebar.TFrame')
        button_container.pack(fill='x')

        self.create_action_button(button_container, "➕ New", self.new_prompt, self.COLORS['success']).pack(fill='x', pady=(0, 5))
        self.create_action_button(button_container, "✏️ Rename", self.rename_prompt, self.COLORS['warning']).pack(fill='x', pady=(0, 5))
        self.create_action_button(button_container, "🗑️ Delete", self.delete_prompt, self.COLORS['danger']).pack(fill='x')

        # ============================================
        # RIGHT EDITOR PANEL
        # ============================================
        editor_panel = ttk.Frame(container, style='Card.TFrame', relief='solid', borderwidth=1)
        editor_panel.pack(side='left', fill='both', expand=True)

        # Editor header
        editor_header = ttk.Frame(editor_panel, style='Card.TFrame', padding="15")
        editor_header.pack(fill='x')

        ttk.Label(editor_header, text="📄 Prompt Content", style='SectionTitle.TLabel').pack(anchor='w')

        # Editor content
        editor_content = ttk.Frame(editor_panel, style='Card.TFrame', padding="15")
        editor_content.pack(fill='both', expand=True)

        self.prompt_editor = scrolledtext.ScrolledText(editor_content, wrap=tk.WORD,
                                                        font=('Consolas', 10),
                                                        relief='flat', borderwidth=1,
                                                        bg='#FAFAFA')
        self.prompt_editor.pack(fill='both', expand=True)

        # Info label
        info_container = ttk.Frame(editor_content, style='Card.TFrame')
        info_container.pack(fill='x', pady=(10, 0))

        ttk.Label(info_container,
                 text="💡 Placeholders: {participants_list}, {session_number}, {session_content}, {participants_table}",
                 style='Info.TLabel').pack(anchor='w')

        # Editor footer with buttons
        editor_footer = ttk.Frame(editor_panel, style='Card.TFrame', padding="15")
        editor_footer.pack(fill='x')

        self.create_action_button(editor_footer, "💾 Save Changes", self.save_prompt, self.COLORS['primary']).pack(side='left', padx=(0, 10))
        self.create_action_button(editor_footer, "↺ Reset", self.reset_prompt, self.COLORS['text_secondary']).pack(side='left', padx=(0, 10))
        self.create_action_button(editor_footer, "⭐ Set as Active", self.set_active_prompt, self.COLORS['warning']).pack(side='left')

        # Status
        self.prompt_status_label = tk.Label(editor_footer, text="Select a prompt to begin",
                                            bg=self.COLORS['bg_card'],
                                            fg=self.COLORS['text_secondary'],
                                            font=('Segoe UI', 9))
        self.prompt_status_label.pack(side='right')

    def create_sessions_tab(self):
        """Create the Sessions management tab"""
        tab = ttk.Frame(self.notebook, style='Main.TFrame', padding="15")
        self.notebook.add(tab, text="  📅 Sessions  ")

        # Main container
        container = ttk.Frame(tab, style='Main.TFrame')
        container.pack(fill='both', expand=True)

        # ============================================
        # LEFT SIDEBAR
        # ============================================
        sidebar = ttk.Frame(container, style='Sidebar.TFrame', width=280)
        sidebar.pack(side='left', fill='y', padx=(0, 15))
        sidebar.pack_propagate(False)

        sidebar_content = ttk.Frame(sidebar, style='Sidebar.TFrame', padding="15")
        sidebar_content.pack(fill='both', expand=True)

        # File list
        ttk.Label(sidebar_content, text="Available Sessions", style='SidebarLabel.TLabel').pack(anchor='w', pady=(0, 5))

        list_container = ttk.Frame(sidebar_content, style='Sidebar.TFrame')
        list_container.pack(fill='both', expand=True, pady=(0, 15))

        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side='right', fill='y')

        self.session_listbox = tk.Listbox(list_container, yscrollcommand=scrollbar.set,
                                          font=('Segoe UI', 9), relief='flat',
                                          borderwidth=1, highlightthickness=1,
                                          highlightcolor=self.COLORS['primary'],
                                          selectbackground=self.COLORS['primary_light'],
                                          selectforeground=self.COLORS['primary_dark'])
        self.session_listbox.pack(side='left', fill='both', expand=True)
        self.session_listbox.bind("<<ListboxSelect>>", self.on_session_select)
        scrollbar.config(command=self.session_listbox.yview)

        # Action buttons
        button_container = ttk.Frame(sidebar_content, style='Sidebar.TFrame')
        button_container.pack(fill='x')

        self.create_action_button(button_container, "➕ New", self.new_session, self.COLORS['success']).pack(fill='x', pady=(0, 5))
        self.create_action_button(button_container, "✏️ Rename", self.rename_session, self.COLORS['warning']).pack(fill='x', pady=(0, 5))
        self.create_action_button(button_container, "🗑️ Delete", self.delete_session, self.COLORS['danger']).pack(fill='x', pady=(0, 5))
        self.create_action_button(button_container, "🔄 Refresh", self.refresh_sessions, self.COLORS['text_secondary']).pack(fill='x')

        # ============================================
        # RIGHT EDITOR PANEL
        # ============================================
        editor_panel = ttk.Frame(container, style='Card.TFrame', relief='solid', borderwidth=1)
        editor_panel.pack(side='left', fill='both', expand=True)

        # Editor header
        editor_header = ttk.Frame(editor_panel, style='Card.TFrame', padding="15")
        editor_header.pack(fill='x')

        ttk.Label(editor_header, text="📄 Session Content", style='SectionTitle.TLabel').pack(anchor='w')

        # Editor content
        editor_content = ttk.Frame(editor_panel, style='Card.TFrame', padding="15")
        editor_content.pack(fill='both', expand=True)

        self.session_editor = scrolledtext.ScrolledText(editor_content, wrap=tk.WORD,
                                                         font=('Consolas', 10),
                                                         relief='flat', borderwidth=1,
                                                         bg='#FAFAFA')
        self.session_editor.pack(fill='both', expand=True)

        # Info label
        info_container = ttk.Frame(editor_content, style='Card.TFrame')
        info_container.pack(fill='x', pady=(10, 0))

        ttk.Label(info_container,
                 text="💡 Define session objectives, goals, and success criteria here",
                 style='Info.TLabel').pack(anchor='w')

        # Editor footer with buttons
        editor_footer = ttk.Frame(editor_panel, style='Card.TFrame', padding="15")
        editor_footer.pack(fill='x')

        self.create_action_button(editor_footer, "💾 Save Changes", self.save_session, self.COLORS['primary']).pack(side='left', padx=(0, 10))
        self.create_action_button(editor_footer, "↺ Reset", self.reset_session, self.COLORS['text_secondary']).pack(side='left')

        # Status
        self.session_status_label = tk.Label(editor_footer, text="Select a session to begin",
                                             bg=self.COLORS['bg_card'],
                                             fg=self.COLORS['text_secondary'],
                                             font=('Segoe UI', 9))
        self.session_status_label.pack(side='right')

        # Load sessions
        self.refresh_sessions()

    def load_config(self):
        """Load config.json"""
        config_path = self.base_path / "config.json"
        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {}

    def save_config_file(self):
        """Save config.json"""
        config_path = self.base_path / "config.json"
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")

    def set_screen_capture_protection(self, enable=True):
        """Enable or disable screen capture protection for this window"""
        try:
            if sys.platform == "win32":
                # Wait for window to be created
                self.window.update_idletasks()
                hwnd = ctypes.windll.user32.GetParent(self.window.winfo_id())
                if enable:
                    ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 0x00000011)
                else:
                    ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 0x00000000)
        except Exception as e:
            print(f"Could not set screen capture protection on Configuration Window: {e}")

    def create_action_button(self, parent, text, command, color):
        """Create a styled action button"""
        return tk.Button(parent, text=text, command=command,
                        bg=color, fg='white' if color != self.COLORS['text_secondary'] else self.COLORS['text_primary'],
                        font=('Segoe UI', 9, 'bold'),
                        relief='flat', padx=15, pady=8,
                        cursor='hand2')

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

        active_prompt = self.active_prompts.get(category, "default")

        for file in sorted(prompt_dir.glob("*.txt")):
            filename = file.stem
            # Mark active prompt with star
            if filename == active_prompt:
                display_name = f"⭐ {filename}"
            else:
                display_name = filename
            self.prompt_listbox.insert(tk.END, display_name)

    def on_prompt_select(self, event=None):
        """When a prompt is selected from the list"""
        selection = self.prompt_listbox.curselection()
        if not selection:
            return

        display_name = self.prompt_listbox.get(selection[0])
        # Strip star emoji if present
        filename = display_name.replace("⭐ ", "")
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

            self.prompt_editor.delete(1.0, tk.END)
            self.prompt_editor.insert(1.0, content)

            self.prompt_status_label.config(text=f"✓ Loaded: {file_path.name}",
                                           fg=self.COLORS['success'])

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load prompt:\n{e}")
            self.prompt_status_label.config(text=f"✗ Error: {e}",
                                           fg=self.COLORS['danger'])

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
            self.prompt_status_label.config(text="✓ Saved successfully",
                                           fg=self.COLORS['success'])
            messagebox.showinfo("Success", f"Saved: {self.current_file.name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save:\n{e}")
            self.prompt_status_label.config(text=f"✗ Error: {e}",
                                           fg=self.COLORS['danger'])

    def reset_prompt(self):
        """Reset prompt editor to original content"""
        if not self.current_file:
            return

        self.prompt_editor.delete(1.0, tk.END)
        self.prompt_editor.insert(1.0, self.original_content)
        self.prompt_status_label.config(text="↺ Reset to original",
                                       fg=self.COLORS['primary'])

    def new_prompt(self):
        """Create a new prompt file"""
        category = self.prompt_category_var.get()
        if not category:
            messagebox.showwarning("No Category", "Please select a prompt type first.")
            return

        filename = simpledialog.askstring("New Prompt", "Enter filename (without .txt):")
        if not filename:
            return

        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()
        if not filename:
            messagebox.showerror("Invalid Name", "Filename cannot be empty.")
            return

        file_path = self.prompt_paths[category] / f"{filename}.txt"

        if file_path.exists():
            messagebox.showerror("File Exists", f"A prompt named '{filename}' already exists.")
            return

        template = f"# {filename}\n\nYour prompt content here...\n"

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(template)

            self.refresh_prompts()
            self.prompt_status_label.config(text=f"✓ Created: {filename}.txt",
                                           fg=self.COLORS['success'])
            messagebox.showinfo("Success", f"Created new prompt: {filename}.txt")

            # Select the new file
            for i in range(self.prompt_listbox.size()):
                display_name = self.prompt_listbox.get(i)
                clean_name = display_name.replace("⭐ ", "")
                if clean_name == filename:
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

        display_name = self.prompt_listbox.get(selection[0])
        old_name = display_name.replace("⭐ ", "")
        category = self.prompt_category_var.get()

        new_name = simpledialog.askstring("Rename Prompt", f"Rename '{old_name}' to:", initialvalue=old_name)
        if not new_name or new_name == old_name:
            return

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
            self.prompt_status_label.config(text=f"✓ Renamed to: {new_name}.txt",
                                           fg=self.COLORS['success'])

            for i in range(self.prompt_listbox.size()):
                display_name = self.prompt_listbox.get(i)
                clean_name = display_name.replace("⭐ ", "")
                if clean_name == new_name:
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

        display_name = self.prompt_listbox.get(selection[0])
        filename = display_name.replace("⭐ ", "")
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
            self.prompt_status_label.config(text=f"✓ Deleted: {filename}.txt",
                                           fg=self.COLORS['warning'])

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete:\n{e}")

    def set_active_prompt(self):
        """Set the selected prompt as the active one for recording"""
        selection = self.prompt_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a prompt to set as active.")
            return

        category = self.prompt_category_var.get()
        if not category:
            messagebox.showwarning("No Category", "Please select a prompt type first.")
            return

        display_name = self.prompt_listbox.get(selection[0])
        # Strip star emoji if present
        filename = display_name.replace("⭐ ", "")

        # Update active prompts dictionary
        self.active_prompts[category] = filename

        # Update config with appropriate key
        if category == "Live Analysis":
            self.config["active_live_analysis_prompt"] = filename
        elif category == "Final Report":
            self.config["active_final_report_prompt"] = filename

        # Save config
        self.save_config_file()

        # Refresh the list to show new active prompt
        self.refresh_prompts()

        # Update status
        self.prompt_status_label.config(text=f"✓ Set '{filename}' as active for {category}",
                                       fg=self.COLORS['success'])
        messagebox.showinfo("Success", f"'{filename}' is now the active prompt for {category}")

    # ============================================
    # SESSION TAB METHODS (similar to prompt methods)
    # ============================================

    def refresh_sessions(self):
        """Refresh the list of available sessions"""
        self.session_listbox.delete(0, tk.END)

        if not self.session_path.exists():
            self.session_path.mkdir(parents=True, exist_ok=True)
            return

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

            self.session_editor.delete(1.0, tk.END)
            self.session_editor.insert(1.0, content)

            self.session_status_label.config(text=f"✓ Loaded: {file_path.name}",
                                            fg=self.COLORS['success'])

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load session:\n{e}")
            self.session_status_label.config(text=f"✗ Error: {e}",
                                            fg=self.COLORS['danger'])

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
            self.session_status_label.config(text="✓ Saved successfully",
                                            fg=self.COLORS['success'])
            messagebox.showinfo("Success", f"Saved: {self.current_file.name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save:\n{e}")
            self.session_status_label.config(text=f"✗ Error: {e}",
                                            fg=self.COLORS['danger'])

    def reset_session(self):
        """Reset session editor to original content"""
        if not self.current_file:
            return

        self.session_editor.delete(1.0, tk.END)
        self.session_editor.insert(1.0, self.original_content)
        self.session_status_label.config(text="↺ Reset to original",
                                        fg=self.COLORS['primary'])

    def new_session(self):
        """Create a new session file"""
        filename = simpledialog.askstring("New Session", "Enter session filename (e.g., session_4):")
        if not filename:
            return

        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()
        if not filename:
            messagebox.showerror("Invalid Name", "Filename cannot be empty.")
            return

        file_path = self.session_path / f"{filename}.txt"

        if file_path.exists():
            messagebox.showerror("File Exists", f"A session named '{filename}' already exists.")
            return

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
            self.session_status_label.config(text=f"✓ Created: {filename}.txt",
                                            fg=self.COLORS['success'])
            messagebox.showinfo("Success", f"Created new session: {filename}.txt")

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
            self.session_status_label.config(text=f"✓ Renamed to: {new_name}.txt",
                                            fg=self.COLORS['success'])

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
            self.session_status_label.config(text=f"✓ Deleted: {filename}.txt",
                                            fg=self.COLORS['warning'])

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete:\n{e}")
