import pandas as pd
import barcode
from barcode.writer import ImageWriter
import os
import csv
import re
options = {
    'module_width': 0.2,    # 单条宽度
    'module_height': 15.0,  # 条形码高度
    'font_size': 10,        # 底部文字大小
    'text_distance': 5.0,   # 文字与条形码距离
    'background': 'white',  # 背景色
    'foreground': 'black',  # 前景色
    'write_text': False      # 是否显示数字文本
}

def read_data_from_csv(csv_file: str):
    """从CSV文件中读取伤亡数字数据"""
    cells = []
    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            for cell in row:
                cell = cell.strip()
                if cell:
                    cells.append(cell)
    return cells


# 2. 生成条形码
def generate_barcodes(values, output_dir='barcodes'):
    """为每个数字生成条形码图片"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generated_files = []

    for value in values:
        # 将数字转换为字符串
        data = str(value)  # 确保是整数

        # 选择条形码类型(CODE128是最通用的)
        code = barcode.get('code128', data, writer=ImageWriter())

        # 保存条形码图片
        filename = os.path.join(output_dir, f"casualty_{data}")
        saved_file = code.save(filename)
        generated_files.append(saved_file)

        print(f"已生成条形码: {saved_file}")

    return generated_files

# 3. 主程序
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
