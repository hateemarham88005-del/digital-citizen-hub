import streamlit as st
import pandas as pd
import random

# --- Page config ---
st.set_page_config(page_title="Digital Citizen Hub", page_icon="🌐", layout="wide")

# --- CSS styling ---
st.markdown("""
<style>
body {background-color: #f7f9fc;}
h1, h2, h3 {color: #003566; font-weight: 700;}
.card {
    background-color: white; border-radius: 12px; padding: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08); margin-bottom: 15px;
}
.status-resolved {color: green; font-weight: bold;}
.status-pending {color: orange; font-weight: bold;}
.status-urgent {color: red; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# --- Language selector ---
lang = st.sidebar.radio("🌐 Choose Language / زبان منتخب کریں", ["English", "اردو"])

# --- Sidebar navigation text ---
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
        "success": "✅ Your complaint has been submitted! Tracking ID:",
        "track_title": "Track Your Complaint",
        "track_input": "Enter your Complaint ID",
        "track_btn": "Check Status",
        "dashboard_title": "Transparency Dashboard",
        "dashboard_desc": "Overview of complaints in the system.",
        "footer": "Empowering governance through AI and transparency 🇵🇰"
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
        "success": "✅ آپ کی شکایت موصول ہو گئی! ٹریکنگ آئی ڈی:",
        "track_title": "شکایت ٹریک کریں",
        "track_input": "اپنی شکایت کی آئی ڈی درج کریں",
        "track_btn": "حالت چیک کریں",
        "dashboard_title": "شفافیت کا ڈیش بورڈ",
        "dashboard_desc": "سسٹم میں شکایات کا جائزہ۔",
        "footer": "مصنوعی ذہانت اور شفافیت کے ذریعے گورننس کو مضبوط بنانا 🇵🇰"
    }
}

# --- Sidebar navigation ---
page = st.sidebar.radio("Navigate", 
                        [text[lang]["home"], text[lang]["submit"], text[lang]["track"], text[lang]["dashboard"]])

# --- Initialize session state for complaints ---
if "complaints" not in st.session_state:
    st.session_state.complaints = []

# --- Department mapping ---
department_mapping = {
    "Electricity": "QESCO",
    "Water": "Water Board",
    "Health": "Health Dept",
    "Roads": "Public Works",
    # Urdu
    "بجلی": "قیسکوا",
    "پانی": "واٹر بورڈ",
    "صحت": "ہیلتھ ڈیپارٹمنٹ",
    "سڑکیں": "پبلک ورکس"
}

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
            # Add complaint to session state
            st.session_state.complaints.append({
                "ID": tracking_id,
                "Name": name,
                "Category": category,
                "Department": assigned_dept,
                "Status": "Pending" if lang=="English" else "زیرِ کارروائی"
            })
            st.success(f"{text[lang]['success']} #{tracking_id}\nAssigned to: {assigned_dept}")
        elif submitted:
            st.warning("⚠️ Please fill all fields!" if lang=="English" else "⚠️ تمام خانے پُر کریں!")

# --- TRACK COMPLAINT ---
elif page == text[lang]["track"]:
    st.header(text[lang]["track_title"])
    complaint_id = st.text_input(text[lang]["track_input"])
    if st.button(text[lang]["track_btn"]):
        if complaint_id.strip():
            found = None
            for c in st.session_state.complaints:
                if str(c["ID"]) == complaint_id.strip():
                    found = c
                    break
            if found:
                st.success(f"✅ Complaint ID {found['ID']} - Status: {found['Status']}\nAssigned Dept: {found['Department']}")
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
        # Color-coded status
        def color_status(status):
            if status in ["Resolved","حل شدہ"]: return "✅ Resolved" if lang=="English" else "✅ حل شدہ"
            elif status in ["Pending","زیرِ کارروائی"]: return "🕓 Pending" if lang=="English" else "🕓 زیرِ کارروائی"
            else: return status
        df["Status"] = df["Status"].apply(color_status)
        st.table(df)
        # Metrics
        total = len(st.session_state.complaints)
        resolved = len([c for c in st.session_state.complaints if c["Status"].startswith("✅")])
        pending = total - resolved
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Complaints" if lang=="English" else "کل شکایات", total)
        col2.metric("Resolved" if lang=="English" else "حل شدہ", resolved)
        col3.metric("Pending" if lang=="English" else "زیرِ کارروائی", pending)
    else:
        st.info("No complaints submitted yet." if lang=="English" else "ابھی کوئی شکایت درج نہیں ہوئی۔")

st.write("---")
st.markdown(f"**{text[lang]['footer']}**")
