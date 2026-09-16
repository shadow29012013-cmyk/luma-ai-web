from __future__ import annotations

from datetime import date
from html import escape

import streamlit as st

from bus.chat_bus import ChatBus
from bus.study_bus import StudyBus

st.set_page_config(page_title="StudySync | Quản lý học tập", page_icon="◈", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --ink:#17212b; --muted:#6b7882; --mint:#d8f3e8; --orange:#f47d5c; --line:#e3e8e5; }
    html,body,[class*="css"] { font-family:'DM Sans',sans-serif; color:var(--ink); }
    h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.025em; }
    .stApp { background:#f7faf8; }
    [data-testid="stSidebar"] { background:#17212b; }
    [data-testid="stSidebar"] * { color:#eef6f0 !important; }
    .brand { padding:1rem 0 2rem; }.brand-mark { display:inline-flex; width:38px; height:38px; border-radius:12px; background:var(--orange); color:#fff; align-items:center; justify-content:center; font-size:1.35rem; font-weight:700; }.brand-name { font:700 1.2rem 'Space Grotesk'; margin-left:.55rem; vertical-align:8px; }
    .eyebrow { color:#dc6d4b; text-transform:uppercase; letter-spacing:.12em; font-size:.7rem; font-weight:700; }.hero { background:var(--mint); border-radius:24px; padding:2.4rem 2.8rem; min-height:220px; position:relative; overflow:hidden; }.hero h1 { font-size:clamp(2.2rem,4vw,4rem); line-height:1; margin:.6rem 0 1rem; }.hero p { color:#3d5a50; max-width:590px; font-size:1.03rem; }.hero-orbit { position:absolute; right:7%; bottom:-30%; width:250px; height:250px; border:30px solid #a8dfca; border-radius:50%; }
    .metric { background:#fff; border:1px solid var(--line); border-radius:16px; padding:1rem 1.15rem; min-height:106px; }.metric-label { color:var(--muted); font-size:.82rem; }.metric-value { font:700 2rem 'Space Grotesk'; margin-top:.25rem; }.metric-note { color:#4a8a6c; font-size:.78rem; }.section-title { margin:2rem 0 .8rem; }.lesson { border-left:4px solid var(--orange); background:#fff; border-radius:10px; padding:.8rem 1rem; margin:.55rem 0; border-top:1px solid var(--line); border-right:1px solid var(--line); border-bottom:1px solid var(--line); }.lesson strong { font-family:'Space Grotesk'; }.lesson small,.task small { color:var(--muted); }.task { background:#fff; border:1px solid var(--line); border-radius:12px; padding:.85rem 1rem; margin:.55rem 0; }.task-title { font-weight:700; }.priority { color:#d15d3e; font-size:.75rem; font-weight:700; text-transform:uppercase; letter-spacing:.06em; }.notice { background:#fff5e8; border:1px solid #f5d7ad; color:#765024; border-radius:12px; padding:.8rem 1rem; margin:.5rem 0; }.chat-shell { background:#fff; border:1px solid var(--line); border-radius:16px; padding:1.2rem; }.bubble { padding:.85rem 1rem; border-radius:15px; margin:.55rem 0; max-width:80%; line-height:1.5; }.bubble.user { background:#17212b; color:#fff; margin-left:auto; border-bottom-right-radius:4px; }.bubble.ai { background:#eef5f0; color:var(--ink); margin-right:auto; border-bottom-left-radius:4px; }.role { display:block; font-size:.68rem; font-weight:700; opacity:.65; margin-bottom:.25rem; text-transform:uppercase; letter-spacing:.08em; }.muted { color:var(--muted); }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_services() -> tuple[StudyBus, ChatBus]:
    return StudyBus(), ChatBus()


study, chat = get_services()


def render_task(task: dict[str, str | bool]) -> None:
    due = date.fromisoformat(str(task["due_date"])).strftime("%d/%m/%Y")
    status = "Đã xong" if task["completed"] else f"Hạn {due}"
    st.markdown(
        f'<div class="task"><div class="task-title">{escape(str(task["title"]))}</div>'
        f'<small>{escape(str(task["subject"]))} · {status}</small>'
        f'<div class="priority">{escape(str(task["priority"]))}</div></div>',
        unsafe_allow_html=True,
    )


with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-mark">◈</span><span class="brand-name">StudySync</span></div>', unsafe_allow_html=True)
    page = st.radio("Điều hướng", ["Dashboard", "Thời khóa biểu", "Bài tập & Deadline", "Chat với AI"], label_visibility="collapsed")
    st.divider()
    st.caption("Học có kế hoạch. Tiến bộ mỗi ngày.")


if page == "Dashboard":
    st.markdown('<div class="hero"><div class="eyebrow">Không gian học tập cá nhân</div><h1>Học có nhịp.<br>Tiến bộ có hình.</h1><p>StudySync gom lịch học, deadline và tiến độ vào một dashboard rõ ràng để bạn biết hôm nay cần làm gì tiếp theo.</p><div class="hero-orbit"></div></div>', unsafe_allow_html=True)
    stats = study.stats()
    st.markdown('<h2 class="section-title">Tổng quan của bạn</h2>', unsafe_allow_html=True)
    metrics = st.columns(4)
    labels = ["Bài tập tổng", "Đã hoàn thành", "Đang chờ", "Tỷ lệ hoàn thành"]
    values = [stats["total"], stats["completed"], stats["pending"], f'{stats["completion_rate"]}%']
    notes = ["trong học kỳ", "tốt lắm", "ưu tiên hôm nay", "mục tiêu tuần"]
    for column, label, value, note in zip(metrics, labels, values, notes):
        with column:
            st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Tiến độ tuần</h2>', unsafe_allow_html=True)
    st.progress(int(stats["completion_rate"]) / 100, text=f'{stats["completion_rate"]}% bài tập đã hoàn thành')
    st.bar_chart({"Đã hoàn thành": stats["completed"], "Đang chờ": stats["pending"]}, horizontal=True)
    left, right = st.columns([1.05, .95])
    with left:
        st.markdown('<h2 class="section-title">Lịch học sắp tới</h2>', unsafe_allow_html=True)
        for lesson in study.schedule()[:4]:
            st.markdown(f'<div class="lesson"><strong>{escape(str(lesson["subject"]))}</strong><br><small>{lesson["day"]} · {lesson["start"]} · Phòng {escape(str(lesson["room"]))} · {escape(str(lesson["lecturer"]))}</small></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<h2 class="section-title">Deadline trong 7 ngày</h2>', unsafe_allow_html=True)
        due_soon = study.due_soon()
        if due_soon:
            for task in due_soon[:4]:
                render_task(task)
        else:
            st.markdown('<div class="notice">Bạn đang không có deadline gần.</div>', unsafe_allow_html=True)

elif page == "Thời khóa biểu":
    st.markdown('<div class="eyebrow">Lịch học</div><h1>Thời khóa biểu</h1>', unsafe_allow_html=True)
    st.write("Lưu môn học, phòng học và giảng viên.")
    with st.expander("＋ Thêm buổi học mới"):
        with st.form("schedule_form", clear_on_submit=True):
            subject = st.text_input("Tên môn học")
            day = st.selectbox("Ngày học", ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"])
            start = st.time_input("Giờ bắt đầu")
            room = st.text_input("Phòng học")
            lecturer = st.text_input("Giảng viên")
            if st.form_submit_button("Lưu buổi học", use_container_width=True):
                try:
                    study.add_schedule(subject, day, start.strftime("%H:%M"), room, lecturer)
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))
    for lesson in study.schedule():
        st.markdown(f'<div class="lesson"><strong>{escape(str(lesson["subject"]))}</strong><br><small>{lesson["day"]} · {lesson["start"]} · Phòng {escape(str(lesson["room"]))} · {escape(str(lesson["lecturer"]))}</small></div>', unsafe_allow_html=True)

elif page == "Bài tập & Deadline":
    st.markdown('<div class="eyebrow">Danh sách việc cần làm</div><h1>Bài tập & Deadline</h1>', unsafe_allow_html=True)
    st.write("Ghi rõ việc cần làm, môn học và mức độ ưu tiên.")
    with st.expander("＋ Thêm bài tập mới"):
        with st.form("assignment_form", clear_on_submit=True):
            title = st.text_input("Tên bài tập")
            subject = st.text_input("Môn học")
            due_date = st.date_input("Hạn nộp", min_value=date.today())
            priority = st.selectbox("Mức độ ưu tiên", ["Gấp", "Quan trọng", "Bình thường"])
            if st.form_submit_button("Lưu bài tập", use_container_width=True):
                try:
                    study.add_assignment(title, subject, due_date, priority)
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))
    for task in study.assignments():
        columns = st.columns([.08, .92])
        with columns[0]:
            checked = st.checkbox("Hoàn thành", value=bool(task["completed"]), key=str(task["id"]), label_visibility="collapsed")
        with columns[1]:
            render_task(task)
        if checked != task["completed"]:
            study.set_completed(str(task["id"]), checked)
            st.rerun()

else:
    st.markdown('<div class="eyebrow">Trợ lý học tập</div><h1>Chat với AI</h1>', unsafe_allow_html=True)
    st.write("Hỏi AI cách lập kế hoạch, giải thích bài học hoặc chia deadline thành các bước nhỏ.")
    if st.button("Xóa cuộc trò chuyện"):
        chat.clear_chat()
        st.rerun()
    st.caption("● " + ("AI thật" if chat.ai_model.is_configured else "Chế độ mô phỏng"))
    st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
    messages = chat.get_messages()
    if not messages:
        st.markdown('<p class="muted">Hãy thử hỏi: “Lập kế hoạch ôn Toán trong 7 ngày cho mình.”</p>', unsafe_allow_html=True)
    for message in messages:
        role = "Bạn" if message["role"] == "user" else "StudySync AI"
        css_class = "user" if message["role"] == "user" else "ai"
        content = escape(str(message["content"])).replace("\n", "<br>")
        st.markdown(f'<div class="bubble {css_class}"><span class="role">{role}</span>{content}</div>', unsafe_allow_html=True)
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
