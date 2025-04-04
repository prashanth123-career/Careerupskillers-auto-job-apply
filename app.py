import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Global AI Job Finder", page_icon="🌎", layout="centered")

# Language options (ISO 639-1 codes)
LANGUAGES = {
    "English": "en",
    "Arabic": "ar",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Chinese": "zh"
}

# ---------------- LinkedIn Smart Filtered Link ----------------
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
        "hl": language  # Language parameter
    }

    return f"https://www.linkedin.com/jobs/search/?{urllib.parse.urlencode({k: v for k, v in params.items() if v})}"

# ---------------- Indeed Smart Filtered Link ----------------
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
        "hl": language  # Language parameter
    }
    
    if salary and country not in ["India", "UAE"]:
        params["salary"] = salary
    
    return f"{base_url}?{urllib.parse.urlencode(params)}"

# ---------------- Google Jobs Link ----------------
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

# ---------------- Global Portals Generator ----------------
def generate_job_links(keyword, location, country, salary=None, language="en"):
    query = urllib.parse.quote_plus(keyword)
    loc = urllib.parse.quote_plus(location)

    portals = []
    
    # Common portals for all countries
    portals.append(("Google Jobs", google_jobs_url(keyword, location, country, language)))
    portals.append(("Indeed", indeed_url(keyword, location, country, salary, language)))
    
    # Country-specific portals
    if country == "USA":
        portals.extend([
            ("Glassdoor", f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={query}&locKeyword={loc}"),
            ("Monster", f"https://www.monster.com/jobs/search/?q={query}&where={loc}"),
            ("ZipRecruiter", f"https://www.ziprecruiter.com/jobs-search?search={query}&location={loc}")
        ])
    elif country == "UK":
        portals.extend([
            ("Reed", f"https://www.reed.co.uk/jobs/{query}-jobs-in-{location.replace(' ', '-')}"),
            ("TotalJobs", f"https://www.totaljobs.com/jobs/{query}/in-{location.replace(' ', '-')}")
        ])
    elif country == "India":
        portals.extend([
            ("Naukri", f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"),
            ("Shine", f"https://www.shine.com/job-search/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}")
        ])
    elif country == "UAE":
        portals.extend([
            ("Bayt", f"https://www.bayt.com/en/uae/jobs/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}/"),
            ("GulfTalent", f"https://www.gulftalent.com/jobs/{keyword.replace(' ', '-')}/in-{location.replace(' ', '-')}")
        ])
    elif country == "Germany":
        portals.extend([
            ("StepStone", f"https://www.stepstone.de/jobs/{keyword.replace(' ', '-')}/in-{location.replace(' ', '-')}"),
            ("Indeed DE", f"https://de.indeed.com/jobs?q={query}&l={loc}")
        ])
    
    return portals

# ---------------- UI ----------------
st.title("🌍 Global AI Job Finder")
st.markdown("🔎 Get LinkedIn + top job portals for any country with smart filters!")

with st.form("job_form"):
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("Job Title / Keywords", "Data Scientist")
        location = st.text_input("Preferred Location", "Remote")
        country = st.selectbox("🌐 Country", ["USA", "UK", "India", "Australia", "Canada", "UAE", "Germany", "New Zealand"])
        language = st.selectbox("🌍 Language", list(LANGUAGES.keys()))
    
    with col2:
        time_filter = st.selectbox("📅 LinkedIn Date Posted", ["Past 24 hours", "Past week", "Past month", "Any time"])
        experience = st.selectbox("📈 Experience Level", ["Any", "Internship", "Entry level", "Associate", "Mid-Senior level", "Director"])
        remote_option = st.selectbox("🏢 Work Type", ["Any", "Remote", "On-site", "Hybrid"])
        easy_apply = st.checkbox("⚡ Easy Apply only", value=False)
    
    # Salary filter only shown for supported countries
    if country not in ["India", "UAE"]:
        salary = st.number_input("💰 Minimum Salary (per year)", min_value=0, value=0, step=10000)
    else:
        salary = None
    
    submitted = st.form_submit_button("🔍 Find Jobs")

if submitted:
    lang_code = LANGUAGES[language]
    
    st.subheader("🔗 LinkedIn Smart Search")
    linkedin_link = linkedin_url(keyword, location, time_filter, experience, remote_option, easy_apply, lang_code)
    st.markdown(f"✅ [Open LinkedIn Search]({linkedin_link})")

    st.subheader(f"🌐 Job Portals in {country}")
    for name, url in generate_job_links(keyword, location, country, salary if salary else None, lang_code):
        st.markdown(f"- 🔗 [{name}]({url})")

    st.success("🎯 All job search links generated successfully!")
    
    # Career Counseling CTA
    st.markdown("""
    <div style='background-color:#f0f2f6; padding:20px; border-radius:10px; margin-top:30px;'>
        <h3 style='color:#1e3a8a;'>Need career guidance?</h3>
        <p style='font-size:16px;'>Get personalized career advice in your preferred language</p>
        <a href='https://careerupskillers-ai-advisor-d8vugggkkncjpxirbrcbx6.streamlit.app/' target='_blank' style='background-color:#1e3a8a; color:white; padding:10px 15px; text-decoration:none; border-radius:5px; display:inline-block; margin-top:10px;'>
            🚀 Get Free Career Counseling
        </a>
    </div>
    """, unsafe_allow_html=True)
