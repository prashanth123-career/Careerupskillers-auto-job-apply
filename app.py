# ✅ app.py (updated with fresher logic, interview & courses section live)

import streamlit as st
import urllib.parse
from datetime import datetime

# Hide Streamlit header and footer
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.set_page_config(page_title="🌍 Global AI Career Hub", page_icon="🚀", layout="wide")

# ---------------- Sidebar Navigation ----------------
st.sidebar.title("🌍 CareerUpskillers")
page = st.sidebar.radio("Choose Section", ["AI Job Finder", "Interview Preparation", "Free Courses"])

# ---------------- Constants ----------------
LANGUAGES = {
    "English": "en",
    "Arabic": "ar",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Chinese": "zh"
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
                ("🦾 Hugging Face Course", "https://huggingface.co/course")
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
    exec(open("/mount/src/careerupskillers-auto-job-apply/app.py").read())
