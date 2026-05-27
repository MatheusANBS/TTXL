import os
import zipfile
import shutil
import re
from pathlib import Path

class ExcelUnlocker:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.temp_dir = Path("temp_excel_extraction")

    def unlock(self):
        """
        Removes sheet and workbook protection from an XLSX file.
        """
        try:
            # 1. Extract the XLSX (which is a ZIP)
            with zipfile.ZipFile(self.input_file, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)

            # 2. Remove protection tags from XML files
            self._remove_protection_tags()

            # 3. Re-zip the files back into an XLSX
            self._repackage()
            
            print(f"Successfully unlocked: {self.output_file}")
        finally:
            # Cleanup
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)

    def _remove_protection_tags(self):
        """
        Searches for <sheetProtection ... /> and <workbookProtection ... /> 
        tags in XML files and removes them.
        """
        # Pattern to match sheetProtection or workbookProtection tags
        protection_pattern = re.compile(r'<sheetProtection[^>]*/>|<workbookProtection[^>]*/>')

        for xml_file in self.temp_dir.rglob("*.xml"):
            content = xml_file.read_text(encoding="utf-8")
            if protection_pattern.search(content):
                new_content = protection_pattern.sub("", content)
                xml_file.write_text(new_content, encoding="utf-8")

    def _repackage(self):
        """
        Zips the extracted content back into a .xlsx file.
        """
        with zipfile.ZipFile(self.output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    # Add file to zip with relative path
                    zipf.write(file_path, file_path.relative_to(self.temp_dir))

if __name__ == "__main__":
    # Quick manual test logic if run directly
    import sys
    if len(sys.argv) > 2:
        unlocker = ExcelUnlocker(sys.argv[1], sys.argv[2])
        unlocker.unlock()
    else:
        print("Usage: python unlocker.py <input.xlsx> <output.xlsx>")
