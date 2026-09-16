# Luma AI Web

Ứng dụng web học tập cá nhân gồm Home, Product và Chat với AI. Project dùng kiến trúc 3 tầng đơn giản:

- `web_app.py`: giao diện Streamlit.
- `bus/chat_bus.py`: điều phối nghiệp vụ.
- `database/chat_repository.py`: lưu hội thoại trong `data/messages.json`.
- `model/ai_model.py`: kết nối API tương thích OpenAI.

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
