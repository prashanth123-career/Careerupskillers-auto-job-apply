import streamlit as st
import urllib.parse

# Hide Streamlit logo and default style
st.set_page_config(
    page_title="CareerUpSkillers Job Finder",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for a stylish interface
st.markdown(
    """
    <style>
    /* Hide Streamlit footer and logo */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stApp {
        background-color: #f0f4f8;
        font-family: 'Arial', sans-serif;
    }
    .header {
        background-color: #003087;
        color: #ffd700;
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .card:hover {
        transform: scale(1.02);
    }
    .btn {
        background-color: #003087;
        color: #ffd700;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        transition: background-color 0.3s;
    }
    .btn:hover {
        background-color: #001f5f;
    }
    .footer {
        text-align: center;
        padding: 10px;
        background-color: #003087;
        color: #ffd700;
        position: fixed;
        width: 100%;
        bottom: 0;
        border-top: 1px solid #ffd700;
    }
    .social-btn {
        background-color: #003087;
        color: #ffd700;
        padding: 8px 15px;
        border-radius: 5px;
        text-decoration: none;
        margin: 0 5px;
        transition: background-color 0.3s;
    }
    .social-btn:hover {
        background-color: #001f5f;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Portal database with LinkedIn filter support ---
PORTALS_BY_COUNTRY = {
    "USA": [
        ("LinkedIn", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("USAJobs (Govt)", lambda k, l, e, d: f"https://www.usajobs.gov/Search/Results?k={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Indeed", lambda k, l, e, d: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Glassdoor", lambda k, l, e, d: f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={urllib.parse.quote(k)}&locT=C&locName={urllib.parse.quote(l)}"),
        ("Monster", lambda k, l, e, d: f"https://www.monster.com/jobs/search?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}"),
        ("CareerBuilder", lambda k, l, e, d: f"https://www.careerbuilder.com/jobs?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "UK": [
        ("LinkedIn UK", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Guardian Jobs (Govt)", lambda k, l, e, d: f"https://jobs.theguardian.com/jobs/{urllib.parse.quote(k)}/in-{urllib.parse.quote(l)}"),
        ("Indeed UK", lambda k, l, e, d: f"https://uk.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Reed", lambda k, l, e, d: f"https://www.reed.co.uk/jobs?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Totaljobs", lambda k, l, e, d: f"https://www.totaljobs.com/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}"),
        ("CV-Library", lambda k, l, e, d: f"https://www.cv-library.co.uk/search-jobs?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "India": [
        ("LinkedIn India", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Government Jobs (India)", lambda k, l, e, d: f"https://www.indgovtjobs.in/search/label/{urllib.parse.quote(k)}"),
        ("Indeed India", lambda k, l, e, d: f"https://www.indeed.co.in/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Naukri", lambda k, l, e, d: f"https://www.naukri.com/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-') if l != 'Remote' else 'india'}"),
        ("Shine", lambda k, l, e, d: f"https://www.shine.com/job-search/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("TimesJobs", lambda k, l, e, d: f"https://www.timesjobs.com/jobs/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("Freshersworld", lambda k, l, e, d: f"https://www.freshersworld.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "Canada": [
        ("LinkedIn Canada", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Job Bank (Govt)", lambda k, l, e, d: f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={urllib.parse.quote(k)}&locationstring={urllib.parse.quote(l)}"),
        ("Indeed CA", lambda k, l, e, d: f"https://ca.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Workopolis", lambda k, l, e, d: f"https://www.workopolis.com/jobsearch/find-jobs?ak={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Monster CA", lambda k, l, e, d: f"https://www.monster.ca/jobs/search?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}"),
        ("Eluta", lambda k, l, e, d: f"https://www.eluta.ca/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "Australia": [
        ("LinkedIn Australia", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("APS Jobs (Govt)", lambda k, l, e, d: f"https://www.apsjobs.gov.au/s/search?query={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed AU", lambda k, l, e, d: f"https://au.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Seek", lambda k, l, e, d: f"https://www.seek.com.au/{k.lower().replace(' ', '-')}-jobs/in-{l.lower().replace(' ', '-')}"),
        ("CareerOne", lambda k, l, e, d: f"https://www.careerone.com.au/jobs?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Jora", lambda k, l, e, d: f"https://au.jora.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "UAE": [
        ("LinkedIn UAE", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Dubai Careers (Govt)", lambda k, l, e, d: f"https://dubaicareers.ae/en/Pages/Search.aspx?k={urllib.parse.quote(k)}"),
        ("Bayt", lambda k, l, e, d: f"https://www.bayt.com/en/uae/jobs/{k.lower().replace(' ', '-')}-jobs/"),
        ("GulfTalent", lambda k, l, e, d: f"https://www.gulftalent.com/uae/jobs?q={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Naukrigulf", lambda k, l, e, d: f"https://www.naukrigulf.com/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("JobsAbuDhabi", lambda k, l, e, d: f"https://jobsabudhabi.ae/en/search-jobs/?q={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "Germany": [
        ("LinkedIn Germany", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("StepStone", lambda k, l, e, d: f"https://www.stepstone.de/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}"),
        ("Xing", lambda k, l, e, d: f"https://www.xing.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Jobware", lambda k, l, e, d: f"https://www.jobware.de/jobs/{k.lower().replace(' ', '-')}/{l.lower().replace(' ', '-')}"),
        ("Meinestadt", lambda k, l, e, d: f"https://jobs.meinestadt.de/deutschland?query={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Bundesagentur für Arbeit (Govt)", lambda k, l, e, d: f"https://jobboerse.arbeitsagentur.de/stellenangebote/suche?was={urllib.parse.quote(k)}&wo={urllib.parse.quote(l)}")
    ]
}

# --- UI ---
st.markdown('<div class="header"><h1>CareerUpSkillers Job Finder</h1><p>🔍 Empowering Your Career Journey Worldwide</p></div>', unsafe_allow_html=True)

with st.form("job_form"):
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("Job Title / Keywords", "Data Scientist", key="keyword_input")
        location = st.text_input("Preferred Location", "Remote", key="location_input")
        country = st.selectbox("Country", list(PORTALS_BY_COUNTRY.keys()), key="country_select")
    with col2:
        experience = st.selectbox("Experience Level", ["Any", "Entry", "Mid", "Senior", "Executive"], key="experience_select")
        date_posted = st.selectbox("Date Posted", ["Any time", "Past month", "Past week", "Past 24 hours"], key="date_select")

    # Ensure submit button is inside the form
    submitted = st.form_submit_button("🔍 Find Jobs", key="submit_button")

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

    # Display portals as styled buttons
    for name, url_func in PORTALS_BY_COUNTRY[country]:
        if "LinkedIn" in name:
            url = url_func(keyword, location, e_filter, d_filter)
        else:
            url = url_func(keyword, location, "", "")  # Non-LinkedIn portals don’t use exp/date filters here
        
        # Create a styled button card
        card_html = f"""
        <div class="card">
            <a href="{url}" target="_blank" class="btn">
                🔍 Search on {name}
            </a>
            <p style="font-size: 12px; color: #666;">If you are logged into {name}, this will take you directly to the relevant job listings.</p>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    st.success(f"✅ Generated {len(PORTALS_BY_COUNTRY[country])} job search links.")

    # Google fallback and social links
    google_jobs = f"https://www.google.com/search?q={urllib.parse.quote(keyword)}+jobs+in+{urllib.parse.quote(location)}&ibp=htl;jobs"
    contact_us = "https://www.careerupskillers.com/post/the-ultimate-ai-career-guide-jobs-freelancing-and-startups#contact"
    whatsapp = "https://api.whatsapp.com/send/?phone=917892116728&text&type=phone_number&app_absent=0"
    about_us = "https://www.careerupskillers.com/about-1"
    privacy = "https://www.careerupskillers.com/about-1"  # Assuming privacy is under about page; update if separate
    linkedin = "https://www.linkedin.com/company/79362047/admin/dashboard/"
    instagram = "https://www.instagram.com/careerupskillers?igsh=YWNmOGMwejBrb24z"
    youtube = "https://www.youtube.com/@Careerupskillers"
    facebook = "https://www.facebook.com/Careerupskillers?rdid=VxU12OcSC0C7hU8Z&share_url=https%3A%2F%2Fwww.facebook.com%2Fshare%2F18gUeR73H6%2F#"

    st.markdown(f"""
    <div style='background-color:#f0f4f8; padding:20px; border-radius:10px; margin-top:30px; text-align:center;'>
        <h3 style='color:#003087;'>Need more options?</h3>
        <a href='{google_jobs}' target='_blank' class='social-btn'>
            🔍 Search Google Jobs
        </a>
        <a href='{contact_us}' target='_blank' class='social-btn'>
            📧 Contact Us
        </a>
        <a href='{whatsapp}' target='_blank' class='social-btn'>
            💬 WhatsApp
        </a>
        <a href='{about_us}' target='_blank' class='social-btn'>
            ℹ️ About Us
        </a>
        <a href='{privacy}' target='_blank' class='social-btn'>
            🔒 Privacy
        </a>
        <a href='{linkedin}' target='_blank' class='social-btn'>
            💼 LinkedIn
        </a>
        <a href='{instagram}' target='_blank' class='social-btn'>
            📸 Instagram
        </a>
        <a href='{youtube}' target='_blank' class='social-btn'>
            🎥 YouTube
        </a>
        <a href='{facebook}' target='_blank' class='social-btn'>
            👍 Facebook
        </a>
    </div>
    """, unsafe_allow_html=True)

# Footer with social links
st.markdown(
    f"""
    <div class="footer">
        © 2025 CareerUpSkillers | 
        <a href="{contact_us}" target="_blank" style="color:#ffd700; text-decoration:none; margin:0 5px;">Contact</a> | 
        <a href="{about_us}" target="_blank" style="color:#ffd700; text-decoration:none; margin:0 5px;">About</a> | 
        <a href="{privacy}" target="_blank" style="color:#ffd700; text-decoration:none; margin:0 5px;">Privacy</a> | 
        <a href="{linkedin}" target="_blank" style="color:#ffd700; text-decoration:none; margin:0 5px;">LinkedIn</a> | 
        <a href="{instagram}" target="_blank" style="color:#ffd700; text-decoration:none; margin:0 5px;">Instagram</a> | 
        <a href="{youtube}" target="_blank" style="color:#ffd700; text-decoration:none; margin:0 5px;">YouTube</a> | 
        <a href="{facebook}" target="_blank" style="color:#ffd700; text-decoration:none; margin:0 5px;">Facebook</a>
    </div>
    """,
    unsafe_allow_html=True
)
