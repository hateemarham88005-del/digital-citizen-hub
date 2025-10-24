import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Digital Citizen Hub",
    page_icon="🌐",
    layout="wide",
)

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #003566;
        text-align: center;
        margin-bottom: 0.3em;
    }
    .subtitle {
        font-size: 18px;
        color: #555;
        text-align: center;
        margin-bottom: 2em;
    }
    .feature-card {
        background-color: #f9f9f9;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    .feature-card:hover {
        background-color: #eef3fa;
    }
    </style>
""", unsafe_allow_html=True)

# --- Language selector ---
lang = st.sidebar.radio("🌐 Choose Language / زبان منتخب کریں", ("English", "اردو"))

# --- Text dictionary ---
text = {
    "English": {
        "title": "Digital Citizen Hub",
        "subtitle": "An AI-powered GovTech platform transforming governance in Balochistan.",
        "about": "Digital Citizen Hub leverages Artificial Intelligence to make public services transparent, efficient, and citizen-focused. From complaint automation to policy intelligence — everything in one ecosystem.",
        "sections": {
            "Complaint": ("Citizen Service Automation & Complaint Redressal", 
                          "Citizens can submit complaints through web or mobile (text, voice, or image). AI categorizes and routes them automatically for faster resolution."),
            "Transparency": ("Transparency & Accountability Dashboard", 
                             "A public dashboard shows complaint data, resolution times, and departmental performance to ensure accountability."),
            "Policy": ("AI-Driven Policy Recommendations", 
                       "AI analyzes citizen feedback and government data to identify policy gaps and recommend improvements."),
            "Fraud": ("Fraud Detection in Public Finance", 
                      "Machine learning models detect anomalies in government transactions to ensure financial integrity.")
        },
        "footer": "Empowering governance through AI and transparency 🇵🇰"
    },
    "اردو": {
        "title": "ڈیجیٹل سٹیزن حب",
        "subtitle": "بلوچستان میں گورننس کو بہتر بنانے کے لیے مصنوعی ذہانت سے چلنے والا پلیٹ فارم۔",
        "about": "ڈیجیٹل سٹیزن حب عوامی خدمات کو شفاف، مؤثر اور شہریوں کے لیے آسان بنانے کے لیے مصنوعی ذہانت استعمال کرتا ہے۔ شکایات کے خودکار نظام سے لے کر پالیسی تجاویز تک — سب کچھ ایک ہی پلیٹ فارم پر۔",
        "sections": {
            "Complaint": ("شہری خدمات اور شکایات کا خودکار نظام", 
                          "شہری ویب یا موبائل کے ذریعے (متن، آواز یا تصویر) شکایات درج کر سکتے ہیں۔ مصنوعی ذہانت ان کو خودکار طور پر متعلقہ محکمے کو بھیجتی ہے۔"),
            "Transparency": ("شفافیت اور احتساب کا ڈیش بورڈ", 
                             "ایک عوامی ڈیش بورڈ شکایات، حل کے وقت اور محکموں کی کارکردگی کے اعداد و شمار ظاہر کرتا ہے تاکہ احتساب یقینی بنایا جا سکے۔"),
            "Policy": ("پالیسی کے لیے مصنوعی ذہانت پر مبنی تجاویز", 
                       "مصنوعی ذہانت شہری آراء اور سرکاری ڈیٹا کا تجزیہ کر کے پالیسی میں موجود خامیوں اور بہتری کے مواقع کی نشاندہی کرتی ہے۔"),
            "Fraud": ("عوامی مالیات میں دھوکہ دہی کی نشاندہی", 
                      "مشین لرننگ ماڈلز سرکاری مالیاتی لین دین میں بے ضابطگیوں کا پتہ لگاتے ہیں تاکہ مالی شفافیت یقینی بنائی جا سکے۔")
        },
        "footer": "مصنوعی ذہانت اور شفافیت کے ذریعے گورننس کو مضبوط بنانا 🇵🇰"
    }
}

# --- Page content ---
st.markdown(f"<h1 class='main-title'>{text[lang]['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>{text[lang]['subtitle']}</p>", unsafe_allow_html=True)
st.write("---")

# About section
st.info(text[lang]["about"])

# --- Features Grid ---
cols = st.columns(2)
for i, (key, (title, desc)) in enumerate(text[lang]["sections"].items()):
    with cols[i % 2]:
        st.markdown(f"<div class='feature-card'><h4>{title}</h4><p>{desc}</p></div>", unsafe_allow_html=True)
        st.write("")

st.write("---")
st.markdown(f"### {text[lang]['footer']}")
