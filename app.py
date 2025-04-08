import streamlit as st
import urllib.parse

# ---------------- LANGUAGE SUPPORT ----------------
LANGUAGES = {
    "English": "en", "Hindi": "hi", "Tamil": "ta", "Telugu": "te",
    "Malayalam": "ml", "Kannada": "kn", "Mandarin": "zh", "Japanese": "ja",
    "German": "de", "French": "fr", "Arabic": "ar"
}

TRANSLATIONS = {
    "en": {
        "title": "CareerUpskillers | AI Job Hub",
        "tagline": "Your AI-powered career launchpad",
        "description": "Smart Job Search | Interview Prep | Free Certifications",
        "job_finder": "Job Finder", "interview_prep": "Interview Preparation", "free_courses": "Free Courses",
        "find_jobs": "Find Jobs", "generate_link": "Generate Interview Prep Link", "find_courses": "Find Courses",
        "job_title": "Job Title / Keywords", "location": "Preferred Location", "country": "Country",
        "experience": "Experience Level", "date_posted": "Date Posted",
        "search_course": "Search Course / Skill / Job Title",
        "experience_options": ["Any", "Entry", "Mid", "Senior", "Executive"],
        "date_posted_options": ["Any time", "Past month", "Past week", "Past 24 hours"],
    },
    "hi": {
        "title": "कैरियर अपस्किलर्स | एआई जॉब हब", "tagline": "आपका एआई-संचालित करियर लॉन्चपैड",
        "description": "स्मार्ट जॉब खोज | इंटरव्यू तैयारी | मुफ्त प्रमाणपत्र",
        "job_finder": "नौकरी खोजें", "interview_prep": "इंटरव्यू तैयारी", "free_courses": "नि:शुल्क पाठ्यक्रम",
        "find_jobs": "नौकरी ढूंढें", "generate_link": "इंटरव्यू लिंक बनाएँ", "find_courses": "पाठ्यक्रम ढूंढें",
        "job_title": "नौकरी शीर्षक / कीवर्ड", "location": "पसंदीदा स्थान", "country": "देश",
        "experience": "अनुभव स्तर", "date_posted": "पोस्ट की तारीख",
        "search_course": "कोर्स / स्किल / नौकरी शीर्षक खोजें",
        "experience_options": ["कोई भी", "प्रवेश स्तर", "मध्यम", "वरिष्ठ", "कार्यकारी"],
        "date_posted_options": ["कभी भी", "पिछला महीना", "पिछला सप्ताह", "पिछले 24 घंटे"],
    },
    # Add other languages if needed
}

# ---------------- SETUP ----------------
st.set_page_config(page_title="CareerUpskillers | AI Job Hub", page_icon="🌟", layout="centered")
lang = st.sidebar.selectbox("🌐 Select Language", list(LANGUAGES.keys()))
t = TRANSLATIONS.get(LANGUAGES[lang], TRANSLATIONS["en"])

# Branding
st.markdown(f"<h1 style='text-align:center'>{t['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center'>{t['tagline']}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center'>{t['description']}</p>", unsafe_allow_html=True)

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs([f"🌍 {t['job_finder']}", f"🧠 {t['interview_prep']}", f"🎓 {t['free_courses']}"])

# ---------------- TAB 1: JOB FINDER ----------------
with tab1:
    st.subheader(f"🌍 {t['job_finder']}")
    keyword = st.text_input(t["job_title"], "Data Scientist")
    location = st.text_input(t["location"], "Remote")
    experience = st.selectbox(t["experience"], t["experience_options"])
    date_posted = st.selectbox(t["date_posted"], t["date_posted_options"])
    country = st.selectbox(t["country"], [
        "India", "USA", "UK", "UAE", "Germany", "Australia", "New Zealand",
        "Japan", "China", "Russia", "Singapore", "Malaysia"
    ])
    if st.button(f"🔍 {t['find_jobs']}"):
        time_map = {
            t["date_posted_options"][0]: "",
            t["date_posted_options"][1]: "r2592000",
            t["date_posted_options"][2]: "r604800",
            t["date_posted_options"][3]: "r86400"
        }
        exp_map = {
            t["experience_options"][0]: "",
            t["experience_options"][1]: "entry",
            t["experience_options"][2]: "mid",
            t["experience_options"][3]: "senior",
            t["experience_options"][4]: "executive"
        }
        d_filter = time_map[date_posted]
        e_filter = exp_map[experience]
        st.markdown("### 🔗 Job Portals:")
        portals = [
            ("LinkedIn", f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(keyword)}&location={urllib.parse.quote(location)}&f_E={e_filter}&f_TPR={d_filter}"),
            ("Indeed", f"https://www.indeed.com/jobs?q={urllib.parse.quote(keyword)}&l={urllib.parse.quote(location)}&explvl={e_filter}"),
            ("Monster", f"https://www.monster.com/jobs/search/?q={urllib.parse.quote(keyword)}&where={urllib.parse.quote(location)}"),
            ("Google Jobs", f"https://www.google.com/search?q={urllib.parse.quote(keyword + ' jobs in ' + location)}")
        ]
        for name, url in portals:
            st.markdown(f"<a href='{url}' target='_blank' style='display:block; padding:10px; margin:5px; background:#4CAF50; color:white; border-radius:5px; text-decoration:none;'>🔗 {name}</a>", unsafe_allow_html=True)

# ---------------- TAB 2: INTERVIEW PREP ----------------
with tab2:
    st.subheader(f"🧠 {t['interview_prep']}")
    role = st.text_input(t["job_title"], "Software Engineer")
    company = st.text_input("Company", "Google")
    prep_type = st.selectbox("Prep Type", ["Technical", "Behavioral", "Case Study", "HR", "Salary Negotiation"])
    if st.button(f"🎯 {t['generate_link']}"):
        query = f"{role} interview questions {prep_type} {company}"
        st.markdown(f"[🔍 Google Search](https://www.google.com/search?q={urllib.parse.quote_plus(query)})", unsafe_allow_html=True)
        st.markdown(f"[🎥 YouTube Videos](https://www.youtube.com/results?search_query={urllib.parse.quote_plus(query)})", unsafe_allow_html=True)
        st.markdown(f"[📄 PDF Guides](https://www.google.com/search?q={urllib.parse.quote_plus(query)}+filetype:pdf)", unsafe_allow_html=True)

# ---------------- TAB 3: FREE COURSES ----------------
with tab3:
    st.subheader(f"🎓 {t['free_courses']}")
    course = st.text_input(t["search_course"], "Machine Learning")
    if st.button(f"🎓 {t['find_courses']}"):
        platforms = {
            "Google": f"https://grow.google/certificates/?q={urllib.parse.quote_plus(course)}",
            "IBM": f"https://skillsbuild.org/learn?search={urllib.parse.quote_plus(course)}",
            "AWS": f"https://explore.skillbuilder.aws/learn?searchTerm={urllib.parse.quote_plus(course)}",
            "Microsoft": "https://learn.microsoft.com/en-us/training/",
            "LinkedIn Learning": "https://www.linkedin.com/learning/",
            "YouTube": f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(course)}+free+course"
        }
        for name, url in platforms.items():
            st.markdown(f"<a href='{url}' target='_blank' style='display:block; background:#6366f1; color:white; padding:10px; border-radius:5px; margin-bottom:5px;'>📘 {name}</a>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
---
<div style='text-align:center; font-size:14px;'>
    🚀 Built by <b>CareerUpskillers</b> • 
    <a href='https://www.linkedin.com/company/careerupskillers' target='_blank'>LinkedIn</a> • 
    <a href='https://instagram.com/careerupskillers' target='_blank'>Instagram</a>
</div>
""", unsafe_allow_html=True)
