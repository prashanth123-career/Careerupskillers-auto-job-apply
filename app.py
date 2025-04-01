import streamlit as st
import openai
import PyPDF2
import docx2txt
import urllib.parse

st.set_page_config(page_title="Smart Job Finder", page_icon="💼", layout="centered")

# ✅ Set OpenAI key safely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ✅ Resume Parser
def parse_resume(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    return ""

# ✅ Cover Letter with OpenAI (v1+ compatible)
def generate_cover_letter(role, experience, skills):
    prompt = f"""
Write a short and professional cover letter for the role of {role}.
The candidate has {experience} years of experience and skills: {skills}.
Tone: Confident and formal.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

# ✅ LinkedIn Search Link
def linkedin_url(keyword, location, time_range):
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

# ✅ Streamlit UI
st.title("💼 Smart Job Finder + AI Cover Letter")

with st.form("job_form"):
    role = st.text_input("Job Role", "Data Scientist")
    experience = st.number_input("Experience (years)", min_value=0.0, max_value=30.0, value=2.5, step=0.1)
    skills = st.text_input("Key Skills", "Python, Machine Learning, SQL")
    location = st.text_input("Preferred Job Location", "Remote")
    time_range = st.selectbox("Show jobs from", ["Past 24 hours", "Past week", "Past month", "Any time"])
    resume = st.file_uploader("Upload Your Resume", type=["pdf", "docx"])
    generate = st.checkbox("Generate AI Cover Letter", value=True)
    submit = st.form_submit_button("🔍 Search Jobs")

if submit:
    if not role or not skills or not resume:
        st.error("Please fill all fields and upload a resume.")
    else:
        resume_text = parse_resume(resume)
        search_link = linkedin_url(role, location, time_range)
        st.success("✅ Search Ready")
        st.markdown(f"🔗 [Click here to view LinkedIn Jobs]({search_link})")

        if generate:
            with st.spinner("✍️ Generating Cover Letter..."):
                cover = generate_cover_letter(role, experience, skills)
                st.text_area("📩 Your AI-Generated Cover Letter", value=cover, height=300)
