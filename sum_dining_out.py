"""Summarize "Dinning Out" expenses from an Excel credit card workbook.

This utility reads sheets whose names match the pattern `dd dddd`, skips the
first 20 rows, and sums values from column C when column D equals
`Dinning Out`.

Usage:
    python sum_dining_out.py
    python sum_dining_out.py "C:/Users/XIAOM/OneDrive/Home Budget/CreditCard.xlsx"

Example Output:
    Sheet '04 2024': 123.45
    Sheet '05 2024': 67.89

    Grand total for 'Dinning Out': 191.34
"""

import re
from pathlib import Path
from typing import Iterable

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

SHEET_NAME_PATTERN = re.compile(r"^\d{2} \d{4}$")
TARGET_CATEGORY = "Gas"
START_ROW = 21  # After row 20
COLUMN_C = 3
COLUMN_D = 4


def iter_matching_sheets(workbook) -> Iterable[Worksheet]:
    for sheet_name in workbook.sheetnames:
        if SHEET_NAME_PATTERN.fullmatch(sheet_name):
            yield workbook[sheet_name]


def sum_dining_out_values(sheet: Worksheet) -> float:
    total = 0.0
    for row in sheet.iter_rows(min_row=START_ROW, values_only=True):
        if len(row) < COLUMN_D:
            continue

        value_c = row[COLUMN_C - 1]
        value_d = row[COLUMN_D - 1]
        if value_d != TARGET_CATEGORY:
            continue

        if isinstance(value_c, (int, float)):
            total += float(value_c)
            continue

        try:
            total += float(value_c)
        except (TypeError, ValueError):
            continue
    return total


def main(excel_path: str) -> None:
    path = Path(excel_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {path}")

    try:
        workbook = load_workbook(path, data_only=True, read_only=True)
    except PermissionError as exc:
        raise PermissionError(
            f"Permission denied when opening Excel file: {path}. "
            "Ensure the file is not locked by another program and you have access rights."
        ) from exc
    except OSError as exc:
        raise OSError(
            f"Unable to open Excel file: {path}. "
            f"Verify the file is accessible and is a valid .xlsx workbook.\n" 
            f"Original error: {exc}"
        ) from exc

    grand_total = 0.0

    try:
        for sheet in iter_matching_sheets(workbook):
            sheet_total = sum_dining_out_values(sheet)
            grand_total += sheet_total
            print(f"Sheet '{sheet.title}': {sheet_total:.2f} Grand total so far: {grand_total:.2f}")

        print(f"\nGrand total for '{TARGET_CATEGORY}': {grand_total}")
    finally:
        try:
            workbook.close()
        except Exception:
            pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Sum values in column C for rows where column D is 'Dinning Out' in matching sheets."
    )
    parser.add_argument(
        "excel_path",
        nargs="?",
        default=r"C:\Users\XIAOM\OneDrive\Home Budget\CreditCard.xlsx",
        help="Path to the Excel workbook."
    )
    args = parser.parse_args()

    main(args.excel_path)
