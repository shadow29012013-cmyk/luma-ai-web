# StudySync Web

Ứng dụng quản lý học tập cá nhân dành cho học sinh, sinh viên. StudySync tập trung vào lịch học, deadline, nhắc việc và tiến độ học tập.

## Tính năng

- **Dashboard:** lịch học sắp tới, deadline trong 7 ngày, tỷ lệ hoàn thành và biểu đồ tiến độ.
- **Thời khóa biểu:** thêm môn học, ngày, giờ, phòng học và giảng viên.
- **Bài tập & Deadline:** thêm bài tập theo môn, hạn nộp, mức độ `Gấp`, `Quan trọng`, `Bình thường`, đánh dấu hoàn thành.
- **Nhắc việc thông minh:** Dashboard cảnh báo các bài chưa hoàn thành trong 7 ngày tới. Đây là lớp nhắc việc hiện tại; push notification trình duyệt có thể bổ sung khi chuyển sang backend có scheduler.
- **Chat với AI:** hỏi cách học, lập kế hoạch hoặc chia nhỏ bài tập.

## User flow

1. Mở StudySync và xem Dashboard.
2. Vào **Thời khóa biểu**, nhập lịch học thủ công.
3. Vào **Bài tập & Deadline**, gắn bài tập với môn và chọn ưu tiên.
4. Mỗi lần mở Dashboard, xem cảnh báo deadline trong 7 ngày.
5. Đánh dấu bài đã hoàn thành để cập nhật biểu đồ tiến độ.

- `web_app.py`: giao diện Streamlit.
- `bus/study_bus.py`, `bus/chat_bus.py`: nghiệp vụ lịch học, bài tập và AI.
- `database/study_repository.py`: lưu lịch/bài tập trong `data/study_data.json`.
- `database/chat_repository.py`: lưu hội thoại trong `data/messages.json`.
- `model/ai_model.py`: kết nối API tương thích OpenAI.

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

Chưa có API key vẫn chạy được ở chế độ mô phỏng. Muốn dùng AI thật, mở `.env` và điền:

```env
AI_API_KEY=your_api_key_here
AI_API_URL=https://api.openai.com/v1/chat/completions
AI_MODEL=gpt-4o-mini
```

Không đưa file `.env` lên GitHub.

## Công khai thành link web

1. Tạo repository mới trên GitHub.
2. Đưa toàn bộ project lên GitHub, nhưng bỏ qua `.env`.
3. Truy cập [share.streamlit.io](https://share.streamlit.io), đăng nhập GitHub.
4. Chọn repository, branch và file chính `web_app.py`.
5. Trong phần **Advanced settings > Secrets**, thêm:

```toml
AI_API_KEY = "your_api_key_here"
AI_API_URL = "https://api.openai.com/v1/chat/completions"
AI_MODEL = "gpt-4o-mini"
```

6. Bấm **Deploy**. Streamlit sẽ cấp một đường link công khai cho website.

## Lưu ý dữ liệu

Bản local lưu tin nhắn vào JSON. Trên dịch vụ cloud, filesystem có thể được làm mới khi ứng dụng khởi động lại, vì vậy dữ liệu lâu dài sau này nên chuyển sang một dịch vụ database online.
