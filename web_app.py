from __future__ import annotations

import streamlit as st

from bus.chat_bus import ChatBus


st.set_page_config(
    page_title="Luma AI | Góc học tập của bạn",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --ink:#17212b; --muted:#687582; --mint:#d8f3e8; --orange:#ff8d67; --line:#e6e9e7; }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.02em; }
    .stApp { background: #f8faf8; }
    [data-testid="stSidebar"] { background: #17212b; }
    [data-testid="stSidebar"] * { color: #eef6f0 !important; }
    [data-testid="stSidebar"] .stRadio label { padding: .5rem .25rem; }
    .brand { padding: 1rem 0 2rem; }
    .brand-mark { display:inline-flex; width:38px; height:38px; border-radius:12px; background:var(--orange); color:white; align-items:center; justify-content:center; font-size:1.4rem; font-weight:700; }
    .brand-name { font: 700 1.25rem 'Space Grotesk'; margin-left:.55rem; vertical-align:8px; }
    .eyebrow { color:#e36e4b; text-transform:uppercase; letter-spacing:.12em; font-size:.72rem; font-weight:700; }
    .hero { background:var(--mint); border-radius:24px; padding:3rem; min-height:300px; position:relative; overflow:hidden; }
    .hero h1 { font-size: clamp(2.3rem, 5vw, 4.8rem); line-height:.98; max-width:700px; margin:.7rem 0 1.2rem; }
    .hero p { color:#3d5a50; max-width:560px; font-size:1.05rem; }
    .hero-orbit { position:absolute; right:7%; bottom:-22%; width:270px; height:270px; border:32px solid #a8dfca; border-radius:50%; }
    .section-title { margin:2.5rem 0 1rem; }
    .feature { background:#fff; border:1px solid var(--line); border-radius:16px; padding:1.25rem; min-height:150px; }
    .feature h3 { margin:.8rem 0 .4rem; font-size:1.1rem; }
    .feature p { color:var(--muted); font-size:.92rem; }
    .icon { font-size:1.5rem; }
    .product { background:#fff; border:1px solid var(--line); border-radius:16px; padding:1.4rem; min-height:220px; }
    .product h3 { margin:.7rem 0 .4rem; }
    .price { color:#e36e4b; font-weight:700; font-size:1.3rem; }
    .chat-shell { background:#fff; border:1px solid var(--line); border-radius:18px; padding:1.2rem; }
    .status { color:#427b63; font-size:.85rem; margin-bottom:1rem; }
    .bubble { padding:.85rem 1rem; border-radius:15px; margin:.55rem 0; max-width:80%; line-height:1.5; }
    .bubble.user { background:#17212b; color:#fff; margin-left:auto; border-bottom-right-radius:4px; }
    .bubble.ai { background:#eef5f0; color:var(--ink); margin-right:auto; border-bottom-left-radius:4px; }
    .role { display:block; font-size:.7rem; font-weight:700; opacity:.65; margin-bottom:.25rem; text-transform:uppercase; letter-spacing:.08em; }
    .muted { color:var(--muted); }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_bus() -> ChatBus:
    return ChatBus()


bus = get_bus()

with st.sidebar:
    st.markdown(
        '<div class="brand"><span class="brand-mark">✦</span><span class="brand-name">Luma AI</span></div>',
        unsafe_allow_html=True,
    )
    page = st.radio("Điều hướng", ["Home", "Product", "Chat với AI"], label_visibility="collapsed")
    st.divider()
    st.caption("Góc học tập nhỏ, ý tưởng lớn.")


if page == "Home":
    st.markdown(
        '<div class="hero"><div class="eyebrow">Không gian học tập cá nhân</div>'
        '<h1>Học nhẹ hơn.<br>Hiểu sâu hơn.</h1>'
        '<p>Luma AI giúp bạn sắp xếp ý tưởng, khám phá kiến thức và trò chuyện với một trợ lý luôn sẵn sàng lắng nghe.</p>'
        '<div class="hero-orbit"></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<h2 class="section-title">Mọi thứ bạn cần để bắt đầu</h2>', unsafe_allow_html=True)
    columns = st.columns(3)
    features = [
        ("◌", "Tập trung", "Một không gian gọn gàng để bạn học mà không bị phân tâm."),
        ("✦", "Khám phá", "Đặt câu hỏi, thử ý tưởng và biến tò mò thành hiểu biết."),
        ("↗", "Tiến bộ", "Lưu lại các cuộc trò chuyện để nhìn thấy hành trình của mình."),
    ]
    for column, (icon, title, text) in zip(columns, features):
        with column:
            st.markdown(f'<div class="feature"><div class="icon">{icon}</div><h3>{title}</h3><p>{text}</p></div>', unsafe_allow_html=True)

elif page == "Product":
    st.markdown('<div class="eyebrow">Bộ công cụ của Luma</div><h1>Product</h1>', unsafe_allow_html=True)
    st.write("Những tính năng được thiết kế để việc học trở nên rõ ràng và thú vị hơn.")
    columns = st.columns(3)
    products = [
        ("01", "AI Study Buddy", "Trợ lý giải thích bài học bằng ngôn ngữ dễ hiểu.", "Miễn phí"),
        ("02", "Idea Canvas", "Nơi biến những ghi chú rời rạc thành kế hoạch cụ thể.", "Sắp ra mắt"),
        ("03", "Daily Spark", "Một gợi ý nhỏ mỗi ngày để giữ nhịp tò mò.", "Sắp ra mắt"),
    ]
    for column, (number, title, description, price) in zip(columns, products):
        with column:
            st.markdown(f'<div class="product"><span class="eyebrow">{number}</span><h3>{title}</h3><p class="muted">{description}</p><p class="price">{price}</p></div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="eyebrow">Trợ lý học tập</div><h1>Chat với AI</h1>', unsafe_allow_html=True)
    st.write("Hỏi bất cứ điều gì. Bắt đầu từ một câu hỏi thật đơn giản cũng được.")
    left, right = st.columns([3, 1])
    with right:
        if st.button("Xóa cuộc trò chuyện", use_container_width=True):
            bus.clear_chat()
            st.rerun()
        mode = "AI thật" if bus.ai_model.is_configured else "Chế độ mô phỏng"
        st.markdown(f'<div class="status">● {mode}</div>', unsafe_allow_html=True)
    with left:
        st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
        messages = bus.get_messages()
        if not messages:
            st.markdown('<p class="muted">Chưa có tin nhắn. Hãy thử hỏi: “Giải thích phân số cho mình nhé!”</p>', unsafe_allow_html=True)
        for message in messages:
            role_label = "Bạn" if message["role"] == "user" else "Luma AI"
            css_class = "user" if message["role"] == "user" else "ai"
            safe_content = message["content"].replace("<", "&lt;").replace(">", "&gt;")
            st.markdown(f'<div class="bubble {css_class}"><span class="role">{role_label}</span>{safe_content}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        prompt = st.text_area("Tin nhắn", placeholder="Viết câu hỏi của bạn...", label_visibility="collapsed", height=90)
        submitted = st.form_submit_button("Gửi tin nhắn  ↗", use_container_width=True)
    if submitted:
        if not prompt.strip():
            st.warning("Bạn hãy nhập một tin nhắn trước nhé.")
        else:
            with st.spinner("Luma đang suy nghĩ..."):
                bus.send_message(prompt)
            st.rerun()
