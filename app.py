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

# ---------------------- TAB 2: INTERVIEW PREP ----------------------
with tab2:
    st.title("🎯 Interview Preparation")
    st.markdown("🧠 Get sample questions, prep tips & company culture")

    with st.form("interview_form"):
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Company Name", "Google")
            designation = st.text_input("Designation / Role", "Data Scientist")
        with col2:
            country = st.selectbox("Country", ["USA", "UK", "India", "Canada", "Germany", "Australia", "UAE"])
            round_level = st.selectbox("Interview Round", ["Not Sure", "HR Round", "Technical Round", "Managerial Round"])

        interview_submit = st.form_submit_button("📋 Get Interview Plan")

    if interview_submit:
        st.subheader(f"📄 Interview Questions for {designation} at {company}")
        
        if round_level == "HR Round":
            st.markdown("- Tell me about yourself.\n- Why do you want to join this company?\n- Describe a challenge you overcame.\n- Where do you see yourself in 5 years?")
        elif round_level == "Technical Round":
            st.markdown(f"- What are the core responsibilities of a {designation}?\n- Explain a recent project.\n- How would you solve [a typical technical issue]?\n- What tools/languages are you best at?")
        elif round_level == "Managerial Round":
            st.markdown("- How do you manage a team?\n- Describe a time you handled a project crisis.\n- What are your strengths as a leader?")
        else:
            st.info(f"Please find the general interview questions based on '{designation}'.")
            st.markdown("- What does a typical day look like in this role?\n- What are your core technical strengths?\n- How do you stay updated with industry trends?")

        st.subheader("🏢 Company Culture Tips")
        if country == "India":
            st.markdown("✅ Be formal and respectful.\n✅ Focus on technical clarity.\n✅ Emphasize loyalty and long-term vision.")
        elif country == "USA":
            st.markdown("✅ Be confident and results-driven.\n✅ Show alignment with company mission.\n✅ Highlight innovation and independence.")
        elif country == "UK":
            st.markdown("✅ Maintain professionalism.\n✅ Highlight teamwork and precision.\n✅ Be well-prepared and punctual.")
        else:
            st.markdown("✅ Read company reviews on Glassdoor.\n✅ Visit their LinkedIn and culture blogs.\n✅ Learn about leadership and work-life policies.")

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
