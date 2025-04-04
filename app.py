import streamlit as st
import urllib.parse
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO
import PyPDF2
import base64

# --------------------------
# SETUP & CONFIGURATION
# --------------------------
st.set_page_config(
    page_title="🌍 Global AI Job Finder Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'applications' not in st.session_state:
    st.session_state.applications = []
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""

# Load SBERT model (cache for performance)
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# --------------------------
# FILE HANDLING FUNCTIONS
# --------------------------
def extract_text_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(BytesIO(file.read()))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""  # Handle None returns
        return text
    except Exception as e:
        st.error(f"PDF extraction error: {str(e)}")
        return ""

def extract_text_from_txt(file):
    try:
        # Try UTF-8 first, fallback to latin-1 if needed
        try:
            return file.read().decode("utf-8")
        except UnicodeDecodeError:
            return file.read().decode("latin-1")
    except Exception as e:
        st.error(f"Text file reading error: {str(e)}")
        return ""

def process_uploaded_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        return extract_text_from_txt(uploaded_file)
    else:
        st.error("Unsupported file type")
        return ""

# --------------------------
# CORE JOB SEARCH FUNCTIONS
# --------------------------
def linkedin_url(keyword, location, time_filter, experience, remote_option, easy_apply, visa_sponsorship=False):
    time_map = {
        "Past 24 hours": "r86400",
        "Past week": "r604800",
        "Past month": "r2592000",
        "Any time": ""
    }
    exp_map = {
        "Any": "",
        "Internship": "1",
        "Entry level": "2",
        "Associate": "3",
        "Mid-Senior level": "4",
        "Director": "5"
    }
    remote_map = {
        "Any": "",
        "Remote": "2",
        "On-site": "1",
        "Hybrid": "3"
    }

    params = {
        "keywords": keyword,
        "location": location,
        "f_TPR": time_map.get(time_filter, ""),
        "f_E": exp_map.get(experience, ""),
        "f_WT": remote_map.get(remote_option, ""),
        "f_AL": "true" if easy_apply else "",
        "f_SB2": "4" if visa_sponsorship else ""
    }

    return f"https://www.linkedin.com/jobs/search/?{urllib.parse.urlencode({k: v for k, v in params.items() if v})}"

def indeed_url(keyword, location, country, salary=None):
    domain_map = {
        "USA": "www.indeed.com",
        "UK": "uk.indeed.com",
        "Canada": "ca.indeed.com",
        "Australia": "au.indeed.com",
        "India": "www.indeed.co.in"
    }
    
    base_url = f"https://{domain_map.get(country, 'www.indeed.com')}/jobs"
    params = {
        "q": keyword,
        "l": location
    }
    
    if salary and country != "India":
        params["salary"] = salary
    
    return f"{base_url}?{urllib.parse.urlencode(params)}"

def generate_job_links(keyword, location, country, salary=None):
    query = urllib.parse.quote_plus(keyword)
    loc = urllib.parse.quote_plus(location)

    portals = []
    indeed_link = indeed_url(keyword, location, country, salary)
    
    if country == "USA":
        portals = [
            ("Indeed", indeed_link),
            ("Glassdoor", f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={query}&locKeyword={loc}"),
            ("SimplyHired", f"https://www.simplyhired.com/search?q={query}&l={loc}")
        ]
    elif country == "UK":
        portals = [
            ("Indeed UK", indeed_link),
            ("Reed", f"https://www.reed.co.uk/jobs/{query}-jobs-in-{location.replace(' ', '-')}"),
            ("CV-Library", f"https://www.cv-library.co.uk/search-jobs?kw={query}&loc={loc}")
        ]
    elif country == "India":
        portals = [
            ("Naukri", f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"),
            ("Indeed India", indeed_link),
            ("Shine", f"https://www.shine.com/job-search/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}")
        ]
    else:  # Generic fallback
        portals = [
            ("Indeed", indeed_link),
            ("Google Jobs", f"https://www.google.com/search?q={query}+jobs+in+{loc}")
        ]

    return portals

# --------------------------
# AI ANALYSIS FUNCTIONS
# --------------------------
def calculate_match_score(resume_text, job_description):
    try:
        if not resume_text or not job_description:
            return 0.0
            
        embeddings = model.encode([resume_text, job_description])
        return float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
    except Exception as e:
        st.error(f"Match calculation error: {str(e)}")
        return 0.0

def analyze_skills_gap(user_skills, job_skills="Python,SQL,Machine Learning,Data Analysis,Statistics"):
    try:
        if not user_skills:
            return []
            
        user_skills_lower = [s.strip().lower() for s in user_skills.split(",")]
        job_skills_lower = [s.strip().lower() for s in job_skills.split(",")]
        return [skill for skill in job_skills_lower if skill not in user_skills_lower][:3]
    except Exception as e:
        st.error(f"Skills analysis error: {str(e)}")
        return []

# --------------------------
# UI COMPONENTS
# --------------------------
def show_salary_insights(country, role):
    salary_data = {
        "USA": {"avg": 120000, "entry": 85000, "senior": 160000},
        "UK": {"avg": 65000, "entry": 45000, "senior": 90000},
        "India": {"avg": 1500000, "entry": 800000, "senior": 2500000},
        "Australia": {"avg": 110000, "entry": 75000, "senior": 140000},
        "Canada": {"avg": 95000, "entry": 65000, "senior": 120000}
    }
    
    data = salary_data.get(country, salary_data["USA"])  # Default to USA if country not found
    df = pd.DataFrame({
        "Level": ["Entry", "Average", "Senior"],
        "Salary": [data["entry"], data["avg"], data["senior"]],
        "Currency": ["USD" if country == "USA" else 
                    "GBP" if country == "UK" else 
                    "INR" if country == "India" else 
                    "AUD" if country == "Australia" else 
                    "CAD"]
    })
    
    fig = px.bar(df, x="Level", y="Salary", text="Currency",
                title=f"Salary Range for {role} in {country}",
                color="Level")
    st.plotly_chart(fig, use_container_width=True)

def application_tracker():
    with st.expander("📝 My Job Applications", expanded=True):
        if not st.session_state.applications:
            st.info("No applications tracked yet")
            return
            
        df = pd.DataFrame(st.session_state.applications)
        edited_df = st.data_editor(
            df,
            column_config={
                "date": st.column_config.DateColumn("Date"),
                "company": "Company",
                "role": "Position",
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Applied", "Interview", "Rejected", "Offer"],
                    required=True
                )
            },
            hide_index=True,
            use_container_width=True,
            num_rows="dynamic"
        )
        
        # Update session state if changes were made
        st.session_state.applications = edited_df.to_dict('records')

# --------------------------
# MAIN APP LAYOUT
# --------------------------
def main():
    st.title("🌍 Global AI Job Finder Pro")
    st.markdown("🔍 Smart job search with AI-powered matching and career tools")
    
    # Sidebar - User Profile Section
    with st.sidebar:
        st.header("🧑‍💻 My Profile")
        
        # Resume Upload
        uploaded_file = st.file_uploader("Upload Resume (PDF/TXT)", 
                                       type=["pdf", "txt"],
                                       help="Upload your resume for personalized matching")
        if uploaded_file:
            st.session_state.resume_text = process_uploaded_file(uploaded_file)
            if st.session_state.resume_text:
                with st.expander("View Resume Text"):
                    st.text(st.session_state.resume_text[:500] + "...")  # Show preview
        
        # Skills Input
        user_skills = st.text_area("My Skills (comma separated)", 
                                 "Python, SQL, Machine Learning",
                                 help="List your top skills for better recommendations")
        
        # Application Tracker
        application_tracker()
    
    # Main Search Form
    with st.form("job_form"):
        col1, col2 = st.columns(2)
        with col1:
            keyword = st.text_input("Job Title", "Data Scientist")
            location = st.text_input("Location", "Remote")
            country = st.selectbox("Country", ["USA", "UK", "India", "Australia", "Canada", "Others"])
            
        with col2:
            time_filter = st.selectbox("Date Posted", ["Past week", "Past 24 hours", "Past month", "Any time"])
            experience = st.selectbox("Experience Level", ["Any", "Entry level", "Mid-Senior level", "Director"])
            remote_option = st.selectbox("Work Type", ["Remote", "Hybrid", "On-site", "Any"])
        
        # Advanced Filters
        with st.expander("Advanced Filters"):
            visa_sponsorship = st.checkbox("Show only visa sponsorship jobs", False)
            easy_apply = st.checkbox("Easy Apply only", True)
            
            if country != "India":
                salary = st.slider("Minimum Salary", 50000, 250000, 100000, 10000)
            else:
                salary = None
        
        submitted = st.form_submit_button("🔍 Find Jobs", type="primary")

    if submitted:
        # --------------------------
        # JOB SEARCH RESULTS
        # --------------------------
        st.success("🎯 Search completed! Analyzing opportunities...")
        
        # LinkedIn Search
        st.subheader("🔗 LinkedIn Smart Search")
        linkedin_link = linkedin_url(keyword, location, time_filter, experience, remote_option, easy_apply, visa_sponsorship)
        st.markdown(f"✅ [Open LinkedIn Search]({linkedin_link})")
        
        # Global Portals
        st.subheader(f"🌐 Top Job Portals in {country}")
        portals = generate_job_links(keyword, location, country, salary if salary else None)
        
        # Display with match scores if resume exists
        if st.session_state.resume_text:
            for name, url in portals:
                score = calculate_match_score(st.session_state.resume_text, f"{keyword} {location}")
                progress = int(score * 100)
                st.markdown(f"""
                <div style="margin-bottom: 10px;">
                    <a href="{url}" target="_blank" style="text-decoration: none;">
                        <div style="display: flex; align-items: center;">
                            <div style="width: 60px; margin-right: 10px;">
                                <div style="background: linear-gradient(90deg, #4CAF50 {progress}%, #e0e0e0 {progress}%); 
                                            height: 20px; border-radius: 10px; display: flex; 
                                            align-items: center; justify-content: center;">
                                    <span style="color: white; font-size: 12px;">{progress}%</span>
                                </div>
                            </div>
                            <span style="font-weight: bold;">{name}</span>
                        </div>
                    </a>
                </div>
                """, unsafe_allow_html=True)
        else:
            for name, url in portals:
                st.markdown(f"- 🔗 [{name}]({url})")
        
        # --------------------------
        # CAREER TOOLS SECTION
        # --------------------------
        st.divider()
        
        # Salary Insights
        with st.expander("💸 Salary Insights", expanded=True):
            show_salary_insights(country, keyword)
        
        # Skills Gap Analysis
        with st.expander("📊 Skills Gap Analysis", expanded=True):
            missing_skills = analyze_skills_gap(user_skills)
            
            if missing_skills:
                st.warning(f"**Top skills to develop:** {', '.join(missing_skills)}")
                
                # Learning Resources
                st.markdown("""
                **Recommended Learning Path:**
                - [Machine Learning Specialization (Coursera)](https://www.coursera.org)
                - [Advanced SQL Course (Udemy)](https://www.udemy.com)
                - [Data Visualization with Python (DataCamp)](https://www.datacamp.com)
                """)
            else:
                st.success("Your skills match well with typical requirements for this role!")
        
        # Interview Preparation
        with st.expander("🎤 Interview Coach", expanded=True):
            question_type = st.selectbox("Practice question type:", [
                "Technical",
                "Behavioral",
                "Case Study",
                "Salary Negotiation"
            ])
            
            if st.button("Generate Practice Question"):
                questions = {
                    "Technical": f"Explain how you would implement a {keyword} solution for...",
                    "Behavioral": "Describe a time you solved a difficult problem at work",
                    "Case Study": f"How would you approach this {keyword} challenge for our company?",
                    "Salary Negotiation": "What are your salary expectations for this role?"
                }
                st.session_state.current_question = questions.get(question_type, "")
            
            if 'current_question' in st.session_state:
                st.text_area("Question:", st.session_state.current_question, disabled=True)
                
                if st.button("Show Sample Answer"):
                    with st.spinner("Generating AI-suggested answer..."):
                        st.markdown(f"""
                        **Suggested Answer Approach:**
                        > "As a {experience} {keyword} professional, I would approach this by...
                        
                        **Key Points to Cover:**
                        1. Technical details about {user_skills.split(',')[0]}
                        2. Business impact of the solution
                        3. Lessons learned from past experience
                        """)
        
        # Application Tracking
        with st.expander("➕ Track New Application", expanded=True):
            app_col1, app_col2, app_col3 = st.columns(3)
            with app_col1:
                company = st.text_input("Company Name", key="app_company")
            with app_col2:
                role = st.text_input("Position", keyword, key="app_role")
            with app_col3:
                app_date = st.date_input("Application Date", datetime.now(), key="app_date")
            
            if st.button("Add to Tracker", key="add_tracker"):
                st.session_state.applications.append({
                    "company": company,
                    "role": role,
                    "date": app_date.strftime("%Y-%m-%d"),
                    "status": "Applied"
                })
                st.success("Application tracked! View in sidebar")

if __name__ == "__main__":
    main()
