import tkinter as tk
from tkinter import filedialog
import os
import sys
import subprocess

class LightweightEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lightweight Code Editor")
        self.geometry("800x600")
        self.configure(bg="#1e1e1e") # Dark attractive theme
        
        # Open in full screen as requested
        self.attributes('-fullscreen', True)
        
        self.current_file_path = None
        self.show_home_screen()

    # --- UI COMPONENTS ---
    def create_hover_button(self, parent, text, font, bg, fg, hover_bg, command, width=30):
        """Creates a modern flat button with a hover effect."""
        btn = tk.Button(parent, text=text, font=font, bg=bg, fg=fg, 
                        activebackground=hover_bg, activeforeground=fg, 
                        width=width, height=2, relief="flat", cursor="hand2", command=command)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    # --- SCREEN 1: HOME SCREEN ---
    def show_home_screen(self):
        self.clear_screen()
        frame = tk.Frame(self, bg="#1e1e1e")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = tk.Label(frame, text="Code Editor", font=("Segoe UI", 40, "bold"), bg="#1e1e1e", fg="#ffffff")
        title.pack(pady=40)
        
        btn_new = self.create_hover_button(frame, "Create a File", ("Segoe UI", 16), "#2d2d30", "white", "#3e3e42", self.show_language_screen)
        btn_new.pack(pady=10)
        
        btn_open = self.create_hover_button(frame, "Open & Edit Existing File", ("Segoe UI", 16), "#2d2d30", "white", "#3e3e42", self.open_existing_file)
        btn_open.pack(pady=10)

        btn_exit = tk.Button(frame, text="Exit Application", font=("Segoe UI", 12), bg="#d9534f", fg="white", 
                             relief="flat", cursor="hand2", command=self.destroy)
        btn_exit.pack(pady=40)

    # --- SCREEN 2: LANGUAGE SELECTION ---
    def show_language_screen(self):
        self.clear_screen()
        frame = tk.Frame(self, bg="#1e1e1e")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = tk.Label(frame, text="Choose Language", font=("Segoe UI", 36, "bold"), bg="#1e1e1e", fg="#ffffff")
        title.pack(pady=40)
        
        languages = ["Python", "Java", "JavaScript", "HTML", "CSS", "C++", "C#", "SQL", "PHP", "Ruby", "Go", "Plain Text"]
        grid_frame = tk.Frame(frame, bg="#1e1e1e")
        grid_frame.pack()
        
        row, col = 0, 0
        for lang in languages:
            btn = self.create_hover_button(grid_frame, lang, ("Segoe UI", 14), "#252526", "#4fc3f7", "#333337", 
                                           lambda l=lang: self.start_editor(l), width=12)
            btn.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 3: # 4 columns wide
                col = 0
                row += 1

        btn_back = tk.Button(frame, text="Back to Home", font=("Segoe UI", 12), bg="#3a3d41", fg="white", 
                             relief="flat", cursor="hand2", command=self.show_home_screen)
        btn_back.pack(pady=30)

    # --- SCREEN 3: EDITOR SCREEN ---
    def start_editor(self, language, content="", file_path=None):
        self.current_file_path = file_path
        self.clear_screen()
        
        self.editor_frame = tk.Frame(self, bg="#1e1e1e")
        self.editor_frame.pack(fill="both", expand=True)
        
        # Top Header Bar
        top_bar = tk.Frame(self.editor_frame, bg="#2d2d30", height=35)
        top_bar.pack(fill="x", side="top")
        
        file_name = os.path.basename(file_path) if file_path else f"Untitled - {language}"
        self.lbl_title = tk.Label(top_bar, text=file_name, bg="#2d2d30", fg="#cccccc", font=("Segoe UI", 11))
        self.lbl_title.pack(side="left", padx=15, pady=5)
        
        btn_close = tk.Button(top_bar, text="Close File", bg="#d9534f", fg="white", relief="flat", command=self.show_home_screen)
        btn_close.pack(side="right", padx=5)

        text_container = tk.Frame(self.editor_frame, bg="#1e1e1e")
        text_container.pack(fill="both", expand=True)

        # Left Side: Line Numbers
        self.line_numbers = tk.Text(text_container, width=5, padx=5, pady=5, bg="#1e1e1e", fg="#858585", 
                                    font=("Consolas", 14), state="disabled", relief="flat", highlightthickness=0)
        self.line_numbers.pack(side="left", fill="y")
        
        # Right Side: Code Area
        self.text_area = tk.Text(text_container, bg="#1e1e1e", fg="#d4d4d4", font=("Consolas", 14), pady=5,
                                 insertbackground="white", relief="flat", highlightthickness=0, undo=True)
        self.text_area.pack(side="right", fill="both", expand=True)
        
        if content:
            self.text_area.insert("1.0", content)
            
        self.update_line_numbers()
        
        # Key Bindings for dynamic updates and shortcuts
        self.text_area.bind("<Any-KeyPress>", self.update_line_numbers)
        self.text_area.bind("<MouseWheel>", self.update_line_numbers)
        self.text_area.bind("<Button-1>", self.update_line_numbers)
        
        # Shortcuts (*Note: Used standard Ctrl+S for re-saving as requested, Tkinter uses Ctrl+Z for undo by default)
        self.bind("<Control-s>", self.save_file)
        self.bind("<Control-S>", self.save_file)
        self.bind("<Control-n>", self.new_window)
        self.bind("<Control-N>", self.new_window)
        
        self.text_area.focus_set()

    def update_line_numbers(self, event=None):
        """Keeps the line numbers on the left synced with the text code."""
        lines = str(self.text_area.get("1.0", "end-1c").count("\n") + 1)
        line_numbers_content = "\n".join(str(i) for i in range(1, int(lines) + 1))
        
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", line_numbers_content)
        self.line_numbers.yview_moveto(self.text_area.yview()[0]) # Sync scrolling
        self.line_numbers.config(state="disabled")
        
        # Slight delay to ensure scroll syncs perfectly when holding keys
        self.after(10, lambda: self.line_numbers.yview_moveto(self.text_area.yview()[0]))

    # --- FUNCTIONALITY ---
    def open_existing_file(self):
        file_path = filedialog.askopenfilename(title="Open File")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.start_editor(language="Auto", content=content, file_path=file_path)
            except Exception:
                pass # Silently fail to prevent crashes on unsupported files

    def save_file(self, event=None):
        if self.current_file_path is None:
            # Opens 'Save As' browse screen
            extensions = [("All Files", "*.*"), ("Python", "*.py"), ("HTML", "*.html"), ("Text", "*.txt")]
            file_path = filedialog.asksaveasfilename(title="Save As", defaultextension=".txt", filetypes=extensions)
            if file_path:
                self.current_file_path = file_path
            else:
                return "break"
                
        # Saves code locally without closing the page
        try:
            content = self.text_area.get("1.0", "end-1c")
            with open(self.current_file_path, "w", encoding="utf-8") as file:
                file.write(content)
            self.lbl_title.config(text=f"Saved: {os.path.basename(self.current_file_path)}")
        except Exception:
            pass
            
        return "break"

    def new_window(self, event=None):
        """Triggers a completely new instance of the application."""
        if getattr(sys, 'frozen', False):
            # If running as a compiled .exe
            subprocess.Popen([sys.executable] + sys.argv[1:])
        else:
            # If running as a .py script
            subprocess.Popen([sys.executable] + sys.argv)
        return "break"

    def clear_screen(self):
        """Destroys current screen widgets before drawing the new screen."""
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = LightweightEditor()
    app.mainloop()