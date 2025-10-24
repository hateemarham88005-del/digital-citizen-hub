import streamlit as st
import pandas as pd
import random
import datetime

# Page setup
st.set_page_config(page_title="Digital Citizen Hub", page_icon="🏛️", layout="wide")

# Sidebar Navigation
st.sidebar.title("🏛️ Digital Citizen Hub")
menu = st.sidebar.radio("Navigate", ["🏠 Home", "📨 Submit Complaint", "🔎 Track Complaint", "📊 Dashboard", "ℹ️ About"])

# --- Home Page ---
if menu == "🏠 Home":
    st.title("Welcome to Digital Citizen Hub")
    st.subheader("AI-Powered Governance for Balochistan 🇵🇰")
    st.write("""
    **Digital Citizen Hub** bridges the gap between citizens and government through AI and automation.
    Citizens can submit complaints, track their progress, and view government transparency dashboards.
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/2965/2965358.png", width=200)
    st.success("Empowering citizens through transparency, accountability, and technology!")

# --- Complaint Submission Page ---
elif menu == "📨 Submit Complaint":
    st.header("📨 Submit Your Complaint")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name")
        category = st.selectbox("Select Category", ["Electricity", "Water Supply", "Roads", "Education", "Health", "Other"])
        urgency = st.slider("Urgency Level", 1, 5, 3)
    with col2:
        location = st.text_input("City / Area")
        image = st.file_uploader("Attach an image (optional)", type=["png", "jpg", "jpeg"])
        complaint = st.text_area("Describe your issue")

    if st.button("Submit Complaint"):
        if not complaint.strip():
            st.warning("⚠️ Please describe your complaint before submitting.")
        else:
            tracking_id = f"CMP-{random.randint(1000,9999)}"
            st.success(f"✅ Complaint submitted successfully! Your tracking ID: **{tracking_id}**")

            # Simulate AI feedback
            st.info("🤖 AI Analysis Result:")
            ai_feedback = random.choice([
                "This issue appears to be critical and related to infrastructure.",
                "Complaint categorized as a routine maintenance issue.",
                "Possible service disruption reported in your area.",
                "High-priority complaint — alerting local authorities.",
                "AI detected multiple similar complaints from your region."
            ])
            st.write(ai_feedback)

            st.write(f"**Estimated Resolution Time:** {random.randint(2,7)} days")

# --- Complaint Tracking Page ---
elif menu == "🔎 Track Complaint":
    st.header("🔎 Track Your Complaint Status")
    tracking_input = st.text_input("Enter your Tracking ID (e.g., CMP-1234)")

    if st.button("Check Status"):
        if tracking_input.strip() == "":
            st.warning("Please enter a valid Tracking ID.")
        else:
            st.success(f"Tracking ID: {tracking_input}")
            status = random.choice(["Pending", "In Progress", "Resolved", "Under Review"])
            progress = {"Pending": 20, "In Progress": 60, "Under Review": 80, "Resolved": 100}[status]
            st.info(f"Current Status: **{status}**")
            st.progress(progress/100)
            st.write(f"Last Updated: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

# --- Dashboard Page ---
elif menu == "📊 Dashboard":
    st.header("📊 Transparency & Accountability Dashboard")

    data = {
        "Department": ["Electricity", "Water", "Roads", "Education", "Health"],
        "Complaints": [random.randint(30, 120) for _ in range(5)],
        "Resolved (%)": [random.randint(40, 95) for _ in range(5)],
    }
    df = pd.DataFrame(data)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 Complaint Overview")
        st.dataframe(df)

    with col2:
        st.subheader("📈 Performance Chart")
        st.bar_chart(df.set_index("Department")["Resolved (%)"])

    avg_res = df["Resolved (%)"].mean()
    total_complaints = sum(df["Complaints"])

    st.metric(label="Average Resolution Rate", value=f"{avg_res:.1f}%")
    st.metric(label="Total Complaints Logged", value=total_complaints)

# --- About Page ---
elif menu == "ℹ️ About":
    st.header("ℹ️ About Digital Citizen Hub")
    st.write("""
    **Digital Citizen Hub** is an AI-powered GovTech solution to improve governance in Balochistan.
    It automates complaint redressal, promotes transparency, and supports policy-making through data analytics.

    **Core Features:**
    - 🧠 AI-driven complaint categorization  
    - 🕵️ Fraud detection in public finance *(future module)*  
    - 📊 Real-time transparency dashboard  
    - 🔍 Complaint tracking and citizen feedback  
    - 🌐 Inclusive design for all literacy levels  
    """)

    st.success("Developed by Team Algorithm Avengers 🚀")
