import csv
import os
import re
from pathlib import Path

import barcode
from barcode.errors import IllegalCharacterError
from barcode.writer import ImageWriter
from requests import options

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MAX_SLUG_LEN = 40        # truncate very long values so filenames stay readable
ROW_PAD      = 5         # zero‑pad row index: 00001, 00002 …

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def slugify(text: str, max_len: int = MAX_SLUG_LEN) -> str:
    """Return an ASCII‑only, filesystem‑safe slug trimmed to *max_len* chars."""
    # Replace path‑forbidden characters / whitespace with underscore
    slug = re.sub(r"[\\/:*?\"<>|\s]+", "_", text)
    slug = slug.strip("_") or "blank"
    return slug[:max_len]


def read_data_from_csv(csv_file: str):
    """Read *every* non‑empty cell—numbers and words—from a CSV into a list."""
    cells = []
    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            cells.extend(cell.strip() for cell in row if cell.strip())
    return cells


def ensure_unique_path(base_path: Path) -> Path:
    """Append _1, _2 … until the *.png* filename is unique on disk."""
    candidate = base_path
    counter   = 1
    while candidate.with_suffix(".png").exists():
        candidate = base_path.with_name(f"{base_path.name}_{counter}")
        counter  += 1
    return candidate


# ---------------------------------------------------------------------------
# barcode generation
# ---------------------------------------------------------------------------

def generate_barcodes(values, output_dir: str = "barcodes"):
    """Generate a Code‑128 PNG for each *value* (number **or** word)."""
    out_dir = Path(output_dir)
    out_dir.mkdir(exist_ok=True)

    generated_files = []
    writer_opts = {"write_text": False}

    for idx, value in enumerate(values, start=1):
        data = str(value)
        slug = slugify(data)
        fname_root = f"{idx:0{ROW_PAD}d}_{slug}"       # e.g. 00001_HelloWorld
        target = ensure_unique_path(out_dir / fname_root)

        try:
            code = barcode.get("code128", data, writer=ImageWriter())
            saved_file = code.save(target),
            generated_files.append(saved_file)
            print(f"已生成条形码: {saved_file}")
        except IllegalCharacterError as e:
            print(f"⚠️  无法为 '{data}' 生成 CODE128 条形码: {e}. 已跳过。")

    return generated_files


# ---------------------------------------------------------------------------
# main entry point
# ---------------------------------------------------------------------------

def main():
    csv_file = input("请输入CSV文件路径(或直接回车使用默认文件): ") or "casualty_data.csv"
    values = read_data_from_csv(csv_file)

    if not values:
        print("未找到有效数据，请检查CSV文件格式。")
        return

    print(f"从CSV文件中读取到 {len(values)} 个数据点")

    output_dir = input("请输入输出目录(或直接回车使用默认目录): ") or "casualty_barcodes"
    generated_files = generate_barcodes(values, output_dir)

    print(f"\n成功生成 {len(generated_files)} 个条形码文件到 '{output_dir}' 目录")


if __name__ == "__main__":
    main()
