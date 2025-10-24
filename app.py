import streamlit as st
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="Digital Citizen Hub", page_icon="🌐", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
.main-title {
    font-size: 36px; font-weight: 700; color: #003566; text-align: center; margin-bottom: 5px;
}
.subtitle {
    text-align: center; color: #555; font-size: 18px; margin-bottom: 25px;
}
.card {
    background-color: #f9f9f9; border-radius: 12px; padding: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# --- LANGUAGE SELECTOR ---
lang = st.sidebar.radio("🌐 Choose Language / زبان منتخب کریں", ["English", "اردو"])

# --- PAGE SELECTOR ---
page = st.sidebar.radio(
    "📑 Navigate",
    ["Submit Complaint" if lang == "English" else "شکایت درج کریں",
     "Track Complaint" if lang == "English" else "شکایت ٹریک کریں",
     "Dashboard" if lang == "English" else "ڈیش بورڈ"]
)

# --- TRANSLATION DATA ---
text = {
    "English": {
        "title": "Digital Citizen Hub",
        "subtitle": "AI-powered platform transforming governance in Balochistan.",
        "submit_title": "Submit a Complaint",
        "submit_desc": "Fill out the form below to report an issue. AI will categorize and route your complaint automatically.",
        "name": "Full Name",
        "category": "Complaint Type",
        "description": "Describe your issue",
        "submit_btn": "Submit Complaint",
        "success": "✅ Your complaint has been submitted! Tracking ID:",
        "track_title": "Track Your Complaint",
        "track_input": "Enter your Complaint ID",
        "track_btn": "Check Status",
        "status_result": "Your complaint is currently being processed by the relevant department.",
        "dashboard_title": "Transparency Dashboard",
        "dashboard_desc": "Real-time summary of complaints and resolutions.",
        "footer": "Empowering governance through AI and transparency 🇵🇰"
    },
    "اردو": {
        "title": "ڈیجیٹل سٹیزن حب",
        "subtitle": "بلوچستان میں گورننس کو بہتر بنانے کے لیے مصنوعی ذہانت سے چلنے والا پلیٹ فارم۔",
        "submit_title": "شکایت درج کریں",
        "submit_desc": "مسئلہ رپورٹ کرنے کے لیے نیچے دیا گیا فارم پُر کریں۔ مصنوعی ذہانت آپ کی شکایت کو خودکار طور پر درجہ بند کرے گی۔",
        "name": "نام",
        "category": "شکایت کی قسم",
        "description": "مسئلہ بیان کریں",
        "submit_btn": "شکایت جمع کریں",
        "success": "✅ آپ کی شکایت موصول ہو گئی ہے! ٹریکنگ آئی ڈی:",
        "track_title": "شکایت ٹریک کریں",
        "track_input": "اپنی شکایت کی آئی ڈی درج کریں",
        "track_btn": "حالت چیک کریں",
        "status_result": "آپ کی شکایت متعلقہ محکمے میں زیرِ کارروائی ہے۔",
        "dashboard_title": "شفافیت کا ڈیش بورڈ",
        "dashboard_desc": "شکایات اور ان کے حل کی حقیقی وقت کی رپورٹ۔",
        "footer": "مصنوعی ذہانت اور شفافیت کے ذریعے گورننس کو مضبوط بنانا 🇵🇰"
    }
}

# --- PAGE CONTENT ---
st.markdown(f"<h1 class='main-title'>{text[lang]['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>{text[lang]['subtitle']}</p>", unsafe_allow_html=True)
st.write("---")

# 📝 Submit Complaint Page
if page.startswith("Submit") or page.startswith("شکایت"):
    st.header(text[lang]["submit_title"])
    st.write(text[lang]["submit_desc"])
    st.write("")

    with st.form("complaint_form"):
        name = st.text_input(text[lang]["name"])
        category = st.selectbox(
            text[lang]["category"],
            ["Electricity", "Water", "Health", "Education", "Roads"] if lang == "English"
            else ["بجلی", "پانی", "صحت", "تعلیم", "سڑکیں"]
        )
        description = st.text_area(text[lang]["description"], height=120)
        submitted = st.form_submit_button(text[lang]["submit_btn"])

        if submitted and name and description:
            complaint_id = random.randint(1000, 9999)
            st.success(f"{text[lang]['success']} #{complaint_id}")
        elif submitted:
            st.warning("⚠️ Please fill in all fields!" if lang == "English" else "⚠️ تمام خانے پُر کریں!")

# 🔍 Track Complaint Page
elif page.startswith("Track") or page.startswith("ٹریک"):
    st.header(text[lang]["track_title"])
    complaint_id = st.text_input(text[lang]["track_input"])
    if st.button(text[lang]["track_btn"]):
        if complaint_id.strip():
            st.info(f"🕓 {text[lang]['status_result']}")
        else:
            st.warning("⚠️ Enter a valid ID!" if lang == "English" else "⚠️ درست آئی ڈی درج کریں!")

# 📊 Dashboard Page
else:
    st.header(text[lang]["dashboard_title"])
    st.write(text[lang]["dashboard_desc"])
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Complaints" if lang == "English" else "کل شکایات", "1,245")
    col2.metric("Resolved" if lang == "English" else "حل شدہ", "982")
    col3.metric("Pending" if lang == "English" else "زیرِ کارروائی", "263")

    st.write("---")
    st.markdown(f"### {text[lang]['footer']}")
