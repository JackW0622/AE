import csv
import re
from pathlib import Path

import barcode
from barcode.errors import IllegalCharacterError
from barcode.writer import ImageWriter

# ---------------------------------------------------------------------------
# Configuration (use uppercase for constants!)
# ---------------------------------------------------------------------------
MAX_SLUG_LEN = 40        # truncate very long values so filenames stay readable
ROW_PAD      = 5         # zero-pad row index: 00001, 00002 …

# ---------------------------------------------------------------------------
# helpers: slugify and ensure_unique_path must come before generate_barcodes
# ---------------------------------------------------------------------------

def slugify(text: str, max_len: int = MAX_SLUG_LEN) -> str:
    """Return an ASCII-only, filesystem-safe slug trimmed to *max_len* chars."""
    slug = re.sub(r"[\\/:*?\"<>|\s]+", "_", text)
    slug = slug.strip("_") or "blank"
    return slug[:max_len]

def ensure_unique_path(base_path: Path) -> Path:
    """Append _1, _2 … until the *.png* filename is unique on disk."""
    candidate = base_path
    counter   = 1
    while candidate.with_suffix(".png").exists():
        candidate = base_path.with_name(f"{base_path.name}_{counter}")
        counter  += 1
    return candidate

def text_to_numeric_seq(text: str) -> str:
    """Convert every char in text to its 3-digit ASCII code."""
    return "".join(f"{ord(c):03d}" for c in text)

# ---------------------------------------------------------------------------
# barcode generation
# ---------------------------------------------------------------------------

def generate_barcodes(values, output_dir: str = "barcodes"):
    out_dir = Path(output_dir)
    out_dir.mkdir(exist_ok=True)

    generated_files = []
    for idx, value in enumerate(values, start=1):
        plain = str(value)                             # original text
        data  = text_to_numeric_seq(plain)             # numeric sequence for barcode
        slug  = slugify(plain)                         # human-readable filename portion
        fname = f"{idx:0{ROW_PAD}d}_{slug}"             # uses ROW_PAD constant
        target = ensure_unique_path(out_dir / fname)

        try:
            code = barcode.get("code128", data, writer=ImageWriter())
            saved = code.save(str(target), options={"write_text": False})
            generated_files.append(saved)
            print(f"Generated barcode: {saved} (from “{plain}” → {data})")
        except IllegalCharacterError as e:
            print(f"⚠️  Cannot barcode “{plain}”: {e}. Skipping.")

    return generated_files

# ---------------------------------------------------------------------------
# main entry point
# ---------------------------------------------------------------------------

def read_data_from_csv(csv_file: str):
    cells = []
    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            cells.extend(cell.strip() for cell in row if cell.strip())
    return cells

def main():
    csv_file = input("CSV file path (enter for default): ") or "casualty_data.csv"
    values   = read_data_from_csv(csv_file)
    if not values:
        print("No data found.")
        return

    output_dir = input("Output directory (enter for default): ") or "casualty_barcodes"
    files = generate_barcodes(values, output_dir)
    print(f"\nCreated {len(files)} barcodes in “{output_dir}”")

if __name__ == "__main__":
    main()
