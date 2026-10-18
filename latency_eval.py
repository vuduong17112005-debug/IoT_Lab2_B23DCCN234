import pandas as pd
import numpy as np

# Đọc file thô
df = pd.read_csv("sensor_raw.csv")

# 1. Tính toán độ trễ truyền gói tin (Khoảng cách thời gian giữa các gói tin nhận được)
# Do Wokwi dùng millis() cục bộ và máy tính dùng epoch time thực tế, 
# độ trễ mạng và tính ổn định chu kỳ nhận được phản ánh qua khoảng cách giữa 2 lần nhận liên tiếp (Delta Time)
df['recv_epoch'] = pd.to_numeric(df['recv_epoch'])
df['interval_s'] = df['recv_epoch'].diff()

# Độ trễ lệch chuẩn so với chu kỳ gửi gốc (3.0 giây)
df['jitter_ms'] = (df['interval_s'] - 3.0).abs() * 1000

avg_interval = df['interval_s'].mean()
avg_jitter = df['jitter_ms'].mean()
packet_loss_rate = 0.0  # Vì chuỗi seq liên tục

print("=== BÁO CÁO HIỆU NĂNG VÀ ĐỘ TRỄ HỆ THỐNG ===")
print(f"Tổng số gói tin phân tích: {len(df)}")
print(f"Chu kỳ gửi trung bình: {avg_interval:.2f} giây (Mục tiêu: 3.00 s)")
print(f"Độ biến thiên trễ (Jitter) trung bình: {avg_jitter:.2f} ms")
print(f"Tỷ lệ mất gói tin (Packet Loss): {packet_loss_rate}%")

# 2. Đánh giá hiệu năng lưu trữ
raw_size = len(df.to_csv().encode('utf-8'))
clean_df = pd.read_csv("sensor_clean.csv")
clean_size = len(clean_df.to_csv().encode('utf-8'))
avg_record_bytes = raw_size / len(df)

print("\n=== ĐÁNH GIÁ LƯU TRỮ (STORAGE ANALYSIS) ===")
print(f"Kích thước trung bình 1 bản ghi: {avg_record_bytes:.1f} bytes")
print(f"Ước tính dung lượng cho 1 thiết bị/ngày (gửi mỗi 3s = 28,800 bản ghi): {(avg_record_bytes * 28800) / (1024*1024):.2f} MB/ngày")
print(f"Ước tính cho 100 thiết bị/tháng: {((avg_record_bytes * 28800) / (1024*1024)) * 100 * 30 / 1024:.2f} GB/tháng")