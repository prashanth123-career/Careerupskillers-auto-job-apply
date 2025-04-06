import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Mega Job Finder", page_icon="🌐", layout="centered")
tab1, tab2, tab3 = st.tabs(["🌐 Job Finder", "🎯 Interview Preparation", "🎓 Free Courses"])

# ---------------------- TAB 1: JOB FINDER ----------------------
with tab1:
    st.title("🌍 Mega Job Finder")
    st.markdown("🔍 Access **50+ job portals** worldwide with smart filters")

    PORTALS_BY_COUNTRY = {
        "USA": [
            ("LinkedIn", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
            ("USAJobs (Govt)", lambda k, l, e, d: f"https://www.usajobs.gov/Search/Results?k={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
            ("Indeed", lambda k, l, e, d: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
            ("Glassdoor", lambda k, l, e, d: f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={urllib.parse.quote(k)}&locT=C&locName={urllib.parse.quote(l)}"),
            ("Monster", lambda k, l, e, d: f"https://www.monster.com/jobs/search?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}"),
            ("CareerBuilder", lambda k, l, e, d: f"https://www.careerbuilder.com/jobs?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
        ],
        "India": [
            ("LinkedIn India", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
            ("Government Jobs (India)", lambda k, l, e, d: f"https://www.indgovtjobs.in/search/label/{urllib.parse.quote(k)}"),
            ("Indeed India", lambda k, l, e, d: f"https://www.indeed.co.in/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
            ("Naukri", lambda k, l, e, d: f"https://www.naukri.com/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-') if l != 'Remote' else 'india'}"),
            ("Shine", lambda k, l, e, d: f"https://www.shine.com/job-search/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
            ("TimesJobs", lambda k, l, e, d: f"https://www.timesjobs.com/jobs/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
            ("Freshersworld", lambda k, l, e, d: f"https://www.freshersworld.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
        ]
        # Add other countries from your original list...
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
        st.subheader(f"🌐 Job Portals in {country}")
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

        d_filter = time_map[date_posted]
        e_filter = exp_map[experience]

        for name, url_func in PORTALS_BY_COUNTRY[country]:
            url = url_func(keyword, location, e_filter, d_filter) if "LinkedIn" in name else url_func(keyword, location, "", "")
            st.markdown(f"""
            <a href="{url}" target="_blank" style="display:inline-block; padding:10px 20px; background-color:#4CAF50; color:white; text-decoration:none; border-radius:5px; margin:5px 0;">
                🔍 Search on {name}
            </a>
            <p style="font-size: 12px; color: #666;">Opens in a new tab with filtered results.</p>
            """, unsafe_allow_html=True)

        google_jobs = f"https://www.google.com/search?q={urllib.parse.quote(keyword)}+jobs+in+{urllib.parse.quote(location)}&ibp=htl;jobs"
        st.markdown(f"""
        <div style='background-color:#f0f2f6; padding:20px; border-radius:10px; margin-top:30px;'>
            <h3 style='color:#1e3a8a;'>Need more options?</h3>
            <a href='{google_jobs}' target='_blank' style='background-color:#1e3a8a; color:white; padding:10px 15px; text-decoration:none; border-radius:5px;'>🔍 Search Google Jobs</a>
        </div>
        """, unsafe_allow_html=True)

# ---------------------- TAB 2: INTERVIEW PREPARATION PLATFORMS ----------------------
with tab2:
    st.title("🎯 Smart Interview Preparation")
    st.markdown("🔍 Get filtered interview prep links based on role, country, and platform.")

    with st.form("interview_links_form"):
        col1, col2 = st.columns(2)
        with col1:
            role = st.text_input("Job Role", "Data Scientist")
            country = st.selectbox("Country", ["India", "USA", "UK", "Canada", "Germany", "UAE", "Australia"])
        with col2:
            platform = st.selectbox("Choose Platform", [
                "LeetCode", "HackerRank", "GeeksforGeeks", "Glassdoor", "Pramp", 
                "IndiaBix", "AmbitionBox", "Final Round AI", "Big Interview", "iScalePro"
            ])
        link_submit = st.form_submit_button("🔗 Generate Link")

    if link_submit:
        query = urllib.parse.quote_plus(role + " " + country)

        PLATFORM_LINKS = {
            "LeetCode": f"https://leetcode.com/problemset/all/?search={query}",
            "HackerRank": f"https://www.hackerrank.com/interview/interview-preparation-kit",
            "GeeksforGeeks": f"https://www.geeksforgeeks.org/?s={query}",
            "Glassdoor": f"https://www.glassdoor.com/Interview/{query}-interview-questions-SRCH_KO0,{len(query)}.htm",
            "Pramp": f"https://www.pramp.com/#interview-prep",
            "IndiaBix": f"https://www.indiabix.com/interview/questions-and-answers/?search={query}",
            "AmbitionBox": f"https://www.ambitionbox.com/interviews?title={query}",
            "Final Round AI": f"https://www.finalroundai.com/ai-mock-interview",
            "Big Interview": f"https://www.biginterview.com/",
            "iScalePro": f"https://www.iscalepro.com/jobseekers/"
        }

        if platform in PLATFORM_LINKS:
            st.markdown(f"### 🔗 Your Custom Interview Prep Link")
            st.markdown(f"""
            <a href="{PLATFORM_LINKS[platform]}" target="_blank" style="display:inline-block; background:#2563eb; color:white; padding:12px 24px; border-radius:5px; text-decoration:none;">
                👉 Prep on {platform}
            </a>
            """, unsafe_allow_html=True)

            st.info("Explore company-specific questions, mock interviews, and prep content on this platform.")
        else:
            st.error("Platform not supported. Please choose another.")
# ---------------------- TAB 3: FREE COURSES ----------------------
with tab3:
    st.title("🎓 Free Courses with Certificates")
    st.markdown("💡 Learn free from top platforms: Google, IBM, Coursera, YouTube")

    with st.form("course_form"):
        course_input = st.text_input("Search Course / Skill / Designation", "Python for Data Science")
        course_submit = st.form_submit_button("🔍 Show Free Courses")

    if course_submit:
        st.subheader(f"🎓 Free Courses Related to '{course_input}'")
        search_query = urllib.parse.quote(course_input)

        course_links = [
            ("Google Career Certificates", f"https://grow.google/certificates/?q={search_query}"),
            ("Coursera Free (Google, IBM, Meta)", f"https://www.coursera.org/search?query={search_query}&price=Free"),
            ("edX Free Courses", f"https://www.edx.org/search?q={search_query}&price=Free"),
            ("YouTube Learning", f"https://www.youtube.com/results?search_query={search_query}+course"),
            ("Alison Certified Courses", f"https://alison.com/courses?query={search_query}"),
            ("FutureLearn Free Courses", f"https://www.futurelearn.com/search?q={search_query}")
        ]

        for name, url in course_links:
            st.markdown(f"""
            <a href="{url}" target="_blank" style="display:block; background:#6366f1; color:white; padding:10px; margin:10px 0; border-radius:5px; text-align:center;">
                🎓 {name}
            </a>
            """, unsafe_allow_html=True)

        st.success("✅ Explore and start learning for free with certification!")
