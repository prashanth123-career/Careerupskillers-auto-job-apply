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
    ],
    "UK": [
        ("LinkedIn UK", lambda k,l,s: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed UK", lambda k,l,s: f"https://uk.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Reed", lambda k,l,s: f"https://www.reed.co.uk/jobs/{k.lower().replace(' ','-')}-jobs-in-{l.lower().replace(' ','-')}"),
        ("TotalJobs", lambda k,l,s: f"https://www.totaljobs.com/jobs/{k.lower().replace(' ','-')}/in-{l.lower().replace(' ','-')}"),
        ("CV-Library", lambda k,l,s: f"https://www.cv-library.co.uk/search-jobs?kw={urllib.parse.quote(k)}&loc={urllib.parse.quote(l)}"),
        ("Jobsite", lambda k,l,s: f"https://www.jobsite.co.uk/jobs/{k.lower().replace(' ','-')}/in-{l.lower().replace(' ','-')}"),
        ("Guardian Jobs", lambda k,l,s: f"https://jobs.theguardian.com/jobs/{urllib.parse.quote(k)}/in-{urllib.parse.quote(l)}"),
        ("CWJobs (Tech)", lambda k,l,s: f"https://www.cwjobs.co.uk/jobs/{k.lower().replace(' ','-')}/in-{l.lower().replace(' ','-')}"),
        ("Jobs.ac.uk (Academic)", lambda k,l,s: f"https://www.jobs.ac.uk/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("CityJobs (Finance)", lambda k,l,s: f"https://www.cityjobs.com/search/?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "India": [
        ("LinkedIn India", lambda k,l,s: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed India", lambda k,l,s: f"https://www.indeed.co.in/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Naukri", lambda k,l,s: f"https://www.naukri.com/{k.lower().replace(' ','-')}-jobs-in-{l.lower().replace(' ','-')}"),
        ("Shine", lambda k,l,s: f"https://www.shine.com/job-search/{k.lower().replace(' ','-')}-jobs-in-{l.lower().replace(' ','-')}"),
        ("TimesJobs", lambda k,l,s: f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={urllib.parse.quote(k)}&txtLocation={urllib.parse.quote(l)}"),
        ("Monster India", lambda k,l,s: f"https://www.monsterindia.com/search/{k.lower().replace(' ','-')}-jobs-in-{l.lower().replace(' ','-')}"),
        ("Freshersworld", lambda k,l,s: f"https://www.freshersworld.com/jobs/jobsearch/{urllib.parse.quote(k)}?location={urllib.parse.quote(l)}"),
        ("HireMee (Freshers)", lambda k,l,s: f"https://www.hiremee.co.in/job-search?skill={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("UpGrad (EdTech)", lambda k,l,s: f"https://www.upgrad.com/jobs/?role={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("CutShort (Startups)", lambda k,l,s: f"https://cutshort.io/jobs?search={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "Australia": [
        ("LinkedIn Australia", lambda k,l,s: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed AU", lambda k,l,s: f"https://au.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Seek", lambda k,l,s: f"https://www.seek.com.au/{k.lower().replace(' ','-')}-jobs/in-{l.lower().replace(' ','-')}"),
        ("Jora", lambda k,l,s: f"https://au.jora.com/j?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("CareerOne", lambda k,l,s: f"https://www.careerone.com.au/jobs?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}"),
        ("Adzuna AU", lambda k,l,s: f"https://www.adzuna.com.au/search?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}"),
        ("GradConnection (Grads)", lambda k,l,s: f"https://www.gradconnection.com/jobs/?search={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Australian Government Jobs", lambda k,l,s: f"https://www.apsjobs.gov.au/s/search?query={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "Canada": [
        ("LinkedIn Canada", lambda k,l,s: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed CA", lambda k,l,s: f"https://ca.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Job Bank", lambda k,l,s: f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={urllib.parse.quote(k)}&locationstring={urllib.parse.quote(l)}"),
        ("Workopolis", lambda k,l,s: f"https://www.workopolis.com/jobsearch/find-jobs?ak={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Eluta", lambda k,l,s: f"https://www.eluta.ca/search?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("TorontoJobs", lambda k,l,s: f"https://www.torontojobs.com/job-search?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("BCJobs", lambda k,l,s: f"https://www.bcjobs.ca/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "UAE": [
        ("LinkedIn UAE", lambda k,l,s: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Bayt", lambda k,l,s: f"https://www.bayt.com/en/uae/jobs/{k.lower().replace(' ','-')}-jobs/"),
        ("GulfTalent", lambda k,l,s: f"https://www.gulftalent.com/jobs/{k.lower().replace(' ','-')}"),
        ("Naukri Gulf", lambda k,l,s: f"https://www.naukrigulf.com/{k.lower().replace(' ','-')}-jobs-in-{l.lower().replace(' ','-')}"),
        ("DubaiJobs", lambda k,l,s: f"https://www.dubaijobs.com/search/{urllib.parse.quote(k)}/{urllib.parse.quote(l)}")
    ],
    "Germany": [
        ("LinkedIn Germany", lambda k,l,s: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed DE", lambda k,l,s: f"https://de.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("StepStone", lambda k,l,s: f"https://www.stepstone.de/jobs/{k.lower().replace(' ','-')}/in-{l.lower().replace(' ','-')}"),
        ("Xing", lambda k,l,s: f"https://www.xing.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Arbeitsagentur", lambda k,l,s: f"https://www.arbeitsagentur.de/jobsuche/suche?was={urllib.parse.quote(k)}&wo={urllib.parse.quote(l)}")
    ],
    "Others": [
        ("LinkedIn Global", lambda k,l,s: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Global", lambda k,l,s: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Google Jobs", lambda k,l,s: f"https://www.google.com/search?q={urllib.parse.quote(k)}+jobs+in+{urllib.parse.quote(l)}&ibp=htl;jobs"),
        ("RemoteOK", lambda k,l,s: f"https://remoteok.com/remote-{k.lower().replace(' ','-')}-jobs"),
        ("We Work Remotely", lambda k,l,s: f"https://weworkremotely.com/remote-jobs/search?term={urllib.parse.quote(k)}")
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
