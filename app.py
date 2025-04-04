# ✅ app.py (fully merged single script with job finder, interview prep, and courses)

import streamlit as st
import urllib.parse
from datetime import datetime

# Hide Streamlit header and footer
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="🌍 Global AI Career Hub", page_icon="🚀", layout="wide")

# ---------------- Sidebar Navigation ----------------
st.sidebar.title("🌍 CareerUpskillers")
page = st.sidebar.radio("Choose Section", ["AI Job Finder", "Interview Preparation", "Free Courses"])

# ---------------- Constants ----------------
LANGUAGES = {
    "English": "en", "Arabic": "ar", "Hindi": "hi", "German": "de",
    "French": "fr", "Spanish": "es", "Chinese": "zh"
}

JOB_RESOURCES = {
    "Data Scientist": {
        "interview": {
            "free": [
                ("📹 Data Science Interview Guide (YouTube)", "https://youtu.be/r4ofQ8X0Xq0"),
                ("📚 StrataScratch (450+ Problems)", "https://www.stratascratch.com"),
                ("💻 LeetCode Data Science Questions", "https://leetcode.com/explore/learn/card/data-structure/")
            ],
            "paid": [
                ("🎓 Data Science Interview Prep (Udemy)", "https://www.udemy.com/course/data-science-interview-prep/"),
                ("📊 Interview Cake (Full Course)", "https://www.interviewcake.com/data-science-interview-questions")
            ]
        },
        "courses": {
            "free": [
                ("📚 Google Data Analytics (Coursera)", "https://www.coursera.org/professional-certificates/google-data-analytics"),
                ("📈 Kaggle Learn (Interactive)", "https://www.kaggle.com/learn/overview"),
                ("🐍 Python for Data Science (freeCodeCamp)", "https://www.freecodecamp.org/news/python-for-data-science-course/")
            ]
        }
    },
    "AI Engineer": {
        "interview": {
            "free": [
                ("📹 AI System Design (YouTube)", "https://youtu.be/qiWhe4jzx0c"),
                ("💻 AI Interview Questions (GitHub)", "https://github.com/Developer-Y/ai-interview-questions"),
                ("📚 ML Cheatsheets", "https://github.com/afshinea/stanford-cs-229-machine-learning")
            ],
            "paid": [
                ("🎓 Grokking AI Interviews (Educative)", "https://www.educative.io/courses/grokking-ai-software-engineer-interview"),
                ("🤖 Interview Kickstart AI Course", "https://www.interviewkickstart.com/courses/ai-ml-course")
            ]
        },
        "courses": {
            "free": [
                ("🧠 Fast.ai (Practical DL)", "https://course.fast.ai"),
                ("🤖 Andrew Ng's ML (Coursera)", "https://www.coursera.org/learn/machine-learning"),
                ("🧫 Hugging Face Course", "https://huggingface.co/course")
            ]
        }
    }
}

# ---------------- Helper Functions ----------------
def show_interview_resources(job):
    st.subheader(f"🎤 {job} Interview Preparation")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎁 Free Resources")
        if job in JOB_RESOURCES:
            for name, url in JOB_RESOURCES[job]["interview"]["free"]:
                st.markdown(f"🔗 [{name}]({url})")
    with col2:
        st.markdown("### 💎 Premium Resources")
        if job in JOB_RESOURCES:
            for name, url in JOB_RESOURCES[job]["interview"]["paid"]:
                st.markdown(f"🔗 [{name}]({url})")

def show_course_resources(job):
    st.subheader(f"🎓 Free Courses for {job}")
    if job in JOB_RESOURCES:
        for name, url in JOB_RESOURCES[job]["courses"]["free"]:
            st.markdown(f"🔗 [{name}]({url})")
    st.markdown("### 🔍 More:")
    st.markdown(f"🔗 [YouTube {job} Tutorials](https://www.youtube.com/results?search_query={urllib.parse.quote(job)}+tutorial)")
    st.markdown(f"🔗 [Coursera {job}](https://www.coursera.org/search?query={urllib.parse.quote(job)})")

# ---------------- Routes ----------------
if page == "Interview Preparation":
    st.title("🎤 AI Interview Preparation")
    job = st.selectbox("Choose Job Role", list(JOB_RESOURCES.keys()))
    show_interview_resources(job)

elif page == "Free Courses":
    st.title("🎓 Free AI/ML Courses")
    job = st.selectbox("Choose a Learning Path", list(JOB_RESOURCES.keys()))
    show_course_resources(job)

else:
    st.title("🌍 Global AI Job Finder")
    st.markdown("🔎 Enter your job preferences to discover global job opportunities.")

    with st.form("job_form"):
        col1, col2 = st.columns(2)
        with col1:
            keyword = st.text_input("Job Title", "Data Scientist")
            location = st.text_input("Location", "Remote")
            country = st.selectbox("Country", ["USA", "UK", "India", "UAE", "Germany", "Canada", "Australia"])
        with col2:
            time_filter = st.selectbox("Date Posted", ["Past month", "Past week", "Past 24 hours", "Any time"])
            experience = st.selectbox("Experience Level", ["Any", "Entry level", "Mid-Senior level", "Director"])
            language = st.selectbox("Language", list(LANGUAGES.keys()))

        if st.form_submit_button("🔍 Find Jobs"):
            lang_code = LANGUAGES[language]
            st.subheader("🔗 Smart Job Links")
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote_plus(keyword)}&location={urllib.parse.quote_plus(location)}&f_TPR={time_filter}&f_E={experience}&hl={lang_code}"
            st.markdown(f"✅ [LinkedIn Job Search]({search_url})")
            google_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(keyword)}+jobs+in+{urllib.parse.quote_plus(location)}&ibp=htl;jobs"
            st.markdown(f"✅ [Google Job Listings]({google_url})")
