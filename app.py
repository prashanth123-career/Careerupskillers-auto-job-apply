import streamlit as st
import urllib.parse

# --- App Configuration ---
st.set_page_config(
    page_title="🌍 Global AI Career Hub", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Constants ---
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

# --- Helper Functions ---
def linkedin_url(keyword, location, time_filter, experience, remote_option, easy_apply, language="en"):
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
        "hl": language
    }
    return f"https://www.linkedin.com/jobs/search/?{urllib.parse.urlencode({k: v for k, v in params.items() if v})}"

def indeed_url(keyword, location, country, salary=None, language="en"):
    domain_map = {
        "USA": "www.indeed.com",
        "UK": "uk.indeed.com",
        "Canada": "ca.indeed.com",
        "Australia": "au.indeed.com",
        "India": "www.indeed.co.in",
        "UAE": "www.indeed.ae",
        "Germany": "de.indeed.com",
        "New Zealand": "nz.indeed.com"
    }
    base_url = f"https://{domain_map.get(country, 'www.indeed.com')}/jobs"
    params = {
        "q": keyword,
        "l": location,
        "hl": language
    }
    if salary and country not in ["India", "UAE"]:
        params["salary"] = salary
    return f"{base_url}?{urllib.parse.urlencode(params)}"

def google_jobs_url(keyword, location, country, language="en"):
    country_domain = {
        "USA": "com",
        "UK": "co.uk",
        "Canada": "ca",
        "Australia": "com.au",
        "India": "co.in",
        "UAE": "ae",
        "Germany": "de",
        "New Zealand": "co.nz"
    }
    domain = country_domain.get(country, "com")
    return f"https://www.google.{domain}/search?q={urllib.parse.quote(keyword)}+jobs+in+{urllib.parse.quote(location)}&ibp=htl;jobs&hl={language}"

def generate_job_links(keyword, location, country, salary=None, language="en"):
    query = urllib.parse.quote_plus(keyword)
    loc = urllib.parse.quote_plus(location)
    portals = [
        ("Google Jobs", google_jobs_url(keyword, location, country, language)),
        ("Indeed", indeed_url(keyword, location, country, salary, language))
    ]
    
    if country == "USA":
        portals.extend([
            ("Glassdoor", f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={query}&locKeyword={loc}"),
            ("ZipRecruiter", f"https://www.ziprecruiter.com/jobs-search?search={query}&location={loc}")
        ])
    elif country == "UAE":
        portals.extend([
            ("Bayt", f"https://www.bayt.com/en/uae/jobs/{keyword.replace(' ', '-')}-jobs/"),
            ("GulfTalent", f"https://www.gulftalent.com/jobs/{keyword.replace(' ', '-')}")
        ])
    return portals

def show_interview_prep(job_role):
    st.subheader(f"🎤 {job_role} Interview Preparation")
    tab1, tab2 = st.tabs(["🎁 Free Resources", "💎 Premium Resources"])
    
    with tab1:
        if job_role in JOB_RESOURCES:
            for name, url in JOB_RESOURCES[job_role]["interview"]["free"]:
                st.markdown(f"🔗 [{name}]({url})")
        else:
            st.info("💡 General interview resources:")
            st.markdown("🔗 [📹 Common Technical Interviews (YouTube)](https://youtu.be/1qw5ITr3k9E)")
            st.markdown("🔗 [💻 LeetCode Top Questions](https://leetcode.com/problem-list/top-interview-questions)")
    
    with tab2:
        if job_role in JOB_RESOURCES:
            for name, url in JOB_RESOURCES[job_role]["interview"]["paid"]:
                st.markdown(f"🔗 [{name}]({url})")
        else:
            st.markdown("🔗 [🎓 Interview Prep Courses (Udemy)](https://www.udemy.com/topic/interview-questions/)")

def show_free_courses(job_role):
    st.subheader(f"🎓 Free {job_role} Learning Resources")
    
    if job_role in JOB_RESOURCES:
        st.markdown("### 🏆 Curated Courses")
        for name, url in JOB_RESOURCES[job_role]["courses"]["free"]:
            st.markdown(f"🔗 [{name}]({url})")
    
    st.markdown("### 🔍 Search More Learning Resources")
    st.markdown(f"🔗 [Coursera ({job_role} courses)](https://www.coursera.org/search?query={urllib.parse.quote(job_role)}&productDifficultyLevel=beginner)")
    st.markdown(f"🔗 [edX (Free {job_role} courses)](https://www.edx.org/search?q={urllib.parse.quote(job_role)})")
    st.markdown(f"🔗 [YouTube ({job_role} tutorials)](https://www.youtube.com/results?search_query={urllib.parse.quote(job_role)}+tutorial)")

# --- Main App ---
def main():
    st.sidebar.title("🌍 Navigation")
    app_mode = st.sidebar.radio("Choose Section", 
                               ["AI Job Finder", "Interview Preparation", "Free Courses"],
                               index=0)
    
    if app_mode == "AI Job Finder":
        st.title("🔍 Global AI Job Finder")
        with st.form("job_form"):
            col1, col2 = st.columns(2)
            with col1:
                keyword = st.text_input("Job Title", "Data Scientist")
                location = st.text_input("Location", "Remote")
                country = st.selectbox("Country", ["USA", "UK", "India", "UAE", "Germany", "Canada", "Australia"])
            with col2:
                time_filter = st.selectbox("Date Posted", ["Past month", "Past week", "Past 24 hours", "Any time"])
                experience = st.selectbox("Experience", ["Any", "Entry level", "Mid-Senior level", "Director"])
                language = st.selectbox("Language", list(LANGUAGES.keys()))
            
            if st.form_submit_button("Find Jobs"):
                lang_code = LANGUAGES[language]
                st.session_state['job_role'] = keyword
                
                st.subheader("🔗 Job Search Results")
                linkedin_link = linkedin_url(keyword, location, time_filter, experience, "Remote", False, lang_code)
                st.markdown(f"✅ [LinkedIn Jobs]({linkedin_link})")
                
                for name, url in generate_job_links(keyword, location, country, None, lang_code):
                    st.markdown(f"✅ [{name}]({url})")
    
    elif app_mode == "Interview Preparation":
        st.title("🎤 AI Interview Preparation")
        job_role = st.selectbox("Select Job Role", 
                               list(JOB_RESOURCES.keys()) + ["Other Tech Role"],
                               index=0)
        show_interview_prep(job_role)
    
    elif app_mode == "Free Courses":
        st.title("🎓 Free AI/ML Courses")
        job_role = st.selectbox("Select Learning Path", 
                               list(JOB_RESOURCES.keys()) + ["Other Tech Field"],
                               index=0)
        show_free_courses(job_role)

if __name__ == "__main__":
    main()
