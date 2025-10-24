import streamlit as st
import pandas as pd
import random
import os

# --- Page config ---
st.set_page_config(page_title="Digital Citizen Hub", page_icon="🌐", layout="wide")

# --- File to store complaints ---
DATA_FILE = "complaints.csv"

# --- Load complaints ---
if os.path.exists(DATA_FILE):
    complaints_df = pd.read_csv(DATA_FILE)
else:
    complaints_df = pd.DataFrame(columns=["ID","Name","Category","Department","Priority","Status","Description"])

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
        "home":"Home", "submit":"Submit Complaint","track":"Track Complaint","dashboard":"Dashboard","chatbot":"Chatbot",
        "title":"Digital Citizen Hub – Balochistan","subtitle":"AI-powered platform transforming governance.",
        "mission":"Automating complaints, tracking status, and enhancing transparency in government services.",
        "submit_title":"Submit a Complaint","name":"Full Name","category":"Complaint Type","description":"Describe your issue",
        "image":"Upload an optional image","submit_btn":"Submit Complaint","success":"✅ Your complaint has been submitted! Tracking ID:",
        "track_title":"Track Your Complaint","track_input":"Enter your Complaint ID","track_btn":"Check Status",
        "dashboard_title":"Transparency Dashboard","dashboard_desc":"Overview of complaints in the system.",
        "footer":"Empowering governance through AI and transparency 🇵🇰","resolved_btn":"Mark as Resolved",
        "priority":"Priority","status":"Status","department":"Department"
    },
    "اردو": {
        "home":"ہوم","submit":"شکایت درج کریں","track":"شکایت ٹریک کریں","dashboard":"ڈیش بورڈ","chatbot":"چیٹ بوٹ",
        "title":"ڈیجیٹل سٹیزن حب – بلوچستان","subtitle":"بلوچستان میں گورننس کو بہتر بنانے کے لیے مصنوعی ذہانت سے چلنے والا پلیٹ فارم۔",
        "mission":"شکایات کو خودکار کرنا، ان کی حالت ٹریک کرنا اور سرکاری خدمات میں شفافیت بڑھانا۔",
        "submit_title":"شکایت درج کریں","name":"نام","category":"شکایت کی قسم","description":"مسئلہ بیان کریں",
        "image":"اختیاری تصویر اپ لوڈ کریں","submit_btn":"شکایت جمع کریں","success":"✅ آپ کی شکایت موصول ہو گئی! ٹریکنگ آئی ڈی:",
        "track_title":"شکایت ٹریک کریں","track_input":"اپنی شکایت کی آئی ڈی درج کریں","track_btn":"حالت چیک کریں",
        "dashboard_title":"شفافیت کا ڈیش بورڈ","dashboard_desc":"سسٹم میں شکایات کا جائزہ۔",
        "footer":"مصنوعی ذہانت اور شفافیت کے ذریعے گورننس کو مضبوط بنانا 🇵🇰","resolved_btn":"حل شدہ نشان زد کریں",
        "priority":"اہمیت","status":"حالت","department":"ڈیپارٹمنٹ"
    }
}

# --- Sidebar Navigation ---
page = st.sidebar.radio("Navigate", 
                        [text[lang]["home"], text[lang]["submit"], text[lang]["track"], text[lang]["dashboard"], text[lang]["chatbot"]])

# --- Department mapping ---
department_mapping = {
    "Electricity":"QESCO","Water":"Water Board","Health":"Health Dept","Roads":"Public Works",
    "بجلی":"قیسکوا","پانی":"واٹر بورڈ","صحت":"ہیلتھ ڈیپارٹمنٹ","سڑکیں":"پبلک ورکس"
}

# --- Priority keywords ---
priority_keywords = {"High":["urgent","power cut","flood","fire"],"Medium":["delay","broken","slow"],"Low":["minor","small","cosmetic"]}

# --- MAIN NAVIGATION ---
if page == text[lang]["home"]:
    st.title(text[lang]["title"])
    st.subheader(text[lang]["subtitle"])
    st.info(text[lang]["mission"])

elif page == text[lang]["submit"]:
    st.header(text[lang]["submit_title"])
    with st.form("complaint_form"):
        name = st.text_input(text[lang]["name"])
        category = st.selectbox(text[lang]["category"], ["Electricity","Water","Health","Roads"] if lang=="English" else ["بجلی","پانی","صحت","سڑکیں"])
        description = st.text_area(text[lang]["description"], height=120)
        submitted = st.form_submit_button(text[lang]["submit_btn"])
        if submitted and name and description:
            tracking_id = random.randint(1000,9999)
            dept = department_mapping[category]
            text_lower = description.lower()
            priority = "Low"
            for level, words in priority_keywords.items():
                for word in words:
                    if word in text_lower:
                        priority = level
                        break
            status = "Pending" if lang=="English" else "زیرِ کارروائی"
            complaints_df = pd.concat([complaints_df, pd.DataFrame([{
                "ID":tracking_id,"Name":name,"Category":category,"Department":dept,
                "Priority":priority,"Status":status,"Description":description
            }])], ignore_index=True)
            complaints_df.to_csv(DATA_FILE,index=False)
            st.success(f"{text[lang]['success']} #{tracking_id}\n{text[lang]['department']}: {dept}\n{text[lang]['priority']}: {priority}")
        elif submitted:
            st.warning("⚠️ Please fill all fields!" if lang=="English" else "⚠️ تمام خانے پُر کریں!")

elif page == text[lang]["track"]:
    st.header(text[lang]["track_title"])
    complaint_id = st.text_input(text[lang]["track_input"])
    if st.button(text[lang]["track_btn"]):
        if complaint_id.strip():
            try:
                cid = int(complaint_id.strip())
                found = complaints_df[complaints_df["ID"]==cid]
            except ValueError:
                found = pd.DataFrame()
            if not found.empty:
                st.success(f"{text[lang]['department']}: {found.iloc[0]['Department']}\n{text[lang]['status']}: {found.iloc[0]['Status']}\n{text[lang]['priority']}: {found.iloc[0]['Priority']}\nDescription: {found.iloc[0]['Description']}")
            else:
                st.warning("❌ Complaint not found!" if lang=="English" else "❌ شکایت موجود نہیں!")
        else:
            st.warning("⚠️ Enter a valid ID!" if lang=="English" else "⚠️ درست آئی ڈی درج کریں!")

elif page == text[lang]["dashboard"]:
    st.header(text[lang]["dashboard_title"])
    st.write(text[lang]["dashboard_desc"])
    if not complaints_df.empty:
        st.dataframe(complaints_df)
        total = len(complaints_df)
        resolved = len(complaints_df[complaints_df["Status"]=="Resolved"])
        pending = total - resolved
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Complaints" if lang=="English" else "کل شکایات", total)
        col2.metric("Resolved" if lang=="English" else "حل شدہ", resolved)
        col3.metric("Pending" if lang=="English" else "زیرِ کارروائی", pending)

        st.subheader("Admin: Resolve Complaint" if lang=="English" else "ایڈمن: شکایت حل کریں")
        resolve_id = st.number_input("Enter Complaint ID to resolve" if lang=="English" else "حل کرنے کے لیے شکایت کی آئی ڈی درج کریں", min_value=0, step=1)
        if st.button(text[lang]["resolved_btn"]):
            idx = complaints_df[complaints_df["ID"]==resolve_id].index
            if len(idx)>0:
                complaints_df.at[idx[0],"Status"]="Resolved"
                complaints_df.to_csv(DATA_FILE,index=False)
                st.success(f"Complaint #{resolve_id} marked as Resolved ✅")
            else:
                st.warning("Complaint not found!" if lang=="English" else "شکایت موجود نہیں!")
    else:
        st.info("No complaints submitted yet." if lang=="English" else "ابھی کوئی شکایت درج نہیں ہوئی۔")

elif page == text[lang]["chatbot"]:
    st.header("Digital Citizen Hub Chatbot 🤖")
    user_input = st.text_input("You:", "")
    if st.button("Send") and user_input:
        user_input_lower = user_input.lower()
        if "how to submit complaint" in user_input_lower:
            answer = "You can submit a complaint by going to 'Submit Complaint' page and filling the form."
        elif "track complaint" in user_input_lower:
            answer = "Go to 'Track Complaint' page and enter your tracking ID."
        else:
            answer = "Sorry, I don't understand. Please contact support or try again."
        st.text_area("Bot:", value=answer, height=150)

st.write("---")
st.markdown(f"**{text[lang]['footer']}**")
