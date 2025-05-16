#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import argparse

media_opt   = 'media=Custom.057x0.0mm'  # 57 mm roll, unlimited length
scale_opt   = 'fit-to-page'            # auto-scale to fill width

def batch_print(directory, printer, batch_size=5, pause_secs=30):
    # Gather and sort all files in the directory
    files = sorted(
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    )
    total = len(files)
    print(f"Found {total} files in {directory}. Sending in batches of {batch_size}…")

    for i in range(0, total, batch_size):
        batch = files[i:i+batch_size]
        print(f"\n▶ Batch #{i//batch_size + 1}:")
        for filepath in batch:
            print(f"  • Printing: {os.path.basename(filepath)}")
            try:
                subprocess.run(['lp', '-d', printer, filepath],
                               check=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                print(f"    ⚠️ Error printing {filepath}: {e.stderr.decode().strip()}")
        if i + batch_size < total:
            print(f"Batch sent. Pausing for {pause_secs} seconds…")
            time.sleep(pause_secs)

    print("\n✅ All jobs sent.")

if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description="Print files in batches with pauses between batches."
    )
    p.add_argument('directory',
                   nargs='?',
                   default='/Users/haoyangwang/Desktop/Barcode creation/number combat report',
                   help="Directory containing files to print (default: %(default)s)")

    p.add_argument('-p', '--printer',
                   default='ZONERICH_58mm_2',
                   help="CUPS printer name (run `lpstat -p` to list)")
    p.add_argument('-b', '--batch-size',
                   type=int,
                   default=5,
                   help="Number of jobs per batch")
    p.add_argument('-w', '--wait',
                   type=int,
                   default=30,
                   help="Seconds to wait between batches")
    args = p.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory.")
        sys.exit(1)

    batch_print(args.directory, args.printer, args.batch_size, args.wait)
