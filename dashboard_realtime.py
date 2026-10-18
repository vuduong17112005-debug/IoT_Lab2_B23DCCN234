import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 7))
fig.suptitle("HỆ THỐNG GIÁM SÁT REAL-TIME IoT (B23DCCN234)", fontsize=13, fontweight='bold')

def update(frame):
    if not os.path.exists("sensor_raw.csv"):
        return
    try:
        df = pd.read_csv("sensor_raw.csv")
        if len(df) < 2:
            return
        
        # Lấy tối đa 20 điểm dữ liệu mới nhất để vẽ đồ thị cuộn
        df_tail = df.tail(20)
        
        ax1.clear(); ax2.clear(); ax3.clear()
        
        latest = df.iloc[-1]
        
        # Nhiệt độ
        ax1.plot(df_tail['seq'], df_tail['temperature'], 'r-o', label=f"Nhiệt độ hiện tại: {latest['temperature']} °C")
        ax1.set_ylabel("Nhiệt độ (°C)")
        ax1.legend(loc="upper left")
        ax1.grid(True, linestyle=":", alpha=0.6)
        
        # Độ ẩm
        ax2.plot(df_tail['seq'], df_tail['humidity'], 'b-s', label=f"Độ ẩm hiện tại: {latest['humidity']} %RH")
        ax2.set_ylabel("Độ ẩm (%RH)")
        ax2.legend(loc="upper left")
        ax2.grid(True, linestyle=":", alpha=0.6)
        
        # Khoảng cách
        ax3.plot(df_tail['seq'], df_tail['distance_cm'], 'g-^', label=f"Khoảng cách hiện tại: {latest['distance_cm']} cm")
        ax3.set_ylabel("Khoảng cách (cm)")
        ax3.set_xlabel("Số thứ tự gói tin (Sequence)")
        ax3.legend(loc="upper left")
        ax3.grid(True, linestyle=":", alpha=0.6)
        
    except Exception:
        pass

ani = FuncAnimation(fig, update, interval=1500)
plt.tight_layout()
plt.show()