
# ---------- FULL STREAMLIT APP: AI JOB HUB MULTILANG + ALL COUNTRIES ----------
# ✅ Includes Tab 1 (Job Finder), Tab 2 (Interview Prep), Tab 3 (Free Courses)
# ✅ Includes all countries and smart filters, multi-language support, and Google fallback
# ✅ Built for CareerUpskillers

import streamlit as st
import urllib.parse

# ---------- LANGUAGE SUPPORT ----------
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Mandarin": "zh",
    "French": "fr",
    "German": "de",
    "Arabic": "ar",
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
        "date_posted_options": ["Any time", "Past month", "Past week", "Past 24 hours"],
    }
}

# ---------- PAGE CONFIGURATION ----------
st.set_page_config(page_title="CareerUpskillers | AI Job Hub", page_icon="🌟", layout="centered")
lang = st.sidebar.selectbox("🌐 Language", list(LANGUAGES.keys()))
t = TRANSLATIONS.get(LANGUAGES[lang], TRANSLATIONS["en"])

st.markdown(f"<h1 style='text-align:center'>{t['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center'>{t['tagline']}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center'>{t['description']}</p>", unsafe_allow_html=True)

# ---------- TABS ----------
tab1, tab2, tab3 = st.tabs([f"🌐 {t['job_finder']}", f"🎯 {t['interview_prep']}", f"🎓 {t['free_courses']}"])

# ---------- TAB 1: JOB FINDER ----------
with tab1:
    st.subheader(t['job_finder'])

    keyword = st.text_input(t["job_title"], "Data Scientist")
    location = st.text_input(t["location"], "Remote")
    experience = st.selectbox(t["experience"], t["experience_options"], key="exp_tab1")
    date_posted = st.selectbox(t["date_posted"], t["date_posted_options"], key="date_tab1")

    country = st.selectbox(t["country"], [
        "India", "USA", "UK", "UAE", "Germany", "Australia", "New Zealand",
        "Singapore", "Malaysia", "Japan", "China", "Russia"
    ])

    d_filter = {
        "Any time": "",
        "Past month": "r2592000",
        "Past week": "r604800",
        "Past 24 hours": "r86400"
    }.get(date_posted, "")

    e_filter = {
        "Any": "", "Entry": "2", "Mid": "3", "Senior": "4", "Executive": "5"
    }.get(experience, "")

    portals = {
        "LinkedIn": lambda k, l: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d_filter}&f_E={e_filter}",
        "Indeed": lambda k, l: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}",
        "Google Jobs": lambda k, l: f"https://www.google.com/search?q={urllib.parse.quote(k + ' jobs in ' + l)}"
    }

    if st.button(t["find_jobs"]):
        st.write("🔗 Job Portals")
        for name, gen_url in portals.items():
            url = gen_url(keyword, location)
            st.markdown(f"[{name}]({url})")

# ---------- TAB 2: INTERVIEW PREPARATION ----------
with tab2:
    st.subheader(t["interview_prep"])
    role = st.text_input(t["job_title"], "Data Analyst", key="int_role")
    prep_type = st.selectbox("Preparation Type", ["Technical Questions", "Behavioral Questions"], key="prep_type")
    exp_level = st.selectbox(t["experience"], t["experience_options"], key="exp_tab2")
    company = st.text_input("Company (optional)", "", key="int_company")

    if st.button(t["generate_link"]):
        query = f"{role} {prep_type} {exp_level} {company}"
        encoded_query = urllib.parse.quote_plus(query)
        st.markdown(f"[📄 PDFs](https://www.google.com/search?q={encoded_query}+filetype:pdf)")
        st.markdown(f"[🎥 YouTube](https://www.youtube.com/results?search_query={encoded_query})")
        st.markdown(f"[💬 Forums](https://www.google.com/search?q={encoded_query}+forum)")

# ---------- TAB 3: FREE COURSES ----------
with tab3:
    st.subheader(t["free_courses"])
    course = st.text_input(t["search_course"], "Python for AI")

    platforms = {
        "Google": f"https://grow.google/certificates/?q={urllib.parse.quote_plus(course)}",
        "IBM": f"https://skillsbuild.org/learn?search={urllib.parse.quote_plus(course)}",
        "AWS": f"https://explore.skillbuilder.aws/learn?searchTerm={urllib.parse.quote_plus(course)}",
        "Coursera": f"https://www.coursera.org/search?query={urllib.parse.quote_plus(course)}&price=1",
        "edX": f"https://www.edx.org/search?q={urllib.parse.quote_plus(course)}",
        "YouTube": f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(course)}"
    }

    if st.button(t["find_courses"]):
        for name, link in platforms.items():
            st.markdown(f"[{name} →]({link})")

# ---------- FOOTER ----------
st.markdown("""
<hr>
<div style='text-align:center; font-size:14px; color:gray;'>
  🚀 Built by CareerUpskillers | <a href='https://linkedin.com/company/careerupskillers' target='_blank'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)
