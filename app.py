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

# ----------------- TAB 1: JOB FINDER -----------------
with tab1:
    st.subheader("🌍 Smart Job Links by Country")

    keyword = st.text_input(t["job_title"], "Data Scientist")
    location = st.text_input(t["location"], "Remote")
    experience = st.selectbox(t["experience"], t["experience_options"])
    date_posted = st.selectbox(t["date_posted"], t["date_posted_options"])
    country = st.selectbox(t["country"], [
        "India", "USA", "UK", "UAE", "Germany", "Australia", "New Zealand",
        "Japan", "China", "Russia", "Singapore", "Malaysia"
    ])

    # Filter mappings
    time_map = {
        "Any time": "", "Past month": "r2592000",
        "Past week": "r604800", "Past 24 hours": "r86400"
    }
    exp_map = {
        "Any": "", "Entry": "2", "Mid": "3", "Senior": "4", "Executive": "5"
    }
    d_filter = time_map[date_posted]
    e_filter = exp_map[experience]

    if st.button(t["find_jobs"]):
        st.subheader(f"🔗 Job Portals in {country}")

        portals = {
            "India": [
                ("LinkedIn", f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}&f_E={e_filter}&f_TPR={d_filter}"),
                ("Indeed", f"https://in.indeed.com/jobs?q={keyword}&l={location}"),
                ("Naukri", f"https://www.naukri.com/{keyword.lower().replace(' ', '-')}-jobs-in-{location.lower().replace(' ', '-')}"),
                ("Shine", f"https://www.shine.com/job-search/{keyword.lower().replace(' ', '-')}-jobs-in-{location.lower().replace(' ', '-')}"),
            ],
            "USA": [
                ("LinkedIn", f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}&f_E={e_filter}&f_TPR={d_filter}"),
                ("Indeed", f"https://www.indeed.com/jobs?q={keyword}&l={location}"),
                ("USAJobs", f"https://www.usajobs.gov/Search/Results?k={keyword}&l={location}"),
                ("Monster", f"https://www.monster.com/jobs/search/?q={keyword}&where={location}"),
            ],
            "UK": [
                ("LinkedIn", f"https://uk.linkedin.com/jobs/search/?keywords={keyword}&location={location}"),
                ("Indeed", f"https://uk.indeed.com/jobs?q={keyword}&l={location}"),
                ("Reed", f"https://www.reed.co.uk/jobs/{keyword.lower().replace(' ', '-')}-jobs-in-{location.lower().replace(' ', '-')}"),
                ("TotalJobs", f"https://www.totaljobs.com/jobs/{keyword.lower().replace(' ', '-')}/in-{location.lower().replace(' ', '-')}")
            ],
            "UAE": [
                ("LinkedIn", f"https://ae.linkedin.com/jobs/search/?keywords={keyword}&location={location}"),
                ("Bayt", f"https://www.bayt.com/en/uae/jobs/{keyword.lower().replace(' ', '-')}-jobs-in-{location.lower().replace(' ', '-')}"),
                ("GulfTalent", f"https://www.gulftalent.com/uae/jobs/title/{keyword.lower().replace(' ', '-')}"),
                ("NaukriGulf", f"https://www.naukrigulf.com/{keyword.lower().replace(' ', '-')}-jobs-in-{location.lower().replace(' ', '-')}"),
            ],
            "Germany": [
                ("LinkedIn", f"https://de.linkedin.com/jobs/search/?keywords={keyword}&location={location}"),
                ("StepStone", f"https://www.stepstone.de/jobs/{keyword.lower().replace(' ', '-')}/in-{location.lower().replace(' ', '-')}.html"),
                ("Monster DE", f"https://www.monster.de/jobs/suche/?q={keyword}&where={location}"),
                ("XING", f"https://www.xing.com/jobs/search?q={keyword}"),
            ],
            "Australia": [
                ("LinkedIn", f"https://au.linkedin.com/jobs/search/?keywords={keyword}&location={location}"),
                ("Seek", f"https://www.seek.com.au/{keyword.lower().replace(' ', '-')}-jobs/in-{location.lower().replace(' ', '-')}"),
                ("Adzuna", f"https://www.adzuna.com.au/search?q={keyword}&loc={location}"),
                ("CareerOne", f"https://www.careerone.com.au/jobs?q={keyword}&where={location}"),
            ],
            "New Zealand": [
                ("Seek NZ", f"https://www.seek.co.nz/{keyword.lower().replace(' ', '-')}-jobs/in-{location.lower().replace(' ', '-')}"),
                ("TradeMe", f"https://www.trademe.co.nz/a/jobs/search?search_string={keyword}"),
                ("MyJobSpace", f"https://www.myjobspace.co.nz/jobs?q={keyword}"),
                ("Indeed NZ", f"https://nz.indeed.com/jobs?q={keyword}&l={location}"),
            ],
            "Singapore": [
                ("LinkedIn", f"https://sg.linkedin.com/jobs/search/?keywords={keyword}&location={location}"),
                ("JobStreet", f"https://www.jobstreet.com.sg/en/job-search/{keyword.lower().replace(' ', '-')}-jobs-in-{location.lower().replace(' ', '-')}"),
                ("JobsCentral", f"https://jobscentral.com.sg/search/{keyword}"),
                ("FastJobs", f"https://www.fastjobs.sg/singapore-job-ad/{keyword}"),
            ],
            "Malaysia": [
                ("LinkedIn", f"https://my.linkedin.com/jobs/search/?keywords={keyword}&location={location}"),
                ("JobStreet MY", f"https://www.jobstreet.com.my/en/job-search/{keyword.lower().replace(' ', '-')}-jobs-in-{location.lower().replace(' ', '-')}"),
                ("Indeed MY", f"https://my.indeed.com/jobs?q={keyword}&l={location}"),
                ("Jobstore", f"https://www.jobstore.com/my/browse/{keyword.lower().replace(' ', '-')}-jobs-in-{location.lower().replace(' ', '-')}"),
            ],
            "Japan": [
                ("LinkedIn", f"https://jp.linkedin.com/jobs/search/?keywords={keyword}&location={location}"),
                ("Daijob", f"https://www.daijob.com/en/jobs/search?keyword={keyword}"),
                ("Jobs in Japan", f"https://jobsinjapan.com/jobs/?search={keyword}"),
                ("GaijinPot", f"https://jobs.gaijinpot.com/index/index/search?keywords={keyword}"),
            ],
            "China": [
                ("LinkedIn", f"https://cn.linkedin.com/jobs/search/?keywords={keyword}&location={location}"),
                ("51Job", f"https://search.51job.com/list/000000,000000,0000,00,9,99,{keyword},2,1.html"),
                ("Zhaopin", f"https://sou.zhaopin.com/?jl=530&kw={keyword}"),
                ("Liepin", f"https://www.liepin.com/zhaopin/?key={keyword}"),
            ],
            "Russia": [
                ("LinkedIn", f"https://ru.linkedin.com/jobs/search/?keywords={keyword}&location={location}"),
                ("hh.ru", f"https://hh.ru/search/vacancy?text={keyword}&area=113"),
                ("SuperJob", f"https://www.superjob.ru/vacancy/search/?keywords={keyword}"),
                ("Rabota", f"https://www.rabota.ru/vacancy?query={keyword}"),
            ],
        }

        for name, url in portals.get(country, []):
            st.markdown(f"🔹 [{name}]({url})")

        # Google Jobs fallback
        g_url = f"https://www.google.com/search?q={urllib.parse.quote(keyword + ' jobs in ' + location)}"
        st.markdown(f"\n🌐 [Search on Google Jobs]({g_url})")

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
