# Code test 10th Nov 2024 SUNDAY
#plot Fig02 slide Mo phong voi PYTHON
import cv2
import ffmpeg
import numpy as np
import os
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr

# Hàm tính PSNR giữa video gốc và video đã nén
def calculate_psnr(original_frame, compressed_frame):
    return psnr(original_frame, compressed_frame)

# Hàm nén video bằng H.264 và H.265
def compress_video(input_video, codec, output_video):
    codec_map = {'H.264': 'libx264', 'H.265': 'libx265'}
    if codec not in codec_map:
        print(f"Codec {codec} không hợp lệ!")
        return None
    
    codec_option = codec_map[codec]
    
    # Force overwrite by adding the '-y' flag
    ffmpeg.input(input_video).output(output_video, vcodec=codec_option, crf=23).run(cmd='C:/ffmpeg/bin/ffmpeg.exe -y')  # This forces overwrite

# Hàm tính bitrate
def calculate_bitrate(compressed_video):
    cap = cv2.VideoCapture(compressed_video)
    total_bits = 0
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        total_bits += frame.nbytes * 8  # Tính số bit của mỗi frame
        frame_count += 1
    
    cap.release()
    
    # Tính bitrate (bit/giây)
    total_time = frame_count / 30  # Giả sử 30 fps
    bitrate = total_bits / total_time
    return bitrate

# Đường dẫn video đầu vào
input_video = "videotest.mp4"

# Đường dẫn video nén
compressed_h264 = "compressed_h264.mp4"
compressed_h265 = "compressed_h265.mp4"

# Kiểm tra nếu video đã tồn tại, bỏ qua nén nếu có
if os.path.exists(compressed_h264):
    print(f"File {compressed_h264} đã tồn tại, bỏ qua nén H.264.")
else:
    compress_video(input_video, 'H.264', compressed_h264)

if os.path.exists(compressed_h265):
    print(f"File {compressed_h265} đã tồn tại, bỏ qua nén H.265.")
else:
    compress_video(input_video, 'H.265', compressed_h265)

# Hàm lấy frame từ video
def get_frame_from_video(video_path, frame_index=10):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Chuyển đổi sang RGB để hiển thị đúng
    else:
        return None

# Đọc video gốc và nén
def calculate_video_psnr_and_bitrate(input_video, compressed_video):
    cap_input = cv2.VideoCapture(input_video)
    cap_compressed = cv2.VideoCapture(compressed_video)

    psnr_values = []
    bitrate_values = []
    
    # Lặp qua từng frame của video
    while True:
        ret_input, frame_input = cap_input.read()
        ret_compressed, frame_compressed = cap_compressed.read()
        
        if not ret_input or not ret_compressed:
            break
        
        # Tính PSNR cho từng frame
        psnr_value = calculate_psnr(frame_input, frame_compressed)
        psnr_values.append(psnr_value)
    
    # Tính bitrate cho video nén
    bitrate = calculate_bitrate(compressed_video)
    
    cap_input.release()
    cap_compressed.release()
    
    return psnr_values, bitrate

# Tính PSNR và bitrate cho H.264 và H.265
psnr_h264, bitrate_h264 = calculate_video_psnr_and_bitrate(input_video, compressed_h264)
psnr_h265, bitrate_h265 = calculate_video_psnr_and_bitrate(input_video, compressed_h265)

# Figure 1: Plot PSNR vs Bitrate

# Figure 2: Show video frames with annotations
frame_h264 = get_frame_from_video(compressed_h264, frame_index=10)
frame_h265 = get_frame_from_video(compressed_h265, frame_index=10)

plt.figure(figsize=(12, 6))

# H.264 Frame with PSNR and Bitrate annotations
plt.subplot(1, 2, 1)
plt.imshow(frame_h264)
plt.title(f"H.264 Frame\nPSNR: {np.mean(psnr_h264):.2f} dB\nBitrate: {bitrate_h264 / 1e6:.2f} Mbps")
plt.axis("off")

# H.265 Frame with PSNR and Bitrate annotations
plt.subplot(1, 2, 2)
plt.imshow(frame_h265)
plt.title(f"H.265 Frame\nPSNR: {np.mean(psnr_h265):.2f} dB\nBitrate: {bitrate_h265 / 1e6:.2f} Mbps")
plt.axis("off")

# Hiển thị đồ thị
plt.tight_layout()
plt.show()
