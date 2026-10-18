import pandas as pd
import matplotlib.pyplot as plt

# 1. Đọc dữ liệu thô và dữ liệu sạch
raw_df = pd.read_csv("sensor_raw.csv")
clean_df = pd.read_csv("sensor_clean.csv")

# 2. Khởi tạo biểu đồ so sánh 3 thông số
fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
fig.suptitle("IoT Lab 2: So sánh dữ liệu Cảm biến Trước và Sau Tiền xử lý (B23DCCN234)", fontsize=13, fontweight='bold')

# --- Đồ thị Nhiệt độ ---
axs[0].plot(raw_df.index, raw_df['temperature'], label='Thô (Raw - có Outlier)', color='salmon', linestyle='--', marker='o', markersize=3)
axs[0].plot(clean_df.index, clean_df['temperature'], label='Đã lọc Outlier (IQR)', color='crimson', linewidth=2)
axs[0].plot(clean_df.index, clean_df['temp_rolling_avg'], label='Làm mịn (Rolling Mean)', color='darkblue', linewidth=1.5)
axs[0].set_ylabel("Nhiệt độ (°C)")
axs[0].legend(loc="upper right")
axs[0].grid(True, linestyle=":", alpha=0.6)

# --- Đồ thị Độ ẩm ---
axs[1].plot(raw_df.index, raw_df['humidity'], label='Thô (Raw)', color='lightblue', linestyle='--', marker='s', markersize=3)
axs[1].plot(clean_df.index, clean_df['humidity'], label='Đã xử lý (Clean)', color='teal', linewidth=2)
axs[1].set_ylabel("Độ ẩm (%RH)")
axs[1].legend(loc="upper right")
axs[1].grid(True, linestyle=":", alpha=0.6)

# --- Đồ thị Khoảng cách ---
axs[2].plot(raw_df.index, raw_df['distance_cm'], label='Thô (Raw)', color='khaki', linestyle='--', marker='^', markersize=3)
axs[2].plot(clean_df.index, clean_df['distance_cm'], label='Đã xử lý (Clean)', color='forestgreen', linewidth=2)
axs[2].set_ylabel("Khoảng cách (cm)")
axs[2].set_xlabel("Số thứ tự mẫu dữ liệu (Sample Index)")
axs[2].legend(loc="upper right")
axs[2].grid(True, linestyle=":", alpha=0.6)

plt.tight_layout()
plt.savefig("pipeline_comparison.png", dpi=300)
print("Đã lưu biểu đồ vào file 'pipeline_comparison.png'!")
plt.show()