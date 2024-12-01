# Code test 12th Nov 2024 Remove CRF The crf value (constant rate factor), ExampeCRF= 28,
#  which is controlling the quality of the compression independently of the bitrate setting
#plot Fig03 slide Mo phong voi PYTHON
import cv2
import ffmpeg
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr

# Function to calculate PSNR between original and compressed frames
def calculate_frame_psnr(original_video, compressed_video):
    cap_orig = cv2.VideoCapture(original_video)
    cap_comp = cv2.VideoCapture(compressed_video)
    
    psnr_values = []
    
    while True:
        ret_orig, frame_orig = cap_orig.read()
        ret_comp, frame_comp = cap_comp.read()
        
        if not ret_orig or not ret_comp:
            break
        
        # Convert frames to float32 and normalize to [0, 255]
        frame_orig = frame_orig.astype(np.float32)
        frame_comp = frame_comp.astype(np.float32)
        
        # Ensure pixel values are in the range [0, 255]
        frame_orig = np.clip(frame_orig, 0, 255)
        frame_comp = np.clip(frame_comp, 0, 255)
        
        # Calculate PSNR with data_range=255 for 8-bit images
        psnr_value = psnr(frame_orig, frame_comp, data_range=255)
        psnr_values.append(psnr_value)
        
    cap_orig.release()
    cap_comp.release()
    
    return np.mean(psnr_values)  # Return the average PSNR value

# Function to compress video using H.264 and H.265 codecs
def compress_video(input_video, codec, output_video, bitrate):
    codec_map = {'H.264': 'libx264', 'H.265': 'libx265'}
    if codec not in codec_map:
        print(f"Invalid codec {codec}!")
        return None
    
    codec_option = codec_map[codec]
    
    # Compress the video with the specified codec, bitrate, and additional bitrate control options
    ffmpeg.input(input_video).output(output_video, vcodec=codec_option, bitrate=bitrate, maxrate=bitrate, bufsize='2M').run(overwrite_output=True)

# Bitrates to use for compression
bitrates = ['500k', '2M', '4M', '6M', '8M', '10M']

# Input video path
input_video = "videotest.mp4"
#input_video02 = "videotest.mp4"

# Store PSNR values for each codec at different bitrates
psnr_h264 = []
psnr_h265 = []

# Compress the video for each bitrate and calculate PSNR
for bitrate in bitrates:
    # Output video paths
    compressed_h264 = f"compressed_h264_{bitrate}.mp4"
    compressed_h265 = f"compressed_h265_{bitrate}.mp4"
    
    # Compress videos
    compress_video(input_video, 'H.264', compressed_h264, bitrate)
    compress_video(input_video, 'H.265', compressed_h265, bitrate)
    
    # Calculate PSNR for each compression
    psnr_h264.append(calculate_frame_psnr(input_video, compressed_h264))
    psnr_h265.append(calculate_frame_psnr(input_video, compressed_h265))

# Plot PSNR vs Bitrate for H.264 and H.265
plt.figure(figsize=(10, 6))

# Plot H.264
plt.plot(bitrates, psnr_h264, 'bo-', label="H.264", alpha=0.7)
# Plot H.265
plt.plot(bitrates, psnr_h265, 'ro-', label="H.265", alpha=0.7)

plt.title("PSNR vs Bitrate for H.264 and H.265")
plt.xlabel("Bitrate (Mbps)")
plt.ylabel("PSNR (dB)")
plt.legend()
plt.grid(True)
plt.show()
