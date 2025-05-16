import pandas as pd
import numpy as np
import imageio
import os

# --- USER CONFIGURABLE PARAMETERS ---
csv_path = '/test 2.csv'  # Path to your CSV file
output_video = '/mnt/data/barcode_video_16bit.mp4'
stripe_width = 4                         # Width of each bit stripe in pixels
frame_height = 100                       # Height of each barcode frame in pixels
bit_width = 16                           # Use 16 bits per value


# Read the CSV
df = pd.read_csv(csv_path)

# Function to convert integer to fixed-width binary
def to_binary(val, width):
    try:
        num = int(val)
    except ValueError:
        # For non-integers, convert to int first or handle differently
        num = int(float(val))
    return format(num, f'0{width}b')

# Convert dataframe values to binary strings
binary_matrix = df.applymap(lambda x: to_binary(x, bit_width)).values
rows, cols = binary_matrix.shape

# Generate frames
frames = []
for r in range(rows):
    # Concatenate all binary strings in the row
    bits = ''.join(binary_matrix[r])
    bit_count = len(bits)
    # Build stripe image: 1->255, 0->0
    arr = np.array([[int(bits[i])] * stripe_width for i in range(bit_count)]).T
    img = np.uint8(arr * 255)
    # Scale to desired frame height
    repeat_factor = frame_height // img.shape[0] + 1
    img_scaled = np.repeat(img, repeat_factor, axis=0)[:frame_height]
    frames.append(img_scaled)

# Write to video
with imageio.get_writer(output_video, fps=1) as writer:
    for frame in frames:
        writer.append_data(frame)

print(f"Generated 16-bit barcode video at: {output_video}")
