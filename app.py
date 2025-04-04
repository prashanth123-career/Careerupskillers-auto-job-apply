import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Mega Job Finder", page_icon="🌐", layout="centered")

# --- Enhanced Portal Database ---
PORTALS_BY_COUNTRY = {
    "USA": [
        ("LinkedIn", lambda k,l,s: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed", lambda k,l,s: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Glassdoor", lambda k,l,s: f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={urllib.parse.quote(k)}&locKeyword={urllib.parse.quote(l)}"),
        ("Monster", lambda k,l,s: f"https://www.monster.com/jobs/search/?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}"),
        ("ZipRecruiter", lambda k,l,s: f"https://www.ziprecruiter.com/jobs-search?search={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Dice (Tech)", lambda k,l,s: f"https://www.dice.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Built In (Startups)", lambda k,l,s: f"https://builtin.com/jobs?search={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("AngelList (Startups)", lambda k,l,s: f"https://angel.co/jobs?role={urllib.parse.quote(k)}&locations[]={urllib.parse.quote(l)}"),
        ("USAJobs (Govt)", lambda k,l,s: f"https://www.usajobs.gov/Search/Results?k={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("CareerBuilder", lambda k,l,s: f"https://www.careerbuilder.com/jobs?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("SimplyHired", lambda k,l,s: f"https://www.simplyhired.com/search?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Ladders ($100K+)", lambda k,l,s: f"https://www.theladders.com/jobs/search-jobs?searchString={urllib.parse.quote(k)}&locationString={urllib.parse.quote(l)}"),
        ("Hired (Tech)", lambda k,l,s: f"https://hired.com/search?query={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Robert Half", lambda k,l,s: f"https://www.roberthalf.com/jobs/{urllib.parse.quote(k.lower().replace(' ','-'))}/{urllib.parse.quote(l.lower().replace(' ','-'))}")
    ]
    # Other countries unchanged...
}

# --- UI with Enhanced Filters ---
st.title("🌍 Mega Job Finder")
st.markdown("🔎 Access **50+ job portals** worldwide with smart filters")

with st.form("job_form"):
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("Job Title / Keywords", "Data Scientist")
        location = st.text_input("Preferred Location", "Remote")
        country = st.selectbox("Country", list(PORTALS_BY_COUNTRY.keys()))

    with col2:
        experience = st.selectbox("Experience Level", ["Any", "Entry", "Mid", "Senior", "Executive"])
        remote_option = st.selectbox("Work Type", ["Any", "Remote", "Hybrid", "On-site"])
        date_posted = st.selectbox("Date Posted", ["Any time", "Past month", "Past week", "Past 24 hours"])

    submitted = st.form_submit_button("🔍 Find Jobs")

if submitted:
    st.subheader(f"🌐 {len(PORTALS_BY_COUNTRY[country])} Job Portals in {country}")

    for name, url_func in PORTALS_BY_COUNTRY[country]:
        url = url_func(keyword, location, "")
        st.markdown(f"- 🔗 [{name}]({url})")

    st.success(f"✅ Generated {len(PORTALS_BY_COUNTRY[country])} job search links")

    st.markdown("""
    <div style='background-color:#f0f2f6; padding:20px; border-radius:10px; margin-top:30px;'>
        <h3 style='color:#1e3a8a;'>Need more options?</h3>
        <p>Try these global aggregators:</p>
        <a href='https://www.google.com/search?q={urllib.parse.quote(keyword)}+jobs+in+{urllib.parse.quote(location)}&ibp=htl;jobs' 
           target='_blank' 
           style='background-color:#1e3a8a; color:white; padding:10px 15px; text-decoration:none; border-radius:5px; display:inline-block; margin-top:10px;'>
            🔍 Search Google Jobs
        </a>
    </div>
    """, unsafe_allow_html=True)
