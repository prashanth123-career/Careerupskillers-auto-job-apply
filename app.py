# CareerUpskillers | AI Job Hub
# Full Streamlit Script with 3 Tabs: Job Finder, Interview Prep, Free Courses (with all countries and categories)

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
    }
}

# ----------------- SETUP -----------------
st.set_page_config(page_title="CareerUpskillers | AI Job Hub", page_icon="🌟", layout="centered")

# Language selection
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

# ----------------- TAB 1: JOB FINDER -----------------
with tab1:
    st.header(f"🌐 {t['job_finder']}")
    with st.form("job_form"):
        col1, col2 = st.columns(2)
        with col1:
            keyword = st.text_input(t["job_title"], "Data Scientist")
            location = st.text_input(t["location"], "Remote")
            country = st.selectbox(t["country"], ["India", "USA", "UK", "UAE", "Germany", "Australia", "New Zealand", "Russia", "China", "Japan"])
        with col2:
            experience = st.selectbox(t["experience"], t["experience_options"])
            date_posted = st.selectbox(t["date_posted"], t["date_posted_options"])
        submitted = st.form_submit_button(f"🔍 {t['find_jobs']}")

    if submitted:
        time_map = {
            t["date_posted_options"][0]: "",
            t["date_posted_options"][1]: "r2592000",
            t["date_posted_options"][2]: "r604800",
            t["date_posted_options"][3]: "r86400"
        }
        exp_map = {
            t["experience_options"][0]: "",
            t["experience_options"][1]: "2",
            t["experience_options"][2]: "3",
            t["experience_options"][3]: "4",
            t["experience_options"][4]: "5"
        }
        d_filter = time_map[date_posted]
        e_filter = exp_map[experience]

        portals = {
            "India": ["LinkedIn", "Naukri", "Shine", "Indeed"],
            "USA": ["LinkedIn", "USAJobs", "Indeed"],
            "UK": ["LinkedIn", "Reed", "TotalJobs"],
            "UAE": ["LinkedIn", "Bayt", "NaukriGulf"],
            "Germany": ["LinkedIn", "StepStone"],
            "Australia": ["LinkedIn", "Seek", "Indeed"],
            "New Zealand": ["LinkedIn", "Seek NZ", "TradeMe Jobs"],
            "Russia": ["hh.ru", "SuperJob"],
            "China": ["51Job", "Zhaopin"],
            "Japan": ["Daijob", "Jobs in Japan"]
        }

        st.subheader(f"🔗 Top Job Portals in {country}")
        for portal in portals.get(country, []):
            url = f"https://www.google.com/search?q={urllib.parse.quote(keyword + ' site:' + portal)}+jobs+in+{urllib.parse.quote(location)}"
            st.markdown(f"<a href='{url}' target='_blank' style='display:block; padding:10px; background:#4CAF50; color:white; border-radius:5px; margin-bottom:5px;'>🔍 {portal}</a>", unsafe_allow_html=True)

# ----------------- TAB 2: INTERVIEW PREPARATION -----------------
with tab2:
    st.header(f"🎯 {t['interview_prep']}")
    with st.form("interview_form"):
        role = st.text_input(t["job_title"], "Data Analyst")
        country = st.selectbox(t["country"], ["India", "USA", "UK", "Canada"])
        company = st.text_input("Target Company (optional)", placeholder="Google, TCS, etc.")
        prep_type = st.selectbox("Preparation Type", ["Technical Questions", "Behavioral Questions", "Case Studies", "Salary Negotiation", "Resume Tips"])
        submitted = st.form_submit_button(f"🔗 {t['generate_link']}")

    if submitted:
        query = f"{role} {prep_type} {company} {country} interview"
        encoded = urllib.parse.quote_plus(query)
        st.markdown(f"""
        <h4>🎯 Recommended Resources</h4>
        <ul>
        <li><a href='https://www.google.com/search?q={encoded}+filetype:pdf' target='_blank'>📄 PDF Guides</a></li>
        <li><a href='https://www.google.com/search?q={encoded}+site:youtube.com' target='_blank'>🎥 YouTube Tutorials</a></li>
        <li><a href='https://www.google.com/search?q={encoded}+forum' target='_blank'>💬 Forums & Discussions</a></li>
        </ul>
        """, unsafe_allow_html=True)

# ----------------- TAB 3: FREE COURSES -----------------
with tab3:
    st.header(f"🎓 {t['free_courses']}")
    with st.form("course_form"):
        search = st.text_input(t["search_course"], "Python, AutoCAD, Finance...")
        submitted = st.form_submit_button(f"🎯 {t['find_courses']}")

    if submitted:
        query = urllib.parse.quote_plus(search)
        st.subheader("🌐 Free Course Platforms")
        platforms = {
            "Google": "https://grow.google/certificates/?q=",
            "IBM": "https://skillsbuild.org/learn?search=",
            "AWS": "https://explore.skillbuilder.aws/learn?searchTerm=",
            "Coursera": "https://www.coursera.org/search?query=",
            "edX": "https://www.edx.org/search?q=",
            "Alison": "https://alison.com/courses?query=",
            "NPTEL": "https://nptel.ac.in/courses",
            "SWAYAM": "https://swayam.gov.in/search?text=",
            "FutureLearn": "https://www.futurelearn.com/search?q=",
            "OpenLearn": "https://www.open.edu/openlearn/search-results?query="
        }
        for name, base in platforms.items():
            full_url = base + query
            st.markdown(f"<a href='{full_url}' target='_blank' style='display:block; padding:10px; background:#1e40af; color:white; border-radius:5px; margin-bottom:5px;'>📘 {name}</a>", unsafe_allow_html=True)

st.markdown("""
<hr style='margin-top:40px;'>
<div style='text-align:center; font-size:16px; color:gray;'>
    🚀 Powered by <strong>CareerUpskillers</strong>
</div>
""", unsafe_allow_html=True)
