import streamlit as st
from openai import OpenAI
import PyPDF2
import docx2txt
import urllib.parse

st.set_page_config(page_title="Job Finder + Cover Letter", page_icon="💼", layout="centered")

# ---- Setup OpenAI Client ----
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
Write a concise and professional cover letter for the role of {role}.
Candidate has {experience} years of experience and these skills: {skills}.
Keep it formal and job-application friendly.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

# ---- LinkedIn Smart Search Link ----
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
    return f"https://www.linkedin.com/jobs/search/?{urllib.parse.urlencode({k: v for k, v in params.items() if v})}"

# ---- Streamlit UI ----
st.title("💼 AI Job Finder + Cover Letter Generator")
st.markdown("📄 Upload your resume, and find jobs with smart search + AI-generated cover letters.")

with st.form("job_form"):
    col1, col2 = st.columns(2)
    with col1:
        role = st.text_input("Job Role", "Data Scientist")
        experience = st.number_input("Experience (years)", min_value=0.0, max_value=30.0, value=2.5, step=0.1)
        skills = st.text_input("Skills (comma-separated)", "Python, SQL, ML")
    with col2:
        location = st.text_input("Preferred Location", "Remote")
        time_range = st.selectbox("Job Posted In", ["Past 24 hours", "Past week", "Past month", "Any time"])
        resume = st.file_uploader("Upload Resume", type=["pdf", "docx"])
        generate = st.checkbox("Generate AI Cover Letter", value=True)

    submitted = st.form_submit_button("🔍 Search & Generate")

if submitted:
    if not resume or not role or not skills:
        st.error("Please fill all fields and upload your resume.")
    else:
        st.success("✅ Resume parsed and job search started.")
        resume_text = parse_resume(resume)
        search_link = linkedin_search_url(role, location, time_range)

        st.markdown(f"🔗 [Click here to view jobs on LinkedIn]({search_link})")

        if generate:
            with st.spinner("✍️ Generating AI Cover Letter..."):
                cover = generate_cover_letter(role, experience, skills)
                st.text_area("📩 AI-Generated Cover Letter", cover, height=300)
