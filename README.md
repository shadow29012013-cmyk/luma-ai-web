# StudySync Web

Ứng dụng quản lý học tập cá nhân dành cho học sinh, sinh viên. StudySync tập trung vào lịch học, deadline, nhắc việc và tiến độ học tập.

## Tính năng

- **Dashboard:** lịch học sắp tới, deadline trong 7 ngày, tỷ lệ hoàn thành và biểu đồ tiến độ.
- **Thời khóa biểu:** thêm môn học, ngày, giờ, phòng học và giảng viên.
- **Bài tập & Deadline:** thêm bài tập theo môn, hạn nộp, mức độ `Gấp`, `Quan trọng`, `Bình thường`, đánh dấu hoàn thành.
- **Thông báo:** hiển thị nhắc lịch học theo số phút đã chọn và deadline sắp đến hạn.

## User flow

1. Mở StudySync và xem Dashboard.
2. Vào **Thời khóa biểu**, nhập lịch học thủ công.
3. Vào **Bài tập & Deadline**, gắn bài tập với môn và chọn ưu tiên.
4. Vào **Thông báo** để xem lịch học cần chuẩn bị và deadline sắp đến hạn.
5. Đánh dấu bài đã hoàn thành để cập nhật biểu đồ tiến độ.

- `web_app.py`: giao diện Streamlit.
- `bus/study_bus.py`: nghiệp vụ lịch học, bài tập và thông báo.
- `database/study_repository.py`: lưu lịch/bài tập trong `data/study_data.json`.

## UI/UX và kiến trúc

Giao diện dùng phong cách Modern Minimalist, nền sáng, điểm nhấn xanh mint/cam và sidebar điều hướng. Dashboard ưu tiên ba thông tin cần quét nhanh: lịch học sắp tới, bài sắp đến hạn và tiến độ tuần. Dữ liệu local dùng JSON để dễ học và chạy nhẹ; khi triển khai lớn có thể chuyển repository sang SQLite hoặc PostgreSQL.

## Chạy trên máy

Cần cài Python 3.10 trở lên.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run web_app.py
```

Sau đó mở địa chỉ Streamlit hiển thị, thường là `http://localhost:8501`.

Tính năng AI đang tạm tắt. Không cần API key để chạy StudySync.

## Công khai thành link web

1. Tạo repository mới trên GitHub.
2. Đưa toàn bộ project lên GitHub, nhưng bỏ qua `.env`.
3. Truy cập [share.streamlit.io](https://share.streamlit.io), đăng nhập GitHub.
4. Chọn repository, branch và file chính `web_app.py`.
5. Bấm **Deploy**. Streamlit sẽ cấp một đường link công khai cho website.

## Lưu ý dữ liệu

Bản local lưu thời khóa biểu và bài tập vào JSON. Push notification trực tiếp đến điện thoại cần bổ sung Firebase Cloud Messaging hoặc Telegram Bot với backend scheduler; trang **Thông báo** hiện là trung tâm nhắc việc trong app.
