import streamlit as st
import urllib.parse
import geocoder

# ----------------- LANGUAGE SUPPORT -----------------
LANGUAGES = {
    "English": "en",
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
}

# ----------------- SETUP -----------------
st.set_page_config(page_title="CareerUpskillers | AI Job Hub", page_icon="🌟", layout="centered")
lang = st.sidebar.selectbox("Select Language", list(LANGUAGES.keys()), index=0)
t = TRANSLATIONS.get(LANGUAGES[lang], TRANSLATIONS["en"])

# Branding
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

    # Filter maps
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

    # Sample country/job portal setup
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
    }

    with st.form("job_form"):
        col1, col2 = st.columns(2)
        with col1:
            keyword = st.text_input(t["job_title"], "Data Scientist")
            location = st.text_input(t["location"], "Remote")
            manual_mode = st.checkbox("Manually select country", value=True)
            if manual_mode:
                country = st.selectbox(t["country"], list(PORTALS_BY_COUNTRY.keys()))
            else:
                g = geocoder.ip('me')
                country = g.country if g and g.country in PORTALS_BY_COUNTRY else "India"
                st.markdown(f"🌍 Detected Country: **{country}**")
        with col2:
            experience = st.selectbox(t["experience"], t["experience_options"])
            date_posted = st.selectbox(t["date_posted"], t["date_posted_options"])
        submitted = st.form_submit_button(t["find_jobs"])

    if submitted:
        d_filter = time_map[date_posted]
        e_filter = exp_map[experience]
        st.subheader(f"🔗 Job Search Links in {country}")
        for name, url_func in PORTALS_BY_COUNTRY[country]:
            url = url_func(keyword, location, e_filter, d_filter)
            st.markdown(
                f'<a href="{url}" target="_blank" style="display:inline-block; padding:10px 20px; background:#4CAF50; color:white; border-radius:5px; text-decoration:none; margin-bottom:5px;">Search on {name}</a>',
                unsafe_allow_html=True
            )
        google_jobs_url = f"https://www.google.com/search?q={urllib.parse.quote(keyword + ' jobs in ' + location)}"
        st.markdown(
            f'<a href="{google_jobs_url}" target="_blank" style="display:inline-block; padding:10px 20px; background:#4285F4; color:white; border-radius:5px; text-decoration:none; margin-bottom:5px;">Search on Google Jobs</a>',
            unsafe_allow_html=True
        )

# ----------------- TAB 2: INTERVIEW PREPARATION -----------------
with tab2:
    st.header(f"🎯 {t['interview_prep']}")
    GOOGLE_SEARCH = lambda query, extra="": f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}{extra}"
    YOUTUBE_SEARCH = lambda query: GOOGLE_SEARCH(query, "+site:youtube.com")
    FORUM_SEARCH = lambda query: GOOGLE_SEARCH(query, "+forum")

    with st.form("interview_form"):
        col1, col2 = st.columns([1, 2])
        with col1:
            role = st.text_input(t["job_title"], "Data Analyst", key="int_role")
            country = st.selectbox(t["country"], ["India", "USA", "UK", "Canada"], key="int_country")
            exp_level = st.selectbox(t["experience"], t["experience_options"])
        with col2:
            prep_type = st.selectbox("Preparation Type", [
                "Technical Questions", "Behavioral Questions",
                "Case Studies", "Salary Negotiation", "Resume Tips"
            ])
            company = st.text_input("Target Company (optional)", placeholder="Google, TCS, etc.")
        submitted = st.form_submit_button(f"🔗 {t['generate_link']}")

    if submitted:
        base_query = f"{role} {prep_type} {exp_level} {company} {country}"
        RESOURCE_MATRIX = {
            "Technical Questions": {
                "India": "https://www.indiabix.com",
                "Global": "https://leetcode.com"
            },
            "Behavioral Questions": {
                "India": "https://www.ambitionbox.com/interviews",
                "Global": "https://www.themuse.com/advice/behavioral-interview-questions"
            }
        }
        main_resource = RESOURCE_MATRIX.get(prep_type, {}).get("India" if country == "India" else "Global")
        if main_resource:
            st.markdown(f"""
            <div style="padding:15px; background:#e8f5e9; border-radius:10px; margin-bottom:20px;">
                <h4>🎯 Recommended Resource</h4>
                <a href="{main_resource}" target="_blank" style="color:#2e7d32;">Best {prep_type} Guide for {country}</a>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="padding:15px; background:#fff3e0; border-radius:10px;">
            <h4>🔎 More Resources</h4>
            <a href="{GOOGLE_SEARCH(base_query, '+filetype:pdf')}" target="_blank">📄 PDF Guides</a><br>
            <a href="{YOUTUBE_SEARCH(base_query)}" target="_blank">🎥 YouTube Videos</a><br>
            <a href="{FORUM_SEARCH(base_query)}" target="_blank">💬 Forums</a>
        </div>
        """, unsafe_allow_html=True)

        checklist_items = {
            "Technical Questions": ["Review core concepts", "Practice coding problems", "Study system design"],
            "Behavioral Questions": ["Prepare STAR stories", "Research company values", "Practice timing"]
        }.get(prep_type, [])
        for item in checklist_items:
            st.checkbox(item, key=f"check_{item}")

# ----------------- TAB 3: FREE COURSES -----------------
with tab3:
    st.header(f"🎓 {t['free_courses']}")
    COURSE_LINKS = {
        "Google": lambda q: f"https://grow.google/certificates/?q={urllib.parse.quote_plus(q)}",
        "IBM": lambda q: f"https://skillsbuild.org/learn?search={urllib.parse.quote_plus(q)}",
        "AWS": lambda q: f"https://explore.skillbuilder.aws/learn?searchTerm={urllib.parse.quote_plus(q)}",
        "Microsoft (LinkedIn)": lambda q: "https://www.linkedin.com/learning/",
        "Meta": lambda q: f"https://www.facebook.com/business/learn/courses?search={urllib.parse.quote_plus(q)}"
    }

    with st.form("course_form"):
        search = st.text_input(t["search_course"], "AI for Business")
        course_submit = st.form_submit_button(f"🎯 {t['find_courses']}")

    if course_submit:
        st.subheader("🧠 Tech Giants")
        for name, url_func in COURSE_LINKS.items():
            course_url = url_func(search)
            st.markdown(
                f"<a href='{course_url}' target='_blank' style='display:block; background:#3b82f6; color:white; padding:10px; border-radius:5px; margin-bottom:5px;'>📘 {name}</a>",
                unsafe_allow_html=True
            )

# ----------------- FOOTER -----------------
st.markdown("""
<hr style='margin-top:40px;'>
<div style='text-align:center; font-size:16px; color:gray;'>
    🚀 Powered by <strong>CareerUpskillers</strong> |
    <a href='https://www.linkedin.com/company/careerupskillers' target='_blank'>LinkedIn</a> • 
    <a href='https://twitter.com/careerupskill' target='_blank'>Twitter</a> • 
    <a href='https://instagram.com/careerupskillers' target='_blank'>Instagram</a> • 
    <a href='https://youtube.com/@careerupskillers' target='_blank'>YouTube</a>
</div>
""", unsafe_allow_html=True)
