import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Mega Job Finder", page_icon="🌐", layout="centered")

# --- Enhanced Portal database with more industries and government jobs ---
PORTALS_BY_COUNTRY = {
    "USA": [
        ("LinkedIn", lambda k,l,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("USAJobs (Govt)", lambda k,l,e,d: f"https://www.usajobs.gov/Search/Results?k={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Indeed", lambda k,l,e,d: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Monster", lambda k,l,e,d: f"https://www.monster.com/jobs/search/?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}"),
        ("CareerBuilder", lambda k,l,e,d: f"https://www.careerbuilder.com/jobs?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Dice (Tech)", lambda k,l,e,d: f"https://www.dice.com/jobs?q={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Built In (Tech)", lambda k,l,e,d: f"https://builtin.com/jobs?search={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Mediabistro (Media)", lambda k,l,e,d: f"https://www.mediabistro.com/jobs/search/?q={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("BioSpace (Biotech)", lambda k,l,e,d: f"https://www.biospace.com/jobs/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Idealist (Nonprofit)", lambda k,l,e,d: f"https://www.idealist.org/en/?q={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("HigherEdJobs (Education)", lambda k,l,e,d: f"https://www.higheredjobs.com/search/advanced_action.cfm?Keyword={urllib.parse.quote(k)}&Location={urllib.parse.quote(l)}"),
        ("State Government Jobs", lambda k,l,e,d: f"https://www.governmentjobs.com/careers/{l.lower().replace(' ','') if l else 'home'}?keywords={urllib.parse.quote(k)}"),
        ("Federal Government Jobs", lambda k,l,e,d: f"https://www.federaljobs.net/search-jobs.htm?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("HospitalCareers (Healthcare)", lambda k,l,e,d: f"https://www.hospitalcareers.com/jobs/?search={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Energy Jobline (Energy)", lambda k,l,e,d: f"https://www.energyjobline.com/jobs?query={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "UK": [
        ("LinkedIn UK", lambda k,l,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Guardian Jobs (Govt)", lambda k,l,e,d: f"https://jobs.theguardian.com/jobs/{urllib.parse.quote(k)}/in-{urllib.parse.quote(l)}"),
        ("Indeed UK", lambda k,l,e,d: f"https://uk.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Reed", lambda k,l,e,d: f"https://www.reed.co.uk/jobs/{k.lower().replace(' ','-')}-jobs-in-{l.lower().replace(' ','-')}"),
        ("Totaljobs", lambda k,l,e,d: f"https://www.totaljobs.com/jobs/{k.lower().replace(' ','-')}/in-{l.lower().replace(' ','-')}"),
        ("CWJobs (Tech)", lambda k,l,e,d: f"https://www.cwjobs.co.uk/jobs/{k.lower().replace(' ','-')}/in-{l.lower().replace(' ','-')}"),
        ("Jobs.ac.uk (Academic)", lambda k,l,e,d: f"https://www.jobs.ac.uk/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("NHS Jobs (Healthcare)", lambda k,l,e,d: f"https://www.jobs.nhs.uk/xi/search_vacancy/?action=search&keyword={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Civil Service Jobs", lambda k,l,e,d: f"https://www.civil-service.jobs.gov.uk/search/?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("EnvironmentJob (Environmental)", lambda k,l,e,d: f"https://www.environmentjob.co.uk/jobs?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("CharityJob (Nonprofit)", lambda k,l,e,d: f"https://www.charityjob.co.uk/jobs/{k.lower().replace(' ','-')}-jobs?location={urllib.parse.quote(l)}"),
        ("Local Government Jobs", lambda k,l,e,d: f"https://www.lgjobs.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "India": [
        ("LinkedIn India", lambda k,l,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Government Jobs (India)", lambda k,l,e,d: f"https://www.indgovtjobs.in/search/label/{urllib.parse.quote(k)}"),
        ("Indeed India", lambda k,l,e,d: f"https://www.indeed.co.in/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Naukri", lambda k,l,e,d: f"https://www.naukri.com/{k.lower().replace(' ','-')}-jobs-in-{l.lower().replace(' ','-')}"),
        ("Shine", lambda k,l,e,d: f"https://www.shine.com/job-search/{k.lower().replace(' ','-')}-jobs-in-{l.lower().replace(' ','-')}"),
        ("TimesJobs", lambda k,l,e,d: f"https://www.timesjobs.com/jobsearch/{k.lower().replace(' ','-')}_{l.lower().replace(' ','-')}_jobs.html"),
        ("Freshersworld", lambda k,l,e,d: f"https://www.freshersworld.com/jobs/search?q={urllib.parse.quote(k)}&place={urllib.parse.quote(l)}"),
        ("Sarkari Naukri", lambda k,l,e,d: f"https://www.sarkari-naukri.in/?s={urllib.parse.quote(k)}"),
        ("Sarkari Result", lambda k,l,e,d: f"https://www.sarkariresult.com/search/{urllib.parse.quote(k)}/"),
        ("TechGig (Tech)", lambda k,l,e,d: f"https://www.techgig.com/jobs/search?keyword={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("UpGrad (EdTech)", lambda k,l,e,d: f"https://www.upgrad.com/jobs/search?q={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("MedJobs (Healthcare)", lambda k,l,e,d: f"https://www.medjobs.in/search?q={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Banking Jobs", lambda k,l,e,d: f"https://www.bankjobsindia.in/search/label/{urllib.parse.quote(k)}"),
        ("Railway Jobs", lambda k,l,e,d: f"https://www.indianrailways.gov.in/railwayjobs/Pages/default.aspx?q={urllib.parse.quote(k)}")
    ],
    "Canada": [
        ("LinkedIn Canada", lambda k,l,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Job Bank (Govt)", lambda k,l,e,d: f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={urllib.parse.quote(k)}&locationstring={urllib.parse.quote(l)}"),
        ("Indeed CA", lambda k,l,e,d: f"https://ca.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Workopolis", lambda k,l,e,d: f"https://www.workopolis.com/jobsearch/find-jobs?ak={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Eluta", lambda k,l,e,d: f"https://www.eluta.ca/search?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("CanadaVisa Jobs", lambda k,l,e,d: f"https://www.canadavisa.com/career/jobs/search?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Charity Village (Nonprofit)", lambda k,l,e,d: f"https://charityvillage.com/jobs/search/?search={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Public Service Jobs", lambda k,l,e,d: f"https://emploisfp-psjobs.cfp-psc.gc.ca/psrs-srfp/applicant/page2440?toggleLanguage=en&searchString={urllib.parse.quote(k)}"),
        ("EcoCanada (Environmental)", lambda k,l,e,d: f"https://www.eco.ca/jobs/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("HealthcareJobs.ca", lambda k,l,e,d: f"https://www.healthcarejobs.ca/jobsearch/?search={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "Australia": [
        ("LinkedIn Australia", lambda k,l,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("APS Jobs (Govt)", lambda k,l,e,d: f"https://www.apsjobs.gov.au/s/search?query={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed AU", lambda k,l,e,d: f"https://au.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Seek", lambda k,l,e,d: f"https://www.seek.com.au/{k.lower().replace(' ','-')}-jobs/in-{l.lower().replace(' ','-')}"),
        ("Jora", lambda k,l,e,d: f"https://au.jora.com/j?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("CareerOne", lambda k,l,e,d: f"https://www.careerone.com.au/jobs/keyword/{urllib.parse.quote(k)}/location/{urllib.parse.quote(l)}"),
        ("University Jobs (Academic)", lambda k,l,e,d: f"https://www.universityjobs.edu.au/search?Keywords={urllib.parse.quote(k)}&Location={urllib.parse.quote(l)}"),
        ("State Government Jobs", lambda k,l,e,d: f"https://jobs.wa.gov.au/jobtools/jncustomsearch.jobsearch?in_organid=18304&in_jobDate=all&in_keyword={urllib.parse.quote(k)}"),
        ("EthicalJobs (Nonprofit)", lambda k,l,e,d: f"https://www.ethicaljobs.com.au/Jobs?Keywords={urllib.parse.quote(k)}&Location={urllib.parse.quote(l)}"),
        ("MiningJobs (Mining)", lambda k,l,e,d: f"https://www.miningjobs.com/search/?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "UAE": [
        ("LinkedIn UAE", lambda k,l,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Dubai Careers (Govt)", lambda k,l,e,d: f"https://dubaicareers.ae/en/Pages/Search.aspx?k={urllib.parse.quote(k)}"),
        ("Bayt", lambda k,l,e,d: f"https://www.bayt.com/en/uae/jobs/{k.lower().replace(' ','-')}-jobs/"),
        ("GulfTalent", lambda k,l,e,d: f"https://www.gulftalent.com/jobs/search?query={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Naukrigulf", lambda k,l,e,d: f"https://www.naukrigulf.com/{k.lower().replace(' ','-')}-jobs-in-{l.lower().replace(' ','-')}"),
        ("Dubizzle Jobs", lambda k,l,e,d: f"https://uae.dubizzle.com/jobs/?keywords={urllib.parse.quote(k)}&locations={urllib.parse.quote(l)}"),
        ("Michael Page UAE", lambda k,l,e,d: f"https://www.michaelpage.ae/jobs/{k.lower().replace(' ','-')}?locations={urllib.parse.quote(l)}"),
        ("Oil and Gas Jobs", lambda k,l,e,d: f"https://www.oilandgasjobsearch.com/jobs/{k.lower().replace(' ','-')}/in-{l.lower().replace(' ','-')}"),
        ("ConstructionWeekJobs", lambda k,l,e,d: f"https://www.constructionweekonline.com/jobs/search?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "Germany": [
        ("LinkedIn Germany", lambda k,l,e,d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("StepStone", lambda k,l,e,d: f"https://www.stepstone.de/jobs/{k.lower().replace(' ','-')}/in-{l.lower().replace(' ','-')}"),
        ("Xing", lambda k,l,e,d: f"https://www.xing.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed DE", lambda k,l,e,d: f"https://de.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Arbeitsagentur (Govt)", lambda k,l,e,d: f"https://jobboerse.arbeitsagentur.de/vamJB/jobboerse?dk={urllib.parse.quote(k)}&wo={urllib.parse.quote(l)}"),
        ("Absolventa (Graduates)", lambda k,l,e,d: f"https://www.absolventa.de/jobs?utf8=%E2%9C%93&q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Jobvector (Science)", lambda k,l,e,d: f"https://www.jobvector.de/en/jobs.html?tx_solr%5Bq%5D={urllib.parse.quote(k)}&tx_solr%5Bfilter%5D%5B0%5D=location%3A{urllib.parse.quote(l)}"),
        ("Medizinjobs (Healthcare)", lambda k,l,e,d: f"https://www.medizinjobs.de/stellenangebote/?tx_solr%5Bq%5D={urllib.parse.quote(k)}&tx_solr%5Bfilter%5D%5B0%5D=location%3A{urllib.parse.quote(l)}"),
        ("Bund.de (Govt Jobs)", lambda k,l,e,d: f"https://www.bund.de/SiteGlobals/Forms/Suche/DE/Interministerielle_Stellenboerse/Stellenboerse_Formular.html?nn=4642518&resourceId=4642516&input_=4642516&pageLocale=de&templatename=submitSearchForm&cl2Categories_Stelle=&cl2Categories_Thema={urllib.parse.quote(k)}&cl2Categories_Bundesland=&cl2Categories_Einrichtung=&cl2Categories_Art="),
        ("Ingenieurjobs (Engineering)", lambda k,l,e,d: f"https://www.ingenieurjobs.de/jobs/?tx_solr%5Bq%5D={urllib.parse.quote(k)}&tx_solr%5Bfilter%5D%5B0%5D=location%3A{urllib.parse.quote(l)}")
    ],
    "Global": [
        ("Remote OK", lambda k,l,e,d: f"https://remoteok.com/remote-{k.lower().replace(' ','-')}-jobs"),
        ("We Work Remotely", lambda k,l,e,d: f"https://weworkremotely.com/remote-jobs/search?term={urllib.parse.quote(k)}"),
        ("AngelList (Startups)", lambda k,l,e,d: f"https://angel.co/jobs?ref=search_landing&role_types%5B%5D=any&locations%5B%5D=Remote&keywords={urllib.parse.quote(k)}"),
        ("UN Jobs", lambda k,l,e,d: f"https://careers.un.org/lbw/home.aspx?viewtype=SJ&explevel=all&lang=en-US&occup=0&department=0&bydate=0&occnet=0&location=all&level=0&searchtype=0&curr=0&fos=0&gpid=1000000&sort=desc&j={urllib.parse.quote(k)}"),
        ("Relocate.me", lambda k,l,e,d: f"https://relocate.me/search?query={urllib.parse.quote(k)}&country={urllib.parse.quote(l)}"),
        ("Glassdoor", lambda k,l,e,d: f"https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword={urllib.parse.quote(k)}&sc.keyword={urllib.parse.quote(k)}&locT=C&locId=1147401&jobType="),
        ("FlexJobs", lambda k,l,e,d: f"https://www.flexjobs.com/search?search={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Working Nomads", lambda k,l,e,d: f"https://www.workingnomads.com/jobs?search={urllib.parse.quote(k)}"),
        ("EuroBrussels (EU Jobs)", lambda k,l,e,d: f"https://www.eurobrussels.com/job_search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("DevITjobs (Tech)", lambda k,l,e,d: f"https://devitjobs.uk/jobs/{k.lower().replace(' ','-')}"),
        ("Hitmarker (Gaming)", lambda k,l,e,d: f"https://hitmarker.net/jobs?query={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Krop (Creative)", lambda k,l,e,d: f"https://www.krop.com/creative-jobs/{k.lower().replace(' ','-')}/"),
        ("Authentic Jobs (Design)", lambda k,l,e,d: f"https://authenticjobs.com/?search=advanced&options%5Btitle%5D=Y&options%5Bdescription%5D=Y&options%5Bcompany_desc%5D=Y&options%5Bjob_types%5D%5B0%5D=1&options%5Bjob_types%5D%5B1%5D=2&options%5Bjob_types%5D%5B2%5D=3&options%5Blocations%5D%5B0%5D=1&options%5Blocations%5D%5B1%5D=2&keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("JustRemote", lambda k,l,e,d: f"https://justremote.co/remote-jobs/search?search={urllib.parse.quote(k)}"),
        ("Jobbatical", lambda k,l,e,d: f"https://jobbatical.com/jobs?search={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ]
}

# --- UI ---
st.title("🌍 Mega Job Finder")
st.markdown("🔍 Access **300+ job portals** worldwide with smart filters")

with st.form("job_form"):
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("Job Title / Keywords", "Data Scientist")
        location = st.text_input("Preferred Location", "Remote")
        country = st.selectbox("Country", ["Global"] + list(PORTALS_BY_COUNTRY.keys()))
    with col2:
        experience = st.selectbox("Experience Level", ["Any", "Entry", "Mid", "Senior", "Executive"])
        date_posted = st.selectbox("Date Posted", ["Any time", "Past month", "Past week", "Past 24 hours"])

    submitted = st.form_submit_button("🔍 Find Jobs")

if submitted:
    st.subheader(f"🌐 Job Portals in {country}")

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
    
    for name, url_func in portals:
        if "LinkedIn" in name:
            url = url_func(keyword, location, e_filter, d_filter)
        else:
            url = url_func(keyword, location, "", "")
        st.markdown(f"- 🔗 [{name}]({url})")

    st.success(f"✅ Generated {len(portals)} job search links.")

    # Google fallback
    google_jobs = f"https://www.google.com/search?q={urllib.parse.quote(keyword)}+jobs+in+{urllib.parse.quote(location)}&ibp=htl;jobs"
    st.markdown(f"""
    <div style='background-color:#f0f2f6; padding:20px; border-radius:10px; margin-top:30px;'>
        <h3 style='color:#1e3a8a;'>Need more options?</h3>
        <p>Try these global aggregators:</p>
        <a href='{google_jobs}' 
           target='_blank' 
           style='background-color:#1e3a8a; color:white; padding:10px 15px; text-decoration:none; border-radius:5px; display:inline-block; margin-top:10px;'>
            🔍 Search Google Jobs
        </a>
    </div>
    """, unsafe_allow_html=True)
