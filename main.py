import tkinter as tk
from tkinter import filedialog, messagebox, ttk
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
        self.root.title("✂️ Advanced File Splitter")
        self.root.geometry("600x360")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f2f5")

        # Configure generic ttk styles for the entry and spinbox
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use('clam')
            
        style.configure("TEntry", fieldbackground="#ffffff", borderwidth=1)
        style.configure("TSpinbox", fieldbackground="#ffffff", borderwidth=1)

        # Header Banner
        header_bg = "#2c3e50"
        header_frame = tk.Frame(root, bg=header_bg, pady=15, padx=20)
        header_frame.pack(fill=tk.X)
        
        lbl_title = tk.Label(header_frame, text="Advanced File Splitter", font=("Segoe UI", 16, "bold"), bg=header_bg, fg="#ffffff")
        lbl_title.pack(side=tk.LEFT)
        
        # Flat modern dev button
        self.btn_dev = tk.Button(header_frame, text="Developer: Myst_25 🧑‍💻", font=("Segoe UI", 9, "bold"), 
                                 bg="#34495e", fg="#ffffff", relief="flat", padx=10, pady=5, cursor="hand2",
                                 activebackground="#3b5998", activeforeground="#ffffff", command=self.show_dev_card)
        self.btn_dev.pack(side=tk.RIGHT)
        self.btn_dev.bind("<Enter>", lambda e: self.btn_dev.config(bg="#3b5998"))
        self.btn_dev.bind("<Leave>", lambda e: self.btn_dev.config(bg="#34495e"))

        # Main Card (White background)
        self.card_frame = tk.Frame(root, bg="#ffffff", padx=30, pady=30, highlightbackground="#d1d8e0", highlightthickness=1)
        self.card_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.card_frame.columnconfigure(1, weight=1)

        self.input_file = tk.StringVar()
        self.num_parts = tk.IntVar(value=2)

        # Input file row
        lbl_input = tk.Label(self.card_frame, text="📄 Input File:", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#2f3640")
        lbl_input.grid(row=0, column=0, sticky='w', pady=(0, 20))
        
        ttk.Entry(self.card_frame, textvariable=self.input_file, font=("Segoe UI", 10)).grid(row=0, column=1, sticky='ew', padx=15, pady=(0, 20), ipady=4)
        
        self.btn_browse = tk.Button(self.card_frame, text="Browse...", font=("Segoe UI", 9, "bold"),
                                    bg="#ecf0f1", fg="#2c3e50", relief="flat", padx=15, pady=4, cursor="hand2",
                                    activebackground="#bdc3c7", command=self.browse_file)
        self.btn_browse.grid(row=0, column=2, sticky='e', pady=(0, 20))
        self.btn_browse.bind("<Enter>", lambda e: self.btn_browse.config(bg="#bdc3c7"))
        self.btn_browse.bind("<Leave>", lambda e: self.btn_browse.config(bg="#ecf0f1"))

        # Num parts row
        lbl_parts = tk.Label(self.card_frame, text="✂️ Number of parts:", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#2f3640")
        lbl_parts.grid(row=1, column=0, sticky='w', pady=(0, 25))
        
        ttk.Spinbox(self.card_frame, from_=2, to=1000, textvariable=self.num_parts, width=10, font=("Segoe UI", 11)).grid(row=1, column=1, sticky='w', padx=15, pady=(0, 25), ipady=3)

        # Split button (Primary CTA)
        self.btn_split = tk.Button(self.card_frame, text="▶ SPLIT FILE NOW", font=("Segoe UI", 11, "bold"), 
                                   bg="#27ae60", fg="#ffffff", relief="flat", padx=20, pady=8, cursor="hand2",
                                   activebackground="#2ecc71", activeforeground="#ffffff", command=self.split_file)
        self.btn_split.grid(row=2, column=0, columnspan=3, pady=(10, 0), sticky='ew')
        self.btn_split.bind("<Enter>", lambda e: self.btn_split.config(bg="#2ecc71"))
        self.btn_split.bind("<Leave>", lambda e: self.btn_split.config(bg="#27ae60"))

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
        popup.geometry("350x460")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()

        popup.configure(bg="#ffffff")
        
        # Subtle header
        header = tk.Frame(popup, bg="#2c3e50", height=100)
        header.pack(fill=tk.X)
        
        try:
            if DEV_AVATAR_B64:
                img_data = base64.b64decode(DEV_AVATAR_B64)
                self.dev_img = tk.PhotoImage(data=img_data)
                lbl_img = tk.Label(popup, image=self.dev_img, bg="#ffffff", highlightthickness=0, bd=0)
                lbl_img.place(relx=0.5, y=100, anchor="center") # Overlay the avatar
        except Exception:
            pass

        content_frame = tk.Frame(popup, bg="#ffffff")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(55, 15))

        lbl_name = tk.Label(content_frame, text="Myst_25", font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#2c3e50")
        lbl_name.pack(pady=(0, 5))

        lbl_desc = tk.Label(content_frame, text="Creator of Advanced File Splitter", font=("Segoe UI", 10), bg="#ffffff", fg="#7f8fa6")
        lbl_desc.pack(pady=(0, 20))

        def create_link_btn(parent, text, url, bg, hover_bg):
            btn = tk.Button(parent, text=text, font=("Segoe UI", 10, "bold"), bg=bg, fg="#ffffff", 
                            relief="flat", cursor="hand2", activebackground=hover_bg, activeforeground="#ffffff",
                            command=lambda: webbrowser.open(url))
            btn.pack(fill=tk.X, padx=40, pady=6, ipady=4)
            btn.bind("<Enter>", lambda e, b=btn, c=hover_bg: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=bg: b.config(bg=c))
            return btn

        create_link_btn(content_frame, "⭐ GitHub: myst-25", "https://github.com/myst-25/", "#333333", "#555555")
        create_link_btn(content_frame, "✈️ Telegram: Myst_25", "https://t.me/Myst_25", "#0088cc", "#00aaff")
        
        btn_close = tk.Button(content_frame, text="Close", font=("Segoe UI", 9, "bold"), bg="#ecf0f1", fg="#2c3e50", 
                              relief="flat", cursor="hand2", activebackground="#bdc3c7", command=popup.destroy)
        btn_close.pack(pady=(15, 0), ipady=4, ipadx=20)
        btn_close.bind("<Enter>", lambda e: btn_close.config(bg="#bdc3c7"))
        btn_close.bind("<Leave>", lambda e: btn_close.config(bg="#ecf0f1"))

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSplitterApp(root)
    root.mainloop()