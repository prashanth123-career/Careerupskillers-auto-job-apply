import streamlit as st
st.set_page_config(page_title="All-in-One Job Auto-Applier", page_icon="💼", layout="wide")

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
# from transformers import pipeline  # Temporarily disabled to prevent crashes
import docx2txt
import PyPDF2
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_oauth import OAuth2Component
import json
import time
import plotly.express as px
import pytz
from googletrans import Translator
import base64
import threading

# -------------------- Authentication --------------------
CLIENT_ID = st.secrets.get("OAUTH_CLIENT_ID", "")
CLIENT_SECRET = st.secrets.get("OAUTH_CLIENT_SECRET", "")
AUTHORIZE_URL = st.secrets.get("OAUTH_AUTHORIZE_URL", "")
TOKEN_URL = st.secrets.get("OAUTH_TOKEN_URL", "")
REFRESH_TOKEN_URL = st.secrets.get("OAUTH_REFRESH_TOKEN_URL", "")
REVOKE_TOKEN_URL = st.secrets.get("OAUTH_REVOKE_TOKEN_URL", "")
REDIRECT_URI = st.secrets.get("OAUTH_REDIRECT_URI", "")
SCOPE = "openid profile email"

# Debug: Display OAuth configuration
st.write("Debug - OAuth Config:")
st.write(f"Client ID: {CLIENT_ID[:10]}...")  # Show partial Client ID for security
st.write(f"Redirect URI: {REDIRECT_URI}")

oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'token' not in st.session_state:
    st.session_state.token = None

# -------------------- Enhanced Resume Parser --------------------
def parse_resume(file):
    text = ""
    ext = file.name.split(".")[-1].lower()
    if ext == "pdf":
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif ext == "docx":
        text = docx2txt.process(file)
    
    details = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "education": extract_education(text)
    }
    return text, details

def extract_name(text):
    lines = text.split('\n')
    for line in lines[:5]:
        if re.search(r'[A-Z][a-z]+ [A-Z][a-z]+', line.strip()):
            return line.strip()
    return ""

def extract_email(text):
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return email.group(0) if email else ""

def extract_phone(text):
    phone = re.search(r'(\+?\d[\d -]{8,}\d)', text)
    return phone.group(0) if phone else ""

def extract_skills(text):
    skills_list = ["python", "java", "sql", "machine learning", "data analysis", 
                  "project management", "communication", "teamwork", "leadership"]
    found_skills = []
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text.lower()):
            found_skills.append(skill.title())
    return found_skills[:10]

def extract_experience(text):
    exp = re.search(r'(\d+)\s*(years?|yrs?)', text.lower())
    return exp.group(1) if exp else "0"

def extract_education(text):
    degrees = ["bachelor", "master", "phd", "mba", "bsc", "msc", "btech", "mtech"]
    for line in text.split('\n'):
        for degree in degrees:
            if degree in line.lower():
                return line.strip()
    return ""

# -------------------- AI Models (Disabled Temporarily) --------------------
# @st.cache_resource
# def load_models():
#     try:
#         generator = pipeline("text2text-generation", model="google/flan-t5-base")
#         classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
#         qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")
#         return generator, classifier, qa_model
#     except Exception as e:
#         st.error(f"Failed to load models: {e}")
#         return None, None, None

# generator, classifier, qa_model = load_models()
# if generator is None:
#     st.error("AI models failed to load. Some features may not work.")

# Temporarily set to None to avoid loading issues
generator, classifier, qa_model = None, None, None

# -------------------- Cover Letter Generator --------------------
def generate_cover_letter(resume_text, job_title, job_description=""):
    if generator is None:
        return "Placeholder cover letter (AI model loading disabled)."
    prompt = f"""
    Write a professional cover letter for a {job_title} position based on this resume information: 
    {resume_text[:1000]}
    
    The job description is: {job_description[:500]}
    
    The cover letter should:
    - Be 3-4 paragraphs long
    - Highlight relevant skills and experience
    - Show enthusiasm for the position
    - Be tailored to the job description
    """
    result = generator(prompt, max_length=500, do_sample=True, temperature=0.7)
    return result[0]['generated_text']

# -------------------- Resume Tailoring --------------------
def tailor_resume(resume_text, job_description):
    if generator is None:
        return "Placeholder resume tailoring (AI model loading disabled)."
    prompt = f"""
    Analyze this job description: {job_description[:1000]}
    
    Suggest improvements for this resume to better match the job requirements: 
    {resume_text[:2000]}
    
    Provide specific recommendations for:
    - Skills to emphasize
    - Experience to highlight
    - Keywords to include
    - Any missing qualifications
    """
    result = generator(prompt, max_length=600, do_sample=True, temperature=0.7)
    return result[0]['generated_text']

# -------------------- Interview Prep --------------------
def generate_interview_questions(job_title, job_description):
    if generator is None:
        return "Placeholder interview questions (AI model loading disabled)."
    prompt = f"""
    Generate 10 technical and 5 behavioral interview questions for a {job_title} position.
    
    Job description: {job_description[:1000]}
    
    Organize the questions into categories and provide sample answers for 2 key questions.
    """
    result = generator(prompt, max_length=800, do_sample=True, temperature=0.7)
    return result[0]['generated_text']

# -------------------- Salary Comparison --------------------
def get_salary_data(job_title, location):
    salaries = {
        "Data Scientist": {"Remote": "$120,000", "New York": "$140,000", "San Francisco": "$150,000"},
        "Software Engineer": {"Remote": "$110,000", "New York": "$130,000", "San Francisco": "$140,000"},
        "Marketing Manager": {"Remote": "$90,000", "New York": "$110,000", "San Francisco": "$120,000"}
    }
    
    if job_title in salaries and location in salaries[job_title]:
        return salaries[job_title][location]
    elif job_title in salaries:
        return salaries[job_title]["Remote"]
    else:
        return "$100,000"

# -------------------- Job Platform Scrapers --------------------
def scrape_monster(keyword, location):
    return [{"Title": "Test Job", "Company": "Monster Inc", "Platform": "Monster", "Link": "http://example.com"}]

def scrape_angellist(keyword, location):
    return []

def scrape_internshala(keyword):
    return []

def scrape_naukri(keyword, location):
    return []

def scrape_indeed(keyword, location):
    return []

def scrape_timesjobs(keyword):
    return []

def scrape_linkedin(keyword, location):
    return []

def scrape_job_platforms(keyword, location):
    with st.spinner("Searching across multiple platforms..."):
        results = []
        
        def run_scraper(scraper_func, *args):
            try:
                results.extend(scraper_func(*args))
            except:
                pass
        
        scrapers = [
            (scrape_monster, (keyword, location)),
            (scrape_angellist, (keyword, location)),
            (scrape_internshala, (keyword,)),
            (scrape_naukri, (keyword, location)),
            (scrape_indeed, (keyword, location)),
            (scrape_timesjobs, (keyword,)),
            (scrape_linkedin, (keyword, location))
        ]
        
        threads = []
        for scraper, args in scrapers:
            t = threading.Thread(target=run_scraper, args=(scraper, *args))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
        
        return results

# -------------------- Application Tracker --------------------
def init_application_tracker():
    if 'applications' not in st.session_state:
        st.session_state.applications = pd.DataFrame(columns=[
            "Date", "Company", "Position", "Platform", "Status", 
            "Response", "InterviewDate", "Notes"
        ])

def add_application(company, position, platform):
    new_app = pd.DataFrame([{
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Company": company,
        "Position": position,
        "Platform": platform,
        "Status": "Applied",
        "Response": "",
        "InterviewDate": "",
        "Notes": ""
    }])
    
    st.session_state.applications = pd.concat(
        [st.session_state.applications, new_app], ignore_index=True)
    save_applications()

def save_applications():
    if 'applications' in st.session_state:
        st.session_state.applications.to_csv("job_applications.csv", index=False)

def load_applications():
    try:
        st.session_state.applications = pd.read_csv("job_applications.csv")
    except:
        init_application_tracker()

# -------------------- Notifications --------------------
def send_email_alert(to_email, subject, body):
    try:
        sender_email = st.secrets.get("EMAIL_SENDER", "default@example.com")
        sender_password = st.secrets.get("EMAIL_PASSWORD", "")
        smtp_server = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = st.secrets.get("SMTP_PORT", 587)

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = to_email

        text = body
        part = MIMEText(text, "plain")
        message.attach(part)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
    except Exception as e:
        st.warning(f"Failed to send email: {e}")

# -------------------- Translation --------------------
def translate_text(text, target_language="en"):
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except:
        return text

# -------------------- UI Components --------------------
def show_login():
    st.title("🔐 Login to CareerUpskillers")
    st.markdown("Access your personalized job search dashboard")
    
    result = oauth2.authorize_button("Login with Google", REDIRECT_URI, SCOPE)
    
    if result:
        st.write("OAuth Result:", result)  # Debug: Show OAuth response
        if 'token' in result:
            st.session_state.token = result.get('token')
            st.session_state.auth = True
            userinfo = oauth2.get_user_info(result.get('token'))
            st.write("User Info:", userinfo)  # Debug: Show user info
            st.session_state.user = userinfo
            st.write("Login successful, redirecting...")
            st.rerun()
    else:
        st.write("Please log in to continue.")

def dashboard_header():
    try:
        st.markdown(f"""
        <style>
            .header {{
                background: linear-gradient(90deg, #2AB7CA 0%, #1A3550 100%);
                color: white;
                padding: 15px;
                border-radius: 12px;
                margin-bottom: 20px;
            }}
            .welcome {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .last-login {{
                font-size: 12px;
                color: #e0e0e0;
            }}
        </style>
        <div class="header">
            <div class="welcome">👋 Welcome, {st.session_state.user.get('name', 'User')}</div>
            <div class="last-login">Last login: {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error in dashboard_header: {e}")

def job_search_section():
    with st.expander("🔍 Advanced Job Search", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            keyword = st.text_input("Job Title / Keywords", value="Data Science")
            location = st.text_input("Search Location", value="Remote")
        with col2:
            salary_range = st.slider("Minimum Salary Expectation ($)", 30000, 200000, 80000, 5000)
            experience_level = st.selectbox("Experience Level", 
                                          ["Entry Level", "Mid Level", "Senior", "Executive"])
        
        job_type = st.multiselect("Job Type", 
                                ["Full-time", "Part-time", "Contract", "Internship", "Remote"],
                                default=["Full-time", "Remote"])
        
        if st.button("🚀 Search Jobs", use_container_width=True):
            return {
                "keyword": keyword,
                "location": location,
                "salary_range": salary_range,
                "experience_level": experience_level,
                "job_type": job_type
            }
    return None

def display_job_results(jobs, resume_text):
    if not jobs:
        st.warning("No jobs found with these criteria. Try different filters.")
        return
    
    st.subheader(f"📋 Found {len(jobs)} Jobs")
    
    tab1, tab2, tab3 = st.tabs(["Job List", "Application Stats", "Salary Insights"])
    
    with tab1:
        for i, job in enumerate(jobs):
            with st.container(border=True):
                cols = st.columns([3,1])
                with cols[0]:
                    st.markdown(f"### {job['Title']}")
                    st.markdown(f"**Company:** {job['Company']} | **Platform:** {job['Platform']}")
                with cols[1]:
                    if st.button(f"Apply #{i+1}", key=f"apply_{i}"):
                        apply_for_job(job, resume_text)
                
                with st.expander("Job Details & Tools"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"[🔗 View Job Posting]({job['Link']})")
                        if st.button("📝 Generate Cover Letter", key=f"letter_{i}"):
                            with st.spinner("Generating tailored cover letter..."):
                                cover_letter = generate_cover_letter(
                                    resume_text, job['Title'], "Sample job description")
                                st.text_area("Cover Letter", cover_letter, height=300)
                    with col2:
                        if st.button("✨ Tailor My Resume", key=f"tailor_{i}"):
                            with st.spinner("Analyzing job requirements..."):
                                recommendations = tailor_resume(
                                    resume_text, "Sample job description")
                                st.text_area("Recommendations", recommendations, height=300)
    
    with tab2:
        if 'applications' in st.session_state and not st.session_state.applications.empty:
            st.write("Your Application History")
            
            df = st.session_state.applications.copy()
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date', ascending=False)
            
            status_counts = df['Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            fig1 = px.pie(status_counts, values='Count', names='Status', 
                         title='Application Status Distribution')
            st.plotly_chart(fig1, use_container_width=True)
            
            df['Month'] = df['Date'].dt.strftime('%Y-%m')
            timeline = df.groupby(['Month', 'Status']).size().unstack().fillna(0)
            fig2 = px.bar(timeline, barmode='stack', 
                         title='Applications Over Time')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("You haven't applied to any jobs yet.")
    
    with tab3:
        salary_data = {
            "Position": ["Data Scientist", "Software Engineer", "Product Manager"],
            "Remote": [120000, 110000, 95000],
            "New York": [140000, 130000, 115000],
            "San Francisco": [150000, 140000, 125000]
        }
        df = pd.DataFrame(salary_data).melt(id_vars="Position", 
                                          var_name="Location", 
                                          value_name="Salary")
        
        fig = px.bar(df, x="Position", y="Salary", color="Location",
                     barmode="group", title="Salary Comparison by Role and Location")
        st.plotly_chart(fig, use_container_width=True)

def apply_for_job(job, resume_text):
    st.session_state.current_application = job
    st.session_state.show_application_form = True
