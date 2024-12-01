# Code test 11th Nov 2024 MONDAY
#plot Fig.1 slide Mo phong voi PYTHON
import cv2
import ffmpeg
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr

# Function to calculate PSNR between the original and compressed videos
def calculate_psnr(original_video, compressed_video):
    cap_orig = cv2.VideoCapture(original_video)
    cap_comp = cv2.VideoCapture(compressed_video)
    
    psnr_values = []
    frame_count = 0
    
    while True:
        ret_orig, frame_orig = cap_orig.read()
        ret_comp, frame_comp = cap_comp.read()
        
        if not ret_orig or not ret_comp:
            break
            
        psnr_value = psnr(frame_orig, frame_comp)
        psnr_values.append(psnr_value)
        frame_count += 1
        
    cap_orig.release()
    cap_comp.release()
    
    avg_psnr = np.mean(psnr_values)
    return avg_psnr, psnr_values

# Function to compress video using H.264 and H.265 codecs
def compress_video(input_video, codec, output_video):
    codec_map = {'H.264': 'libx264', 'H.265': 'libx265'}
    if codec not in codec_map:
        print(f"Codec {codec} không hợp lệ!")
        return None
    
    codec_option = codec_map[codec]
    
    # Specify the path to ffmpeg if it's not in PATH
    ffmpeg.input(input_video).output(output_video, vcodec=codec_option, crf=23).run(cmd='C:/ffmpeg/bin/ffmpeg.exe')

# Function to calculate bitrate
def calculate_bitrate(compressed_video):
    cap = cv2.VideoCapture(compressed_video)
    total_bits = 0
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        total_bits += frame.nbytes * 8  # Calculate the number of bits for each frame
        frame_count += 1
    
    cap.release()
    
    # Calculate bitrate (bits per second)
    total_time = frame_count / 30  # Assume 30 fps
    bitrate = total_bits / total_time
    return bitrate

# Input video path
input_video = "videotest.mp4"

# Output paths for compressed videos
compressed_h264 = "compressed_h264.mp4"
compressed_h265 = "compressed_h265.mp4"

# Compress video using H.264 and H.265
compress_video(input_video, 'H.264', compressed_h264)
compress_video(input_video, 'H.265', compressed_h265)

# Calculate PSNR for compressed videos
psnr_h264, psnr_values_h264 = calculate_psnr(input_video, compressed_h264)
psnr_h265, psnr_values_h265 = calculate_psnr(input_video, compressed_h265)

# Calculate bitrate for compressed videos
bitrate_h264 = calculate_bitrate(compressed_h264)
bitrate_h265 = calculate_bitrate(compressed_h265)

# Verify bitrate calculations
print(f"PSNR H.264: {psnr_h264:.2f} dB @", f"Bitrate H.264: {bitrate_h264 / 1e6:.2f} Mbps")
print(f"PSNR H.265: {psnr_h265:.2f} dB @", f"Bitrate H.265: {bitrate_h265 / 1e6:.2f} Mbps" )
#print(f"Bitrate H.264: {bitrate_h264 / 1e6:.2f} Mbps")
#print(f"Bitrate H.265: {bitrate_h265 / 1e6:.2f} Mbps")

# Define bitrate values after successful calculation
bitrate_values = [bitrate_h264, bitrate_h265]

# Plot PSNR comparison
plt.figure(figsize=(8, 6))

# PSNR Plot
plt.subplot(2, 1, 1)
plt.plot(psnr_values_h264, label="H.264", color='b')
plt.plot(psnr_values_h265, label="H.265", color='r')
plt.title("So sánh PSNR giữa H.264 và H.265")
plt.xlabel("Frame")
plt.ylabel("PSNR (dB)")
plt.legend()

# Bitrate Plot with annotations
plt.subplot(2, 1, 2)
plt.bar(['H.264', 'H.265'], bitrate_values, color=['blue', 'red'])
plt.title("So sánh Bitrate giữa H.264 và H.265")
plt.ylabel("Bitrate (Mbps)")
plt.ylim(0, max(bitrate_values) * 1.1)  # Limit y-axis for easier comparison
plt.text(0, bitrate_h264, f"{bitrate_h264 / 1e6:.2f} Mbps\nPSNR: {psnr_h264:.2f} dB", ha='center', color='blue')
plt.text(1, bitrate_h265, f"{bitrate_h265 / 1e6:.2f} Mbps\nPSNR: {psnr_h265:.2f} dB", ha='center', color='red')

# Show the plot
plt.tight_layout()
plt.show()
