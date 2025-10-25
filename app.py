import streamlit as st
import pandas as pd
import random
import os
import plotly.express as px
from textblob import TextBlob

# --- Page config ---
st.set_page_config(page_title="Digital Citizen Hub", page_icon="🌐", layout="wide")

# --- File to store complaints ---
DATA_FILE = "complaints.csv"

# --- Load complaints ---
if os.path.exists(DATA_FILE):
    complaints_df = pd.read_csv(DATA_FILE)
else:
    complaints_df = pd.DataFrame(columns=["ID", "Name", "Category", "Department", "Priority", "Status", "Description", "Sentiment"])

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
        "priority":"Priority","status":"Status","department":"Department","role":"Select Role"
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
        "priority":"اہمیت","status":"حالت","department":"ڈیپارٹمنٹ","role":"کردار منتخب کریں"
    }
}

# --- Sidebar Role & Navigation ---
role = st.sidebar.selectbox(text[lang]["role"], ["Citizen", "Admin"])
page = st.sidebar.radio("Navigate",
                        [text[lang]["home"], text[lang]["submit"], text[lang]["track"], text[lang]["dashboard"], text[lang]["chatbot"]])

# --- Helper: Category & Priority Detection ---
def categorize_complaint(text_input):
    text_input = text_input.lower()
    if any(word in text_input for word in ["electricity", "power", "load", "bill"]):
        return "Electricity"
    elif any(word in text_input for word in ["water", "pipe", "leak", "supply"]):
        return "Water"
    elif any(word in text_input for word in ["hospital", "doctor", "medicine", "health"]):
        return "Health"
    elif any(word in text_input for word in ["road", "street", "traffic", "bridge"]):
        return "Roads"
    elif any(word in text_input for word in ["waste", "garbage", "trash", "clean"]):
        return "Sanitation"
    else:
        return "Other"

def detect_priority(text_input):
    text_input = text_input.lower()
    if any(word in text_input for word in ["urgent", "immediately", "danger", "fire", "flood"]):
        return "High"
    elif any(word in text_input for word in ["delay", "broken", "issue", "problem"]):
        return "Medium"
    else:
        return "Low"

def get_sentiment(text_input):
    polarity = TextBlob(text_input).sentiment.polarity
    if polarity < -0.2: return "Angry"
    elif polarity > 0.2: return "Calm"
    else: return "Neutral"

# --- Department mapping ---
department_mapping = {"Electricity": "QESCO", "Water": "Water Board", "Health": "Health Dept", "Roads": "Public Works", "Sanitation": "Municipal"}

# --- MAIN PAGES ---
if page == text[lang]["home"]:
    st.title(text[lang]["title"])
    st.subheader(text[lang]["subtitle"])
    st.info(text[lang]["mission"])

elif page == text[lang]["submit"] and role == "Citizen":
    st.header(text[lang]["submit_title"])
    with st.form("complaint_form"):
        name = st.text_input(text[lang]["name"])
        description = st.text_area(text[lang]["description"], height=120)
        submitted = st.form_submit_button(text[lang]["submit_btn"])

        if submitted and name and description:
            tracking_id = random.randint(1000, 9999)
            category = categorize_complaint(description)
            dept = department_mapping.get(category, "Other")
            priority = detect_priority(description)
            sentiment = get_sentiment(description)
            status = "Pending"
            complaints_df = pd.concat([complaints_df, pd.DataFrame([{
                "ID": tracking_id, "Name": name, "Category": category, "Department": dept,
                "Priority": priority, "Status": status, "Description": description, "Sentiment": sentiment
            }])], ignore_index=True)
            complaints_df.to_csv(DATA_FILE, index=False)
            st.success(f"{text[lang]['success']} #{tracking_id}\n{text[lang]['department']}: {dept}\n{text[lang]['priority']}: {priority}")
        elif submitted:
            st.warning("⚠️ Please fill all fields!" if lang == "English" else "⚠️ تمام خانے پُر کریں!")

elif page == text[lang]["track"] and role == "Citizen":
    st.header(text[lang]["track_title"])
    complaint_id = st.text_input(text[lang]["track_input"])
    if st.button(text[lang]["track_btn"]):
        if complaint_id.strip():
            try:
                cid = int(complaint_id.strip())
                found = complaints_df[complaints_df["ID"] == cid]
            except ValueError:
                found = pd.DataFrame()
            if not found.empty:
                st.success(f"{text[lang]['department']}: {found.iloc[0]['Department']}\n{text[lang]['status']}: {found.iloc[0]['Status']}\n{text[lang]['priority']}: {found.iloc[0]['Priority']}\nSentiment: {found.iloc[0]['Sentiment']}\nDescription: {found.iloc[0]['Description']}")
            else:
                st.warning("❌ Complaint not found!" if lang == "English" else "❌ شکایت موجود نہیں!")
        else:
            st.warning("⚠️ Enter a valid ID!" if lang == "English" else "⚠️ درست آئی ڈی درج کریں!")

elif page == text[lang]["dashboard"] and role == "Admin":
    st.header(text[lang]["dashboard_title"])
    st.write(text[lang]["dashboard_desc"])
    if not complaints_df.empty:
        st.dataframe(complaints_df)
        total = len(complaints_df)
        resolved = len(complaints_df[complaints_df["Status"] == "Resolved"])
        pending = total - resolved
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Complaints", total)
        col2.metric("Resolved", resolved)
        col3.metric("Pending", pending)

        # --- Visualization Charts ---
        st.subheader("📊 Visual Insights")
        fig1 = px.pie(complaints_df, names="Department", title="Complaints by Department")
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.bar(complaints_df, x="Priority", color="Priority", title="Complaints by Priority")
        st.plotly_chart(fig2, use_container_width=True)

        if "Status" in complaints_df.columns:
            complaints_df["ResolvedFlag"] = complaints_df["Status"].apply(lambda x: 1 if x.lower() == "resolved" else 0)
            fig3 = px.line(complaints_df.groupby("Priority")["ResolvedFlag"].mean().reset_index(),
                           x="Priority", y="ResolvedFlag", title="Resolution Rate by Priority")
            st.plotly_chart(fig3, use_container_width=True)

        # --- Resolve Complaint ---
        st.subheader("🧑‍💼 Resolve Complaint")
        resolve_id = st.number_input("Enter Complaint ID to resolve", min_value=0, step=1)
        if st.button(text[lang]["resolved_btn"]):
            idx = complaints_df[complaints_df["ID"] == resolve_id].index
            if len(idx) > 0:
                complaints_df.at[idx[0], "Status"] = "Resolved"
                complaints_df.to_csv(DATA_FILE, index=False)
                st.success(f"Complaint #{resolve_id} marked as Resolved ✅")
            else:
                st.warning("Complaint not found!")
    else:
        st.info("No complaints submitted yet.")

elif page == text[lang]["chatbot"]:
    st.header("Digital Citizen Hub Chatbot 🤖")
    user_input = st.text_input("You:", "")
    if st.button("Send") and user_input:
        ui = user_input.lower()
        if "submit" in ui:
            answer = "You can submit a complaint under 'Submit Complaint' page."
        elif "track" in ui:
            answer = "To track your complaint, visit the 'Track Complaint' section and enter your ID."
        elif "resolved" in ui:
            answer = "Admins can mark complaints as resolved in the Dashboard."
        elif "department" in ui:
            answer = "Departments include: Electricity (QESCO), Water, Health, Roads, and Sanitation."
        elif "priority" in ui:
            answer = "Complaints are automatically categorized as High, Medium, or Low priority based on urgency."
        else:
            answer = "I'm here to help! You can ask about complaints, departments, or resolution."
        st.text_area("Bot:", value=answer, height=150)

st.write("---")
st.markdown(f"**{text[lang]['footer']}**")
