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
    ]
    # You can add other countries here similarly if needed.
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
    <div style='background-color:#f0f2f6; padding:20px; border-radius:10px; margin-top:30px;'><h
