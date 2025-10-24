import streamlit as st
import pandas as pd
import random

# --- Page config ---
st.set_page_config(page_title="Digital Citizen Hub", page_icon="🌐", layout="wide")

# --- CSS Styling ---
st.markdown("""
<style>
body {background-color: #f7f9fc;}
h1, h2, h3 {color: #003566; font-weight: 700;}
.card {background-color: white; border-radius: 12px; padding: 20px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.08); margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

# --- Language selector ---
lang = st.sidebar.radio("🌐 Choose Language / زبان منتخب کریں", ["English", "اردو"])

# --- Text dictionary ---
text = {
    "English": {
        "home": "Home",
        "submit": "Submit Complaint",
        "track": "Track Complaint",
        "dashboard": "Dashboard",
        "title": "Digital Citizen Hub – Balochistan",
        "subtitle": "AI-powered platform transforming governance.",
        "mission": "Automating complaints, tracking status, and enhancing transparency in government services.",
        "submit_title": "Submit a Complaint",
        "name": "Full Name",
        "category": "Complaint Type",
        "description": "Describe your issue",
        "image": "Upload an optional image",
        "submit_btn": "Submit Complaint",
        "success": "Your complaint has been submitted!",
        "track_title": "Track Your Complaint",
        "track_input": "Enter your Complaint ID",
        "track_btn": "Check Status",
        "dashboard_title": "Transparency Dashboard",
        "dashboard_desc": "Overview of complaints in the system.",
        "footer": "Empowering governance through AI and transparency 🇵🇰",
        "resolved_btn": "Mark as Resolved"
    },
    "اردو": {
        "home": "ہوم",
        "submit": "شکایت درج کریں",
        "track": "شکایت ٹریک کریں",
        "dashboard": "ڈیش بورڈ",
        "title": "ڈیجیٹل سٹیزن حب – بلوچستان",
        "subtitle": "بلوچستان میں گورننس کو بہتر بنانے کے لیے مصنوعی ذہانت سے چلنے والا پلیٹ فارم۔",
        "mission": "شکایات کو خودکار کرنا، ان کی حالت ٹریک کرنا اور سرکاری خدمات میں شفافیت بڑھانا۔",
        "submit_title": "شکایت درج کریں",
        "name": "نام",
        "category": "شکایت کی قسم",
        "description": "مسئلہ بیان کریں",
        "image": "اختیاری تصویر اپ لوڈ کریں",
        "submit_btn": "شکایت جمع کریں",
        "success": "آپ کی شکایت موصول ہو گئی!",
        "track_title": "شکایت ٹریک کریں",
        "track_input": "اپنی شکایت کی آئی ڈی درج کریں",
        "track_btn": "حالت چیک کریں",
        "dashboard_title": "شفافیت کا ڈیش بورڈ",
        "dashboard_desc": "سسٹم میں شکایات کا جائزہ۔",
        "footer": "مصنوعی ذہانت اور شفافیت کے ذریعے گورننس کو مضبوط بنانا 🇵🇰",
        "resolved_btn": "حل شدہ نشان زد کریں"
    }
}

# --- Sidebar Navigation ---
page = st.sidebar.radio("Navigate", 
                        [text[lang]["home"], text[lang]["submit"], text[lang]["track"], text[lang]["dashboard"]])

# --- Initialize session state ---
if "complaints" not in st.session_state:
    st.session_state.complaints = []

# --- Department mapping ---
department_mapping = {
    "Electricity": "QESCO",
    "Water": "Water Board",
    "Health": "Health Dept",
    "Roads": "Public Works",
    "بجلی": "قیسکوا",
    "پانی": "واٹر بورڈ",
    "صحت": "ہیلتھ ڈیپارٹمنٹ",
    "سڑکیں": "پبلک ورکس"
}

# --- Priority mapping ---
priority_levels = ["Low", "Medium", "High"]
priority_badges = {"Low": "Low", "Medium": "Medium", "High": "High"}
priority_badges_urdu = {"Low": "کم", "Medium": "درمیانہ", "High": "زیادہ"}

# --- Status mapping ---
status_badges = {"Pending": "Pending", "Resolved": "Resolved"}
status_badges_urdu = {"زیرِ کارروائی": "زیرِ کارروائی", "حل شدہ": "حل شدہ"}

# --- HOME PAGE ---
if page == text[lang]["home"]:
    st.title(text[lang]["title"])
    st.subheader(text[lang]["subtitle"])
    st.info(text[lang]["mission"])

# --- SUBMIT COMPLAINT ---
elif page == text[lang]["submit"]:
    st.header(text[lang]["submit_title"])
    with st.form("complaint_form"):
        name = st.text_input(text[lang]["name"])
        category = st.selectbox(
            text[lang]["category"], 
            ["Electricity","Water","Health","Roads"] if lang=="English" else ["بجلی","پانی","صحت","سڑکیں"]
        )
        description = st.text_area(text[lang]["description"], height=120)
        uploaded_file = st.file_uploader(text[lang]["image"], type=["png","jpg","jpeg"])
        submitted = st.form_submit_button(text[lang]["submit_btn"])
        if submitted and name and description:
            tracking_id = random.randint(1000,9999)
            assigned_dept = department_mapping[category]
            priority = random.choices(priority_levels, weights=[0.5,0.3,0.2])[0]
            status = "Pending" if lang=="English" else "زیرِ کارروائی"
            st.session_state.complaints.append({
                "ID": tracking_id,
                "Name": name,
                "Category": category,
                "Department": assigned_dept,
                "Priority": priority,
                "Status": status
            })
            priority_display = priority_badges[priority] if lang=="English" else priority_badges_urdu[priority]
            st.markdown(f"✅ {text[lang]['success']} #{tracking_id}<br>Assigned Dept: {assigned_dept}<br>Priority: {priority_display}", unsafe_allow_html=True)
        elif submitted:
            st.warning("⚠️ Please fill all fields!" if lang=="English" else "⚠️ تمام خانے پُر کریں!")

# --- TRACK COMPLAINT ---
elif page == text[lang]["track"]:
    st.header(text[lang]["track_title"])
    complaint_id = st.text_input(text[lang]["track_input"])
    if st.button(text[lang]["track_btn"]):
        if complaint_id.strip():
            try:
                cid = int(complaint_id.strip())
                found = next((c for c in st.session_state.complaints if c["ID"] == cid), None)
            except ValueError:
                found = None
            if found:
                status_display = status_badges.get(found["Status"], found["Status"]) if lang=="English" else status_badges_urdu.get(found["Status"], found["Status"])
                priority_display = priority_badges.get(found["Priority"], found["Priority"]) if lang=="English" else priority_badges_urdu.get(found["Priority"], found["Priority"])
                st.markdown(f"**Complaint ID:** {found['ID']}<br>Status: {status_display}<br>Department: {found['Department']}<br>Priority: {priority_display}", unsafe_allow_html=True)
                if st.button(text[lang]["resolved_btn"]):
                    found["Status"] = "Resolved" if lang=="English" else "حل شدہ"
                    st.success("✅ Status updated!" if lang=="English" else "✅ حالت اپڈیٹ ہو گئی!")
            else:
                st.warning("❌ Complaint not found!" if lang=="English" else "❌ شکایت موجود نہیں!")
        else:
            st.warning("⚠️ Enter a valid ID!" if lang=="English" else "⚠️ درست آئی ڈی درج کریں!")

# --- DASHBOARD ---
elif page == text[lang]["dashboard"]:
    st.header(text[lang]["dashboard_title"])
    st.write(text[lang]["dashboard_desc"])
    if st.session_state.complaints:
        df = pd.DataFrame(st.session_state.complaints)
        df_display = df.copy()
        df_display["Priority"] = df_display["Priority"].apply(lambda x: priority_badges.get(x,x) if lang=="English" else priority_badges_urdu.get(x,x))
        df_display["Status"] = df_display["Status"].apply(lambda x: status_badges.get(x,x) if lang=="English" else status_badges_urdu.get(x,x))
        st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
        total = len(df)
        resolved = len([c for c in df["Status"] if c=="Resolved" or c=="حل شدہ"])
        pending = total - resolved
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Complaints" if lang=="English" else "کل شکایات", total)
        col2.metric("Resolved" if lang=="English" else "حل شدہ", resolved)
        col3.metric("Pending" if lang=="English" else "زیرِ کارروائی", pending)
    else:
        st.info("No complaints submitted yet." if lang=="English" else "ابھی کوئی شکایت درج نہیں ہوئی۔")

st.write("---")
st.markdown(f"**{text[lang]['footer']}**")
