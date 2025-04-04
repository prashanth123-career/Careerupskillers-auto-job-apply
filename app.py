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

# Load SBERT model
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# --------------------------
# SALARY DATA (2024 Benchmarks)
# --------------------------
SALARY_DATA = {
    "USA": {
        "Data Scientist": {"entry": 95000, "avg": 135000, "senior": 190000, "currency": "USD"},
        "AI Engineer": {"entry": 105000, "avg": 150000, "senior": 210000, "currency": "USD"},
        "ML Engineer": {"entry": 110000, "avg": 155000, "senior": 200000, "currency": "USD"},
        "Data Analyst": {"entry": 65000, "avg": 85000, "senior": 120000, "currency": "USD"}
    },
    "UK": {
        "Data Scientist": {"entry": 45000, "avg": 70000, "senior": 100000, "currency": "GBP"},
        "AI Engineer": {"entry": 50000, "avg": 80000, "senior": 110000, "currency": "GBP"}
    },
    "India": {
        "Data Scientist": {"entry": 900000, "avg": 1500000, "senior": 2500000, "currency": "INR"},
        "AI Engineer": {"entry": 1000000, "avg": 1800000, "senior": 3000000, "currency": "INR"}
    },
    "Germany": {
        "Data Scientist": {"entry": 55000, "avg": 75000, "senior": 100000, "currency": "EUR"}
    }
}

# --------------------------
# CORE FUNCTIONS
# --------------------------
def extract_text_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(BytesIO(file.read()))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"PDF error: {str(e)}")
        return ""

def extract_text_from_txt(file):
    try:
        return file.read().decode("utf-8")
    except UnicodeDecodeError:
        return file.read().decode("latin-1")

def process_uploaded_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        return extract_text_from_txt(uploaded_file)
    return ""

def show_salary_insights(country, role):
    try:
        country_data = SALARY_DATA.get(country, SALARY_DATA["USA"])
        role_data = country_data.get(role, country_data["Data Scientist"])
        
        levels = ["Entry", "Average", "Senior"]
        df = pd.DataFrame({
            "Level": levels,
            "Salary": [role_data["entry"], role_data["avg"], role_data["senior"]],
            "Currency": [role_data["currency"]] * 3
        })
        
        fig = px.bar(df,
                    x="Level",
                    y="Salary",
                    color="Level",
                    title=f"{role} Salaries in {country} (2024)",
                    text="Salary")
        
        currency_symbol = {"USD": "$", "GBP": "£", "INR": "₹", "EUR": "€"}.get(role_data["currency"], "")
        fig.update_layout(yaxis_tickprefix=currency_symbol)
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Couldn't display salary data: {str(e)}")

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
    params = {"q": keyword, "l": location}
    if salary and country != "India":
        params["salary"] = salary
    return f"{base_url}?{urllib.parse.urlencode(params)}"

def generate_job_links(keyword, location, country, salary=None):
    query = urllib.parse.quote_plus(keyword)
    loc = urllib.parse.quote_plus(location)
    indeed_link = indeed_url(keyword, location, country, salary)
    
    if country == "USA":
        return [
            ("Indeed", indeed_link),
            ("Glassdoor", f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={query}&locKeyword={loc}"),
            ("SimplyHired", f"https://www.simplyhired.com/search?q={query}&l={loc}")
        ]
    elif country == "UK":
        return [
            ("Indeed UK", indeed_link),
            ("Reed", f"https://www.reed.co.uk/jobs/{query}-jobs-in-{location.replace(' ', '-')}"),
            ("CV-Library", f"https://www.cv-library.co.uk/search-jobs?kw={query}&loc={loc}")
        ]
    elif country == "India":
        return [
            ("Naukri", f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"),
            ("Indeed India", indeed_link),
            ("Shine", f"https://www.shine.com/job-search/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}")
        ]
    else:
        return [
            ("Indeed", indeed_link),
            ("Google Jobs", f"https://www.google.com/search?q={query}+jobs+in+{loc}")
        ]

def calculate_match_score(resume_text, job_description):
    try:
        embeddings = model.encode([resume_text, job_description])
        return float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
    except:
        return 0.0

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
        st.session_state.applications = edited_df.to_dict('records')

# --------------------------
# MAIN APP
# --------------------------
def main():
    st.title("🌍 Global AI Job Finder Pro")
    
    # Sidebar
    with st.sidebar:
        st.header("🧑‍💻 My Profile")
        uploaded_file = st.file_uploader("Upload Resume (PDF/TXT)", type=["pdf", "txt"])
        if uploaded_file:
            st.session_state.resume_text = process_uploaded_file(uploaded_file)
        
        user_skills = st.text_area("My Skills", "Python, SQL, Machine Learning")
        application_tracker()

    # Main form
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
        
        visa_sponsorship = st.checkbox("Visa sponsorship only", False)
        easy_apply = st.checkbox("Easy Apply only", True)
        
        if country != "India":
            salary = st.slider("Minimum Salary", 50000, 250000, 100000, 10000)
        else:
            salary = None
        
        submitted = st.form_submit_button("🔍 Find Jobs")

    if submitted:
        # Salary Insights
        show_salary_insights(country, keyword)
        
        # Job Links
        st.subheader("🔗 Job Portals")
        portals = generate_job_links(keyword, location, country, salary)
        
        if st.session_state.resume_text:
            for name, url in portals:
                score = calculate_match_score(st.session_state.resume_text, f"{keyword} {location}")
                st.markdown(f"- 🔗 [{name} ({score*100:.0f}% match)]({url})")
        else:
            for name, url in portals:
                st.markdown(f"- 🔗 [{name}]({url})")

if __name__ == "__main__":
    main()
