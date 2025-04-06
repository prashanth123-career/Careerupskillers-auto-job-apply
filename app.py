import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Bangalore Tech Job Finder", page_icon="💼", layout="centered")

# Top recruiter-preferred portals for Bangalore
BANGALORE_PORTALS = [
    {
        "name": "LinkedIn (Bangalore Tech)",
        "url": lambda k,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location=Bangalore%2C%20Karnataka&f_TPR={d}&f_E={e}&f_JT=F&f_CR=103644278&position=1&pageNum=0",
        "filter": True
    },
    {
        "name": "Naukri (Bangalore Recruiters)",
        "url": lambda k,e,d: f"https://www.naukri.com/{k.lower().replace(' ','-')}-jobs-in-bangalore?experience={e}&jobAge={d}",
        "filter": True
    },
    {
        "name": "Indeed (Bangalore Tech)",
        "url": lambda k,e,d: f"https://www.indeed.co.in/jobs?q={urllib.parse.quote(k)}&l=Bangalore%2C+Karnataka&fromage={d.replace('r','') if d else ''}&explvl={e.lower()}_level",
        "filter": True
    },
    {
        "name": "AngelList (Bangalore Startups)",
        "url": lambda k,e,d: f"https://angel.co/jobs?ref=search_landing&role_types%5B%5D=any&locations%5B%5D=Bangalore&keywords={urllib.parse.quote(k)}",
        "filter": False
    },
    {
        "name": "Google Jobs (Bangalore)",
        "url": lambda k,e,d: f"https://www.google.com/search?q={urllib.parse.quote(k)}+jobs+in+bangalore&ibp=htl;jobs&htichips=employment_type:INTERN,FULLTIME&htischips=employment_type;explvl:{e.lower()}_level",
        "filter": False
    }
]

# Other options
OTHER_OPTIONS = [
    ("TimesJobs Bangalore", "https://www.timesjobs.com/jobs/{keyword}-jobs-in-bangalore"),
    ("QuikrJobs Bangalore", "https://www.quikr.com/jobs/{keyword}-jobs-in-bangalore+zwqxj5158190035"),
    ("Glassdoor Bangalore", "https://www.glassdoor.co.in/Job/bangalore-{keyword}-jobs-SRCH_IL.0,9_IC2940589_KO10,{keyword_len}.htm"),
    ("Monster Bangalore", "https://www.monsterindia.com/srp/results?query={keyword}&locations=Bangalore"),
    ("Hirect (Direct HR Contact)", "https://www.hirect.in/{keyword}-jobs-in-bangalore")
]

# Experience and date mapping
EXP_MAP = {
    "Entry": "1",
    "Mid": "2",
    "Senior": "3",
    "Executive": "4"
}

TIME_MAP = {
    "Past 24 hours": "1",
    "Past week": "7",
    "Past month": "30",
    "Any time": ""
}

# --- UI ---
st.title("💼 Bangalore Tech Job Finder")
st.markdown("🔍 Get **direct recruiter-posted jobs** in Bangalore with precise filters")

with st.form("bangalore_job_form"):
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("Job Title / Keywords", "Software Engineer")
        industry = st.selectbox("Industry", ["Technology", "IT Services", "Product", "Startups", "All Tech"])
    with col2:
        experience = st.selectbox("Experience Level", ["Entry", "Mid", "Senior", "Executive"])
        date_posted = st.selectbox("Date Posted", ["Past 24 hours", "Past week", "Past month", "Any time"])

    submitted = st.form_submit_button("🔍 Find Bangalore Jobs")

if submitted:
    st.subheader(f"💻 {industry} Jobs in Bangalore")
    st.caption(f"Showing {experience.lower()} level jobs posted {date_posted.lower()}")
    
    # Get filter values
    exp_val = EXP_MAP[experience]
    time_val = TIME_MAP[date_posted]
    
    # Display top recruiter portals
    for portal in BANGALORE_PORTALS:
        if portal["filter"]:
            url = portal["url"](keyword, exp_val, time_val)
        else:
            url = portal["url"](keyword, "", "")
        
        if "LinkedIn" in portal["name"]:
            st.markdown(f"""
            <div style='background-color:#f0f8ff; padding:15px; border-radius:10px; margin-bottom:10px;'>
                <h4 style='margin:0;'>⭐ {portal["name"]}</h4>
                <p style='margin:5px 0;'>Pre-filtered with: {experience} level | Posted {date_posted.lower()} | Bangalore only</p>
                <a href='{url}' target='_blank' style='color:white; background-color:#0077b5; padding:5px 10px; border-radius:5px; text-decoration:none;'>Open in LinkedIn</a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background-color:#f9f9f9; padding:15px; border-radius:10px; margin-bottom:10px;'>
                <h4 style='margin:0;'>{portal["name"]}</h4>
                <a href='{url}' target='_blank' style='color:white; background-color:#4CAF50; padding:5px 10px; border-radius:5px; text-decoration:none;'>Search Jobs</a>
            </div>
            """, unsafe_allow_html=True)
    
    st.success(f"✅ Showing top recruiter-preferred portals for Bangalore ({len(BANGALORE_PORTALS)} sources)")
    
    # Other options in flash cards
    st.markdown("---")
    st.subheader("💡 Other Job Search Options")
    
    cols = st.columns(2)
    for idx, (name, url) in enumerate(OTHER_OPTIONS):
        formatted_url = url.replace("{keyword}", keyword.lower().replace(" ","-")).replace("{keyword_len}", str(len(keyword)))
        with cols[idx%2]:
            st.markdown(f"""
            <div style='background-color:#f5f5f5; padding:15px; border-radius:10px; margin-bottom:15px;'>
                <h4 style='margin:0 0 10px 0;'>{name}</h4>
                <a href='{formatted_url}' target='_blank' style='color:white; background-color:#6c757d; padding:3px 8px; border-radius:3px; text-decoration:none; font-size:14px;'>Try This</a>
            </div>
            """, unsafe_allow_html=True)
    
    # Pro tip
    st.markdown("""
    <div style='background-color:#fff3cd; padding:15px; border-radius:10px; margin-top:20px;'>
        <h4 style='margin:0 0 10px 0; color:#856404;'>💡 Pro Tip:</h4>
        <p style='margin:0; color:#856404;'>For best results: <br>
        1. Use exact job titles (e.g., 'Java Developer' instead of 'IT jobs')<br>
        2. Check these portals daily for newest postings<br>
        3. Set up job alerts on each platform</p>
    </div>
    """, unsafe_allow_html=True)
