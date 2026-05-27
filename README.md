# Excel Unlocker
This project removes sheet and workbook protection from `.xlsx` files by manipulating the underlying XML structure.

## How it works
Excel `.xlsx` files are essentially ZIP archives containing XML files. Protection (passwords for sheets/workbooks) is stored as tags like `<sheetProtection ... />`. This tool extracts the archive, removes these tags using regular expressions, and repacks the archive.

**Note:** This tool removes *sheet/workbook* protection. It does NOT decrypt files that are encrypted with a "Password to Open" (which requires a different, much more complex approach).

## Usage
```bash
python main.py path/to/protected.xlsx -o path/to/unlocked.xlsx
```
