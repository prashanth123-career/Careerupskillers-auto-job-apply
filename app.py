import streamlit as st
import urllib.parse

# ----------------- LANGUAGE SUPPORT -----------------
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
    "French": "fr",
    "German": "de",
    "Arabic": "ar",
    "Mandarin": "zh",
    "Japanese": "ja"
}

TRANSLATIONS = {
    "en": {
        "title": "CareerUpskillers | AI Job Hub",
        "tagline": "Your AI-powered career launchpad",
        "description": "Smart Job Search | Interview Prep | Free Certifications",
        "job_finder": "Job Finder",
        "interview_prep": "Interview Preparation",
        "free_courses": "Free Courses",
        "find_jobs": "Find Jobs",
        "generate_link": "Generate Interview Prep Link",
        "find_courses": "Find Courses",
        "job_title": "Job Title / Keywords",
        "location": "Preferred Location",
        "country": "Country",
        "experience": "Experience Level",
        "date_posted": "Date Posted",
        "search_course": "Search Course / Skill / Job Title",
        "experience_options": ["Any", "Entry", "Mid", "Senior", "Executive"],
        "date_posted_options": ["Any time", "Past month", "Past week", "Past 24 hours"]
    },
    "hi": {
        "title": "कैरियर अपस्किलर्स | एआई जॉब हब",
        "tagline": "आपका एआई-संचालित करियर लॉन्चपैड",
        "description": "स्मार्ट जॉब सर्च | साक्षात्कार तैयारी | मुफ्त प्रमाणपत्र",
        "job_finder": "जॉब खोजक",
        "interview_prep": "साक्षात्कार तैयारी",
        "free_courses": "मुफ्त पाठ्यक्रम",
        "find_jobs": "नौकरियाँ खोजें",
        "generate_link": "साक्षात्कार तैयारी लिंक बनाएँ",
        "find_courses": "पाठ्यक्रम खोजें",
        "job_title": "नौकरी शीर्षक / कीवर्ड",
        "location": "पसंदीदा स्थान",
        "country": "देश",
        "experience": "अनुभव स्तर",
        "date_posted": "पोस्ट की तारीख",
        "search_course": "पाठ्यक्रम / कौशल / नौकरी शीर्षक खोजें",
        "experience_options": ["कोई भी", "प्रारंभिक", "मध्य", "वरिष्ठ", "कार्यकारी"],
        "date_posted_options": ["कभी भी", "पिछला महीना", "पिछला सप्ताह", "पिछले 24 घंटे"]
    },
    "zh": {
        "title": "CareerUpskillers | AI 职业平台",
        "tagline": "您开启职业生涯的 AI 助手",
        "description": "智能找工作 | 面试准备 | 免费证书课程",
        "job_finder": "职位搜索",
        "interview_prep": "面试准备",
        "free_courses": "免费课程",
        "find_jobs": "查找工作",
        "generate_link": "生成面试准备链接",
        "find_courses": "查找课程",
        "job_title": "职位名称 / 关键词",
        "location": "首选地点",
        "country": "国家",
        "experience": "经验水平",
        "date_posted": "发布时间",
        "search_course": "课程 / 技能 / 职位搜索",
        "experience_options": ["任何", "初级", "中级", "高级", "专家"],
        "date_posted_options": ["任何时间", "过去一个月", "过去一周", "过去24小时"]
    }
}

# Combine language data for fallback
lang = st.sidebar.selectbox("🌐 Language", list(LANGUAGES.keys()), index=0)
t = TRANSLATIONS.get(LANGUAGES[lang], TRANSLATIONS["en"])

# ----------------- PAGE SETUP -----------------
st.set_page_config(page_title=t["title"], page_icon="🌟", layout="centered")
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

# ----------------- BRANDING -----------------
st.markdown(f"<div style='text-align:center'><h1>{t['title']}</h1><p>{t['tagline']}</p><small>{t['description']}</small></div>", unsafe_allow_html=True)

# ----------------- TABS -----------------
tab1, tab2, tab3 = st.tabs([f"🌐 {t['job_finder']}", f"🎯 {t['interview_prep']}", f"🎓 {t['free_courses']}"])
