import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10, 11))
ax.axis('off')

# Danh sách các tầng và nội dung chuẩn hóa với broker.emqx.io
layers = [
    {
        "title": "1. TẦNG THU THẬP DỮ LIỆU (Perception Layer / Edge Device)",
        "content": "• Cảm biến: DHT22 (Nhiệt độ, Độ ẩm), HC-SR04 (Khoảng cách)\n• Vi điều khiển ESP32 giả lập trên môi trường Wokwi\n• Xử lý biên: Kiểm tra tính hợp lệ isfinite(), đóng gói JSON\n• Chu kỳ gửi: 3 giây/lần kèm send_ts (millis) và seq",
        "bg": "#E3F2FD", "border": "#1976D2", "y": 0.78
    },
    {
        "title": "2. TẦNG TRUYỀN THÔNG & ĐIỀU PHỐI (Network & Broker Layer)",
        "content": "• MQTT Broker: broker.emqx.io, Port: 1883\n• Giao thức vận chuyển: TCP/IP, QoS 0\n• Định tuyến luồng: Topic 'iot/lab2/B23DCCN234/telemetry'",
        "bg": "#E8F5E9", "border": "#388E3C", "y": 0.55
    },
    {
        "title": "3. TẦNG TIỀN XỬ LÝ & LƯU TRỮ (Processing & Storage Layer)",
        "content": "• Bộ thu thập (collector.py): Đón nhận MQTT, xác thực dữ liệu, ghi sensor_raw.csv\n• Bộ tiền xử lý (preprocess.py):\n   - Điền khuyết (linear interpolate, bfill, ffill)\n   - Lọc Outlier theo ngưỡng IQR: [Q1 - 1.5*IQR, Q3 + 1.5*IQR]\n   - Làm mịn bằng Rolling Mean (w=3), tạo đặc trưng Delta\n   - Chuẩn hóa Min-Max Scaling [0, 1] và lưu sensor_clean.csv",
        "bg": "#FFF3E0", "border": "#F57C00", "y": 0.28
    },
    {
        "title": "4. TẦNG ỨNG DỤNG & GIÁM SÁT (Application & Dashboard Layer)",
        "content": "• Giám sát thời gian thực (dashboard_realtime.py): Cập nhật biểu đồ theo luồng gói tin\n• Trực quan hóa đối chứng (visualize.py): Vẽ biểu đồ Raw vs. IQR vs. Rolling Mean\n• Đánh giá hiệu năng (latency_eval.py): Phân tích Jitter, chu kỳ và dung lượng lưu trữ",
        "bg": "#F3E5F5", "border": "#7B1FA2", "y": 0.03
    }
]

box_width = 0.88
box_height = 0.16
box_x = 0.06

for item in layers:
    rect = patches.FancyBboxPatch((box_x, item["y"]), box_width, box_height,
                                  boxstyle="round,pad=0.02,rounding_size=0.02",
                                  facecolor=item["bg"], edgecolor=item["border"], linewidth=2)
    ax.add_patch(rect)
    ax.text(box_x + 0.02, item["y"] + box_height - 0.03, item["title"],
            fontsize=11, fontweight='bold', color=item["border"])
    ax.text(box_x + 0.03, item["y"] + 0.02, item["content"],
            fontsize=9.5, color='#263238', verticalalignment='bottom', linespacing=1.35)

arrow_props = dict(facecolor='#455A64', edgecolor='#455A64', width=2, headwidth=8, shrink=0.05)
arrow_labels = [
    "MQTT Publish\nTopic: iot/lab2/B23DCCN234/telemetry",
    "MQTT Subscribe\nĐón nhận gói tin JSON",
    "Đọc dữ liệu phân tích\n(sensor_raw.csv & sensor_clean.csv)"
]

arrow_y = [0.78, 0.55, 0.28]
for i in range(3):
    ax.annotate('', xy=(0.5, arrow_y[i] - 0.06), xytext=(0.5, arrow_y[i]), arrowprops=arrow_props)
    ax.text(0.53, arrow_y[i] - 0.035, arrow_labels[i], fontsize=8.5, color='#37474F', fontstyle='italic')

plt.title("KIẾN TRÚC PIPELINE THU THẬP, LƯU TRỮ VÀ TIỀN XỬ LÝ DỮ LIỆU IoT\nSinh viên: Vũ Hải Dương - MSSV: B23DCCN234",
          fontsize=12, fontweight='bold', pad=15)

plt.savefig("architecture_diagram.png", dpi=300, bbox_inches='tight')
print("Đã tạo xong file ảnh chuẩn: architecture_diagram.png")
plt.show()