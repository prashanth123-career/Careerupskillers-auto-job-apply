import streamlit as st
import urllib.parse
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime

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
# CORE FUNCTIONS
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

def calculate_match_score(resume_text, job_description):
    embeddings = model.encode([resume_text, job_description])
    return float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])

def analyze_skills_gap(user_skills, job_skills):
    user_skills_lower = [s.strip().lower() for s in user_skills.split(",")]
    job_skills_lower = [s.strip().lower() for s in job_skills.split(",")]
    return [skill for skill in job_skills_lower if skill not in user_skills_lower][:5]

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
    
    data = salary_data.get(country, {"avg": 0, "entry": 0, "senior": 0})
    df = pd.DataFrame({
        "Level": ["Entry", "Average", "Senior"],
        "Salary": [data["entry"], data["avg"], data["senior"]]
    })
    
    fig = px.bar(df, x="Level", y="Salary", title=f"Salary Range for {role} in {country}")
    st.plotly_chart(fig, use_container_width=True)

def application_tracker():
    with st.expander("📝 My Job Applications", expanded=True):
        if not st.session_state.applications:
            st.info("No applications tracked yet")
            return
            
        df = pd.DataFrame(st.session_state.applications)
        st.dataframe(
            df,
            column_config={
                "date": "Date",
                "company": "Company",
                "role": "Position",
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Applied", "Interview", "Rejected", "Offer"],
                    required=True
                )
            },
            hide_index=True,
            use_container_width=True
        )

# --------------------------
# MAIN APP
# --------------------------
def main():
    st.title("🌍 Global AI Job Finder Pro")
    st.markdown("🔍 Smart job search with AI-powered matching, salary insights, and application tracking")
    
    # Sidebar for resume and skills
    with st.sidebar:
        st.header("🧑‍💻 My Profile")
        uploaded_file = st.file_uploader("Upload Resume (PDF/TXT)", type=["pdf", "txt"])
        if uploaded_file:
            st.session_state.resume_text = uploaded_file.read().decode("utf-8")
        
        user_skills = st.text_area("My Skills (comma separated)", 
                                 "Python, SQL, Machine Learning")
        
        application_tracker()
    
    # Main search form
    with st.form("job_form"):
        col1, col2 = st.columns(2)
        with col1:
            keyword = st.text_input("Job Title", "Data Scientist")
            location = st.text_input("Location", "Remote")
            country = st.selectbox("Country", ["USA", "UK", "India", "Australia", "Canada", "Others"])
            
        with col2:
            time_filter = st.selectbox("Date Posted", ["Past week", "Past 24 hours", "Past month", "Any time"])
            experience = st.selectbox("Experience", ["Any", "Entry level", "Mid-Senior level", "Director"])
            remote_option = st.selectbox("Work Type", ["Remote", "Hybrid", "On-site", "Any"])
        
        # Conditional fields
        visa_sponsorship = st.checkbox("Show only visa sponsorship jobs", False)
        easy_apply = st.checkbox("Easy Apply only", True)
        
        if country != "India":
            salary = st.slider("Minimum Salary (USD)", 50000, 250000, 100000, 10000)
        else:
            salary = None
        
        submitted = st.form_submit_button("🔍 Find Jobs")

    if submitted:
        # --------------------------
        # RESULTS SECTION
        # --------------------------
        st.success("🎯 Search completed! Here are your optimized job links:")
        
        # LinkedIn Search
        st.subheader("🔗 LinkedIn Smart Search")
        linkedin_link = linkedin_url(keyword, location, time_filter, experience, remote_option, easy_apply, visa_sponsorship)
        st.markdown(f"✅ [Open LinkedIn Search]({linkedin_link})")
        
        # Global Portals
        st.subheader(f"🌐 Top Job Portals in {country}")
        portals = generate_job_links(keyword, location, country, salary if salary else None)
        
        # Display with match scores if resume exists
        if st.session_state.resume_text:
            st.info("🔍 Calculating match scores based on your resume...")
            for name, url in portals:
                score = calculate_match_score(st.session_state.resume_text, f"{keyword} {location}")
                st.markdown(f"- 🔗 [{name} ({score*100:.0f}% match)]({url})")
        else:
            for name, url in portals:
                st.markdown(f"- 🔗 [{name}]({url})")
        
        # --------------------------
        # NEW FEATURES SECTION
        # --------------------------
        st.divider()
        
        # Salary Insights
        with st.expander("💸 Salary Insights", expanded=True):
            show_salary_insights(country, keyword)
        
        # Skills Gap Analysis
        if st.session_state.resume_text:
            with st.expander("📊 Skills Gap Analysis", expanded=True):
                job_skills = "Python, SQL, Machine Learning, Data Analysis, Statistics, Deep Learning, Cloud Computing"
                missing_skills = analyze_skills_gap(user_skills, job_skills)
                
                if missing_skills:
                    st.warning(f"Top skills to learn: {', '.join(missing_skills)}")
                    st.markdown("""
                    **Recommended Resources:**
                    - [Coursera: Machine Learning Specialization](https://www.coursera.org)
                    - [Udemy: Advanced SQL Course](https://www.udemy.com)
                    """)
                else:
                    st.success("Your skills match well with this job profile!")
        
        # Interview Prep
        with st.expander("🎤 Interview Preparation", expanded=True):
            question = st.selectbox("Practice question:", [
                "Tell me about yourself",
                "Why do you want this job?",
                "Explain a complex project simply"
            ])
            
            if st.button("Generate AI Response"):
                with st.spinner("Generating sample answer..."):
                    st.markdown(f"""
                    **Sample Answer:**
                    > "As a {experience} {keyword}, I've developed expertise in {user_skills.split(',')[0]}. 
                    In my recent role at [Company], I [specific achievement]. This aligns well with 
                    your need for [job requirement] because..."
                    """)
        
        # Application Tracking
        with st.expander("➕ Track This Application", expanded=True):
            app_col1, app_col2, app_col3 = st.columns(3)
            with app_col1:
                company = st.text_input("Company Name")
            with app_col2:
                role = st.text_input("Position", keyword)
            with app_col3:
                app_date = st.date_input("Application Date")
            
            if st.button("Add to Tracker"):
                st.session_state.applications.append({
                    "company": company,
                    "role": role,
                    "date": app_date.strftime("%Y-%m-%d"),
                    "status": "Applied"
                })
                st.success("Application tracked!")
        
        # Career Counseling CTA
        st.markdown("""
        <div style='background-color:#f0f2f6; padding:20px; border-radius:10px; margin-top:30px;'>
            <h3 style='color:#1e3a8a;'>🚀 Ready to level up your career?</h3>
            <p>Get personalized 1:1 coaching with our AI Career Advisor:</p>
            <a href='https://careeradvisor.example.com' target='_blank' 
               style='background-color:#1e3a8a; color:white; padding:10px 15px; 
                      text-decoration:none; border-radius:5px; display:inline-block;'>
                Book Free Session
            </a>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
