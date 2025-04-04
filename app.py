import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Mega Job Finder", page_icon="🌐", layout="centered")

# --- Enhanced Portal Database ---
PORTALS_BY_COUNTRY = {
    "USA": [
        ("LinkedIn", lambda k,l,s,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Indeed", lambda k,l,s,e,d: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Glassdoor", lambda k,l,s,e,d: f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={urllib.parse.quote(k)}&locKeyword={urllib.parse.quote(l)}"),
        ("Monster", lambda k,l,s,e,d: f"https://www.monster.com/jobs/search/?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}"),
        ("ZipRecruiter", lambda k,l,s,e,d: f"https://www.ziprecruiter.com/jobs-search?search={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Dice (Tech)", lambda k,l,s,e,d: f"https://www.dice.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "UK": [
        ("LinkedIn UK", lambda k,l,s,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Indeed UK", lambda k,l,s,e,d: f"https://uk.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "India": [
        ("LinkedIn India", lambda k,l,s,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Indeed India", lambda k,l,s,e,d: f"https://www.indeed.co.in/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "Canada": [
        ("LinkedIn Canada", lambda k,l,s,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Indeed CA", lambda k,l,s,e,d: f"https://ca.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "Australia": [
        ("LinkedIn Australia", lambda k,l,s,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Indeed AU", lambda k,l,s,e,d: f"https://au.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ]
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

    # Filter mappings for LinkedIn-style portals
    time_map = {
        "Any time": "",
        "Past month": "r2592000",
        "Past week": "r604800",
        "Past 24 hours": "r86400"
    }
    exp_map = {
        "Any": "",
        "Entry": "2",
        "Mid": "3",
        "Senior": "4",
        "Executive": "5"
    }
    d_filter = time_map[date_posted]
    e_filter = exp_map[experience]

    for name, url_func in PORTALS_BY_COUNTRY[country]:
        if "LinkedIn" in name:
            url = url_func(keyword, location, "", e_filter, d_filter)
        else:
            url = url_func(keyword, location, "", "", "")
        st.markdown(f"- 🔗 [{name}]({url})")

    st.success(f"✅ Generated {len(PORTALS_BY_COUNTRY[country])} job search links")

    st.markdown(f"""
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
