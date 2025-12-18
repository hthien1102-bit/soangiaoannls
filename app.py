import streamlit as st
import google.generativeai as genai

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="AI Soạn Giáo Án",
    page_icon="📘",
    layout="centered"
)

st.title("📘 AI Soạn Giáo Án Tiểu Học")
st.write("Nhập yêu cầu – AI sẽ hỗ trợ soạn bài cho thầy/cô")

# =========================
# KIỂM TRA API KEY
# =========================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ Chưa cấu hình GOOGLE_API_KEY trong Streamlit Secrets")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# =========================
# KHỞI TẠO MODEL
# =========================
model = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# GIAO DIỆN NHẬP LIỆU
# =========================
lop = st.selectbox("📚 Chọn lớp:", ["Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5"])
mon = st.text_input("📖 Môn học:", placeholder="Ví dụ: Toán, Tiếng Việt, Lịch sử - Địa lí...")
chu_de = st.text_input("📝 Chủ đề / bài học:", placeholder="Ví dụ: Sông Hồng")
yeu_cau = st.text_area(
    "🎯 Yêu cầu thêm:",
    placeholder="Ví dụ: Soạn theo hướng phát triển năng lực, có hoạt động nhóm..."
)

# =========================
# NÚT SOẠN GIÁO ÁN
# =========================
if st.button("✨ Soạn giáo án"):
    if not mon or not chu_de:
        st.warning("⚠️ Vui lòng nhập đầy đủ môn học và chủ đề")
    else:
        with st.spinner("⏳ AI đang soạn giáo án..."):
            prompt = f"""
Bạn là giáo viên tiểu học nhiều kinh nghiệm.
Hãy soạn một giáo án chi tiết cho:

- Lớp: {lop}
- Môn: {mon}
- Chủ đề: {chu_de}

Yêu cầu:
- Đúng chương trình GDPT 2018
- Có: Mục tiêu, Chuẩn bị, Hoạt động dạy học, Đánh giá
- Ngôn ngữ dễ hiểu, phù hợp học sinh tiểu học
- {yeu_cau}
"""

            try:
                response = model.generate_content(prompt)
                st.success("✅ Soạn xong!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"❌ Có lỗi xảy ra: {e}")
