
#!/usr/bin/env python3
import os
import sys
import time
import argparse
import cups


def batch_print_with_cups(directory, printer_name, batch_size=5, pause_secs=60,
                          media='Custom.057x0.0mm', fit_to_page=True):
    """
    Print files in batches using the CUPS Python API instead of shell commands.
    - directory: folder with files to print
    - printer_name: CUPS destination name
    - batch_size: number of jobs per cycle
    - pause_secs: seconds to wait between batches
    - media: CUPS media option (e.g. 'Custom.057x0.0mm')
    - fit_to_page: if True, adds 'fit-to-page' option
    """
    # Establish CUPS connection
    conn = cups.Connection()
    # Verify printer exists
    printers = conn.getPrinters()
    if printer_name not in printers:
        print(f"Error: printer '{printer_name}' not found in CUPS.")
        sys.exit(1)

    # Gather files
    files = sorted(
        os.path.join(directory, fn)
        for fn in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, fn))
    )
    total = len(files)
    print(f"Found {total} files. Sending in batches of {batch_size} to '{printer_name}'")

    job_options = {'media': media}
    if fit_to_page:
        job_options['fit-to-page'] = ''

    # Batch print loop
    for i in range(0, total, batch_size):
        batch = files[i:i+batch_size]
        print(f"\n▶ Batch #{i//batch_size + 1}:")
        for filepath in batch:
            print(f"  • Printing: {os.path.basename(filepath)}")
            try:
                conn.printFile(printer_name, filepath,
                               os.path.basename(filepath), job_options)
            except cups.IPPError as e:
                print(f"    ⚠️ IPPError printing {filepath}: {e}")
        if i + batch_size < total:
            print(f"Batch sent. Pausing for {pause_secs} seconds…")
            time.sleep(pause_secs)

    print("\n✅ All jobs submitted.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Batch-print files via CUPS Python API"
    )
    parser.add_argument('directory',
                        nargs='?',
                        default='/Users/haoyangwang/Desktop/Barcode creation/number combat report',
                        help="Directory with files to print (default: %(default)s)")
    parser.add_argument('-p', '--printer',
                        default='ZONERICH_58mm',
                        help="CUPS printer name (default: %(default)s)")
    parser.add_argument('-b', '--batch-size',
                        type=int, default=5,
                        help="Number of jobs per batch")
    parser.add_argument('-w', '--wait',
                        type=int, default=60,
                        help="Seconds to wait between batches")
    parser.add_argument('-m', '--media',
                        default='A4',
                        help="CUPS media option %(default)s")
    parser.add_argument('--no-fit',
                         action = 'store_false', dest = 'fit_to_page',
                         help = "Disable fit-to-page scaling")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory.")
        sys.exit(1)

    batch_print_with_cups(
        args.directory,
        args.printer,
        args.batch_size,
        args.wait,
        args.media,
        args.fit_to_page
    )
