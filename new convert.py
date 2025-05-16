
import os
import pandas as pd
import hashlib
from pandas.api.types import is_numeric_dtype

def hash_code(s: str, buckets: int = 32) -> int:
    return int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16) % buckets

def encode_column(series: pd.Series,
                  method: str = 'category',
                  hash_buckets: int = 32) -> pd.Series:
    s = series.fillna('<NA>').astype(str)
    if method == 'category':
        cat = s.astype('category')
        return cat.cat.codes
    elif method == 'hash':
        return s.map(lambda x: hash_code(x, buckets=hash_buckets))
    else:
        raise ValueError(f"Unknown method {method!r}")

def encode_mixed_csv(input_csv: str,
                     output_csv: str,
                     method: str = 'category',
                     hash_buckets: int = 32):
    df = pd.read_csv(input_csv)
    df_out = pd.DataFrame(index=df.index)
    for col in df.columns:
        if is_numeric_dtype(df[col]):
            df_out[col] = df[col]
        else:
            df_out[col] = encode_column(df[col], method, hash_buckets)
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_out.to_csv(output_csv, index=False)
    print(f"✅ Written encoded CSV to: {output_csv}")

# --- below is your “main” section, you can run this in any Python context:

if __name__ == '__main__':
    # 1) specify your paths here:
    input_csv  = '/Users/haoyangwang/Desktop/Barcode creation/test 2.csv'
    output_csv = '/Users/haoyangwang/Desktop/Barcode creation/test 2 (renewed).csv'

    # 2) choose method: 'category' or 'hash'
    method = 'category'
    hash_buckets = 64  # only used if method=='hash'

    # 3) run the encoding
    encode_mixed_csv(input_csv, output_csv, method, hash_buckets)
