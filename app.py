import streamlit as st
import urllib.parse
from datetime import datetime

# --- App Configuration ---
st.set_page_config(
    page_title="🌍 AI Career Suite", 
    page_icon="🚀", 
    layout="wide"
)

# --- Constants ---
PLATFORMS = {
    "Interview Preparation": {
        "YouTube": {
            "url": "https://www.youtube.com/results",
            "params": {
                "search_query": "{query} interview preparation",
                "sp": "CAI%253D"  # Sort by relevance
            }
        },
        "LeetCode": {
            "url": "https://leetcode.com/problemset/all/",
            "params": {
                "search": "{query}",
                "topicSlugs": "array"  # Default technical topic
            }
        },
        "Glassdoor": {
            "url": "https://www.glassdoor.com/Interview/index.htm",
            "params": {
                "keyword": "{query}"
            }
        }
    },
    "Free Courses": {
        "Coursera": {
            "url": "https://www.coursera.org/search",
            "params": {
                "query": "{query}",
                "productDifficultyLevel": "beginner",
                "productType": "courses"
            }
        },
        "edX": {
            "url": "https://www.edx.org/search",
            "params": {
                "q": "{query}",
                "subject": "Computer Science"
            }
        },
        "freeCodeCamp": {
            "url": "https://www.freecodecamp.org/news/search/",
            "params": {
                "query": "{query}"
            }
        }
    }
}

# --- URL Builder Functions ---
def build_search_url(base_url, params, query):
    """Constructs a search URL with parameters"""
    formatted_params = {}
    for key, value in params.items():
        formatted_params[key] = value.format(query=urllib.parse.quote(query))
    return f"{base_url}?{urllib.parse.urlencode(formatted_params)}"

def linkedin_jobs_url(keyword, location, filters):
    """LinkedIn job search with UI parameters"""
    params = {
        "keywords": keyword,
        "location": location,
        "f_TPR": filters.get("time", ""),
        "f_E": filters.get("experience", ""),
        "f_WT": filters.get("work_type", "")
    }
    return f"https://www.linkedin.com/jobs/search/?{urllib.parse.urlencode({k: v for k, v in params.items() if v})}"

# --- UI Components ---
def show_job_search():
    st.title("🔍 AI Job Search")
    
    with st.form("job_form"):
        col1, col2 = st.columns(2)
        with col1:
            role = st.text_input("Job Role", "Data Scientist")
            location = st.text_input("Location", "Remote")
            country = st.selectbox("Country", ["USA", "India", "UK", "UAE"])
        
        with col2:
            time_filter = st.selectbox("Posted", ["Past week", "Past month", "Any time"])
            exp_level = st.selectbox("Experience", ["Entry", "Mid", "Senior"])
        
        if st.form_submit_button("Search Jobs"):
            filters = {
                "time": {"Past week": "r604800", "Past month": "r2592000"}.get(time_filter, ""),
                "experience": {"Entry": "2", "Mid": "4", "Senior": "5"}.get(exp_level, ""),
                "work_type": "2"  # Remote
            }
            
            st.success("Generated Search Links:")
            st.markdown(f"""
            - 🔗 [LinkedIn Jobs]({linkedin_jobs_url(role, location, filters)})
            - 🔗 [Indeed Jobs](https://www.indeed.com/jobs?q={urllib.parse.quote(role)}&l={urllib.parse.quote(location)})
            - 🔗 [Google Jobs](https://www.google.com/search?q={urllib.parse.quote(role)}+jobs+in+{urllib.parse.quote(location)}&ibp=htl;jobs)
            """)

def show_resource_search(resource_type):
    st.title(f"🎓 {resource_type} Search")
    
    with st.form(f"{resource_type.lower()}_form"):
        topic = st.text_input("What do you want to learn?", "Machine Learning" if resource_type == "Free Courses" else "Data Structures")
        
        if st.form_submit_button(f"Find {resource_type}"):
            st.success(f"Best {resource_type} Resources:")
            
            for platform, config in PLATFORMS[resource_type].items():
                url = build_search_url(config["url"], config["params"], topic)
                st.markdown(f"- 🔗 [{platform}]({url})")
            
            if resource_type == "Interview Preparation":
                st.markdown(f"""
                Additional Resources:
                - 📚 [Recommended Books](https://www.amazon.com/s?k={urllib.parse.quote(topic)}+interview+prep)
                - 💻 [Practice Tests](https://www.testdome.com/tests?skill={urllib.parse.quote(topic.lower())})
                """)

# --- Main App ---
def main():
    st.sidebar.title("🌍 Navigation")
    tab = st.sidebar.radio("Go to", ["Job Search", "Interview Preparation", "Free Courses"])
    
    if tab == "Job Search":
        show_job_search()
    elif tab == "Interview Preparation":
        show_resource_search("Interview Preparation")
    else:
        show_resource_search("Free Courses")

if __name__ == "__main__":
    main()
