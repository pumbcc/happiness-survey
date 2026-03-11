import streamlit as st
import pandas as pd
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="แบบวัดสุขภาวะองค์กร", layout="centered")

# --- ระบบจัดการข้อมูล ---
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'page' not in st.session_state:
    st.session_state.page = 1

# --- 🛠 CSS ชุดใหญ่: เปลี่ยน Radio เป็นปุ่มกดแบบ GAS ---
st.html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600&display=swap');
    
    /* 1. บังคับสีพื้นหลังของทั้งหน้าให้เป็นสีขาวนวลเสมอ */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
        background-color: #f4f7f6 !important;
    }

    /* 2. บังคับสีฟอนต์ทุกจุดให้เป็นสีดำเข้ม (แก้ปัญหาฟอนต์จม) */
    p, span, label, h1, h2, h3, h4, .stMarkdown, div, .q-text {
        color: #1A1A1A !important;
    }

    /* 3. Header Box: บังคับเขียว ขาว */
    .header-box { 
        background: linear-gradient(135deg, #006400 0%, #228B22 100%) !important; 
        padding: 40px 20px; 
        border-radius: 0 0 40px 40px; 
        text-align: center; 
        margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .header-box h1, .header-box p { color: #FFFFFF !important; }

    /* 4. การ์ดคำถาม: ต้องพื้นขาว ฟอนต์ดำ */
    .question-card { 
        background-color: #FFFFFF !important; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.1); 
        margin-bottom: 10px; 
        border-left: 6px solid #228B22 !important;
    }
    .q-text { font-weight: 600 !important; font-size: 1.1rem !important; }

    /* 5. แก้ไข Dropdown (Selectbox) ให้มองเห็นชัด */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid #D1D1D1 !important;
    }

    /* 6. ปุ่ม Next/Back: ฟอนต์ขาวเท่านั้น */
    .stButton > button {
        background-color: #228B22 !important;
        border-radius: 30px !important;
        height: 55px !important;
        width: 100% !important;
        border: none !important;
    }
    .stButton > button p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
    }

    /* 7. Radio Buttons (ปุ่ม 1-5) */
    div[data-testid="stRadio"] label {
        background-color: #E8F5E9 !important; /* เขียวอ่อนๆ */
        color: #1A1A1A !important;
        border: 1px solid #C8E6C9 !important;
        padding: 15px !important;
        border-radius: 10px !important;
    }
    
    /* เมื่อกดเลือกปุ่ม 1-5 */
    div[data-testid="stRadio"] input:checked + div {
        background-color: #228B22 !important;
        color: #FFFFFF !important;
    }

    /* ซ่อน CSS Code ที่ชอบหลุดออกมา */
    pre, code { display: none !important; }
    </style>
    
    <div class="header-box">
        <h1>แบบวัดสุขภาวะทางปัญญา</h1>
        <p>เพื่อความสุขในการทำงานอย่างยั่งยืน</p>
    </div>
""")
# รายการคำถาม
p1_qs = ["ท่านเห็นว่าตนเองมีอะไรหลายอย่างที่น่าภาคภูมิใจ", "ท่านคิดว่าชีวิตของท่านมีคุณค่า", "ท่านรู้ว่าอะไรคือคุณค่าที่แท้จริงของชีวิต", "ท่านเข้าใจว่าอะไรคือแก่นธรรมของศาสนา", "ท่านให้ความเป็นมิตรกับผู้อื่น", "ท่านให้ความสำคัญต่อความรู้สึกและความต้องการของผู้อื่น", "ท่านปรารถนาอยากจะช่วยให้ผู้อื่นพ้นความทุกข์", "ท่านเห็นความสำคัญกับการได้ช่วยเหลือผู้อื่น", "ท่านเข้าใจว่าตนเองเป็นส่วนหนึ่งและมีความสัมพันธ์เชื่อมโยงกับธรรมชาติ", "ท่านรู้สึกรักในธรรมชาติ", "ท่านได้ใช้ศักยภาพอย่างเต็มที่ ในการทำงานและดำเนินชีวิตอยู่", "ท่านทำสิ่งที่ท่านสนใจหรือให้คุณค่า แม้ว่าสิ่งนั้นจะเป็นสิ่งที่ยาก", "ท่านตั้งใจรับฟังคนที่พูดกับท่านได้จนจบ โดยไม่ตัดสินหรือพูดแทรกขึ้นมา", "ท่านแบ่งเวลาไปทำประโยชน์ให้ผู้อื่นโดยไม่ได้รับสิ่งตอบแทน", "ท่านรู้และตามทันอารมณ์ในใจของตนเอง ก่อนที่จะแสดงมันออกมา", "ท่านควบคุมอารมณ์ของตนเองได้ ก่อนที่จะแสดงออกมา", "ท่านสามารถน้อมรับฟังความคิดเห็น หรือคำวิจารณ์จากผู้อื่นได้", "ท่านให้อภัยตนเองได้", "ท่านยอมรับข้อดีและข้อด้อยของตัวเองโดยไม่ปฏิเสธมัน", "ท่านรู้สึกแจ่มใสเบิกบานในชีวิต", "โดยทั่วไปท่านมีความรู้สึกผ่อนคลาย สบายใจ", "ท่านรับรู้คุณค่าในชีวิตของท่านและดำเนินชีวิตเพื่อสิ่งนั้น", "ท่านทำงานโดยเอาคุณค่าของงานเป็นตัวจูงใจ ไม่ใช่เงินทองหรือสิ่งที่จะได้รับเป็นการตอบแทน", "ท่านรับรู้และยอมรับในข้อดีและข้อด้อยของผู้อื่นได้ด้วยความเข้าใจ", "ท่านรู้สึกชื่นชมและขอบคุณในความดีของผู้อื่นและสรรพสิ่งรอบตัว", "ท่านมีความเข้าอกเข้าใจในความรู้สึกของผู้อื่นได้ แม้ว่าท่านจะไม่เห็นด้วยกับสิ่งที่คนๆ นั้น", "ท่านเห็นคุณค่าในตัวเองอย่างที่ท่านเป็น", "ท่านให้อภัยในความผิดพลาดของตนเองได้", "ท่านให้อภัยในความผิดพลาดของผู้อื่นได้", "ท่านพร้อมเสมอที่จะเสียสละส่วนตนเพื่อประโยชน์ของส่วนรวม", "ท่านหมั่นพัฒนาความรักความเมตตาต่อผู้อื่นให้เพิ่มมากขึ้น", "ท่านมีเพื่อนหรือมีกลุ่มที่มีความสัมพันธ์ที่ดีต่อกัน", "ท่านมีเพื่อนหรือมีผู้ที่ท่านไว้ใจที่สามารถบอกกล่าวความรู้สึกลึกๆ ในใจแก่กันได้", "ท่านอ่านหนังสือหรือรับฟังคำสอนที่เกี่ยวข้องกับหลักคุณงามความดีหรือหลักศาสนา", "ท่านหาโอกาสทำสิ่งต่างๆ ที่เอื้ออำนวยให้เกิดประโยชน์แก่ผู้อื่น", "ท่านหาเวลาที่จะอยู่ใกล้ชิดกับธรรมชาติ เช่น ต้นไม้ใบหญ้า ท้องฟ้า สรรพสัตว์ต่างๆ", "ท่านรับรู้และยอมรับความทุกข์ในชีวิต และทำความเข้าใจกับมัน", "ท่านเป็นส่วนหนึ่งของกิจกรรมสร้างสรรค์สังคมที่เป็นธรรม หรือสิ่งแวดล้อมที่ปลอดภัย"]
p2_qs = ["บริษัทสนับสนุนความก้าวหน้าในสายอาชีพ", "ระบบการสื่อสารภายในบริษัทมีความชัดเจน", "สวัสดิการของบริษัทครอบคลุมความต้องการ", "หัวหน้างานให้การสนับสนุนและคำปรึกษาที่ดี", "บรรยากาศการทำงานส่งเสริมความร่วมมือ", "บริษัทให้ความสำคัญกับความสมดุลชีวิตและการทำงาน", "มีการยกย่องชมเชยเมื่อทำผลงานได้ดี", "บริษัทจัดกิจกรรมสร้างความสัมพันธ์ที่น่าสนใจ", "สภาพแวดล้อมในที่ทำงานมีความปลอดภัยและเหมาะสม", "อุปกรณ์และเครื่องมือทำงานมีความพร้อม", "นโยบายบริษัทมีความเป็นธรรมและโปร่งใส", "บริษัทรับฟังความคิดเห็นของพนักงาน", "เงินเดือนและค่าตอบแทนมีความเหมาะสม", "บริษัทมีเป้าหมายการดำเนินงานที่ชัดเจน", "เพื่อนร่วมงานมีความเป็นมิตรและช่วยเหลือกัน", "ภาพรวมของบริษัททำให้ท่านมีความสุขในการทำงาน"]

# --- หน้าที่ 1 ---
if st.session_state.page == 1:
    st.subheader("📝 ข้อมูลทั่วไป")
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    g = st.selectbox("เพศ", ["ชาย", "หญิง"])
    a = st.number_input("อายุ (ปี)", 18, 80, 30)
    s = st.selectbox("สถานภาพ", ["โสด", "สมรส", "หย่าร้าง/แยกกันอยู่"])
    p = st.selectbox("ตำแหน่งงาน", ["Staff - Head Staff", "Associate - Professional", "Specialist - Sr. Specialist", "ADM - AHO"])
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("ถัดไป ➡️"):
        st.session_state.p1_data = {"เพศ": g, "อายุ": a, "สถานภาพ": s, "ตำแหน่ง": p}
        st.session_state.page = 2
        st.rerun()

# --- หน้าที่ 2 ---
elif st.session_state.page == 2:
    st.subheader("🍃 ส่วนที่ 1: ความรู้สึก (38 ข้อ)")
    feel_res = {}
    for i, q in enumerate(p1_qs):
        st.markdown(f'<div class="question-card"><span class="q-text">{i+1}. {q}</span></div>', unsafe_allow_html=True)
        # Radio ที่จะถูก CSS แปลงเป็นปุ่ม
        feel_res[f"Feel_{i+1}"] = st.radio(f"f{i}", [1,2,3,4,5], horizontal=True, key=f"f{i}")
        st.markdown('<div style="display:flex; justify-content:space-between; padding:5px 10px 20px 10px; font-size:0.8rem; color:#888;"><span>น้อยที่สุด</span><span>มากที่สุด</span></div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("⬅️ ย้อนกลับ"): st.session_state.page = 1; st.rerun()
    with c2: 
        if st.button("ถัดไป ➡️"): st.session_state.p2_data = feel_res; st.session_state.page = 3; st.rerun()

# --- หน้าที่ 3 ---
elif st.session_state.page == 3:
    st.subheader("🏢 ส่วนที่ 2: สิ่งที่ได้รับจากบริษัท (16 ข้อ)")
    corp_res = {}
    for i, q in enumerate(p2_qs):
        st.markdown(f'<div class="question-card"><span class="q-text">{i+1}. {q}</span></div>', unsafe_allow_html=True)
        corp_res[f"Corp_{i+1}"] = st.radio(f"c{i}", [1,2,3,4,5], horizontal=True, key=f"c{i}")
        st.markdown('<div style="display:flex; justify-content:space-between; padding:5px 10px 20px 10px; font-size:0.8rem; color:#888;"><span>น้อยที่สุด</span><span>มากที่สุด</span></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ ย้อนกลับ"): st.session_state.page = 2; st.rerun()
    with c2:
        if st.button("🚀 ส่งข้อมูล"):
            final_data = {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            final_data.update(st.session_state.p1_data)
            final_data.update(st.session_state.p2_data)
            final_data.update(corp_res)
            st.session_state.responses.append(final_data)
            st.session_state.page = 4
            st.rerun()

# --- หน้าสุดท้าย ---
elif st.session_state.page == 4:
    st.balloons()
    st.markdown('<div class="question-card" style="text-align:center; padding:50px;"><h2>ขอบคุณที่ร่วมตอบแบบสอบถามครับ</h2></div>', unsafe_allow_html=True)
    if st.button("ทำแบบสอบถามอีกครั้ง"): st.session_state.page = 1; st.rerun()
