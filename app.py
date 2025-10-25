import streamlit as st
import pandas as pd
import os
import plotly.express as px
from textblob import TextBlob

# --- Page config ---
st.set_page_config(
    page_title="Digital Citizen Hub - Balochistan", 
    page_icon="🏛️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- File to store complaints ---
DATA_FILE = "complaints.csv"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Load complaints ---
if os.path.exists(DATA_FILE):
    complaints_df = pd.read_csv(DATA_FILE)
else:
    complaints_df = pd.DataFrame(columns=[
        "ID", "Name", "Category", "Department", "Priority", 
        "Status", "Description", "Sentiment", "Image"
    ])

# --- Professional CSS Styling ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        color: #1f2937 !important;
        text-align: center;
        margin-bottom: 1rem !important;
        border-bottom: 2px solid #2563eb;
        padding-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.2rem !important;
        color: #4b5563 !important;
        text-align: center;
        margin-bottom: 2rem !important;
        font-weight: 400;
    }
    
    .custom-card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .metric-value {
        font-size: 2rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
        color: #2563eb;
    }
    
    .metric-label {
        font-size: 0.9rem !important;
        color: #6b7280;
        font-weight: 500;
    }
    
    .stButton button {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        width: 100%;
    }
    
    .stButton button:hover {
        background-color: #1d4ed8;
    }
    
    .status-pending { 
        background: #fef3c7; 
        color: #d97706; 
        padding: 0.25rem 0.75rem; 
        border-radius: 12px; 
        font-weight: 500; 
        font-size: 0.8rem;
    }
    .status-resolved { 
        background: #d1fae5; 
        color: #065f46; 
        padding: 0.25rem 0.75rem; 
        border-radius: 12px; 
        font-weight: 500; 
        font-size: 0.8rem;
    }
    .status-high { 
        background: #fee2e2; 
        color: #dc2626; 
        padding: 0.25rem 0.75rem; 
        border-radius: 12px; 
        font-weight: 500; 
        font-size: 0.8rem;
    }
    .status-medium { 
        background: #fef3c7; 
        color: #d97706; 
        padding: 0.25rem 0.75rem; 
        border-radius: 12px; 
        font-weight: 500; 
        font-size: 0.8rem;
    }
    .status-low { 
        background: #d1fae5; 
        color: #065f46; 
        padding: 0.25rem 0.75rem; 
        border-radius: 12px; 
        font-weight: 500; 
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Language Selector ---
st.sidebar.markdown("---")
lang = st.sidebar.radio("Language / زبان", ["English", "اردو"])

# --- Text dictionary ---
text = {
    "English": {
        "home":"Home", "submit":"Submit Complaint", "track":"Track Complaint",
        "dashboard":"Dashboard", "chatbot":"Virtual Assistant",
        "title":"Digital Citizen Hub - Balochistan",
        "subtitle":"Public Service Complaint Management System",
        "mission":"Streamlining citizen-government communication through digital innovation.",
        "submit_title":"Submit Complaint", "name":"Full Name",
        "category":"Complaint Category", "description":"Issue Description",
        "image":"Attach Image (Optional)", "submit_btn":"Submit Complaint",
        "success":"Complaint submitted successfully. Tracking ID:",
        "track_title":"Track Complaint", "track_input":"Enter Complaint ID",
        "track_btn":"Check Status", "dashboard_title":"Administrative Dashboard",
        "dashboard_desc":"Complaint management and analytics",
        "footer":"Government of Balochistan - Digital Transformation Initiative",
        "resolved_btn":"Mark Resolved", "priority":"Priority",
        "status":"Status", "department":"Department", "role":"Role",
        "admin_pass":"Admin Password", "stats_title":"System Overview"
    },
    "اردو": {
        "home":"ہوم", "submit":"شکایت درج کریں", "track":"شکایت ٹریک کریں",
        "dashboard":"ڈیش بورڈ", "chatbot":"ورچوئل معاون",
        "title":"ڈیجیٹل سٹیزن حب - بلوچستان",
        "subtitle":"عوامی خدمات کی شکایت مینجمنٹ سسٹم",
        "mission":"ڈیجیٹل اختراع کے ذریعے شہری-حکومت مواصلات کو بہتر بنانا۔",
        "submit_title":"شکایت درج کریں", "name":"مکمل نام",
        "category":"شکایت کی قسم", "description":"مسئلے کی تفصیل",
        "image":"تصویر منسلک کریں (اختیاری)", "submit_btn":"شکایت جمع کریں",
        "success":"شکایت کامیابی سے جمع ہو گئی۔ ٹریکنگ آئی ڈی:",
        "track_title":"شکایت ٹریک کریں", "track_input":"شکایت کی آئی ڈی درج کریں",
        "track_btn":"حالت چیک کریں", "dashboard_title":"ایڈمنسٹریٹو ڈیش بورڈ",
        "dashboard_desc":"شکایت مینجمنٹ اور تجزیات",
        "footer":"حکومت بلوچستان - ڈیجیٹل تبدیلی کا اقدام",
        "resolved_btn":"حل شدہ قرار دیں", "priority":"ترجیح",
        "status":"حالت", "department":"محکمہ", "role":"کردار",
        "admin_pass":"ایڈمن پاس ورڈ", "stats_title":"سسٹم کا جائزہ"
    }
}

# --- Role Selection ---
st.sidebar.markdown("---")
role = st.sidebar.selectbox(text[lang]["role"], ["Citizen", "Administrator"])

# --- Admin authentication ---
if role == "Administrator":
    admin_password = st.sidebar.text_input(text[lang]["admin_pass"], type="password")
    if admin_password != "admin123":
        st.error("Access Denied")
        st.stop()

# --- Navigation ---
st.sidebar.markdown("---")
if role == "Citizen":
    nav_options = [text[lang]["home"], text[lang]["submit"], text[lang]["track"], text[lang]["chatbot"]]
else:
    nav_options = [text[lang]["home"], text[lang]["dashboard"], text[lang]["chatbot"]]

page = st.sidebar.radio("Navigation", nav_options)

# --- Helper Functions ---
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
    if polarity < -0.2: return "Negative"
    elif polarity > 0.2: return "Positive"
    else: return "Neutral"

def create_status_badge(status, priority=None):
    if status == "Pending":
        return f'<span class="status-pending">{status}</span>'
    elif status == "Resolved":
        return f'<span class="status-resolved">{status}</span>'
    elif priority == "High":
        return f'<span class="status-high">{priority}</span>'
    elif priority == "Medium":
        return f'<span class="status-medium">{priority}</span>'
    elif priority == "Low":
        return f'<span class="status-low">{priority}</span>'
    return status

# --- Department mapping ---
department_mapping = {
    "Electricity": "QESCO", 
    "Water": "Water Board", 
    "Health": "Health Dept", 
    "Roads": "Public Works", 
    "Sanitation": "Municipal",
    "Other": "General Affairs"
}

# --- MAIN LOGIC ---
if page == text[lang]["home"]:
    st.markdown(f'<h1 class="main-header">{text[lang]["title"]}</h1>', unsafe_allow_html=True)
    st.markdown(f'<h3 class="sub-header">{text[lang]["subtitle"]}</h3>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.write(text[lang]["mission"])
    
    if not complaints_df.empty:
        total = len(complaints_df)
        resolved = len(complaints_df[complaints_df["Status"] == "Resolved"])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{total}</div><div class="metric-label">Total Complaints</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{resolved}</div><div class="metric-label">Resolved</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{total-resolved}</div><div class="metric-label">Pending</div></div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

elif page == text[lang]["submit"] and role == "Citizen":
    st.markdown(f'<h1 class="main-header">{text[lang]["submit_title"]}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    
    if lang == "اردو":
        categories = ["بجلی", "پانی", "صحت", "سڑکیں", "صفائی", "دیگر"]
    else:
        categories = ["Electricity", "Water", "Health", "Roads", "Sanitation", "Other"]
    
    with st.form("complaint_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(text[lang]["name"])
            category = st.selectbox(text[lang]["category"], categories)
            
        with col2:
            image = st.file_uploader(text[lang]["image"], type=["jpg", "jpeg", "png"])
        
        description = st.text_area(text[lang]["description"], height=120)
        
        submitted = st.form_submit_button(text[lang]["submit_btn"])

        if submitted and name and description:
            tracking_id = int(pd.Timestamp.now().timestamp())
            category_en = category if lang == "English" else {
                "بجلی": "Electricity", "پانی": "Water", "صحت": "Health",
                "سڑکیں": "Roads", "صفائی": "Sanitation", "دیگر": "Other"
            }.get(category, "Other")
            
            dept = department_mapping.get(category_en, "Other")
            priority = detect_priority(description)
            sentiment = get_sentiment(description)
            status = "Pending"

            if image:
                image_path = os.path.join(UPLOAD_DIR, f"{tracking_id}_{image.name}")
                with open(image_path, "wb") as f:
                    f.write(image.getbuffer())
            else:
                image_path = None

            complaints_df = pd.concat([complaints_df, pd.DataFrame([{
                "ID": tracking_id, "Name": name, "Category": category_en,
                "Department": dept, "Priority": priority, "Status": status,
                "Description": description, "Sentiment": sentiment, "Image": image_path
            }])], ignore_index=True)
            complaints_df.to_csv(DATA_FILE, index=False)

            st.success(f"{text[lang]['success']} #{tracking_id}")
            st.write(f"**{text[lang]['department']}:** {dept}")
            st.write(f"**{text[lang]['priority']}:** {priority}")
            
    st.markdown("</div>", unsafe_allow_html=True)

elif page == text[lang]["track"] and role == "Citizen":
    st.markdown(f'<h1 class="main-header">{text[lang]["track_title"]}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    
    complaint_id = st.text_input(text[lang]["track_input"])
    
    if st.button(text[lang]["track_btn"]):
        if complaint_id.strip():
            try:
                cid = int(complaint_id.strip())
                found = complaints_df[complaints_df["ID"] == cid]
            except ValueError:
                found = pd.DataFrame()
                
            if not found.empty:
                complaint = found.iloc[0]
                st.success("Complaint details found:")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**ID:** #{complaint['ID']}")
                    st.write(f"**{text[lang]['department']}:** {complaint['Department']}")
                    st.write(f"**{text[lang]['status']}:** {complaint['Status']}")
                with col2:
                    st.write(f"**{text[lang]['priority']}:** {complaint['Priority']}")
                    st.write(f"**Sentiment:** {complaint['Sentiment']}")
                
                st.write(f"**Description:** {complaint['Description']}")
                
            else:
                st.error("Complaint not found")
                
    st.markdown("</div>", unsafe_allow_html=True)

elif page == text[lang]["dashboard"] and role == "Administrator":
    st.markdown(f'<h1 class="main-header">{text[lang]["dashboard_title"]}</h1>', unsafe_allow_html=True)
    
    if not complaints_df.empty:
        # Metrics
        total = len(complaints_df)
        resolved = len(complaints_df[complaints_df["Status"] == "Resolved"])
        pending = total - resolved
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{total}</div><div class="metric-label">Total</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{resolved}</div><div class="metric-label">Resolved</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{pending}</div><div class="metric-label">Pending</div></div>', unsafe_allow_html=True)
        with col4:
            high_priority = len(complaints_df[complaints_df["Priority"] == "High"])
            st.markdown(f'<div class="metric-card"><div class="metric-value">{high_priority}</div><div class="metric-label">High Priority</div></div>', unsafe_allow_html=True)
        
        # Charts
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.pie(complaints_df, names="Category", title="Complaints by Category")
            st.plotly_chart(fig1, use_container_width=True)
            
        with col2:
            fig2 = px.bar(complaints_df, x="Priority", title="Complaints by Priority")
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Data Table
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("Complaint Records")
        st.dataframe(complaints_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Resolution
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("Complaint Resolution")
        resolve_id = st.number_input("Complaint ID to resolve", min_value=0, step=1)
        if st.button(text[lang]["resolved_btn"]):
            complaints_df = pd.read_csv(DATA_FILE)
            idx = complaints_df[complaints_df["ID"] == resolve_id].index
            if len(idx) > 0:
                complaints_df.at[idx[0], "Status"] = "Resolved"
                complaints_df.to_csv(DATA_FILE, index=False)
                st.success(f"Complaint #{resolve_id} resolved")
            else:
                st.error("Complaint not found")
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        st.info("No complaints in the system")

elif page == text[lang]["chatbot"]:
    st.markdown(f'<h1 class="main-header">Virtual Assistant</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.write("How can I assist you today?")
    
    user_input = st.text_input("Your question:")
    if st.button("Submit") and user_input:
        ui = user_input.lower()
        if "submit" in ui:
            response = "You can submit complaints through the 'Submit Complaint' page. Provide your details and issue description."
        elif "track" in ui:
            response = "Use the 'Track Complaint' page with your complaint ID to check current status and updates."
        elif "department" in ui:
            response = "We handle complaints for Electricity (QESCO), Water, Health, Roads, Sanitation departments."
        else:
            response = "I can help with complaint submission, tracking, department information, and general guidance."
        
        st.write("**Assistant:**", response)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f'<div style="text-align: center; color: #6b7280; padding: 1rem;">{text[lang]["footer"]}</div>', unsafe_allow_html=True)
