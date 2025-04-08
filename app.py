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

    PORTALS_BY_COUNTRY = {
        "India": [
            ("LinkedIn", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
            ("Naukri", lambda k, l, e, d: f"https://www.naukri.com/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-') if l != 'Remote' else 'india'}"),
            ("Indeed", lambda k, l, e, d: f"https://www.indeed.co.in/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
            ("Shine", lambda k, l, e, d: f"https://www.shine.com/job-search/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}")
        ],
        "USA": [
            ("LinkedIn", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
            ("USAJobs", lambda k, l, e, d: f"https://www.usajobs.gov/Search/Results?k={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
            ("Indeed", lambda k, l, e, d: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
            ("Monster", lambda k, l, e, d: f"https://www.monster.com/jobs/search/?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}")
        ],
        "UK": [
            ("LinkedIn", lambda k, l, e, d: f"https://uk.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
            ("Reed", lambda k, l, e, d: f"https://www.reed.co.uk/jobs/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
            ("TotalJobs", lambda k, l, e, d: f"https://www.totaljobs.com/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}"),
            ("CV-Library", lambda k, l, e, d: f"https://www.cv-library.co.uk/search-jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}")
        ],
        "UAE": [
            ("LinkedIn", lambda k, l, e, d: f"https://ae.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
            ("Bayt", lambda k, l, e, d: f"https://www.bayt.com/en/uae/jobs/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
            ("NaukriGulf", lambda k, l, e, d: f"https://www.naukrigulf.com/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
            ("GulfTalent", lambda k, l, e, d: f"https://www.gulftalent.com/uae/jobs/title/{k.lower().replace(' ', '-')}")
        ],
        "Germany": [
            ("LinkedIn", lambda k, l, e, d: f"https://de.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
            ("StepStone", lambda k, l, e, d: f"https://www.stepstone.de/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}.html"),
            ("XING", lambda k, l, e, d: f"https://www.xing.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
            ("Monster DE", lambda k, l, e, d: f"https://www.monster.de/jobs/suche/?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}")
        ],
        "Australia": [
            ("LinkedIn", lambda k, l, e, d: f"https://au.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
            ("Seek", lambda k, l, e, d: f"https://www.seek.com.au/{k.lower().replace(' ', '-')}-jobs/in-{l.lower().replace(' ', '-')}"),
            ("Adzuna", lambda k, l, e, d: f"https://www.adzuna.com.au/search?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}"),
            ("CareerOne", lambda k, l, e, d: f"https://www.careerone.com.au/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}")
        ],
        "New Zealand": [
            ("Seek NZ", lambda k, l, e, d: f"https://www.seek.co.nz/{k.lower().replace(' ', '-')}-jobs/in-{l.lower().replace(' ', '-')}"),
            ("TradeMe Jobs", lambda k, l, e, d: f"https://www.trademe.co.nz/jobs?q={urllib.parse.quote(k)}"),
            ("MyJobSpace", lambda k, l, e, d: f"https://www.myjobspace.co.nz/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}")
        ],
        "Russia": [
            ("hh.ru", lambda k, l, e, d: f"https://hh.ru/search/vacancy?text={urllib.parse.quote(k)}&area=113"),
            ("SuperJob", lambda k, l, e, d: f"https://www.superjob.ru/vacancy/search/?keywords={urllib.parse.quote(k)}"),
            ("Rabota.ru", lambda k, l, e, d: f"https://www.rabota.ru/vacancy?query={urllib.parse.quote(k)}")
        ],
        "China": [
            ("51Job", lambda k, l, e, d: f"https://search.51job.com/list/000000,000000,0000,00,9,99,{urllib.parse.quote(k)},2,1.html"),
            ("Zhaopin", lambda k, l, e, d: f"https://sou.zhaopin.com/?jl=530&kw={urllib.parse.quote(k)}"),
            ("Liepin", lambda k, l, e, d: f"https://www.liepin.com/zhaopin/?key={urllib.parse.quote(k)}")
        ],
        "Japan": [
            ("Daijob", lambda k, l, e, d: f"https://www.daijob.com/en/jobs/search?keyword={urllib.parse.quote(k)}"),
            ("Jobs in Japan", lambda k, l, e, d: f"https://jobsinjapan.com/jobs/?search={urllib.parse.quote(k)}"),
            ("GaijinPot", lambda k, l, e, d: f"https://jobs.gaijinpot.com/job/index/lang/en/search/{urllib.parse.quote(k)}")
        ]
    }

    with st.form("job_form"):
        col1, col2 = st.columns(2)
        with col1:
            keyword = st.text_input(t["job_title"], "Data Scientist")
            location = st.text_input(t["location"], "Remote")
            manual_mode = st.checkbox("Manually select country", value=True)
            if manual_mode:
                # Replaced by manual/auto-detect mode above
            else:
                import geocoder
                user_location = geocoder.ip('me')
                country = user_location.country if user_location and user_location.country in PORTALS_BY_COUNTRY else "India"
                st.markdown(f"**🌍 Detected Country:** {country}")
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

        st.subheader(f"🔗 Job Search Links in {country}")
        for name, url_func in PORTALS_BY_COUNTRY[country]:
            url = url_func(keyword, location, e_filter, d_filter)
            icon = f"https://logo.clearbit.com/{name.lower().replace(' ', '')}.com"
            st.markdown(f"""
            <a href="{url}" target="_blank" style="display:flex; align-items:center; gap:10px; padding:10px 20px; background:#4CAF50; color:white; border-radius:5px; text-decoration:none; margin-bottom:5px;">
                <img src="{icon}" alt="{name}" style="width:24px; height:24px; border-radius:4px;"> 🔍 {name}
            </a>
            """, unsafe_allow_html=True)
            <a href="{url}" target="_blank" style="display:inline-block; padding:10px 20px; background:#4CAF50; color:white; border-radius:5px; text-decoration:none; margin-bottom:5px;">
                🔍 Search on {name}
            </a>
            """, unsafe_allow_html=True)

        # Add Google Jobs at the end for all countries
        google_jobs_url = f"https://www.google.com/search?q={urllib.parse.quote(keyword + ' jobs in ' + location)}"
        st.markdown(f"""
        <a href="{google_jobs_url}" target="_blank" style="display:inline-block; padding:10px 20px; background:#4285F4; color:white; border-radius:5px; text-decoration:none; margin-bottom:5px;">
            🔍 Search on Google Jobs
        </a>
        """, unsafe_allow_html=True)

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
