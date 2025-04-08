
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

# ------------------ JOB FINDER TAB ------------------
st.header("🌐 " + t['job_finder'])

keyword = st.text_input(t["job_title"], "Data Scientist")
location = st.text_input(t["location"], "Remote")
experience = st.selectbox(t["experience"], t["experience_options"])
date_posted = st.selectbox(t["date_posted"], t["date_posted_options"])
country = st.selectbox(t["country"], [
    "India", "USA", "UK", "UAE", "Germany", "Australia", "New Zealand",
    "Singapore", "Malaysia", "Japan", "China", "Russia"
])

time_map = {
    "Any time": "", "Past month": "r2592000",
    "Past week": "r604800", "Past 24 hours": "r86400"
}
exp_map = {
    "Any": "", "Entry": "2", "Mid": "3", "Senior": "4", "Executive": "5"
}
d_filter = time_map[date_posted]
e_filter = exp_map[experience]

PORTALS = {
    "India": [
        ("LinkedIn", lambda k, l: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_E={e_filter}&f_TPR={d_filter}"),
        ("Naukri", lambda k, l: f"https://www.naukri.com/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-') if l != 'Remote' else 'india'}"),
        ("Shine", lambda k, l: f"https://www.shine.com/job-search/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("TimesJobs", lambda k, l: f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&txtKeywords={urllib.parse.quote(k)}&txtLocation={urllib.parse.quote(l)}")
    ],
    "USA": [
        ("LinkedIn", lambda k, l: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_E={e_filter}&f_TPR={d_filter}"),
        ("Indeed", lambda k, l: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("USAJobs", lambda k, l: f"https://www.usajobs.gov/Search/Results?k={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Monster", lambda k, l: f"https://www.monster.com/jobs/search/?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}")
    ],
    "UK": [
        ("LinkedIn", lambda k, l: f"https://uk.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_E={e_filter}&f_TPR={d_filter}"),
        ("Indeed", lambda k, l: f"https://uk.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Reed", lambda k, l: f"https://www.reed.co.uk/jobs/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("TotalJobs", lambda k, l: f"https://www.totaljobs.com/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}")
    ],
    "UAE": [
        ("LinkedIn", lambda k, l: f"https://ae.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_E={e_filter}&f_TPR={d_filter}"),
        ("Bayt", lambda k, l: f"https://www.bayt.com/en/uae/jobs/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("NaukriGulf", lambda k, l: f"https://www.naukrigulf.com/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("GulfTalent", lambda k, l: f"https://www.gulftalent.com/uae/jobs/title/{k.lower().replace(' ', '-')}")
    ],
    "Germany": [
        ("LinkedIn", lambda k, l: f"https://de.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_E={e_filter}&f_TPR={d_filter}"),
        ("StepStone", lambda k, l: f"https://www.stepstone.de/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}.html"),
        ("XING", lambda k, l: f"https://www.xing.com/jobs/search?q={urllib.parse.quote(k)}"),
        ("Monster DE", lambda k, l: f"https://www.monster.de/jobs/suche/?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}")
    ],
    "Australia": [
        ("LinkedIn", lambda k, l: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_E={e_filter}&f_TPR={d_filter}"),
        ("Seek", lambda k, l: f"https://www.seek.com.au/{k.lower().replace(' ', '-')}-jobs/in-{l.lower().replace(' ', '-')}"),
        ("Adzuna", lambda k, l: f"https://www.adzuna.com.au/search?q={urllib.parse.quote(k)}&loc={urllib.parse.quote(l)}"),
        ("CareerOne", lambda k, l: f"https://www.careerone.com.au/jobs?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}")
    ],
    "New Zealand": [
        ("Seek NZ", lambda k, l: f"https://www.seek.co.nz/{k.lower().replace(' ', '-')}-jobs/in-{l.lower().replace(' ', '-')}"),
        ("TradeMe", lambda k, l: f"https://www.trademe.co.nz/a/jobs/search?search_string={urllib.parse.quote(k)}"),
        ("MyJobSpace", lambda k, l: f"https://www.myjobspace.co.nz/jobs?q={urllib.parse.quote(k)}"),
        ("JobMonster", lambda k, l: f"https://nz.jobmonster.com/?s={urllib.parse.quote(k)}")
    ],
    "Singapore": [
        ("LinkedIn", lambda k, l: f"https://sg.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_E={e_filter}&f_TPR={d_filter}"),
        ("JobsDB", lambda k, l: f"https://sg.jobsdb.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("FastJobs", lambda k, l: f"https://www.fastjobs.sg/search?search={urllib.parse.quote(k)}"),
        ("JobStreet", lambda k, l: f"https://www.jobstreet.com.sg/en/job-search/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}")
    ],
    "Malaysia": [
        ("LinkedIn", lambda k, l: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_E={e_filter}&f_TPR={d_filter}"),
        ("JobStreet", lambda k, l: f"https://www.jobstreet.com.my/en/job-search/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("Indeed", lambda k, l: f"https://malaysia.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Jobstore", lambda k, l: f"https://www.jobstore.com/my/search-jobs?keyword={urllib.parse.quote(k)}")
    ],
    "Japan": [
        ("LinkedIn", lambda k, l: f"https://jp.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Daijob", lambda k, l: f"https://www.daijob.com/en/jobs/search?keyword={urllib.parse.quote(k)}"),
        ("Jobs in Japan", lambda k, l: f"https://jobsinjapan.com/jobs/?search={urllib.parse.quote(k)}"),
        ("GaijinPot", lambda k, l: f"https://jobs.gaijinpot.com/index/index/search?keywords={urllib.parse.quote(k)}")
    ],
    "China": [
        ("51Job", lambda k, l: f"https://search.51job.com/list/000000,000000,0000,00,9,99,{urllib.parse.quote(k)},2,1.html"),
        ("Zhaopin", lambda k, l: f"https://sou.zhaopin.com/?jl=530&kw={urllib.parse.quote(k)}"),
        ("Liepin", lambda k, l: f"https://www.liepin.com/zhaopin/?key={urllib.parse.quote(k)}"),
        ("JobLeadChina", lambda k, l: f"https://jobleadchina.com/job-search/?keywords={urllib.parse.quote(k)}")
    ],
    "Russia": [
        ("hh.ru", lambda k, l: f"https://hh.ru/search/vacancy?text={urllib.parse.quote(k)}&area=113"),
        ("SuperJob", lambda k, l: f"https://www.superjob.ru/vacancy/search/?keywords={urllib.parse.quote(k)}"),
        ("Rabota.ru", lambda k, l: f"https://www.rabota.ru/vacancy?query={urllib.parse.quote(k)}"),
        ("JobLab", lambda k, l: f"https://www.joblab.ru/search.php?keywords={urllib.parse.quote(k)}")
    ]
}

if st.button(t["find_jobs"]):
    st.subheader(f"🔗 Job Links for {country}")
    for name, url_func in PORTALS.get(country, []):
        link = url_func(keyword, location)
        st.markdown(f"[{name}]({link})")

    google_url = f"https://www.google.com/search?q={urllib.parse.quote(keyword + ' jobs in ' + location)}"
    st.markdown(f"[Google Jobs]({google_url})")

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
