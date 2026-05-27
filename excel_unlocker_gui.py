import os
import re
import shutil
import zipfile
import threading
import tempfile
from pathlib import Path
from tkinter import filedialog, messagebox
import customtkinter as ctk

# --- Constants & Theme ---
C_COLOR_BG = "#1A1A1A"      # Deep Charcoal
C_COLOR_ACCENT = "#00FFC8"   # Mint Green / Electric Blue
C_COLOR_TEXT = "#E0E0E0"
C_FONT_HEADER = ("Segoe UI", 24, "bold")
C_FONT_SUBHEADER = ("Segoe UI", 14)
C_FONT_DEFAULT = ("Segoe UI", 12)

class ExcelUnlockerCore:
    """
    Core logic for removing sheet and workbook protection from .xlsx files.
    """
    def __init__(self, file_path: str, status_callback=None):
        self.file_path = Path(file_path)
        self.status_callback = status_callback

    def _update_status(self, text: str):
        if self.status_callback:
            self.status_callback(text)

    def process(self):
        temp_dir = None
        try:
            # 1. Backup Creation
            self._update_status("Creating backup...")
            backup_path = self.file_path.with_name(f"{self.file_path.stem}_Backup{self.file_path.suffix}")
            shutil.copy2(self.file_path, backup_path)

            # 2. Zip Extraction
            self._update_status("Extracting components...")
            temp_dir = Path(tempfile.mkdtemp())
            with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # 3. XML Targeted Modification
            self._update_status("Modifying XML structures...")
            self._remove_protection(temp_dir)

            # 4. Reassembly
            self._update_status("Reassembling Excel...")
            with zipfile.ZipFile(self.file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_full_path = Path(root) / file
                        # Archive path relative to temp_dir root
                        archive_name = file_full_path.relative_to(temp_dir)
                        zipf.write(file_full_path, archive_name)

            self._update_status("Success!")
            return True, "File unlocked successfully!"

        except Exception as e:
            return False, str(e)
        finally:
            if temp_dir and temp_dir.exists():
                shutil.rmtree(temp_dir)

    def _remove_protection(self, root_dir: Path):
        # Pattern to match <sheetProtection ... /> and <workbookProtection ... />
        protection_pattern = re.compile(r'<(?:sheetProtection|workbookProtection)[^>]*/>')

        # Target: All XML files in the archive
        for xml_file in root_dir.rglob("*.xml"):
            # Narrow focus to worksheets and workbook to avoid unnecessary reads
            if "worksheets" in xml_file.parts or "workbook.xml" in xml_file.name:
                content = xml_file.read_text(encoding="utf-8")
                if protection_pattern.search(content):
                    new_content = protection_pattern.sub("", content)
                    xml_file.write_text(new_content, encoding="utf-8")

class UnlockerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("Excel Sheet Unlocker")
        self.geometry("600x400")
        self.minsize(400, 300)
        self.configure(fg_color=C_COLOR_BG)

        # State
        self.selected_file = None

        self._setup_ui()
        self.bind("<Configure>", self._on_resize)

    def _setup_ui(self):
        # Centered Main Frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(expand=True, padx=40, pady=40)

        # Header
        self.header = ctk.CTkLabel(
            self.main_frame, 
            text="Excel Sheet Unlocker", 
            font=C_FONT_HEADER, 
            text_color=C_COLOR_TEXT
        )
        self.header.pack(pady=(0, 5))

        self.subheader = ctk.CTkLabel(
            self.main_frame, 
            text="Remove sheet and workbook restrictions instantly", 
            font=C_FONT_SUBHEADER, 
            text_color="#888888"
        )
        self.subheader.pack(pady=(0, 30))

        # File Selection Area
        self.file_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color="#252525", 
            border_color="#333333", 
            border_width=1,
            corner_radius=10
        )
        self.file_frame.pack(fill="x", pady=(0, 20))

        self.path_label = ctk.CTkLabel(
            self.file_frame,
            text="No file selected",
            font=C_FONT_DEFAULT,
            text_color="#AAAAAA",
            wraplength=300
        )
        self.path_label.pack(side="left", padx=20, pady=20, expand=True)

        self.browse_btn = ctk.CTkButton(
            self.file_frame, 
            text="Browse File", 
            fg_color="#333333", 
            hover_color="#444444", 
            text_color=C_COLOR_TEXT,
            command=self._browse_file,
            width=100
        )
        self.browse_btn.pack(side="right", padx=20, pady=20)

        # Status Indicator
        self.status_label = ctk.CTkLabel(
            self.main_frame, 
            text="Idle", 
            font=C_FONT_DEFAULT, 
            text_color="#888888"
        )
        self.status_label.pack(pady=(0, 20))

        # Action Button
        self.unlock_btn = ctk.CTkButton(
            self.main_frame, 
            text="Unlock Spreadsheet", 
            font=C_FONT_DEFAULT, 
            fg_color=C_COLOR_ACCENT, 
            text_color="#000000", 
            hover_color="#00D1A7", 
            command=self._start_unlock_process,
            state="disabled",
            height=45,
            corner_radius=8
        )
        self.unlock_btn.pack(fill="x", pady=0)

    def _browse_file(self):
        file = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel Files", "*.xlsx *.xlsm *.xltx *.xltm"), ("All Files", "*.*")]
        )
        if file:
            self.selected_file = file
            self.path_label.configure(text=Path(file).name, text_color=C_COLOR_TEXT)
            self.unlock_btn.configure(state="normal")
            self.status_label.configure(text="File ready for unlocking", text_color="#AAAAAA")

    def _update_ui_status(self, text: str):
        # This is called from a separate thread, so we use after() or simply update
        # since CTk labels are usually thread-safe for simple text changes.
        self.after(0, lambda: self.status_label.configure(
            text=text, 
            text_color=C_COLOR_ACCENT if text == "Success!" else "#AAAAAA"
        ))

    def _start_unlock_process(self):
        if not self.selected_file:
            return

        # UI State update
        self.unlock_btn.configure(state="disabled")
        self.browse_btn.configure(state="disabled")
        
        # Launch backend thread
        threading.Thread(target=self._run_backend, daemon=True).start()

    def _run_backend(self):
        unlocker = ExcelUnlockerCore(self.selected_file, self._update_ui_status)
        success, message = unlocker.process()
        
        self.after(0, lambda: self._handle_completion(success, message))

    def _handle_completion(self, success: bool, message: str):
        self.unlock_btn.configure(state="normal")
        self.browse_btn.configure(state="normal")

        if success:
            messagebox.showinfo("Completed", message)
        else:
            self.status_label.configure(text="Error occurred", text_color="#FF4B4B")
            messagebox.showerror("Error", f"An unexpected error occurred:\n\n{message}")

    def _on_resize(self, event):
        # Update wraplength of the path label based on current window width
        # We subtract some padding to ensure it doesn't hit the browse button
        new_wraplength = max(200, self.winfo_width() - 200)
        self.path_label.configure(wraplength=new_wraplength)


if __name__ == "__main__":
    # Initialize App
    app = UnlockerApp()
    # Force dark mode
    ctk.set_appearance_mode("dark")
    app.mainloop()
