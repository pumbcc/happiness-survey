import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="แบบวัดสุขภาวะทางปัญญา", layout="wide")

# --- ส่วนของ Python Logic สำหรับบันทึกข้อมูล ---
def save_data(form_data):
    file_name = "survey_responses.csv"
    data = {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    data.update(form_data)
    df = pd.DataFrame([data])
    
    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        df.to_csv(file_name, mode='a', index=False, header=False, encoding='utf-8-sig')

# --- ส่วนของ HTML/CSS/JS (ยกจาก GAS มาเลย) ---
# ผมปรับปรุงส่วน JS นิดเดียวเพื่อให้คุยกับ Streamlit ได้ครับ
html_code = """
<!DOCTYPE html>
<html>
<head>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Sarabun', sans-serif; background-color: #f4f7f6; color: #333; padding-bottom: 50px; }
    .header-card { background: linear-gradient(135deg, #006400 0%, #228B22 100%); color: white; padding: 40px 20px; border-radius: 0 0 40px 40px; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .card { border: none; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .section-header { color: #228B22; border-left: 5px solid #228B22; padding-left: 15px; margin: 30px 0 15px; font-weight: 600; }
    .question-item { padding: 18px; border-bottom: 1px solid #edf2f0; }
    .rating-btn-group { display: flex; justify-content: space-between; gap: 5px; margin-top: 10px; }
    .btn-check:checked + .btn-outline-success { background-color: #228B22; color: white; }
    .required::after { content: " *"; color: #d9534f; }
    .btn-submit { padding: 12px 60px; border-radius: 30px; font-size: 1.1rem; font-weight: 600; transition: 0.3s; }
  </style>
</head>
<body>

<div class="header-card text-center">
  <h2>แบบวัดสุขภาวะทางปัญญาคนวัยทำงาน</h2>
  <p class="mb-0 opacity-75">คำตอบของท่านจะถูกเก็บเป็นความลับเพื่อใช้พัฒนาองค์กร</p>
</div>

<div class="container">
  <form id="happyForm">
    <h5 class="section-header">ข้อมูลทั่วไป</h5>
    <div class="card p-4">
      <div class="row g-3">
        <div class="col-md-4"><label class="required">เพศ</label>
          <select class="form-select" name="เพศ" required><option value="">เลือก</option><option>ชาย</option><option>หญิง</option></select>
        </div>
        <div class="col-md-4"><label class="required">อายุ (ปี)</label>
          <input type="number" class="form-control" name="อายุ" required>
        </div>
        <div class="col-md-4"><label class="required">สถานภาพ</label>
          <select class="form-select" name="สถานภาพ" required><option value="">เลือก</option><option>โสด</option><option>สมรส</option><option>หย่าร้าง/แยกกันอยู่</option></select>
        </div>
        <div class="col-md-4"><label class="required">ศาสนา</label>
          <select class="form-select" name="ศาสนา" required><option value="">เลือก</option><option>พุทธ</option><option>คริสต์</option><option>อิสลาม</option><option>อื่นๆ</option></select>
        </div>
        <div class="col-md-4"><label class="required">ระดับการศึกษา</label>
          <select class="form-select" name="ระดับการศึกษา" required><option value="">เลือก</option><option>ต่ำกว่าปริญญาตรี</option><option>ปริญญาตรี</option><option>สูงกว่าปริญญาตรี</option></select>
        </div>
        <div class="col-md-4"><label class="required">อายุงาน (ปี)</label>
          <input type="number" class="form-control" name="อายุงาน" step="0.1" required>
        </div>
        <div class="col-md-12"><label class="required">ระดับตำแหน่งงาน</label>
          <select class="form-select" name="ระดับตำแหน่งงาน" required>
            <option value="">เลือกระดับตำแหน่ง</option>
            <option>Staff - Head Staff</option><option>Associate - Professional</option>
            <option>Specialist - Sr. Specialist</option><option>ADM - AHO</option>
          </select>
        </div>
      </div>
    </div>

    <h5 class="section-header">ส่วนที่ 1: แบบประเมินสิ่งที่ท่านรู้สึก (38 ข้อ)</h5>
    <div class="card" id="part1"></div>

    <h5 class="section-header">ส่วนที่ 2: แบบประเมินสิ่งที่ท่านได้รับจากบริษัทฯ (16 ข้อ)</h5>
    <div class="card" id="part2"></div>

    <div class="text-center mt-5">
      <button type="submit" class="btn btn-success btn-submit shadow">ส่งแบบสอบถาม</button>
    </div>
  </form>
</div>

<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
<script>
  const p1 = ["ท่านเห็นว่าตนเองมีอะไรหลายอย่างที่น่าภาคภูมิใจ", "ท่านคิดว่าชีวิตของท่านมีคุณค่า", "ท่านรู้ว่าอะไรคือคุณค่าที่แท้จริงของชีวิต", "ท่านเข้าใจว่าอะไรคือแก่นธรรมของศาสนา", "ท่านให้ความเป็นมิตรกับผู้อื่น", "ท่านให้ความสำคัญต่อความรู้สึกและความต้องการของผู้อื่น", "ท่านปรารถนาอยากจะช่วยให้ผู้อื่นพ้นความทุกข์", "ท่านเห็นความสำคัญกับการได้ช่วยเหลือผู้อื่น", "ท่านเข้าใจว่าตนเองเป็นส่วนหนึ่งและมีความสัมพันธ์เชื่อมโยงกับธรรมชาติ", "ท่านรู้สึกรักในธรรมชาติ", "ท่านได้ใช้ศักยภาพอย่างเต็มที่ ในการทำงานและดำเนินชีวิตอยู่", "ท่านทำสิ่งที่ท่านสนใจหรือให้คุณค่า แม้ว่าสิ่งนั้นจะเป็นสิ่งที่ยาก", "ท่านตั้งใจรับฟังคนที่พูดกับท่านได้จนจบ โดยไม่ตัดสินหรือพูดแทรกขึ้นมา", "ท่านแบ่งเวลาไปทำประโยชน์ให้ผู้อื่นโดยไม่ได้รับสิ่งตอบแทน", "ท่านรู้และตามทันอารมณ์ในใจของตนเอง ก่อนที่จะแสดงมันออกมา", "ท่านควบคุมอารมณ์ของตนเองได้ ก่อนที่จะแสดงออกมา", "ท่านสามารถน้อมรับฟังความคิดเห็น หรือคำวิจารณ์จากผู้อื่นได้", "ท่านให้อภัยตนเองได้", "ท่านยอมรับข้อดีและข้อด้อยของตัวเองโดยไม่ปฏิเสธมัน", "ท่านรู้สึกแจ่มใสเบิกบานในชีวิต", "โดยทั่วไปท่านมีความรู้สึกผ่อนคลาย สบายใจ", "ท่านรับรู้คุณค่าในชีวิตของท่านและดำเนินชีวิตเพื่อสิ่งนั้น", "ท่านทำงานโดยเอาคุณค่าของงานเป็นตัวจูงใจ ไม่ใช่เงินทองหรือสิ่งที่จะได้รับเป็นการตอบแทน", "ท่านรับรู้และยอมรับในข้อดีและข้อด้อยของผู้อื่นได้ด้วยความเข้าใจ", "ท่านรู้สึกชื่นชมและขอบคุณในความดีของผู้อื่นและสรรพสิ่งรอบตัว", "ท่านมีความเข้าอกเข้าใจในความรู้สึกของผู้อื่นได้ แม้ว่าท่านจะไม่เห็นด้วยกับสิ่งที่คนๆ นั้น", "ท่านเห็นคุณค่าในตัวเองอย่างที่ท่านเป็น", "ท่านให้อภัยในความผิดพลาดของตนเองได้", "ท่านให้อภัยในความผิดพลาดของผู้อื่นได้", "ท่านพร้อมเสมอที่จะเสียสละส่วนตนเพื่อประโยชน์ของส่วนรวม", "ท่านหมั่นพัฒนาความรักความเมตตาต่อผู้อื่นให้เพิ่มมากขึ้น", "ท่านมีเพื่อนหรือมีกลุ่มที่มีความสัมพันธ์ที่ดีต่อกัน", "ท่านมีเพื่อนหรือมีผู้ที่ท่านไว้ใจที่สามารถบอกกล่าวความรู้สึกลึกๆ ในใจแก่กันได้", "ท่านอ่านหนังสือหรือรับฟังคำสอนที่เกี่ยวข้องกับหลักคุณงามความดีหรือหลักศาสนา", "ท่านหาโอกาสทำสิ่งต่างๆ ที่เอื้ออำนวยให้เกิดประโยชน์แก่ผู้อื่น", "ท่านหาเวลาที่จะอยู่ใกล้ชิดกับธรรมชาติ เช่น ต้นไม้ใบหญ้า ท้องฟ้า สรรพสัตว์ต่างๆ", "ท่านรับรู้และยอมรับความทุกข์ในชีวิต และทำความเข้าใจกับมัน", "ท่านเป็นส่วนหนึ่งของกิจกรรมสร้างสรรค์สังคมที่เป็นธรรม หรือสิ่งแวดล้อมที่ปลอดภัย"];
  const p2 = ["บริษัทสนับสนุนความก้าวหน้าในสายอาชีพ", "ระบบการสื่อสารภายในบริษัทมีความชัดเจน", "สวัสดิการของบริษัทครอบคลุมความต้องการ", "หัวหน้างานให้การสนับสนุนและคำปรึกษาที่ดี", "บรรยากาศการทำงานส่งเสริมความร่วมมือ", "บริษัทให้ความสำคัญกับความสมดุลชีวิตและการทำงาน", "มีการยกย่องชมเชยเมื่อทำผลงานได้ดี", "บริษัทจัดกิจกรรมสร้างความสัมพันธ์ที่น่าสนใจ", "สภาพแวดล้อมในที่ทำงานมีความปลอดภัยและเหมาะสม", "อุปกรณ์และเครื่องมือทำงานมีความพร้อม", "นโยบายบริษัทมีความเป็นธรรมและโปร่งใส", "บริษัทรับฟังความคิดเห็นของพนักงาน", "เงินเดือนและค่าตอบแทนมีความเหมาะสม", "บริษัทมีเป้าหมายการดำเนินงานที่ชัดเจน", "เพื่อนร่วมงานมีความเป็นมิตรและช่วยเหลือกัน", "ภาพรวมของบริษัททำให้ท่านมีความสุขในการทำงาน"];

  function render(qs, target, prefix) {
    const el = document.getElementById(target);
    qs.forEach((q, i) => {
      const html = `
        <div class="question-item">
          <p class="mb-2 fw-bold text-secondary">${i + 1}. ${q}</p>
          <div class="rating-btn-group">
            ${[1, 2, 3, 4, 5].map(v => `
              <div class="flex-fill">
                <input type="radio" class="btn-check" name="${prefix}_${i+1}" id="${prefix}_${i+1}_${v}" value="${v}" required>
                <label class="btn btn-outline-success w-100 py-2" for="${prefix}_${i+1}_${v}">${v}</label>
              </div>
            `).join('')}
          </div>
        </div>`;
      el.insertAdjacentHTML('beforeend', html);
    });
  }

  render(p1, 'part1', 'Feel');
  render(p2, 'part2', 'Corp');

  document.getElementById('happyForm').onsubmit = function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const obj = Object.fromEntries(formData.entries());
    
    // ส่งข้อมูลกลับไปที่ Streamlit ผ่าน Window Parent
    window.parent.postMessage({
        type: 'streamlit:set_component_value',
        value: obj
    }, '*');
    
    Swal.fire('ขอบคุณครับ!', 'ส่งข้อมูลเรียบร้อยแล้ว', 'success').then(() => {
        window.location.reload();
    });
  };
</script>
</body>
</html>
"""

# แสดงผล HTML ใน Streamlit
# สังเกตว่าเราใช้ height เยอะหน่อยเพื่อให้ครอบคลุมแบบสอบถามทั้งหมด
result = st.components.v1.html(html_code, height=6000, scrolling=False)

# ถ้าได้รับข้อมูลจาก HTML (ตอนกด Submit)
if result:
    save_data(result)
    st.toast("บันทึกข้อมูลสำเร็จ!", icon="✅")

# --- ปุ่ม Admin (ใช้ Password ล็อคไว้) ---
with st.expander("🔐 Admin Panel"):
    if st.text_input("Password", type="password") == "1234":
        if os.path.isfile("survey_responses.csv"):
            df = pd.read_csv("survey_responses.csv")
            st.write(f"จำนวนผู้ตอบ: {len(df)} คน")
            st.download_button("Download CSV", data=df.to_csv(index=False).encode('utf-8-sig'), file_name="results.csv")
