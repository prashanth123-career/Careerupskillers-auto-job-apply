import streamlit as st
import urllib.parse

# ----------------- SETUP -----------------
st.set_page_config(page_title="CareerUpskillers | AI Job Hub", page_icon="🌟", layout="centered")

# 🔒 Hide Streamlit Default Elements
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ----------------- BRANDING -----------------
st.markdown("""
<div style='text-align:center; padding:10px 0;'>
    <h1 style='color:#1f2937;'>🚀 CareerUpskillers</h1>
    <h4 style='color:#374151;'>Your AI-powered career launchpad</h4>
    <p style='font-size:16px;'>Smart Job Search | Interview Prep | Free Certifications</p>
</div>
""", unsafe_allow_html=True)

# ----------------- TABS (Only 3) -----------------
tab1, tab2, tab3 = st.tabs(["🌐 Job Finder", "🎯 Interview Preparation", "🎓 Free Courses"])

# ----------------- TAB 1: JOB FINDER -----------------
with tab1:
    st.header("🌐 Global Job Finder")

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
            ("Indeed", lambda k, l, e, d: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
        ]
    }

    with st.form("job_form"):
        col1, col2 = st.columns(2)
        with col1:
            keyword = st.text_input("Job Title / Keywords", "Data Scientist")
            location = st.text_input("Preferred Location", "Remote")
            country = st.selectbox("Country", list(PORTALS_BY_COUNTRY.keys()))
        with col2:
            experience = st.selectbox("Experience Level", ["Any", "Entry", "Mid", "Senior", "Executive"])
            date_posted = st.selectbox("Date Posted", ["Any time", "Past month", "Past week", "Past 24 hours"])
        submitted = st.form_submit_button("🔍 Find Jobs")

    if submitted:
        time_map = {
            "Any time": "", "Past month": "r2592000",
            "Past week": "r604800", "Past 24 hours": "r86400"
        }
        exp_map = {
            "Any": "", "Entry": "2", "Mid": "3", "Senior": "4", "Executive": "5"
        }
        d_filter = time_map[date_posted]
        e_filter = exp_map[experience]

        st.subheader(f"🔗 Job Search Links in {country}")
        for name, url_func in PORTALS_BY_COUNTRY[country]:
            url = url_func(keyword, location, e_filter, d_filter)
            st.markdown(f"""
            <a href="{url}" target="_blank" style="display:inline-block; padding:10px 20px; background:#4CAF50; color:white; border-radius:5px; text-decoration:none; margin-bottom:5px;">
                🔍 Search on {name}
            </a>
            """, unsafe_allow_html=True)

# ----------------- TAB 2: INTERVIEW PREPARATION -----------------
with tab2:
    st.header("🎯 Smart Interview Preparation")

    with st.form("interview_form"):
        col1, col2 = st.columns(2)
        with col1:
            role = st.text_input("Job Role", "Data Analyst")
            country = st.selectbox("Country", ["India", "USA", "UK", "Canada", "Germany", "UAE", "Australia"])
        with col2:
            platform = st.selectbox("Choose Platform", [
                "LeetCode", "HackerRank", "GeeksforGeeks", "Glassdoor", "Pramp", 
                "IndiaBix", "AmbitionBox", "Final Round AI", "Big Interview", "iScalePro"
            ])
        interview_submit = st.form_submit_button("🔗 Generate Interview Prep Link")

    if interview_submit:
        query = urllib.parse.quote_plus(role + " " + country)
        PLATFORM_LINKS = {
            "LeetCode": f"https://leetcode.com/problemset/all/?search={query}",
            "HackerRank": f"https://www.hackerrank.com/interview/interview-preparation-kit",
            "GeeksforGeeks": f"https://www.geeksforgeeks.org/?s={query}",
            "Glassdoor": f"https://www.glassdoor.com/Interview/{query}-interview-questions-SRCH_KO0,{len(query)}.htm",
            "Pramp": f"https://www.pramp.com/#interview-prep",
            "IndiaBix": f"https://www.indiabix.com/interview/questions-and-answers/?search={query}",
            "AmbitionBox": f"https://www.ambitionbox.com/interviews?title={query}",
            "Final Round AI": "https://www.finalroundai.com/ai-mock-interview",
            "Big Interview": "https://www.biginterview.com/",
            "iScalePro": "https://www.iscalepro.com/jobseekers/"
        }

        link = PLATFORM_LINKS.get(platform)
        if link:
            st.markdown(f"""
            <a href="{link}" target="_blank" style="display:inline-block; padding:12px 24px; background:#2563eb; color:white; border-radius:5px; text-decoration:none;">
                🚀 Prep on {platform}
            </a>
            """, unsafe_allow_html=True)

# ----------------- TAB 3: FREE COURSES -----------------
with tab3:
    st.header("🎓 Free Courses with Certifications")

    with st.form("course_form"):
        search = st.text_input("Search Course / Skill / Job Title", "AI for Business")
        course_submit = st.form_submit_button("🎯 Find Courses")

    if course_submit:
        query = urllib.parse.quote_plus(search)

        st.subheader("🧠 Tech Giants")
        tech = [
            ("Google", f"https://grow.google/certificates/?q={query}"),
            ("IBM", f"https://skillsbuild.org/learn?search={query}"),
            ("Amazon AWS", f"https://explore.skillbuilder.aws/learn?searchTerm={query}"),
            ("Microsoft (via LinkedIn)", "https://www.linkedin.com/learning/"),
            ("Meta", f"https://www.facebook.com/business/learn/courses?search={query}")
        ]
        for name, url in tech:
            st.markdown(f"<a href='{url}' target='_blank' style='display:block; background:#3b82f6; color:white; padding:10px; border-radius:5px; margin-bottom:5px;'>📘 {name}</a>", unsafe_allow_html=True)

        st.subheader("🌐 Online Learning Platforms")
        online = [
            ("Coursera", f"https://www.coursera.org/search?query={query}&price=Free"),
            ("edX", f"https://www.edx.org/search?q={query}&price=Free"),
            ("FutureLearn", f"https://www.futurelearn.com/search?q={query}"),
            ("YouTube", f"https://www.youtube.com/results?search_query={query}+course")
        ]
        for name, url in online:
            st.markdown(f"<a href='{url}' target='_blank' style='display:block; background:#6366f1; color:white; padding:10px; border-radius:5px; margin-bottom:5px;'>🌍 {name}</a>", unsafe_allow_html=True)

        st.subheader("⚙️ Specialized Platforms")
        special = [
            ("GitLab", f"https://about.gitlab.com/handbook/learning-and-development/#free-training?search={query}"),
            ("MongoDB", f"https://learn.mongodb.com/catalog?search={query}"),
            ("Salesforce", f"https://trailhead.salesforce.com/en/search?keywords={query}"),
            ("Twitter", f"https://flightschool.twitter.com/student/catalog/search?query={query}")
        ]
        for name, url in special:
            st.markdown(f"<a href='{url}' target='_blank' style='display:block; background:#10b981; color:white; padding:10px; border-radius:5px; margin-bottom:5px;'>🛠️ {name}</a>", unsafe_allow_html=True)

        st.subheader("🎯 Other Platforms")
        misc = [
            ("Google Digital Garage", f"https://learndigital.withgoogle.com/digitalgarage/courses?search={query}"),
            ("Google Cloud Skills Boost", f"https://www.cloudskillsboost.google/catalog?search={query}"),
            ("Google Skillshop", f"https://skillshop.exceedlms.com/student/catalog/search?query={query}")
        ]
        for name, url in misc:
            st.markdown(f"<a href='{url}' target='_blank' style='display:block; background:#f59e0b; color:white; padding:10px; border-radius:5px; margin-bottom:5px;'>💼 {name}</a>", unsafe_allow_html=True)

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
