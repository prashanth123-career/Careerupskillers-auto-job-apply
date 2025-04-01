# Enhanced Resume Analyzer with Free AI
import streamlit as st
import re
from transformers import pipeline
import docx2txt
import PyPDF2
import urllib.parse

# -------------------- Setup --------------------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🤖", layout="wide")

# Load free AI models
@st.cache_resource
def load_models():
    skill_extractor = pipeline("text2text-generation", model="facebook/bart-base")
    job_matcher = pipeline("text-classification", model="distilbert-base-uncased") 
    return skill_extractor, job_matcher

# -------------------- Resume Analysis --------------------
def extract_skills_ai(text, skill_extractor):
    """Use AI to extract skills from text"""
    prompt = f"Extract technical skills and job roles from this resume text: {text[:2000]}"
    try:
        result = skill_extractor(prompt, max_length=300, do_sample=False)
        return parse_ai_output(result[0]['generated_text'])
    except:
        return []

def parse_ai_output(text):
    """Parse AI output into skills list"""
    skills = re.findall(r'\b(?:Python|Java|SQL|JavaScript|React|AWS|Azure|Machine Learning|Data Analysis|Data Science|Web Development|Cloud Computing)\b', text, re.IGNORECASE)
    roles = re.findall(r'\b(?:Engineer|Developer|Analyst|Specialist|Manager|Designer|Scientist|Architect)\b', text, re.IGNORECASE)
    return list(set(skills + roles))

def suggest_jobs_ai(skills, job_matcher):
    """Use AI to suggest matching jobs"""
    if not skills:
        return []
    
    prompt = f"Suggest 5 job titles that match these skills: {', '.join(skills)}"
    try:
        result = job_matcher(prompt, candidate_labels=[
            "Software Engineer", "Data Analyst", "Web Developer", 
            "Cloud Architect", "ML Engineer", "Product Manager",
            "DevOps Engineer", "UX Designer", "Data Scientist"
        ])
        return [pred['label'] for pred in sorted(result, key=lambda x: x['score'], reverse=True)[:5]]
    except:
        return []

# -------------------- Streamlit UI --------------------
def main():
    st.title("🤖 AI-Powered Resume Analyzer")
    st.markdown("Upload your resume to discover your best job matches")
    
    skill_extractor, job_matcher = load_models()
    
    resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    
    if resume_file and st.button("Analyze My Resume"):
        with st.spinner("AI is analyzing your resume..."):
            # Parse resume text
            text = ""
            if resume_file.name.endswith(".pdf"):
                reader = PyPDF2.PdfReader(resume_file)
                text = " ".join([page.extract_text() or "" for page in reader.pages])
            else:
                text = docx2txt.process(resume_file)
            
            # Extract skills using AI
            skills = extract_skills_ai(text, skill_extractor)
            
            if not skills:
                st.error("Our AI couldn't identify specific skills. Try a more detailed resume.")
                st.info("Common missing elements: Programming languages, tools, job titles")
                return
            
            # Get job suggestions
            suggested_jobs = suggest_jobs_ai(skills, job_matcher)
            
            # Display results
            st.success("🎯 Here's what we found in your resume:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Your Top Skills")
                for skill in skills[:10]:
                    st.markdown(f"- {skill}")
                if len(skills) > 10:
                    st.caption(f"+ {len(skills)-10} more skills")
            
            with col2:
                st.subheader("Recommended Jobs")
                for job in suggested_jobs:
                    search_url = f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(job)}"
                    st.markdown(f"- [{job}]({search_url})")
            
            # Show resume insights
            st.divider()
            st.subheader("AI Analysis Summary")
            st.markdown("""
            Based on your resume, you appear to have experience with:
            - **{primary_skill}** and related technologies
            - Roles like **{sample_role}**
            - Approximately **{years} years** of experience
            """.format(
                primary_skill=skills[0] if skills else "technical fields",
                sample_role=suggested_jobs[0] if suggested_jobs else "technical roles",
                years=min(5, len(re.findall(r'\b(20\d{2})\b', text)))
            )
            
            st.info("💡 Tip: Add more specific skills and technologies to improve matches")

if __name__ == "__main__":
    main()
