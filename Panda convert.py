import pandas as pd
from pandas.api.types import is_numeric_dtype
import os, sys

def encode_mixed_csv(input_csv: str, output_csv: str):
    try:
        # 1. Read the CSV
        df = pd.read_csv(input_csv)
    except Exception as e:
        print(f"❌ Failed to read {input_csv!r}: {e}")
        sys.exit(1)

    # 2. Prepare a new DataFrame to collect everything
    df_out = pd.DataFrame(index=df.index)

    # 3. Loop through columns
    for col in df.columns:
        if is_numeric_dtype(df[col]):
            # Numeric: copy (or normalize if you like)
            df_out[col] = df[col]
        else:
            # Text: convert to categorical codes (0,1,2,…)
            df_out[col] = df[col].astype('category').cat.codes

    # (Optional) Normalize all columns into [0,1]
    # df_out = (df_out - df_out.min()) / (df_out.max() - df_out.min())

    # 4. Save
    try:
        df_out.to_csv(output_csv, index=False)
        print(f"✅ Written numeric CSV to {output_csv!r}")
    except Exception as e:
        print(f"❌ Failed to write {output_csv!r}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 1) ensure you passed both paths, or
    # 2) hard-code them here:
    input_csv  = '/Users/haoyangwang/Desktop/Barcode creation/test 2.csv'
    output_csv = '/Users/haoyangwang/Desktop/Barcode creation/test 2 (encoded).csv'

    # Make sure output folder exists
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    encode_mixed_csv(input_csv, output_csv)
