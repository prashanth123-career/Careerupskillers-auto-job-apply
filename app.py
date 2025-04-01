import streamlit as st
import openai
import PyPDF2
import docx2txt
import urllib.parse

st.set_page_config(page_title="Job Finder + Cover Letter", page_icon="💼", layout="centered")

# ---- Setup API Key ----
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ---- Resume Parser ----
def parse_resume(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    return ""

# ---- Cover Letter Generator ----
def generate_cover_letter(role, experience, skills):
    prompt = f"""
Write a professional, 1-paragraph cover letter for the role of {role}.
Candidate has {experience} years of experience and these skills: {skills}.
Keep it concise, formal and suitable for job applications.
"""
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.5
    )
    return res.choices[0].message.content.strip()

# ---- LinkedIn Job Link ----
def linkedin_search_url(keyword, location, time_range):
    time_map = {
        "Past 24 hours": "r86400",
        "Past week": "r604800",
        "Past month": "r2592000",
        "Any time": ""
    }
    params = {
        "keywords": keyword,
        "location": location,
        "f_TPR": time_map.get(time_range, "")
    }
    return f"https://www.linkedin.com/jobs/search/?{urllib.parse.urlencode({k:v for k,v in params.items() if v})}"

# ---- UI ----
st.title("🔍 Job Finder + AI Cover Letter")

with st.form("job_form"):
    role = st.text_input("Job Title / Role", "Data Scientist")
    experience = st.number_input("Years of Experience", 0.0, 30.0, step=0.1)
    skills = st.text_input("Key Skills", "Python, SQL, Machine Learning")
    location = st.text_input("Preferred Location", "Remote")
    resume = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    time_range = st.selectbox("Jobs Posted In", ["Past 24 hours", "Past week", "Past month", "Any time"])
    generate = st.checkbox("Generate AI Cover Letter", value=True)
    submit = st.form_submit_button("🔍 Search Jobs")

if submit:
    if not role or not skills or not resume:
        st.error("Please fill in all fields and upload your resume.")
    else:
        resume_text = parse_resume(resume)
        job_link = linkedin_search_url(role, location, time_range)
        st.markdown(f"🔗 [View Jobs on LinkedIn]({job_link})")

        if generate:
            with st.spinner("Generating AI cover letter..."):
                cover = generate_cover_letter(role, experience, skills)
                st.text_area("📄 AI-Generated Cover Letter", cover, height=300)
