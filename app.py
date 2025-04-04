import streamlit as st
import urllib.parse

st.set_page_config(
    page_title="🌍 Job Finder",
    layout="centered"
)

def linkedin_url(keyword, location):
    return f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(keyword)}&location={urllib.parse.quote(location)}"

def indeed_url(keyword, location, country="USA"):
    domains = {
        "USA": "www.indeed.com",
        "UK": "uk.indeed.com",
        "India": "www.indeed.co.in"
    }
    domain = domains.get(country, "www.indeed.com")
    return f"https://{domain}/jobs?q={urllib.parse.quote(keyword)}&l={urllib.parse.quote(location)}"

def main():
    st.title("🌍 Simple Job Finder")
    
    keyword = st.text_input("Job Title", "Data Scientist")
    location = st.text_input("Location", "Remote")
    country = st.selectbox("Country", ["USA", "UK", "India"])
    
    if st.button("Search Jobs"):
        st.success("Generated Links:")
        
        st.markdown(f"""
        - 🔗 [LinkedIn Jobs]({linkedin_url(keyword, location)})
        - 🔗 [Indeed Jobs]({indeed_url(keyword, location, country)})
        - 🔗 [Google Jobs](https://www.google.com/search?q={urllib.parse.quote(keyword)}+jobs+in+{urllib.parse.quote(location)})
        """)

if __name__ == "__main__":
    main()
