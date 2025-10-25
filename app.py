import streamlit as st
import pandas as pd
import random
import os
import plotly.express as px
from textblob import TextBlob

# --- Page config ---
st.set_page_config(
    page_title="Digital Citizen Hub", 
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

# --- Enhanced CSS Styling ---
st.markdown("""
<style>
    /* Main background and text */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main .block-container {
        padding-top: 2rem;
    }
    
    /* Headers */
    .main-header {
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(45deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem !important;
    }
    
    .sub-header {
        font-size: 1.5rem !important;
        color: #E8F4FD !important;
        text-align: center;
        margin-bottom: 2rem !important;
    }
    
    /* Cards */
    .custom-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1.5rem;
    }
    
    /* Metrics and stats */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .metric-label {
        font-size: 1rem !important;
        opacity: 0.9;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
    }
    
    /* Sidebar */
    .css-1d391kg, .css-1lcbmhc {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
    
    /* Status badges */
    .status-pending { background: #FFF3CD; color: #856404; padding: 0.3rem 0.8rem; border-radius: 20px; font-weight: 600; }
    .status-resolved { background: #D1ECF1; color: #0C5460; padding: 0.3rem 0.8rem; border-radius: 20px; font-weight: 600; }
    .status-high { background: #F8D7DA; color: #721C24; padding: 0.3rem 0.8rem; border-radius: 20px; font-weight: 600; }
    .status-medium { background: #FFF3CD; color: #856404; padding: 0.3rem 0.8rem; border-radius: 20px; font-weight: 600; }
    .status-low { background: #D1E7DD; color: #0F5132; padding: 0.3rem 0.8rem; border-radius: 20px; font-weight: 600; }
    
    /* Form styling */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 10px !important;
        border: 2px solid #E0E0E0 !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Language Selector ---
st.sidebar.markdown("---")
lang = st.sidebar.radio("🌐 Choose Language / زبان منتخب کریں", ["English", "اردو"], horizontal=True)

# --- Text dictionary ---
text = {
    "English": {
        "home":"🏠 Home","submit":"📝 Submit Complaint","track":"🔍 Track Complaint",
        "dashboard":"📊 Dashboard","chatbot":"🤖 Chatbot",
        "title":"Digital Citizen Hub – Balochistan",
        "subtitle":"AI-powered platform transforming governance in Balochistan",
        "mission":"Automating complaints, tracking status, and enhancing transparency in government services.",
        "submit_title":"Submit a Complaint","name":"Full Name",
        "category":"Complaint Type","description":"Describe your issue",
        "image":"Upload an optional image","submit_btn":"Submit Complaint",
        "success":"✅ Your complaint has been submitted! Tracking ID:",
        "track_title":"Track Your Complaint","track_input":"Enter your Complaint ID",
        "track_btn":"Check Status","dashboard_title":"Transparency Dashboard",
        "dashboard_desc":"Overview of complaints in the system.",
        "footer":"Empowering governance through AI and transparency 🇵🇰",
        "resolved_btn":"Mark as Resolved","priority":"Priority",
        "status":"Status","department":"Department","role":"Select Role",
        "admin_pass":"Enter Admin Password",
        "stats_title":"System Overview", "quick_actions":"Quick Actions"
    },
    "اردو": {
        "home":"🏠 ہوم","submit":"📝 شکایت درج کریں","track":"🔍 شکایت ٹریک کریں",
        "dashboard":"📊 ڈیش بورڈ","chatbot":"🤖 چیٹ بوٹ",
        "title":"ڈیجیٹل سٹیزن حب – بلوچستان",
        "subtitle":"بلوچستان میں گورننس کو بہتر بنانے کے لیے مصنوعی ذہانت سے چلنے والا پلیٹ فارم۔",
        "mission":"شکایات کو خودکار کرنا، ان کی حالت ٹریک کرنا اور سرکاری خدمات میں شفافیت بڑھانا۔",
        "submit_title":"شکایت درج کریں","name":"نام","category":"شکایت کی قسم",
        "description":"مسئلہ بیان کریں","image":"اختیاری تصویر اپ لوڈ کریں",
        "submit_btn":"شکایت جمع کریں",
        "success":"✅ آپ کی شکایت موصول ہو گئی! ٹریکنگ آئی ڈی:",
        "track_title":"شکایت ٹریک کریں","track_input":"اپنی شکایت کی آئی ڈی درج کریں",
        "track_btn":"حالت چیک کریں","dashboard_title":"شفافیت کا ڈیش بورڈ",
        "dashboard_desc":"سسٹم میں شکایات کا جائزہ۔",
        "footer":"مصنوعی ذہانت اور شفافیت کے ذریعے گورننس کو مضبوط بنانا 🇵🇰",
        "resolved_btn":"حل شدہ نشان زد کریں","priority":"اہمیت","status":"حالت",
        "department":"ڈیپارٹمنٹ","role":"کردار منتخب کریں","admin_pass":"ایڈمن پاس ورڈ درج کریں",
        "stats_title":"سسٹم کا جائزہ", "quick_actions":"فوری اقدامات"
    }
}

# --- Sidebar Role Selection ---
st.sidebar.markdown("---")
role = st.sidebar.selectbox(text[lang]["role"], ["Citizen", "Admin"])

# --- Admin authentication ---
if role == "Admin":
    admin_password = st.sidebar.text_input(text[lang]["admin_pass"], type="password")
    if admin_password != "admin123":
        st.error("Access Denied ❌")
        st.stop()

# --- Role-based Navigation ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 Navigation")

if role == "Citizen":
    nav_options = [text[lang]["home"], text[lang]["submit"], text[lang]["track"], text[lang]["chatbot"]]
else:
    nav_options = [text[lang]["home"], text[lang]["dashboard"], text[lang]["chatbot"]]

page = st.sidebar.radio("", nav_options)

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
    if polarity < -0.2: return "Angry"
    elif polarity > 0.2: return "Calm"
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
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<h1 class="main-header">{text[lang]["title"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<h3 class="sub-header">{text[lang]["subtitle"]}</h3>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    
    # Quick Stats
    if not complaints_df.empty:
        total = len(complaints_df)
        resolved = len(complaints_df[complaints_df["Status"] == "Resolved"])
        pending = total - resolved
        
        st.markdown(f"### 📈 {text[lang]['stats_title']}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{total}</div><div class="metric-label">Total Complaints</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{resolved}</div><div class="metric-label">Resolved</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{pending}</div><div class="metric-label">Pending</div></div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown(f"### ⚡ {text[lang]['quick_actions']}")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Submit New Complaint", use_container_width=True):
            st.session_state.page = text[lang]["submit"]
    with col2:
        if st.button("🔍 Track Complaint", use_container_width=True):
            st.session_state.page = text[lang]["track"]
    with col3:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.session_state.page = text[lang]["dashboard"]
    
    # Mission Card
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown(f"### 🎯 Our Mission")
    st.info(text[lang]["mission"])
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
            name = st.text_input(text[lang]["name"], placeholder="Enter your full name")
            category = st.selectbox(text[lang]["category"], categories)
            
        with col2:
            image = st.file_uploader(text[lang]["image"], type=["jpg", "jpeg", "png"])
        
        description = st.text_area(text[lang]["description"], height=120, 
                                 placeholder="Please provide detailed description of your issue...")
        
        submitted = st.form_submit_button(text[lang]["submit_btn"], use_container_width=True)

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

            st.success(f"### {text[lang]['success']} **#{tracking_id}**")
            st.markdown(f"""
            **{text[lang]['department']}:** {dept}  
            **{text[lang]['priority']}:** {create_status_badge(None, priority)}  
            **Status:** {create_status_badge('Pending')}
            """, unsafe_allow_html=True)
        elif submitted:
            st.warning("⚠️ Please fill all required fields!" if lang == "English" else "⚠️ تمام خانے پُر کریں!")
    
    st.markdown("</div>", unsafe_allow_html=True)

elif page == text[lang]["track"] and role == "Citizen":
    st.markdown(f'<h1 class="main-header">{text[lang]["track_title"]}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    
    complaint_id = st.text_input(text[lang]["track_input"], placeholder="Enter your complaint ID here...")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button(text[lang]["track_btn"], use_container_width=True):
            if complaint_id.strip():
                try:
                    cid = int(complaint_id.strip())
                    found = complaints_df[complaints_df["ID"] == cid]
                except ValueError:
                    found = pd.DataFrame()
                
                if not found.empty:
                    st.success("### Complaint Found ✅")
                    
                    complaint = found.iloc[0]
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        **Complaint ID:** #{complaint['ID']}  
                        **Name:** {complaint['Name']}  
                        **Department:** {complaint['Department']}  
                        **Category:** {complaint['Category']}
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        **Status:** {create_status_badge(complaint['Status'])}  
                        **Priority:** {create_status_badge(None, complaint['Priority'])}  
                        **Sentiment:** {complaint['Sentiment']}
                        """, unsafe_allow_html=True)
                    
                    st.markdown(f"**Description:** {complaint['Description']}")
                    
                    if pd.notna(complaint["Image"]) and os.path.exists(complaint["Image"]):
                        st.image(complaint["Image"], caption="Attached Image", use_container_width=True)
                else:
                    st.error("❌ Complaint not found!" if lang == "English" else "❌ شکایت موجود نہیں!")
            else:
                st.warning("⚠️ Please enter a valid Complaint ID!" if lang == "English" else "⚠️ درست آئی ڈی درج کریں!")
    
    st.markdown("</div>", unsafe_allow_html=True)

elif page == text[lang]["dashboard"] and role == "Admin":
    st.markdown(f'<h1 class="main-header">{text[lang]["dashboard_title"]}</h1>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">{text[lang]["dashboard_desc"]}</div>', unsafe_allow_html=True)

    if not complaints_df.empty:
        # Summary Metrics
        total = len(complaints_df)
        resolved = len(complaints_df[complaints_df["Status"] == "Resolved"])
        pending = total - resolved
        high_priority = len(complaints_df[complaints_df["Priority"] == "High"])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{total}</div><div class="metric-label">Total Complaints</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{resolved}</div><div class="metric-label">Resolved</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{pending}</div><div class="metric-label">Pending</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{high_priority}</div><div class="metric-label">High Priority</div></div>', unsafe_allow_html=True)

        # Visualizations
        st.markdown("## 📊 Visual Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig0 = px.pie(complaints_df, names="Category", title="Complaints by Category")
            st.plotly_chart(fig0, use_container_width=True)
            
            fig2 = px.bar(complaints_df, x="Priority", color="Priority", 
                         title="Complaints by Priority", color_discrete_map={
                             'High': '#FF6B6B', 'Medium': '#FFD166', 'Low': '#06D6A0'
                         })
            st.plotly_chart(fig2, use_container_width=True)
            
        with col2:
            fig1 = px.pie(complaints_df, names="Department", title="Complaints by Department")
            st.plotly_chart(fig1, use_container_width=True)
            
            fig4 = px.pie(complaints_df, names="Sentiment", title="Complaints by Sentiment")
            st.plotly_chart(fig4, use_container_width=True)

        # Data Table with Actions
        st.markdown("## 📋 All Complaints")
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        
        # Display formatted dataframe
        display_df = complaints_df.copy()
        display_df['Status'] = display_df.apply(lambda x: create_status_badge(x['Status']), axis=1)
        display_df['Priority'] = display_df.apply(lambda x: create_status_badge(None, x['Priority']), axis=1)
        
        st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Resolution Section
        st.markdown("## 🛠️ Complaint Management")
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            resolve_id = st.number_input("Enter Complaint ID to resolve", min_value=0, step=1)
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(text[lang]["resolved_btn"], use_container_width=True):
                complaints_df = pd.read_csv(DATA_FILE)
                idx = complaints_df[complaints_df["ID"] == resolve_id].index
                if len(idx) > 0:
                    complaints_df.at[idx[0], "Status"] = "Resolved"
                    complaints_df.to_csv(DATA_FILE, index=False)
                    st.success(f"Complaint #{resolve_id} marked as Resolved ✅")
                    st.rerun()
                else:
                    st.warning("Complaint not found!")
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        st.info("No complaints submitted yet.")

elif page == text[lang]["chatbot"]:
    st.markdown(f'<h1 class="main-header">Digital Citizen Hub Chatbot 🤖</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # React to user input
    if prompt := st.chat_input("How can I help you today?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate response
        ui = prompt.lower()
        if "submit" in ui:
            response = "You can submit a complaint under 'Submit Complaint' page. I'll guide you through the process!"
        elif "track" in ui:
            response = "To track your complaint, visit the 'Track Complaint' section and enter your Complaint ID. I can help you find your complaint status!"
        elif "resolved" in ui:
            response = "Admins can mark complaints as resolved in the Dashboard. For citizens, you can check the status in the Track Complaint section."
        elif "department" in ui:
            response = "We work with various departments: Electricity (QESCO), Water Board, Health Department, Public Works (Roads), and Municipal Services (Sanitation)."
        elif "priority" in ui:
            response = "Complaints are automatically categorized as High, Medium, or Low priority based on urgency keywords in your description."
        elif "hello" in ui or "hi" in ui:
            response = "Hello! Welcome to Digital Citizen Hub. How can I assist you with government services today?"
        else:
            response = "I'm here to help with government services! You can ask about submitting complaints, tracking status, departments, or resolution processes."
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f'<div style="text-align: center; color: #666; padding: 2rem;"><b>{text[lang]["footer"]}</b></div>', unsafe_allow_html=True)
