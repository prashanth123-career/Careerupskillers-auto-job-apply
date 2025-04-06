import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Mega Job Finder", page_icon="🌐", layout="centered")

# Industry categories
INDUSTRIES = [
    "All Industries",
    "Technology",
    "Healthcare",
    "Engineering",
    "Finance",
    "Education",
    "Government",
    "Creative/Design",
    "Remote Work",
    "Visa Sponsorship"
]

# Visa sponsorship tags
VISA_SPONSORSHIP_TAGS = {
    "USA": ["H1B", "L1", "OPT"],
    "UK": ["Tier 2", "Skilled Worker"],
    "Canada": ["Express Entry", "PNP"],
    "Australia": ["482", "Skilled Visa"],
    "Germany": ["Blue Card", "Work Permit"],
    "UAE": ["Employment Visa"]
}

# Enhanced Portal database with industry and visa info
PORTALS_BY_COUNTRY = {
    "USA": [
        ("LinkedIn (Visa Sponsorship)", lambda k,l,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}&f_CF={VISA_SPONSORSHIP_TAGS['USA'][0]}", ["Technology", "Engineering", "Visa Sponsorship"]),
        ("USAJobs (Govt)", lambda k,l,e,d: f"https://www.usajobs.gov/Search/Results?k={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}", ["Government"]),
        ("Indeed (Visa Jobs)", lambda k,l,e,d: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}+{VISA_SPONSORSHIP_TAGS['USA'][0]}&l={urllib.parse.quote(l)}", ["Visa Sponsorship"]),
        ("Dice (Tech)", lambda k,l,e,d: f"https://www.dice.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}", ["Technology"]),
        ("MyVisaJobs (Sponsors)", lambda k,l,e,d: f"https://www.myvisajobs.com/Jobs/{urllib.parse.quote(k.lower().replace(' ','-'))}-jobs", ["Visa Sponsorship"])
    ],
    "UK": [
        ("LinkedIn UK (Sponsorship)", lambda k,l,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}&f_CF={VISA_SPONSORSHIP_TAGS['UK'][0]}", ["Technology", "Engineering", "Visa Sponsorship"]),
        ("Guardian Jobs (Govt)", lambda k,l,e,d: f"https://jobs.theguardian.com/jobs/{urllib.parse.quote(k)}/in-{urllib.parse.quote(l)}", ["Government"]),
        ("Indeed UK (Visa Jobs)", lambda k,l,e,d: f"https://uk.indeed.com/jobs?q={urllib.parse.quote(k)}+{VISA_SPONSORSHIP_TAGS['UK'][0]}&l={urllib.parse.quote(l)}", ["Visa Sponsorship"]),
        ("CWJobs (Tech)", lambda k,l,e,d: f"https://www.cwjobs.co.uk/jobs/{k.lower().replace(' ','-')}/in-{l.lower().replace(' ','-')}", ["Technology"]),
        ("UK Visa Jobs", lambda k,l,e,d: f"https://www.ukvisajobs.com/search-results-jobs/?keywords={urllib.parse.quote(k)}", ["Visa Sponsorship"])
    ],
    "India": [
        ("LinkedIn India (Global)", lambda k,l,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote('India')}&f_TPR={d}&f_E={e}&f_CF=visa%20sponsorship", ["Technology", "Engineering", "Visa Sponsorship"]),
        ("Naukri (Global Companies)", lambda k,l,e,d: f"https://www.naukri.com/{k.lower().replace(' ','-')}-jobs-in-{l.lower().replace(' ','-')}?jobType=international", ["Visa Sponsorship"]),
        ("Shine (Overseas Jobs)", lambda k,l,e,d: f"https://www.shine.com/job-search/overseas-{k.lower().replace(' ','-')}-jobs", ["Visa Sponsorship"]),
        ("TimesJobs (Abroad Jobs)", lambda k,l,e,d: f"https://www.timesjobs.com/international-jobs/{k.lower().replace(' ','-')}-jobs-abroad", ["Visa Sponsorship"]),
        ("TechGig (Tech Visa Jobs)", lambda k,l,e,d: f"https://www.techgig.com/jobs/search?keyword={urllib.parse.quote(k)}+visa&location={urllib.parse.quote(l)}", ["Technology", "Visa Sponsorship"]),
        ("Government Jobs", lambda k,l,e,d: f"https://www.indgovtjobs.in/search/label/{urllib.parse.quote(k)}", ["Government"]),
        ("StudyAbroad (Visa Jobs)", lambda k,l,e,d: f"https://www.studyabroad.com/career-options/{k.lower().replace(' ','-')}-jobs-with-visa-sponsorship", ["Visa Sponsorship"]),
        ("OverseasJobsForIndians", lambda k,l,e,d: f"https://overseasjobsforindians.com/search?query={urllib.parse.quote(k)}", ["Visa Sponsorship"])
    ],
    "Canada": [
        ("LinkedIn Canada (Sponsorship)", lambda k,l,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}&f_CF={VISA_SPONSORSHIP_TAGS['Canada'][0]}", ["Technology", "Engineering", "Visa Sponsorship"]),
        ("Job Bank (Govt)", lambda k,l,e,d: f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={urllib.parse.quote(k)}&locationstring={urllib.parse.quote(l)}", ["Government"]),
        ("Indeed CA (Visa Jobs)", lambda k,l,e,d: f"https://ca.indeed.com/jobs?q={urllib.parse.quote(k)}+{VISA_SPONSORSHIP_TAGS['Canada'][0]}&l={urllib.parse.quote(l)}", ["Visa Sponsorship"]),
        ("CanadaVisa Jobs", lambda k,l,e,d: f"https://www.canadavisa.com/career/jobs/search?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}", ["Visa Sponsorship"])
    ],
    "Australia": [
        ("LinkedIn Australia (Sponsorship)", lambda k,l,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}&f_CF={VISA_SPONSORSHIP_TAGS['Australia'][0]}", ["Technology", "Engineering", "Visa Sponsorship"]),
        ("APS Jobs (Govt)", lambda k,l,e,d: f"https://www.apsjobs.gov.au/s/search?query={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}", ["Government"]),
        ("Indeed AU (Visa Jobs)", lambda k,l,e,d: f"https://au.indeed.com/jobs?q={urllib.parse.quote(k)}+{VISA_SPONSORSHIP_TAGS['Australia'][0]}&l={urllib.parse.quote(l)}", ["Visa Sponsorship"])
    ],
    "Global": [
        ("Remote OK (Visa Possible)", lambda k,l,e,d: f"https://remoteok.com/remote-{k.lower().replace(' ','-')}-jobs?&tags=visa_sponsorship", ["Remote Work", "Visa Sponsorship"]),
        ("We Work Remotely (Global)", lambda k,l,e,d: f"https://weworkremotely.com/remote-jobs/search?term={urllib.parse.quote(k)}", ["Remote Work"]),
        ("AngelList (Startups)", lambda k,l,e,d: f"https://angel.co/jobs?ref=search_landing&role_types%5B%5D=any&locations%5B%5D=Remote&keywords={urllib.parse.quote(k)}", ["Technology", "Remote Work"]),
        ("UN Jobs", lambda k,l,e,d: f"https://careers.un.org/lbw/home.aspx?viewtype=SJ&explevel=all&lang=en-US&occup=0&department=0&bydate=0&occnet=0&location=all&level=0&searchtype=0&curr=0&fos=0&gpid=1000000&sort=desc&j={urllib.parse.quote(k)}", ["Government"]),
        ("Relocate.me", lambda k,l,e,d: f"https://relocate.me/search?query={urllib.parse.quote(k)}&country={urllib.parse.quote(l)}", ["Visa Sponsorship"]),
        ("VisaSponsorJobs", lambda k,l,e,d: f"https://visasponsorjobs.com/search?q={urllib.parse.quote(k)}", ["Visa Sponsorship"]),
        ("Jobbatical", lambda k,l,e,d: f"https://jobbatical.com/jobs?search={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}", ["Visa Sponsorship"])
    ]
}

# --- UI ---
st.title("🌍 Mega Job Finder")
st.markdown("🔍 Access **300+ job portals** with industry filters and visa sponsorship options")

with st.form("job_form"):
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("Job Title / Keywords", "Software Engineer")
        location = st.text_input("Preferred Location", "Remote")
        country = st.selectbox("Country", ["Global"] + list(PORTALS_BY_COUNTRY.keys()))
    with col2:
        industry = st.selectbox("Industry", INDUSTRIES)
        experience = st.selectbox("Experience Level", ["Any", "Entry", "Mid", "Senior", "Executive"])
        date_posted = st.selectbox("Date Posted", ["Any time", "Past month", "Past week", "Past 24 hours"])
    
    visa_note = st.container()
    if country != "India":
        visa_note.info("💡 For Indian applicants: Look for 'Visa Sponsorship' tagged jobs that may provide visa after hiring")

    submitted = st.form_submit_button("🔍 Find Jobs")

if submitted:
    st.subheader(f"🌐 {industry} Jobs in {country}")
    
    # Filters mapping
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

    portals = PORTALS_BY_COUNTRY["Global"] if country == "Global" else PORTALS_BY_COUNTRY[country]
    
    # Filter by industry if not "All Industries"
    if industry != "All Industries":
        portals = [p for p in portals if industry in p[2]]
    
    if not portals:
        st.warning(f"No job portals found for {industry} in {country}. Try a different industry or country.")
    else:
        for name, url_func, _ in portals:
            if "LinkedIn" in name:
                url = url_func(keyword, location, e_filter, d_filter)
            else:
                url = url_func(keyword, location, "", "")
            
            # Special styling for visa sponsorship jobs
            if "Visa" in name or "Sponsor" in name:
                st.markdown(f"- 🌎 **[{name}]({url})** *(Visa sponsorship possible)*")
            else:
                st.markdown(f"- 🔗 [{name}]({url})")

        st.success(f"✅ Generated {len(portals)} job search links for {industry}.")

    # Special section for Indian applicants
    if country != "India":
        st.markdown("---")
        st.subheader("🇮🇳 Special for Indian Applicants")
        st.markdown("""
        These international job portals specialize in visa sponsorship opportunities for Indian professionals:
        """)
        
        india_visa_portals = [
            ("Overseas Jobs For Indians", f"https://overseasjobsforindians.com/search?query={urllib.parse.quote(keyword)}"),
            ("Naukri Gulf (Middle East)", f"https://www.naukrigulf.com/{keyword.lower().replace(' ','-')}-jobs"),
            ("Abroad Jobs (TimesJobs)", f"https://www.timesjobs.com/international-jobs/{keyword.lower().replace(' ','-')}-jobs-abroad"),
            ("Shine Overseas Jobs", f"https://www.shine.com/job-search/overseas-{keyword.lower().replace(' ','-')}-jobs"),
            ("Visa Sponsor Jobs", f"https://visasponsorjobs.com/search?q={urllib.parse.quote(keyword)}")
        ]
        
        for name, url in india_visa_portals:
            st.markdown(f"- ✈️ **[{name}]({url})** *(Visa sponsorship after hiring)*")

    # Google fallback with visa search
    google_jobs = f"https://www.google.com/search?q={urllib.parse.quote(keyword)}+jobs+in+{urllib.parse.quote(location)}+visa+sponsorship&ibp=htl;jobs"
    st.markdown(f"""
    <div style='background-color:#f0f2f6; padding:20px; border-radius:10px; margin-top:30px;'>
        <h3 style='color:#1e3a8a;'>Need more options?</h3>
        <p>Try these specialized searches:</p>
        <a href='{google_jobs}' 
           target='_blank' 
           style='background-color:#1e3a8a; color:white; padding:10px 15px; text-decoration:none; border-radius:5px; display:inline-block; margin-top:10px;'>
            🌎 Search Visa Sponsorship Jobs
        </a>
    </div>
    """, unsafe_allow_html=True)
