import argparse
from excel_unlocker.unlocker import ExcelUnlocker

def main():
    parser = argparse.ArgumentParser(description="Remove sheet/workbook protection from Excel files.")
    parser.add_argument("input", help="Path to the password-protected XLSX file")
    parser.add_argument("-o", "--output", help="Path to save the unlocked file (default: unlocked_input.xlsx)")

    args = parser.parse_args()

    output_file = args.output if args.output else f"unlocked_{args.input}"

    try:
        unlocker = ExcelUnlocker(args.input, output_file)
        unlocker.unlock()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
