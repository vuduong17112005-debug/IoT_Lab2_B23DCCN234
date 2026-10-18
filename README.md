# BÀI THỰC HÀNH SỐ 2: THU THẬP, LƯU TRỮ VÀ TIỀN XỬ LÝ DỮ LIỆU IoT
- Sinh viên thực hiện: Vũ Hải Dương
- Mã sinh viên: B23DCCN234
- Lớp môn học: IoT và Ứng dụng (INT14149)

## 1. Kiến trúc hệ thống
- ESP32 (Wokwi mô phỏng) -> MQTT Broker (broker.hivemq.com:1883) -> Python Subscriber (collector.py) -> Lưu trữ chuỗi thời gian CSV -> Tiền xử lý (preprocess.py) -> Trực quan hóa & Giám sát (visualize.py, dashboard_realtime.py).

## 2. Hướng dẫn cài đặt và chạy ứng dụng
1. Cài đặt thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt