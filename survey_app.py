import streamlit as st
import pandas as pd
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="แบบวัดสุขภาวะองค์กร", layout="centered")

# --- ระบบจัดการข้อมูลชั่วคราว (แนะนำเชื่อม Postgres ในอนาคต) ---
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'page' not in st.session_state:
    st.session_state.page = 1

# --- สไตล์ความสวยงาม ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .header-box { background: linear-gradient(135deg, #006400 0%, #228B22 100%); color: white; padding: 40px; border-radius: 0 0 30px 30px; text-align: center; margin-bottom: 30px; }
    .question-card { background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; border-left: 5px solid #228B22; }
    .stProgress > div > div > div > div { background-color: #228B22; }
    </style>
    <div class="header-box">
        <h1 style='color: white;'>แบบวัดสุขภาวะทางปัญญา</h1>
        <p style='color: #e0e0e0; font-size: 1.1em;'>คำตอบของท่านจะช่วยพัฒนาองค์กรให้ดียิ่งขึ้น</p>
    </div>
    """, unsafe_allow_html=True)

# รายการคำถาม (ย่อเพื่อประหยัดพื้นที่ในโค้ด คุณปุ้มใช้รายการเดิมได้เลยครับ)
p1_qs = ["ท่านเห็นว่าตนเองมีอะไรหลายอย่างที่น่าภาคภูมิใจ", "ท่านคิดว่าชีวิตของท่านมีคุณค่า", "ท่านรู้ว่าอะไรคือคุณค่าที่แท้จริงของชีวิต", "ท่านเข้าใจว่าอะไรคือแก่นธรรมของศาสนา", "ท่านให้ความเป็นมิตรกับผู้อื่น", "ท่านให้ความสำคัญต่อความรู้สึกและความต้องการของผู้อื่น", "ท่านปรารถนาอยากจะช่วยให้ผู้อื่นพ้นความทุกข์", "ท่านเห็นความสำคัญกับการได้ช่วยเหลือผู้อื่น", "ท่านเข้าใจว่าตนเองเป็นส่วนหนึ่งและมีความสัมพันธ์เชื่อมโยงกับธรรมชาติ", "ท่านรู้สึกรักในธรรมชาติ", "ท่านได้ใช้ศักยภาพอย่างเต็มที่ ในการทำงานและดำเนินชีวิตอยู่", "ท่านทำสิ่งที่ท่านสนใจหรือให้คุณค่า แม้ว่าสิ่งนั้นจะเป็นสิ่งที่ยาก", "ท่านตั้งใจรับฟังคนที่พูดกับท่านได้จนจบ โดยไม่ตัดสินหรือพูดแทรกขึ้นมา", "ท่านแบ่งเวลาไปทำประโยชน์ให้ผู้อื่นโดยไม่ได้รับสิ่งตอบแทน", "ท่านรู้และตามทันอารมณ์ในใจของตนเอง ก่อนที่จะแสดงมันออกมา", "ท่านควบคุมอารมณ์ของตนเองได้ ก่อนที่จะแสดงออกมา", "ท่านสามารถน้อมรับฟังความคิดเห็น หรือคำวิจารณ์จากผู้อื่นได้", "ท่านให้อภัยตนเองได้", "ท่านยอมรับข้อดีและข้อด้อยของตัวเองโดยไม่ปฏิเสธมัน", "ท่านรู้สึกแจ่มใสเบิกบานในชีวิต", "โดยทั่วไปท่านมีความรู้สึกผ่อนคลาย สบายใจ", "ท่านรับรู้คุณค่าในชีวิตของท่านและดำเนินชีวิตเพื่อสิ่งนั้น", "ท่านทำงานโดยเอาคุณค่าของงานเป็นตัวจูงใจ ไม่ใช่เงินทองหรือสิ่งที่จะได้รับเป็นการตอบแทน", "ท่านรับรู้และยอมรับในข้อดีและข้อด้อยของผู้อื่นได้ด้วยความเข้าใจ", "ท่านรู้สึกชื่นชมและขอบคุณในความดีของผู้อื่นและสรรพสิ่งรอบตัว", "ท่านมีความเข้าอกเข้าใจในความรู้สึกของผู้อื่นได้ แม้ว่าท่านจะไม่เห็นด้วยกับสิ่งที่คนๆ นั้น", "ท่านเห็นคุณค่าในตัวเองอย่างที่ท่านเป็น", "ท่านให้อภัยในความผิดพลาดของตนเองได้", "ท่านให้อภัยในความผิดพลาดของผู้อื่นได้", "ท่านพร้อมเสมอที่จะเสียสละส่วนตนเพื่อประโยชน์ของส่วนรวม", "ท่านหมั่นพัฒนาความรักความเมตตาต่อผู้อื่นให้เพิ่มมากขึ้น", "ท่านมีเพื่อนหรือมีกลุ่มที่มีความสัมพันธ์ที่ดีต่อกัน", "ท่านมีเพื่อนหรือมีผู้ที่ท่านไว้ใจที่สามารถบอกกล่าวความรู้สึกลึกๆ ในใจแก่กันได้", "ท่านอ่านหนังสือหรือรับฟังคำสอนที่เกี่ยวข้องกับหลักคุณงามความดีหรือหลักศาสนา", "ท่านหาโอกาสทำสิ่งต่างๆ ที่เอื้ออำนวยให้เกิดประโยชน์แก่ผู้อื่น", "ท่านหาเวลาที่จะอยู่ใกล้ชิดกับธรรมชาติ เช่น ต้นไม้ใบหญ้า ท้องฟ้า สรรพสัตว์ต่างๆ", "ท่านรับรู้และยอมรับความทุกข์ในชีวิต และทำความเข้าใจกับมัน", "ท่านเป็นส่วนหนึ่งของกิจกรรมสร้างสรรค์สังคมที่เป็นธรรม หรือสิ่งแวดล้อมที่ปลอดภัย"]
p2_qs = ["บริษัทสนับสนุนความก้าวหน้าในสายอาชีพ", "ระบบการสื่อสารภายในบริษัทมีความชัดเจน", "สวัสดิการของบริษัทครอบคลุมความต้องการ", "หัวหน้างานให้การสนับสนุนและคำปรึกษาที่ดี", "บรรยากาศการทำงานส่งเสริมความร่วมมือ", "บริษัทให้ความสำคัญกับความสมดุลชีวิตและการทำงาน", "มีการยกย่องชมเชยเมื่อทำผลงานได้ดี", "บริษัทจัดกิจกรรมสร้างความสัมพันธ์ที่น่าสนใจ", "สภาพแวดล้อมในที่ทำงานมีความปลอดภัยและเหมาะสม", "อุปกรณ์และเครื่องมือทำงานมีความพร้อม", "นโยบายบริษัทมีความเป็นธรรมและโปร่งใส", "บริษัทรับฟังความคิดเห็นของพนักงาน", "เงินเดือนและค่าตอบแทนมีความเหมาะสม", "บริษัทมีเป้าหมายการดำเนินงานที่ชัดเจน", "เพื่อนร่วมงานมีความเป็นมิตรและช่วยเหลือกัน", "ภาพรวมของบริษัททำให้ท่านมีความสุขในการทำงาน"]

# --- หน้าที่ 1: ข้อมูลทั่วไป ---
if st.session_state.page == 1:
    st.progress(0.3)
    st.subheader("📝 ขั้นตอนที่ 1: ข้อมูลทั่วไป")
    with st.container():
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        g = st.selectbox("เพศ", ["ชาย", "หญิง"])
        a = st.number_input("อายุ", 18, 80, 30)
        s = st.selectbox("สถานภาพ", ["โสด", "สมรส", "หย่าร้าง"])
        p = st.selectbox("ตำแหน่งงาน", ["Staff", "Associate", "Specialist", "Management"])
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("ถัดไป ➡️"):
            st.session_state.p1_data = {"เพศ": g, "อายุ": a, "สถานภาพ": s, "ตำแหน่ง": p}
            st.session_state.page = 2
            st.rerun()

# --- หน้าที่ 2: ส่วนที่ 1 ---
elif st.session_state.page == 2:
    st.progress(0.6)
    st.subheader("🍃 ขั้นตอนที่ 2: แบบประเมินความรู้สึก (38 ข้อ)")
    feel_res = {}
    for i, q in enumerate(p1_qs):
        st.markdown(f'<div class="question-card"><b>{i+1}. {q}</b>', unsafe_allow_html=True)
        feel_res[f"Feel_{i+1}"] = st.radio("ระดับคะแนน", [1,2,3,4,5], horizontal=True, key=f"f{i}", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    if col1.button("⬅️ ย้อนกลับ"):
        st.session_state.page = 1
        st.rerun()
    if col2.button("ถัดไป ➡️"):
        st.session_state.p2_data = feel_res
        st.session_state.page = 3
        st.rerun()

# --- หน้าที่ 3: ส่วนที่ 2 ---
elif st.session_state.page == 3:
    st.progress(1.0)
    st.subheader("🏢 ขั้นตอนที่ 3: สิ่งที่ได้รับจากบริษัท (16 ข้อ)")
    corp_res = {}
    for i, q in enumerate(p2_qs):
        st.markdown(f'<div class="question-card"><b>{i+1}. {q}</b>', unsafe_allow_html=True)
        corp_res[f"Corp_{i+1}"] = st.radio("ระดับคะแนน", [1,2,3,4,5], horizontal=True, key=f"c{i}", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    if col1.button("⬅️ ย้อนกลับ"):
        st.session_state.page = 2
        st.rerun()
    if col2.button("🚀 ส่งแบบสอบถาม"):
        final_data = {"Timestamp": datetime.now()}
        final_data.update(st.session_state.p1_data)
        final_data.update(st.session_state.p2_data)
        final_data.update(corp_res)
        st.session_state.responses.append(final_data)
        st.session_state.page = 4
        st.rerun()

# --- หน้าสุดท้าย: ขอบคุณ ---
elif st.session_state.page == 4:
    st.balloons()
    st.success("ส่งข้อมูลเรียบร้อย ขอบคุณที่คุณเป็นส่วนหนึ่งในการพัฒนาองค์กรครับ")
    if st.button("ทำแบบสอบถามอีกครั้ง"):
        st.session_state.page = 1
        st.rerun()

# --- 🔒 ส่วนของ ADMIN (HR Only) ---
st.divider()
with st.expander("🔐 สำหรับเจ้าหน้าที่ HR (Admin Only)"):
    pw = st.text_input("กรุณาใส่รหัสผ่านเพื่อดูข้อมูล", type="password")
    if pw == "HR1234": # คุณปุ้มเปลี่ยนรหัสตรงนี้ได้เลยครับ
        if st.session_state.responses:
            df = pd.DataFrame(st.session_state.responses)
            st.write(f"📊 จำนวนผู้ตอบทั้งหมด: {len(df)} คน")
            st.dataframe(df.head())
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 Download Excel (CSV)", data=csv, file_name="happiness_data.csv", mime="text/csv")
        else:
            st.info("ยังไม่มีข้อมูลถูกบันทึกในรอบนี้")
    elif pw != "":
        st.error("รหัสผ่านไม่ถูกต้อง")
