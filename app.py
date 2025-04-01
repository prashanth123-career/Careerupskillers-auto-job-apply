# Precision Job Matcher with AI
import streamlit as st
import PyPDF2
import docx2txt
import urllib.parse
from transformers import pipeline
import re

# Configure Streamlit
st.set_page_config(page_title="Precision Job Matcher", page_icon="🎯", layout="wide")
st.title("🎯 Precision Job Matcher")
st.markdown("Get job matches tailored to your exact profile")

# Load AI models
@st.cache_resource
def load_models():
    analyzer = pipeline("text2text-generation", model="facebook/bart-large-cnn")
    matcher = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    return analyzer, matcher

# Enhanced Resume Parser
def extract_profile(file):
    text = ""
    if file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages])
    elif file.name.endswith('.docx'):
        text = docx2txt.process(file)
    
    # Extract key details with regex
    profile = {
        'skills': list(set(re.findall(r'\b(?:Python|Java|SQL|Sales|Marketing|AWS|Azure|Counseling|Business Development)\b', text, re.IGNORECASE))),
        'companies': re.findall(r'(?:Company|Employer|Organization).*?([^\n]+)', text),
        'designations': re.findall(r'(?:Title|Position|Role).*?([^\n]+)', text),
        'experience': len(re.findall(r'(20\d{2})', text)) or 1,
        'education': re.findall(r'(?:Education|Degree).*?([^\n]+)', text)
    }
    
    # Clean extracted data
    profile['last_company'] = profile['companies'][-1].strip() if profile['companies'] else ""
    profile['last_designation'] = profile['designations'][-1].strip() if profile['designations'] else ""
    return profile

# Precision Job Matching
def get_precision_matches(profile, location, job_type):
    # Define job categories based on profile
    categories = {
        'Sales': ['Account Executive', 'Sales Manager', 'Business Development'],
        'Technical': ['Software Engineer', 'Data Analyst', 'Cloud Architect'],
        'Education': ['Career Counselor', 'Admissions Counselor', 'EduTech Specialist']
    }
    
    # Determine best category
    best_category = max(categories.keys(), 
                       key=lambda x: sum(skill in profile['skills'] for skill in categories[x]))
    
    # Generate LinkedIn URL with precision filters
    base_url = "https://www.linkedin.com/jobs/search/"
    params = {
        "keywords": f"{best_category} {profile['last_designation']}",
        "location": location,
        "f_TPR": "r2592000",  # Past month
        "f_JT": job_type[0].lower(),  # Job type filter
        "f_E": f"{min(4, profile['experience'])}%2B"  # Experience filter
    }
    query = urllib.parse.urlencode(params)
    return f"{base_url}?{query}"

# Streamlit UI
analyzer, matcher = load_models()

with st.form("profile_form"):
    resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=['pdf', 'docx'])
    location = st.text_input("Preferred Location", "Bengaluru, Karnataka, India")
    job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Contract", "Internship"])
    
    submitted = st.form_submit_button("Find Precision Matches")

if submitted and resume_file:
    with st.spinner("🔍 Finding your precision matches..."):
        profile = extract_profile(resume_file)
        
        if not profile['skills']:
            st.error("Couldn't extract sufficient profile details")
            st.stop()
        
        # Display profile summary
        with st.expander("👤 Your Professional Profile"):
            cols = st.columns(3)
            with cols[0]:
                st.write("**Last Role**", f"{profile['last_designation']} at {profile['last_company']}")
                st.write("**Experience**", f"{profile['experience']} years")
            with cols[1]:
                st.write("**Top Skills**", ", ".join(profile['skills'][:5]))
            with cols[2]:
                st.write("**Education**", ", ".join(profile['education'][:2]))
        
        # Get precision matches
        linkedin_url = get_precision_matches(profile, location, job_type)
        
        st.success("🎯 Found your precision matches!")
        st.markdown(f"""
        Based on your profile as **{profile['last_designation']}** with **{profile['experience']} years** experience in **{location}**, we recommend:
        """)
        
        st.markdown(f"""
        ### 🚀 [View Precision Matches on LinkedIn]({linkedin_url})
        
        Your search includes:
        - **Position:** {profile['last_designation'] or 'Relevant'} roles
        - **Location:** {location}
        - **Experience:** {profile['experience']}+ years
        - **Job Type:** {job_type}
        - **Posted:** Last month
        """)
        
        st.info("💡 Tip: Use LinkedIn's filters to further refine results by salary, company size, etc.")

st.markdown("---")
st.caption("Precision matching combines your resume details with smart filters for better results")
