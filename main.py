import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import math
import os
import webbrowser
import base64

try:
    with open(os.path.join(os.path.dirname(__file__), 'dev_avatar.b64'), 'r') as f:
        DEV_AVATAR_B64 = f.read().replace('\n', '')
except FileNotFoundError:
    DEV_AVATAR_B64 = ""

class FileSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced File Splitter")
        self.root.geometry("550x300")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f6fa")

        # Style
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use('clam')
            
        style.configure("TFrame", background="#f5f6fa")
        style.configure("TLabel", background="#f5f6fa", foreground="#2f3640", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 9))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), foreground="#44bd32")

        # Header
        header_frame = ttk.Frame(root, padding="15 15 15 0")
        header_frame.pack(fill=tk.X)
        
        lbl_title = ttk.Label(header_frame, text="Advanced File Splitter", font=("Segoe UI", 16, "bold"), foreground="#2f3640")
        lbl_title.pack(side=tk.LEFT)
        
        btn_dev = ttk.Button(header_frame, text="Developer: Myst_25 🧑‍💻", command=self.show_dev_card)
        btn_dev.pack(side=tk.RIGHT)

        # Main frame
        self.main_frame = ttk.Frame(root, padding="25")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid column weights to make the entry expand dynamically
        self.main_frame.columnconfigure(1, weight=1)

        self.input_file = tk.StringVar()
        self.num_parts = tk.IntVar(value=2)

        # Input file row
        ttk.Label(self.main_frame, text="Input File:").grid(row=0, column=0, sticky='w', pady=(0, 15))
        ttk.Entry(self.main_frame, textvariable=self.input_file).grid(row=0, column=1, sticky='ew', padx=10, pady=(0, 15))
        ttk.Button(self.main_frame, text="Browse", command=self.browse_file, width=8).grid(row=0, column=2, sticky='e', pady=(0, 15))

        # Num parts row
        ttk.Label(self.main_frame, text="Number of parts:").grid(row=1, column=0, sticky='w', pady=(0, 15))
        ttk.Spinbox(self.main_frame, from_=2, to=1000, textvariable=self.num_parts, width=8).grid(row=1, column=1, sticky='w', padx=10, pady=(0, 15))

        # Split button
        btn_split = ttk.Button(self.main_frame, text="▶ SPLIT FILE", command=self.split_file, style="Accent.TButton")
        btn_split.grid(row=2, column=0, columnspan=3, pady=(25, 0))

    def browse_file(self):
        f = filedialog.askopenfilename(
            title="Select a text file",
            filetypes=[("Text files", "*.txt"), ("Markdown files", "*.md"), ("All files", "*.*")]
        )
        if f:
            self.input_file.set(f)

    def split_file(self):
        input_path = self.input_file.get()
        if not input_path or not os.path.exists(input_path):
            messagebox.showerror("Error", "Please select a valid input file.")
            return

        parts = self.num_parts.get()
        if parts < 2:
            messagebox.showerror("Error", "Number of parts must be at least 2.")
            return

        try:
            with open(input_path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file:\n{e}")
            return

        if not lines:
            messagebox.showinfo("Info", "The file is empty.")
            return
            
        if parts > len(lines):
            messagebox.showwarning("Warning", f"File only has {len(lines)} lines. Splitting into {len(lines)} parts instead.")
            parts = len(lines)

        base_dir = os.path.dirname(input_path)
        base_name, ext = os.path.splitext(os.path.basename(input_path))
        
        lines_per_part = math.ceil(len(lines) / parts)
        saved_files = []

        for i in range(parts):
            start = i * lines_per_part
            end = (i + 1) * lines_per_part
            chunk = lines[start:end]
            
            if not chunk:
                break
                
            out_name = f"{base_name}_part{i+1}{ext}"
            out_path = os.path.join(base_dir, out_name)
            
            with open(out_path, "w", encoding="utf-8") as out_f:
                out_f.writelines(chunk)
            saved_files.append(out_path)
            
        msg = f"Successfully split into {len(saved_files)} parts:\n\n"
        msg += "\n".join([os.path.basename(f) for f in saved_files])
        messagebox.showinfo("Done", msg)

    def show_dev_card(self):
        popup = tk.Toplevel(self.root)
        popup.title("About the Developer")
        popup.geometry("350x450")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()

        popup.configure(bg="#f5f6fa")
        
        try:
            if DEV_AVATAR_B64:
                img_data = base64.b64decode(DEV_AVATAR_B64)
                self.dev_img = tk.PhotoImage(data=img_data)
                lbl_img = tk.Label(popup, image=self.dev_img, bg="#f5f6fa")
                lbl_img.pack(pady=20)
        except Exception:
            pass

        lbl_name = tk.Label(popup, text="Myst_25", font=("Segoe UI", 18, "bold"), bg="#f5f6fa", fg="#2f3640")
        lbl_name.pack(pady=(0, 5))

        lbl_desc = tk.Label(popup, text="Creator of Advanced File Splitter", font=("Segoe UI", 10), bg="#f5f6fa", fg="#7f8fa6")
        lbl_desc.pack(pady=(0, 20))

        btn_github = ttk.Button(popup, text="⭐ GitHub: myst-25", command=lambda: webbrowser.open("https://github.com/myst-25/"))
        btn_github.pack(fill=tk.X, padx=40, pady=5)
        
        btn_tg = ttk.Button(popup, text="✈️ Telegram: Myst_25", command=lambda: webbrowser.open("https://t.me/Myst_25"))
        btn_tg.pack(fill=tk.X, padx=40, pady=5)
        
        btn_close = ttk.Button(popup, text="Close", command=popup.destroy)
        btn_close.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSplitterApp(root)
    root.mainloop()