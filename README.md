# IOTApp

Trước hết cài đặt cassandra:
Tạo keyspace httt;
dùng lệnh use httt để sử dụng keyspace đó

file IOTlab.py để tạo dữ liệu giả đẩy lên adafruit
chạy lệnh python3 IOTlab.py

file client.py để kéo dữ liệu từ adafruit xuống, lưu dữ liệu vào database
chạy lệnh python3 client.py

file app.py để tạo các api,
chạy lệnh python3 app.py 


ngoài ra file getData.py để minh hoạ lấy một data từ api xuống

và file x.py để ví dụ post một dữ liệu lên
