import csv
import json
import os
import time
import paho.mqtt.client as mqtt

# Cấu hình MQTT Broker
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/lab2/B23DCCN234/telemetry"

CSV_FILE = "sensor_raw.csv"

# Khởi tạo file CSV với tiêu đề nếu chưa tồn tại
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",       # Thời gian lúc server nhận gói tin (ISO 8601)
            "recv_epoch",      # Epoch time (giây)
            "device_id",       # Mã thiết bị
            "seq",             # Thứ tự gói tin
            "temperature",     # Nhiệt độ (°C)
            "humidity",        # Độ ẩm (%RH)
            "distance_cm",     # Khoảng cách (cm)
            "rssi",            # Cường độ sóng Wi-Fi (dBm)
            "send_ts",         # Thời gian gửi từ ESP32 (ms)
            "is_valid"         # Cờ đánh giá dữ liệu hợp lệ (True/False)
        ])

def validate_data(temp, hum, dist):
    # Kiểm tra giá trị lỗi (-999) hoặc nằm ngoài dải cảm biến vật lý
    if temp == -999.0 or hum == -999.0 or dist == -999.0:
        return False
    if not (-40 <= temp <= 80):
        return False
    if not (0 <= hum <= 100):
        return False
    if not (2 <= dist <= 400):
        return False
    return True

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[SUCCESS] Đã kết nối MQTT Broker! Đang lắng nghe topic: {MQTT_TOPIC}")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"[FAILED] Kết nối thất bại, mã lỗi rc = {rc}")

def on_message(client, userdata, msg):
    try:
        now_epoch = time.time()
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_epoch))
        payload_str = msg.payload.decode("utf-8")
        data = json.loads(payload_str)

        device_id = data.get("device_id", "Unknown")
        seq = data.get("seq", 0)
        temp = float(data.get("temperature", -999))
        hum = float(data.get("humidity", -999))
        dist = float(data.get("distance_cm", -999))
        rssi = int(data.get("rssi", 0))
        send_ts = int(data.get("send_ts", 0))

        valid = validate_data(temp, hum, dist)

        # Ghi bản ghi vào file CSV
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                time_str, round(now_epoch, 2), device_id, seq,
                temp, hum, dist, rssi, send_ts, valid
            ])

        print(f"[{time_str}] Seq={seq} | T={temp}°C | H={hum}% | D={dist}cm | Valid={valid}")

    except Exception as e:
        print(f"[ERROR] Lỗi phân tích gói tin: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Đang kết nối đến broker.hivemq.com...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
