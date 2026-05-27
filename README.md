# <img src="assets/icon_excel.png" width="40" height="40"> Excel Sheet Unlocker

A professional tool designed to remove sheet and workbook protection from `.xlsx` files by manipulating the underlying XML structure.

## <img src="assets/icon_unlock.png" width="30" height="30"> Features

- **Modern GUI**: A sleek, responsive interface built with `customtkinter` that adapts to different screen resolutions.
- **CLI Mode**: A lightweight command-line interface for quick operations and power users.
- **One-Click Installer**: Professional Windows installer generated via Inno Setup, allowing installation without administrative privileges.
- **Safety First**: Automatically creates a backup of the original file before attempting to unlock it.

## <img src="assets/icon_python.png" width="30" height="30"> Getting Started

### Prerequisites
- Python 3.10+
- Windows 10/11 (for the GUI and Installer)

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Graphical User Interface (GUI)
Launch the modern interface:
```bash
python excel_unlocker_gui.py
```
Simply browse for your `.xlsx` file and click **"Unlock Spreadsheet"**.

### Command Line Interface (CLI)
Run the tool directly from the terminal:
```bash
python main.py path/to/protected.xlsx
```

## <img src="assets/icon_windows.png" width="30" height="30"> Development & Build Process

The project features a fully automated build pipeline to generate a standalone Windows installer.

### Generating the Installer
The build process is orchestrated by a PowerShell script that handles:
1. Cleaning build artifacts.
2. Synchronizing dependencies.
3. Bundling the app with **PyInstaller** (including `customtkinter` assets).
4. Compiling the final installer with **Inno Setup**.

To generate a new installer, run:
```powershell
.\scripts\build.ps1
```
The resulting installer will be available in: `installer_output\ExcelSheetUnlockUnlocker_Setup.exe`.

### Project Structure
- `src/excel_unlocker/`: Core unlocking logic.
- `excel_unlocker_gui.py`: Entry point for the GUI.
- `main.py`: Entry point for the CLI.
- `installer/`: Build configurations (`.spec` and `.iss`).
- `scripts/`: Automation scripts.

## How it Works

Excel `.xlsx` files are essentially ZIP archives containing XML files. Protection (passwords for sheets/workbooks) is stored as tags like `<sheetProtection ... />` or `<workbookProtection ... />`. 

This tool:
1. Creates a backup of the original file.
2. Extracts the ZIP archive into a temporary directory.
3. Uses regular expressions to identify and remove the protection tags from the XML files.
4. Repacks the modified XMLs back into a `.xlsx` archive.

> [!IMPORTANT]
> **Disclaimer:** This tool removes *sheet/workbook* protection. It does **NOT** decrypt files that are encrypted with a "Password to Open", as that requires a different decryption approach.
