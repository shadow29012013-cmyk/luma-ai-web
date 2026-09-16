from __future__ import annotations

from datetime import date
from html import escape

import streamlit as st

from bus.chat_bus import ChatBus
from bus.study_bus import StudyBus

st.set_page_config(
    page_title="StudySync | Quản lý học tập",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --ink:#17212b; --muted:#6b7882; --mint:#d8f3e8; --orange:#f47d5c; --line:#e3e8e5; --paper:#ffffff; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; color:var(--ink); }
    h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.025em; }
    .stApp { background:#f7faf8; }
    [data-testid="stSidebar"] { background:#17212b; }
    [data-testid="stSidebar"] * { color:#eef6f0 !important; }
    .brand { padding:1rem 0 2rem; }
    .brand-mark { display:inline-flex; width:38px; height:38px; border-radius:12px; background:var(--orange); color:#fff; align-items:center; justify-content:center; font-size:1.35rem; font-weight:700; }
    .brand-name { font:700 1.2rem 'Space Grotesk'; margin-left:.55rem; vertical-align:8px; }
    .eyebrow { color:#dc6d4b; text-transform:uppercase; letter-spacing:.12em; font-size:.7rem; font-weight:700; }
    .hero { background:var(--mint); border-radius:24px; padding:2.4rem 2.8rem; min-height:220px; position:relative; overflow:hidden; }
    .hero h1 { font-size:clamp(2.2rem,4vw,4rem); line-height:1; margin:.6rem 0 1rem; }
    .hero p { color:#3d5a50; max-width:590px; font-size:1.03rem; }
    .hero-orbit { position:absolute; right:7%; bottom:-30%; width:250px; height:250px; border:30px solid #a8dfca; border-radius:50%; }
    .panel { background:var(--paper); border:1px solid var(--line); border-radius:16px; padding:1.2rem; }
    .metric { background:var(--paper); border:1px solid var(--line); border-radius:16px; padding:1rem 1.15rem; min-height:106px; }
    .metric-label { color:var(--muted); font-size:.82rem; }
    .metric-value { font:700 2rem 'Space Grotesk'; margin-top:.25rem; }
    .metric-note { color:#4a8a6c; font-size:.78rem; }
    .section-title { margin:2rem 0 .8rem; }
    .lesson { border-left:4px solid var(--orange); background:#fff; border-radius:10px; padding:.8rem 1rem; margin:.55rem 0; border-top:1px solid var(--line); border-right:1px solid var(--line); border-bottom:1px solid var(--line); }
    .lesson strong { font-family:'Space Grotesk'; }
    .lesson small, .task small { color:var(--muted); }
    .task { background:#fff; border:1px solid var(--line); border-radius:12px; padding:.85rem 1rem; margin:.55rem 0; }
    .task-title { font-weight:700; }
    .priority { color:#d15d3e; font-size:.75rem; font-weight:700; text-transform:uppercase; letter-spacing:.06em; }
    .notice { background:#fff5e8; border:1px solid #f5d7ad; color:#765024; border-radius:12px; padding:.8rem 1rem; margin:.5rem 0; }
    .chat-shell { background:#fff; border:1px solid var(--line); border-radius:16px; padding:1.2rem; }
    .bubble { padding:.85rem 1rem; border-radius:15px; margin:.55rem 0; max-width:80%; line-height:1.5; }
    .bubble.user { background:#17212b; color:#fff; margin-left:auto; border-bottom-right-radius:4px; }
    .bubble.ai { background:#eef5f0; color:var(--ink); margin-right:auto; border-bottom-left-radius:4px; }
    .role { display:block; font-size:.68rem; font-weight:700; opacity:.65; margin-bottom:.25rem; text-transform:uppercase; letter-spacing:.08em; }
    .muted { color:var(--muted); }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_services() -> tuple[StudyBus, ChatBus]:
    return StudyBus(), ChatBus()


study, chat = get_services()

with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-mark">◈</span><span class="brand-name">StudySync</span></div>', unsafe_allow_html=True)
    page = st.radio("Điều hướng", ["Dashboard", "Thời khóa biểu", "Bài tập & Deadline", "Chat với AI"], label_visibility="collapsed")
    st.divider()
    st.caption("Học có kế hoạch. Tiến bộ mỗi ngày.")


def render_task(task: dict[str, str | bool]) -> None:
    due = date.fromisoformat(str(task["due_date"])).strftime("%d/%m/%Y")
    status = "Đã xong" if task["completed"] else f"Hạn {due}"
    st.markdown(
        f'<div class="task"><div class="task-title">{escape(str(task["title"]))}</div>'
        f'<small>{escape(str(task["subject"]))} · {status}</small>'
        f'<div class="priority">{escape(str(task["priority"]))}</div></div>',
        unsafe_allow_html=True,
    )


if page == "Dashboard":
    st.markdown('<div class="hero"><div class="eyebrow">Không gian học tập cá nhân</div><h1>Học có nhịp.<br>Tiến bộ có hình.</h1><p>StudySync gom lịch học, deadline và thói quen học vào một dashboard rõ ràng để bạn biết hôm nay cần làm gì tiếp theo.</p><div class="hero-orbit"></div></div>', unsafe_allow_html=True)
    stats = study.stats()
    st.markdown('<h2 class="section-title">Tổng quan của bạn</h2>', unsafe_allow_html=True)
    metrics = st.columns(4)
    for column, label, value, note in zip(metrics, ["Bài tập tổng", "Đã hoàn thành", "Đang chờ", "Tỷ lệ hoàn thành"], [stats["total"], stats["completed"], stats["pending"], f'{stats["completion_rate"]}%'], ["trong học kỳ", "tốt lắm", "ưu tiên hôm nay", "mục tiêu tuần"]):
        with column:
            st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)

    st.markdown('<h2 class="section-title">Tiến độ tuần</h2>', unsafe_allow_html=True)
    st.progress(int(stats["completion_rate"]) / 100, text=f'{stats["completion_rate"]}% bài tập đã hoàn thành')
    st.bar_chart({"Đã hoàn thành": stats["completed"], "Đang chờ": stats["pending"]}, horizontal=True)

    left, right = st.columns([1.05, .95])
    with left:
        st.markdown('<h2 class="section-title">Lịch học sắp tới</h2>', unsafe_allow_html=True)
        schedule = study.schedule()
        if schedule:
            for lesson in schedule[:4]:
                st.markdown(f'<div class="lesson"><strong>{escape(str(lesson["subject"]))}</strong><br><small>{lesson["day"]} · {lesson["start"]} · Phòng {escape(str(lesson["room"]))} · {escape(str(lesson["lecturer"]))}</small></div>', unsafe_allow_html=True)
        else:
            st.info("Bạn chưa có lịch học nào.")
    with right:
        st.markdown('<h2 class="section-title">Deadline trong 7 ngày</h2>', unsafe_allow_html=True)
        due_soon = study.due_soon()
        if due_soon:
            for task in due_soon[:4]:
                render_task(task)
        else:
            st.markdown('<div class="notice">Bạn đang không có deadline gần. Đây là lúc tốt để chuẩn bị trước.</div>', unsafe_allow_html=True)

elif page == "Thời khóa biểu":
    st.markdown('<div class="eyebrow">Lịch học</div><h1>Thời khóa biểu</h1>', unsafe_allow_html=True)
    st.write("Lưu môn học, phòng học và giảng viên để luôn biết mình cần có mặt ở đâu.")
    with st.expander("＋ Thêm buổi học mới", expanded=False):
        with st.form("schedule_form", clear_on_submit=True):
            subject = st.text_input("Tên môn học")
            day = st.selectbox("Ngày học", ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"])
            start = st.time_input("Giờ bắt đầu")
            room = st.text_input("Phòng học")
            lecturer = st.text_input("Giảng viên")
            if st.form_submit_button("Lưu buổi học", use_container_width=True):
                try:
                    study.add_schedule(subject, day, start.strftime("%H:%M"), room, lecturer)
                    st.success("Đã thêm vào thời khóa biểu.")
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))
    for lesson in study.schedule():
        st.markdown(f'<div class="lesson"><strong>{escape(str(lesson["subject"]))}</strong><br><small>{lesson["day"]} · {lesson["start"]} · Phòng {escape(str(lesson["room"]))} · {escape(str(lesson["lecturer"]))}</small></div>', unsafe_allow_html=True)

elif page == "Bài tập & Deadline":
    st.markdown('<div class="eyebrow">Danh sách việc cần làm</div><h1>Bài tập & Deadline</h1>', unsafe_allow_html=True)
    st.write("Chia nhỏ áp lực bằng cách ghi rõ việc cần làm, môn học và mức độ ưu tiên.")
    with st.expander("＋ Thêm bài tập mới", expanded=False):
        with st.form("assignment_form", clear_on_submit=True):
            title = st.text_input("Tên bài tập")
            subject = st.text_input("Môn học")
            due_date = st.date_input("Hạn nộp", min_value=date.today())
            priority = st.selectbox("Mức độ ưu tiên", ["Gấp", "Quan trọng", "Bình thường"])
            if st.form_submit_button("Lưu bài tập", use_container_width=True):
                try:
                    study.add_assignment(title, subject, due_date, priority)
                    st.success("Đã thêm deadline.")
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))
    tasks = study.assignments()
    for task in tasks:
        task_columns = st.columns([.08, .72, .2])
        with task_columns[0]:
            checked = st.checkbox("Hoàn thành", value=bool(task["completed"]), key=str(task["id"]), label_visibility="collapsed")
        with task_columns[1]:
            render_task(task)
        with task_columns[2]:
            if checked != task["completed"]:
                study.set_completed(str(task["id"]), checked)
                st.rerun()

elif page == "Chat với AI":
    st.markdown('<div class="eyebrow">Trợ lý học tập</div><h1>Chat với AI</h1>', unsafe_allow_html=True)
    st.write("Hỏi AI cách lập kế hoạch, giải thích bài học hoặc chia deadline thành các bước nhỏ.")
    if st.button("Xóa cuộc trò chuyện"):
        chat.clear_chat()
        st.rerun()
    mode = "AI thật" if chat.ai_model.is_configured else "Chế độ mô phỏng"
    st.caption(f"● {mode}")
    st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
    messages = chat.get_messages()
    if not messages:
        st.markdown('<p class="muted">Hãy thử hỏi: “Lập kế hoạch ôn Toán trong 7 ngày cho mình.”</p>', unsafe_allow_html=True)
    for message in messages:
        role_label = "Bạn" if message["role"] == "user" else "StudySync AI"
        css_class = "user" if message["role"] == "user" else "ai"
        content = escape(str(message["content"])).replace("\n", "<br>")
        st.markdown(f'<div class="bubble {css_class}"><span class="role">{role_label}</span>{content}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        prompt = st.text_area("Tin nhắn", placeholder="Viết câu hỏi của bạn...", label_visibility="collapsed", height=90)
        submitted = st.form_submit_button("Gửi tin nhắn  ↗", use_container_width=True)
    if submitted:
        if not prompt.strip():
            st.warning("Bạn hãy nhập một tin nhắn trước nhé.")
        else:
            with st.spinner("StudySync AI đang suy nghĩ..."):
                chat.send_message(prompt)
            st.rerun()


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
