import streamlit as st
import pandas as pd
import random
import plotly.express as px

# --- Page config ---
st.set_page_config(page_title="Digital Citizen Hub", page_icon="🌐", layout="wide")

# --- CSS Styling ---
st.markdown("""
<style>
body {background-color: #f7f9fc;}
h1, h2, h3 {color: #003566; font-weight: 700;}
.card {background-color: white; border-radius: 12px; padding: 20px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.08); margin-bottom: 15px;}
.status-high {color: red; font-weight: bold;}
.status-medium {color: orange; font-weight: bold;}
.status-low {color: green; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# --- Language Selector ---
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
    # Urdu
    "بجلی": "قیسکوا",
    "پانی": "واٹر بورڈ",
    "صحت": "ہیلتھ ڈیپارٹمنٹ",
    "سڑکیں": "پبلک ورکس"
}

# --- Priority levels ---
priority_levels = ["Low", "Medium", "High"]
priority_colors = {"Low":"🟢 Low", "Medium":"🟠 Medium", "High":"🔴 High"}
priority_colors_urdu = {"Low":"🟢 کم","Medium":"🟠 درمیانہ","High":"🔴 زیادہ"}

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
            # Simulate priority
            priority = random.choices(priority_levels, weights=[0.5,0.3,0.2])[0]
            st.session_state.complaints.append({
                "ID": tracking_id,
                "Name": name,
                "Category": category,
                "Department": assigned_dept,
                "Priority": priority,
                "Status": "Pending" if lang=="English" else "زیرِ کارروائی"
            })
            priority_display = priority_colors[priority] if lang=="English" else priority_colors_urdu[priority]
            st.success(f"{text[lang]['success']} #{tracking_id}\nAssigned to: {assigned_dept}\nPriority: {priority_display}")
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
                status_display = "✅ Resolved" if found["Status"]=="Resolved" else "🕓 Pending" if lang=="English" else "🕓 زیرِ کارروائی"
                priority_display = priority_colors[found["Priority"]] if lang=="English" else priority_colors_urdu[found["Priority"]]
                st.success(f"Complaint ID {found['ID']}\nStatus: {status_display}\nAssigned Dept: {found['Department']}\nPriority: {priority_display}")
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
        # Display priority with colors
        df_display = df.copy()
        df_display["Priority"] = df_display["Priority"].apply(lambda x: priority_colors[x] if lang=="English" else priority_colors_urdu[x])
        st.table(df_display)
        # Metrics
        total = len(df)
        resolved = len([c for c in df["Status"] if c=="Resolved"])
        pending = total - resolved
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Complaints" if lang=="English" else "کل شکایات", total)
        col2.metric("Resolved" if lang=="English" else "حل شدہ", resolved)
        col3.metric("Pending" if lang=="English" else "زیرِ کارروائی", pending)
        # --- Charts ---
        # Complaints by Department
        fig1 = px.pie(df, names="Department", title="Complaints by Department" if lang=="English" else "محکمہ کے لحاظ سے شکایات")
        st.plotly_chart(fig1, use_container_width=True)
        # Complaints by Priority
        fig2 = px.bar(df, x="Priority", y=[1]*len(df), color="Priority", title="Complaints by Priority" if lang=="English" else "ترجیحات کے لحاظ سے شکایات")
        st.plotly_chart(fig2, use_container_width=True)
        # --- Simulated AI insights ---
        top_cat = df["Category"].value_counts().idxmax()
        st.info(f"🚨 Most complaints in: {top_cat}" if lang=="English" else f"🚨 سب سے زیادہ شکایات: {top_cat}")
    else:
        st.info("No complaints submitted yet." if lang=="English" else "ابھی کوئی شکایت درج نہیں ہوئی۔")

st.write("---")
st.markdown(f"**{text[lang]['footer']}**")
