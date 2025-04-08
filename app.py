import streamlit as st
import urllib.parse

# ----------------- LANGUAGE SUPPORT -----------------
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Mandarin": "zh",
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
        "date_posted_options": ["Any time", "Past month", "Past week", "Past 24 hours"],
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
        "date_posted_options": ["कभी भी", "पिछला महीना", "पिछला सप्ताह", "पिछले 24 घंटे"],
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

# ----------------- SETUP -----------------
st.set_page_config(page_title="CareerUpskillers | AI Job Hub", page_icon="🌟", layout="centered")
lang = st.sidebar.selectbox("Select Language", list(LANGUAGES.keys()), index=0)
t = TRANSLATIONS.get(LANGUAGES[lang], TRANSLATIONS["en"])

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ----------------- BRANDING -----------------
st.markdown(f"""
<div style='text-align:center; padding:10px 0;'>
    <h1 style='color:#1f2937;'>🚀 {t["title"]}</h1>
    <h4 style='color:#374151;'>{t["tagline"]}</h4>
    <p style='font-size:16px;'>{t["description"]}</p>
</div>
""", unsafe_allow_html=True)

# ----------------- TABS -----------------
tab1, tab2, tab3 = st.tabs([f"🌐 {t['job_finder']}", f"🎯 {t['interview_prep']}", f"🎓 {t['free_courses']}"])

# --------------- SMART MAPPINGS ---------------
time_map = {
    "Any time": "",
    "Past month": "r2592000",
    "Past week": "r604800",
    "Past 24 hours": "r86400"
}

exp_map = {
    "Any": "",
    "Entry": "2",
    "Mid": "3",
    "Senior": "4",
    "Executive": "5"
}

google_search = lambda query, extra="": f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}{extra}"
youtube_search = lambda query: google_search(query, "+site:youtube.com")
forum_search = lambda query: google_search(query, "+forum")

# ----------------- TAB 1: JOB FINDER -----------------
with tab1:
    st.header(f"🌐 {t['job_finder']}")
    keyword = st.text_input(t["job_title"], "Data Scientist")
    location = st.text_input(t["location"], "Remote")
    experience = st.selectbox(t["experience"], t["experience_options"])
    date_posted = st.selectbox(t["date_posted"], t["date_posted_options"])
    country = st.selectbox(t["country"], ["India", "USA"])
    if st.button(t["find_jobs"]):
        d_filter = time_map.get(date_posted, "")
        e_filter = exp_map.get(experience, "")
        st.markdown(f"🔗 Job Links for **{country}**")
        if country == "India":
            st.markdown(f"[LinkedIn](https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(keyword)}&location={urllib.parse.quote(location)}&f_TPR={d_filter}&f_E={e_filter})")
        if country == "USA":
            st.markdown(f"[LinkedIn](https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(keyword)}&location={urllib.parse.quote(location)}&f_TPR={d_filter}&f_E={e_filter})")
        st.markdown(f"[Google Jobs](https://www.google.com/search?q={urllib.parse.quote(keyword + ' jobs in ' + location)})")

# ----------------- TAB 2: INTERVIEW PREPARATION -----------------
with tab2:
    st.header(f"🎯 {t['interview_prep']}")
    role = st.text_input(t["job_title"], "Data Analyst", key="int_role")
    prep_type = st.selectbox("Preparation Type", ["Technical Questions", "Behavioral Questions"])
    exp_level = st.selectbox(t["experience"], t["experience_options"])
    company = st.text_input("Target Company (optional)", "")
    if st.button(t["generate_link"]):
        query = f"{role} {prep_type} {exp_level} {company}"
        st.markdown(f"[PDF Guides]({google_search(query, '+filetype:pdf')})")
        st.markdown(f"[YouTube]({youtube_search(query)})")
        st.markdown(f"[Forums]({forum_search(query)})")

# ----------------- TAB 3: FREE COURSES -----------------
with tab3:
    st.header(f"🎓 {t['free_courses']}")
    search = st.text_input(t["search_course"], "AI for Business")
    if st.button(t["find_courses"]):
        links = {
            "Google": f"https://grow.google/certificates/?q={urllib.parse.quote_plus(search)}",
            "IBM": f"https://skillsbuild.org/learn?search={urllib.parse.quote_plus(search)}",
            "AWS": f"https://explore.skillbuilder.aws/learn?searchTerm={urllib.parse.quote_plus(search)}",
            "Coursera": f"https://www.coursera.org/search?query={urllib.parse.quote_plus(search)}&price=1",
            "YouTube": f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(search)}"
        }
        for name, url in links.items():
            st.markdown(f"[{name} →]({url})")

# ----------------- FOOTER -----------------
st.markdown("""
<hr>
<div style='text-align:center; color:gray;'>
  🚀 Built by <b>CareerUpskillers</b> • 
  <a href='https://linkedin.com/company/careerupskillers' target='_blank'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)
