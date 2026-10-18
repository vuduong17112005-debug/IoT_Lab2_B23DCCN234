import pandas as pd
import numpy as np

# 1. Đọc dữ liệu thô từ file CSV
raw_file = "sensor_raw.csv"
clean_file = "sensor_clean.csv"

df = pd.read_csv(raw_file)
print(f"Tổng số bản ghi ban đầu: {len(df)}")

# 2. Xử lý thiếu (Missing Values)
# Thay các giá trị đánh dấu lỗi (-999) thành NaN và nội suy
df.replace(-999.0, np.nan, inplace=True)
numeric_cols = ['temperature', 'humidity', 'distance_cm']
df[numeric_cols] = df[numeric_cols].interpolate(method='linear').bfill().ffill()

# 3. Phát hiện và xử lý Outlier bằng phương pháp IQR (Interquartile Range)
outlier_report = {}
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Tìm các điểm ngoại lai
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    outlier_report[col] = len(outliers)
    
    # Thay thế outlier bằng giá trị cận biên hoặc nội suy
    df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
    df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])

print("Số lượng điểm Outlier phát hiện được:", outlier_report)

# 4. Feature Engineering: Tính giá trị trung bình trượt (Rolling Mean) và biến thiên (Delta)
df['temp_rolling_avg'] = df['temperature'].rolling(window=3, min_periods=1).mean()
df['temp_delta'] = df['temperature'].diff().fillna(0)

# 5. Chuẩn hóa dữ liệu theo phương pháp Min-Max Scaling (đưa về đoạn [0, 1])
for col in numeric_cols:
    min_val = df[col].min()
    max_val = df[col].max()
    if max_val != min_val:
        df[f"{col}_normalized"] = (df[col] - min_val) / (max_val - min_val)
    else:
        df[f"{col}_normalized"] = 0.0

# 6. Lưu dữ liệu đã làm sạch sang file mới
df.to_csv(clean_file, index=False)
print(f"Đã tiền xử lý thành công và lưu kết quả vào: {clean_file}")
print("\n5 dòng dữ liệu sau xử lý:")
print(df[['timestamp', 'temperature', 'temp_rolling_avg', 'temp_delta']].head())