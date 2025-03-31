# Multi-Platform Job Auto-Applier (Final Clean Version)

import streamlit as st
st.set_page_config(page_title="All-in-One Job Auto-Applier", page_icon="💼", layout="wide")

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from transformers import pipeline
import docx2txt
import PyPDF2
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googletrans import Translator
import plotly.express as px

# -------------------- Resume Parser --------------------
def parse_resume(file):
    text = ""
    ext = file.name.split(".")[-1].lower()
    if ext == "pdf":
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif ext == "docx":
        text = docx2txt.process(file)
    return text

# -------------------- Load AI Generator --------------------
@st.cache_resource
def load_generator():
    return pipeline("text2text-generation", model="t5-small")

generator = load_generator()

# -------------------- Cover Letter Generator --------------------
def generate_cover_letter(resume_text, job_title):
    prompt = f"Write a professional cover letter for a {job_title} job based on this resume: {resume_text[:800]}"
    result = generator(prompt, max_length=300, do_sample=False)
    return result[0]['generated_text']

# -------------------- Job Scraper (Sample: LinkedIn, Naukri) --------------------
def scrape_linkedin(keyword, location):
    jobs = []
    job_titles = ["AI Analyst", "Machine Learning Intern", "Remote Data Scientist"]
    companies = ["LinkedIn Inc", "Techverse AI", "NeuroSpace"]
    for i in range(len(job_titles)):
        jobs.append({
            "Title": job_titles[i],
            "Company": companies[i],
            "Link": f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}",
            "Platform": "LinkedIn"
        })
    return jobs

def scrape_naukri(keyword, location):
    try:
        url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = []
        for card in soup.select(".jobTuple")[:5]:
            title = card.select_one("a.title")
            company = card.select_one("a.subTitle")
            if title and company:
                jobs.append({
                    "Title": title.get_text(strip=True),
                    "Company": company.get_text(strip=True),
                    "Link": title['href'],
                    "Platform": "Naukri"
                })
        return jobs
    except:
        return []

# -------------------- Email Notification --------------------
def send_email_alert(to_email, job_count):
    try:
        sender_email = st.secrets.get("EMAIL_SENDER")
        sender_password = st.secrets.get("EMAIL_PASSWORD")
        smtp_server = st.secrets.get("SMTP_SERVER")
        smtp_port = st.secrets.get("SMTP_PORT", 587)

        message = MIMEMultipart("alternative")
        message["Subject"] = "🎯 New Jobs Found for You!"
        message["From"] = sender_email
        message["To"] = to_email

        text = f"Hi,\n\nWe found {job_count} new jobs for your search.\nVisit the app to apply now!\n\n- CareerUpskillers"
        part = MIMEText(text, "plain")
        message.attach(part)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
    except Exception as e:
        st.warning(f"Failed to send email: {e}")

# -------------------- App UI --------------------
st.title("💼 All-in-One careerupskillers Job Auto-Applier")
st.markdown("Apply smartly with AI-powered cover letters and resume autofill.")

st.subheader("📄 Upload Your Resume")
resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
resume_text = ""
if resume_file:
    resume_text = parse_resume(resume_file)
    st.success("Resume uploaded and parsed successfully!")

st.subheader("👤 Candidate Details")
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")
location = st.text_input("Job Location", value="Remote")
keyword = st.text_input("Job Title / Keywords", value="AI Intern")
use_gpt = st.checkbox("Generate AI-based Cover Letter", value=True)

if st.button("🔍 Search Jobs"):
    if not (name and email and phone and resume_file):
        st.warning("Please fill all fields and upload your resume.")
    else:
        results = scrape_linkedin(keyword, location) + scrape_naukri(keyword, location)
        if results:
            st.success(f"✅ Found {len(results)} jobs!")
            for i, job in enumerate(results):
                with st.container():
                    st.markdown(f"""
                        <div style='border:1px solid #ccc;padding:15px;border-radius:10px;background:#f9f9f9;'>
                        <h4>{i+1}. {job['Title']}</h4>
                        <p><strong>Company:</strong> {job['Company']}</p>
                        <p><strong>Platform:</strong> {job['Platform']}</p>
                        <p><a href='{job['Link']}' target='_blank'>🖱️ Click to Apply</a></p>
                        </div>
                    """, unsafe_allow_html=True)

                    if use_gpt and resume_text:
                        with st.expander("🧠 View AI-Generated Cover Letter"):
                            st.text(generate_cover_letter(resume_text, job['Title']))
        else:
            st.warning("No jobs found.")

        # Optional Email Notification
        if email:
            send_email_alert(email, len(results))

# -------------------- Footer --------------------
st.markdown("""
<style>
.footer {
    background: linear-gradient(90deg, #2AB7CA 0%, #1A3550 100%);
    color: white;
    padding: 15px;
    text-align: center;
    font-size: 14px;
    margin-top: 40px;
    border-radius: 12px;
}
.footer a {
    color: white;
    text-decoration: none;
    margin: 0 8px;
}
</style>
<div class="footer">
    © 2025 CareerUpskillers |
    <a href="https://www.careerupskillers.com/about-1">Privacy</a> |
    <a href="https://wa.me/917892116728">WhatsApp</a> |
    <a href="https://www.youtube.com/@Careerupskillers">YouTube</a> |
    <a href="https://www.facebook.com/share/18gUeR73H6/">Facebook</a> |
    <a href="https://www.linkedin.com/company/careerupskillers/">LinkedIn</a> |
    <a href="https://www.instagram.com/careerupskillers?igsh=YWNmOGMwejBrb24z">Instagram</a>
</div>
""", unsafe_allow_html=True)
