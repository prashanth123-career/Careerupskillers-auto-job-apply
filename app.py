import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Mega Job Finder", page_icon="🌐", layout="centered")

tab1, tab2, tab3 = st.tabs(["🌐 Job Finder", "🎯 Interview Preparation", "🎓 Free Courses"])

# ========================== TAB 1: JOB FINDER ==========================
with tab1:
    PORTALS_BY_COUNTRY = {
        "USA": [...],  # (KEEP YOUR FULL COUNTRY DICT HERE)
        # ...
        "Germany": [...]
    }

    st.title("🌍 Mega Job Finder")
    st.markdown("🔍 Access **50+ job portals** worldwide with smart filters")

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
        time_map = {"Any time": "", "Past month": "r2592000", "Past week": "r604800", "Past 24 hours": "r86400"}
        exp_map = {"Any": "", "Entry": "2", "Mid": "3", "Senior": "4", "Executive": "5"}
        d_filter = time_map[date_posted]
        e_filter = exp_map[experience]

        for name, url_func in PORTALS_BY_COUNTRY[country]:
            url = url_func(keyword, location, e_filter, d_filter) if "LinkedIn" in name else url_func(keyword, location, "", "")
            button_html = f"""
            <a href="{url}" target="_blank" style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin: 5px 0;">
                🔍 Search on {name}
            </a>
            <p style="font-size: 12px; color: #666;">If logged into {name}, it opens directly in a new tab.</p>
            """
            st.markdown(button_html, unsafe_allow_html=True)

        st.success(f"✅ Generated {len(PORTALS_BY_COUNTRY[country])} job search links.")

        google_jobs = f"https://www.google.com/search?q={urllib.parse.quote(keyword)}+jobs+in+{urllib.parse.quote(location)}&ibp=htl;jobs"
        st.markdown(f"""
        <div style='background-color:#f0f2f6; padding:20px; border-radius:10px; margin-top:30px;'>
            <h3 style='color:#1e3a8a;'>Need more options?</h3>
            <a href='{google_jobs}' target='_blank' style='background-color:#1e3a8a; color:white; padding:10px 15px; text-decoration:none; border-radius:5px;'>🔍 Search Google Jobs</a>
        </div>
        """, unsafe_allow_html=True)

# ========================== TAB 2: INTERVIEW PREPARATION ==========================
with tab2:
    st.title("🎯 Interview Preparation")
    st.markdown("🧠 Get sample interview questions and prep tips")

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
            st.markdown(f"- What are the core responsibilities of a {designation}?\n- Explain a recent project.\n- How would you solve [common technical problem]?\n- What tools or languages are you comfortable with?")
        elif round_level == "Managerial Round":
            st.markdown("- How do you handle team conflict?\n- How do you prioritize tasks?\n- Describe a leadership experience.")
        else:
            st.info(f"Please find the interview questions based on the role '{designation}'.")
            st.markdown("- What does a typical day look like in this role?\n- What technologies are essential for this position?\n- Share one challenging situation you handled professionally.")

        st.subheader("🏢 Company Culture Tips")
        if country == "India":
            st.markdown("✅ Expect formal process.\n✅ Focus on technical depth.\n✅ Show long-term interest.")
        elif country == "USA":
            st.markdown("✅ Emphasize innovation.\n✅ Be confident, conversational.\n✅ Cultural fit is important.")
        elif country == "UK":
            st.markdown("✅ Show analytical thinking.\n✅ Maintain professional tone.\n✅ Respect punctuality.")
        else:
            st.markdown("✅ Do your research on company reviews.\n✅ Read Glassdoor or LinkedIn profiles of employees.")

# ========================== TAB 3: FREE COURSES ==========================
with tab3:
    st.title("🎓 Free Courses with Certification")
    st.markdown("💡 Search free certified courses from top providers like Google, IBM, YouTube, and more.")

    with st.form("course_form"):
        course_input = st.text_input("Enter Skill / Designation / Course Topic", "Data Analytics")
        course_submit = st.form_submit_button("🎯 Find Free Courses")

    if course_submit:
        st.subheader(f"🎓 Free Courses Related to '{course_input}'")

        search_query = urllib.parse.quote(course_input)
        course_links = [
            ("Google Career Certificates", f"https://grow.google/certificates/?q={search_query}"),
            ("Coursera Free Courses (IBM, Meta, Google)", f"https://www.coursera.org/search?query={search_query}&price=Free"),
            ("edX Free Courses", f"https://www.edx.org/search?q={search_query}&price=Free"),
            ("YouTube Learning", f"https://www.youtube.com/results?search_query={search_query}+course"),
            ("Alison Certifications", f"https://alison.com/courses?query={search_query}"),
            ("FutureLearn", f"https://www.futurelearn.com/search?q={search_query}"),
        ]

        for name, url in course_links:
            st.markdown(f"""
            <a href="{url}" target="_blank" style="display:block; background:#6366f1; color:white; padding:10px; margin:10px 0; border-radius:5px; text-align:center;">
                🎓 {name}
            </a>
            """, unsafe_allow_html=True)

        st.success("✅ Explore these links to enroll for free with certificates!")

