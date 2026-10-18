from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import pandas as pd
import os

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>IoT Real-Time Dashboard</title>
    <meta http-equiv="refresh" content="2">
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; text-align: center; margin: 20px; }
        .card-container { display: flex; justify-content: center; gap: 20px; margin-top: 30px; }
        .card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 220px; }
        .temp { border-top: 5px solid #e74c3c; }
        .hum { border-top: 5px solid #3498db; }
        .dist { border-top: 5px solid #2ecc71; }
        .val { font-size: 32px; font-weight: bold; margin: 15px 0; color: #2c3e50; }
        .title { font-size: 14px; color: #7f8c8d; text-transform: uppercase; }
    </style>
</head>
<body>
    <h2>HỆ THỐNG GIÁM SÁT CẢM BIẾN IoT REAL-TIME</h2>
    <p>Sinh viên: Vũ Hải Dương - MSSV: B23DCCN234</p>
    <div class="card-container">
        <div class="card temp"><div class="title">Nhiệt độ</div><div class="val">{{TEMP}} °C</div></div>
        <div class="card hum"><div class="title">Độ ẩm</div><div class="val">{{HUM}} %RH</div></div>
        <div class="card dist"><div class="title">Khoảng cách</div><div class="val">{{DIST}} cm</div></div>
    </div>
    <p style="margin-top: 30px; color: #888;">Cập nhật tự động mỗi 2 giây | Dữ liệu từ file sensor_raw.csv</p>
</body>
</html>
"""

class SimpleDashboard(BaseHTTPRequestHandler):
    def do_GET(self):
        temp, hum, dist = "--", "--", "--"
        if os.path.exists("sensor_raw.csv"):
            try:
                df = pd.read_csv("sensor_raw.csv")
                if not df.empty:
                    last = df.iloc[-1]
                    temp = f"{last['temperature']:.1f}"
                    hum = f"{last['humidity']:.1f}"
                    dist = f"{last['distance_cm']:.1f}"
            except Exception:
                pass

        page = HTML_TEMPLATE.replace("{{TEMP}}", str(temp)) \
                            .replace("{{HUM}}", str(hum)) \
                            .replace("{{DIST}}", str(dist))

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page.encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), SimpleDashboard)
    print("Dashboard Web đang chạy tại: http://localhost:8080")
    server.serve_forever()