import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Career Assistant Pro", page_icon="💼", layout="centered")

# ================== JOB SEARCH TAB ==================
def job_search_tab():
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
        # ... (keep existing job search code exactly the same) ...

# ================== INTERVIEW PREP TAB ==================
def interview_prep_tab():
    st.title("🎯 Interview Preparation Assistant")
    st.markdown("💡 Get company-specific interview questions and preparation resources")

    with st.form("interview_form"):
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Company Name", "Google")
            designation = st.text_input("Job Designation", "Software Engineer")
        with col2:
            country = st.selectbox("Country", ["USA", "India", "UK", "Canada", "Australia", "Germany", "UAE"])
            interview_round = st.selectbox("Interview Round", ["Technical", "HR", "Managerial", "Case Study"])

        submitted = st.form_submit_button("🚀 Get Preparation Guide")

    if submitted:
        st.subheader(f"📚 {company} {designation} Interview Prep")
        
        # Interview questions database
        questions_db = {
            "Google": {
                "Software Engineer": {
                    "Technical": "https://www.techinterviewhandbook.org/google-interview/",
                    "HR": "https://www.glassdoor.com/Interview/Google-HR-Interview-Questions-EI_IE9079.0,6_KO7,9.htm"
                }
            },
            "Amazon": {
                "Data Scientist": {
                    "Technical": "https://www.interviewkickstart.com/amazon-data-scientist-interview-questions"
                }
            }
        }

        try:
            resources = questions_db[company][designation][interview_round]
            st.markdown(f"""
            <div style='background-color:#e8f5e9; padding:20px; border-radius:10px; margin-bottom:20px;'>
                <h4 style='color:#2e7d32;'>🔍 Found Preparation Resources:</h4>
                <a href='{resources}' target='_blank' style='color:#1b5e20;'>View {interview_round} Round Preparation Guide →</a>
            </div>
            """, unsafe_allow_html=True)
        except KeyError:
            st.warning(f"⚠️ Specific resources not found. Showing general {designation} interview questions:")
            st.markdown(f"""
            <a href='https://www.google.com/search?q={urllib.parse.quote(f"{designation} interview questions {company} {country}")}' 
               target='_blank' 
               style='background-color:#ffecb3; color:#000; padding:10px; border-radius:5px; display:block; margin:10px 0;'>
                🔎 Search Google for {designation} Interview Questions
            </a>
            """, unsafe_allow_html=True)

        # Company culture section
        st.markdown(f"""
        <div style='background-color:#e3f2fd; padding:20px; border-radius:10px; margin-top:20px;'>
            <h4 style='color:#0d47a1;'>🏢 {company} Culture Insights ({country})</h4>
            <a href='https://www.glassdoor.com/Reviews/{company}-Reviews-E{_get_company_id(company)}.htm' 
               target='_blank' 
               style='color:#1565c0; display:block; margin:10px 0;'>
                📖 Read Employee Reviews →
            </a>
            <a href='https://www.youtube.com/results?search_query={urllib.parse.quote(f"{company} work culture {country}")}' 
               target='_blank' 
               style='color:#1565c0; display:block; margin:10px 0;'>
                🎥 Watch Culture Videos →
            </a>
        </div>
        """, unsafe_allow_html=True)

# ================== FREE COURSES TAB ==================  
def free_courses_tab():
    st.title("🎓 Free Learning Hub")
    st.markdown("📚 Discover free certified courses from top platforms")

    COURSES = [
        {"name": "Google Data Analytics", "platform": "Coursera", "url": "https://www.coursera.org/professional-certificates/google-data-analytics", "skills": ["Data Analysis", "SQL", "R"]},
        {"name": "IBM Data Science", "platform": "edX", "url": "https://www.edx.org/professional-certificate/ibm-data-science", "skills": ["Python", "Machine Learning", "Data Science"]},
        {"name": "AWS Fundamentals", "platform": "Coursera", "url": "https://www.coursera.org/specializations/aws-fundamentals", "skills": ["Cloud Computing", "AWS"]},
        {"name": "Digital Marketing", "platform": "Google Digital Garage", "url": "https://learndigital.withgoogle.com/digitalgarage", "skills": ["Marketing", "SEO", "Social Media"]},
        {"name": "Python Programming", "platform": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/scientific-computing-with-python/", "skills": ["Python", "Programming"]}
    ]

    with st.form("course_form"):
        search_query = st.text_input("Search Courses/Skills/Designation", "Data Science")
        submitted = st.form_submit_button("🔍 Find Courses")

    if submitted:
        st.subheader(f"📖 Courses Matching: {search_query}")
        results = [c for c in COURSES if 
                  search_query.lower() in c["name"].lower() or 
                  any(search_query.lower() in s.lower() for s in c["skills"])]
        
        if not results:
            st.info("💡 No exact matches found. Showing popular courses:")
            results = COURSES[:3]

        for course in results:
            st.markdown(f"""
            <div style='background-color:#f5f5f5; padding:15px; border-radius:10px; margin:10px 0;'>
                <h4>{course['name']} ({course['platform']})</h4>
                <p>🔑 Skills: {", ".join(course['skills'])}</p>
                <a href='{course['url']}' target='_blank' 
                   style='background-color:#4CAF50; color:white; padding:8px 16px; 
                          border-radius:5px; text-decoration:none; display:inline-block;'>
                    Enroll Now →
                </a>
            </div>
            """, unsafe_allow_html=True)

# ================== MAIN APP ==================
tabs = ["Job Search", "Interview Prep", "Free Courses"]
page = st.sidebar.selectbox("Choose Section", tabs)

if page == "Job Search":
    job_search_tab()
elif page == "Interview Prep":
    interview_prep_tab()
elif page == "Free Courses":
    free_courses_tab()

# Helper function (mock implementation)
def _get_company_id(company):
    # This would normally call an API, using mock values
    company_ids = {"Google": "9079", "Amazon": "6036", "Microsoft": "1651"}
    return company_ids.get(company, "")
