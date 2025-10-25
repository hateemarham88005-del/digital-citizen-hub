import streamlit as st
import pandas as pd
import os
import plotly.express as px
from textblob import TextBlob

# --- Page config ---
st.set_page_config(
    page_title="Digital Citizen Hub - Balochistan", 
    page_icon="🌐", 
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

# --- Modern Smooth CSS ---
st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #f4f7fb 0%, #e8eef6 100%);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #1e293b;
        }

        .stButton button {
            background: linear-gradient(90deg, #2563eb, #1e40af);
            color: #ffffff !important;
            border: none;
            border-radius: 8px;
            padding: 0.9rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 6px 20px rgba(37,99,235,0.25);
        }

        .stButton button:hover {
            background: linear-gradient(90deg, #1d4ed8, #1e3a8a);
            color: #ffffff !important;
            transform: scale(1.05);
            box-shadow: 0 8px 30px rgba(37,99,235,0.4);
        }

        .main-header {
            font-size: 3rem;
            font-weight: 700;
            color: #1e40af;
            text-align: center;
            margin-bottom: 1rem;
            animation: fadeIn 1.5s ease-in;
        }

        .sub-header {
            font-size: 1.4rem;
            color: #666666;
            text-align: center;
            margin-bottom: 3rem;
            font-weight: 400;
            line-height: 1.5;
        }

        .mission-text {
            font-size: 1.1rem;
            color: #444444;
            text-align: center;
            margin: 2rem 0;
            line-height: 1.6;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }

        .action-container {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin: 3rem 0;
            flex-wrap: wrap;
        }
        
        .action-button {
            background: #000000;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 1.2rem 2.5rem;
            font-weight: 600;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            min-width: 200px;
        }
        
        .action-button:hover {
            background: #333333;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }

        .section-title {
            font-size: 2rem;
            font-weight: 600;
            color: #000000;
            text-align: center;
            margin-bottom: 2rem;
        }

        .clean-card {
            background: white;
            border-radius: 12px;
            padding: 2.5rem;
            border: 1px solid #f0f0f0;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            margin-bottom: 2rem;
        }

        .status-pending { 
            background: #fff3cd; 
            color: #856404; 
            padding: 0.4rem 1rem; 
            border-radius: 20px; 
            font-weight: 500; 
            font-size: 0.8rem;
        }
        .status-resolved { 
            background: #d4edda; 
            color: #155724; 
            padding: 0.4rem 1rem; 
            border-radius: 20px; 
            font-weight: 500; 
            font-size: 0.8rem;
        }
        .status-high { 
            background: #f8d7da; 
            color: #721c24; 
            padding: 0.4rem 1rem; 
            border-radius: 20px; 
            font-weight: 500; 
            font-size: 0.8rem;
        }
        .status-medium { 
            background: #fff3cd; 
            color: #856404; 
            padding: 0.4rem 1rem; 
            border-radius: 20px; 
            font-weight: 500; 
            font-size: 0.8rem;
        }
        .status-low { 
            background: #d1ecf1; 
            color: #0c5460; 
            padding: 0.4rem 1rem; 
            border-radius: 20px; 
            font-weight: 500; 
            font-size: 0.8rem;
        }

        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(20px);}
            to {opacity: 1; transform: translateY(0);}
        }
    </style>
""", unsafe_allow_html=True)

# --- Language Selector ---
st.sidebar.markdown("---")
lang = st.sidebar.radio("Language / زبان", ["English", "اردو"])

# --- Text dictionary ---
text = {
    "English": {
        "home": "Home",
        "submit": "Submit Complaint", 
        "track": "Track Complaint",
        "dashboard": "Dashboard", 
        "chatbot": "Assistant",
        "title": "Digital Citizen Hub – Balochistan",
        "subtitle": "AI-powered platform transforming governance",
        "mission": "Automating complaints, tracking status, and enhancing transparency in government services.",
        "submit_title": "Submit a Complaint", 
        "name": "Full Name",
        "category": "Complaint Type", 
        "description": "Describe your issue",
        "image": "Upload an optional image", 
        "submit_btn": "Submit Complaint",
        "success": "Your complaint has been submitted! Tracking ID:",
        "track_title": "Track Your Complaint", 
        "track_input": "Enter your Complaint ID",
        "track_btn": "Check Status", 
        "dashboard_title": "Transparency Dashboard",
        "dashboard_desc": "Overview of complaints in the system.",
        "footer": "Empowering governance through AI and transparency",
        "resolved_btn": "Mark as Resolved", 
        "priority": "Priority",
        "status": "Status", 
        "department": "Department", 
        "role": "Select Role",
        "admin_pass": "Enter Admin Password",
        "features": "Platform Features"
    },
    "اردو": {
        "home": "ہوم",
        "submit": "شکایت درج کریں", 
        "track": "شکایت ٹریک کریں",
        "dashboard": "ڈیش بورڈ", 
        "chatbot": "معاون",
        "title": "ڈیجیٹل سٹیزن حب – بلوچستان",
        "subtitle": "بلوچستان میں گورننس کو بہتر بنانے کے لیے مصنوعی ذہانت سے چلنے والا پلیٹ فارم۔",
        "mission": "شکایات کو خودکار کرنا، ان کی حالت ٹریک کرنا اور سرکاری خدمات میں شفافیت بڑھانا۔",
        "submit_title": "شکایت درج کریں", 
        "name": "نام",
        "category": "شکایت کی قسم", 
        "description": "مسئلہ بیان کریں",
        "image": "اختیاری تصویر اپ لوڈ کریں", 
        "submit_btn": "شکایت جمع کریں",
        "success": "آپ کی شکایت موصول ہو گئی! ٹریکنگ آئی ڈی:",
        "track_title": "شکایت ٹریک کریں", 
        "track_input": "اپنی شکایت کی آئی ڈی درج کریں",
        "track_btn": "حالت چیک کریں", 
        "dashboard_title": "شفافیت کا ڈیش بورڈ",
        "dashboard_desc": "سسٹم میں شکایات کا جائزہ۔",
        "footer": "مصنوعی ذہانت اور شفافیت کے ذریعے گورننس کو مضبوط بنانا",
        "resolved_btn": "حل شدہ نشان زد کریں", 
        "priority": "اہمیت",
        "status": "حالت", 
        "department": "ڈیپارٹمنٹ", 
        "role": "کردار منتخب کریں",
        "admin_pass": "ایڈمن پاس ورڈ درج کریں",
        "features": "پلیٹ فارم کی خصوصیات"
    }
}

# --- Role Selection ---
st.sidebar.markdown("---")
role = st.sidebar.selectbox(text[lang]["role"], ["Citizen", "Admin"])

# --- Admin authentication ---
if role == "Admin":
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

page = st.sidebar.radio("Navigate", nav_options)

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
    # Hero Section
    st.markdown(f'<h1 class="main-header">{text[lang]["title"]}</h1>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">{text[lang]["subtitle"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="mission-text">{text[lang]["mission"]}</div>', unsafe_allow_html=True)
    
    # Action Buttons - Fixed using Streamlit buttons instead of HTML links
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Complaint", use_container_width=True):
            st.session_state.page = text[lang]["submit"]
    with col2:
        if st.button("Track Complaint", use_container_width=True):
            st.session_state.page = text[lang]["track"]
    
    # Divider
    st.markdown("---")
    
    # Features Section
    st.markdown(f'<div class="section-title">{text[lang]["features"]}</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h3 style="color: #000000; margin-bottom: 1rem;">AI-Powered</h3>
            <p style="color: #666666;">Smart complaint categorization and priority detection using artificial intelligence.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h3 style="color: #000000; margin-bottom: 1rem;">Real-time Tracking</h3>
            <p style="color: #666666;">Monitor your complaint status in real-time with transparent updates.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h3 style="color: #000000; margin-bottom: 1rem;">Multi-department</h3>
            <p style="color: #666666;">Integrated system connecting all government departments for efficient resolution.</p>
        </div>
        """, unsafe_allow_html=True)

elif page == text[lang]["submit"] and role == "Citizen":
    st.markdown(f'<h1 class="main-header">{text[lang]["submit_title"]}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="clean-card">', unsafe_allow_html=True)
    
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
            
            # Fixed category translation logic
            if lang == "اردو":
                translation_map = {
                    "بجلی": "Electricity", "پانی": "Water", "صحت": "Health",
                    "سڑکیں": "Roads", "صفائی": "Sanitation", "دیگر": "Other"
                }
                category_en = translation_map.get(category, "Other")
            else:
                category_en = category
            
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
            st.write(f"**Department:** {dept}")
            st.write(f"**Priority:** {priority}")
            
    st.markdown("</div>", unsafe_allow_html=True)

elif page == text[lang]["track"] and role == "Citizen":
    st.markdown(f'<h1 class="main-header">{text[lang]["track_title"]}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="clean-card">', unsafe_allow_html=True)
    
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
                    st.write(f"**Department:** {complaint['Department']}")
                    st.write(f"**Status:** {complaint['Status']}")
                with col2:
                    st.write(f"**Priority:** {complaint['Priority']}")
                    st.write(f"**Sentiment:** {complaint['Sentiment']}")
                
                st.write(f"**Description:** {complaint['Description']}")
                
            else:
                st.error("Complaint not found")
                
    st.markdown("</div>", unsafe_allow_html=True)

elif page == text[lang]["dashboard"] and role == "Admin":
    st.markdown(f'<h1 class="main-header">{text[lang]["dashboard_title"]}</h1>', unsafe_allow_html=True)
    
    if not complaints_df.empty:
        # Metrics
        total = len(complaints_df)
        resolved = len(complaints_df[complaints_df["Status"] == "Resolved"])
        pending = total - resolved
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Complaints", total)
        with col2:
            st.metric("Resolved", resolved)
        with col3:
            st.metric("Pending", pending)
        with col4:
            high_priority = len(complaints_df[complaints_df["Priority"] == "High"])
            st.metric("High Priority", high_priority)
        
        # Charts
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.subheader("Visual Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.pie(complaints_df, names="Category", title="Complaints by Category")
            st.plotly_chart(fig1, use_container_width=True)
            
        with col2:
            fig2 = px.bar(complaints_df, x="Priority", title="Complaints by Priority")
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Data Table
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.subheader("Complaint Records")
        st.dataframe(complaints_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Resolution
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.subheader("Complaint Resolution")
        resolve_id = st.number_input("Enter Complaint ID to resolve", min_value=0, step=1)
        if st.button(text[lang]["resolved_btn"]):
            complaints_df = pd.read_csv(DATA_FILE)
            idx = complaints_df[complaints_df["ID"] == resolve_id].index
            if len(idx) > 0:
                complaints_df.at[idx[0], "Status"] = "Resolved"
                complaints_df.to_csv(DATA_FILE, index=False)
                st.success(f"Complaint #{resolve_id} marked as Resolved")
            else:
                st.error("Complaint not found")
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        st.info("No complaints submitted yet.")

elif page == text[lang]["chatbot"]:
    st.markdown(f'<h1 class="main-header">Digital Citizen Hub Assistant</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="clean-card">', unsafe_allow_html=True)
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
st.markdown(f'<div style="text-align: center; color: #666666; padding: 2rem;">{text[lang]["footer"]}</div>', unsafe_allow_html=True)
