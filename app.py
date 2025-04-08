import streamlit as st
import urllib.parse

# ----------------- LANGUAGE SUPPORT -----------------
LANGUAGES = {
    "English": "en",
    "Assamese": "as",
    "Bengali": "bn",
    "Bodo": "brx",
    "Dogri": "doi",
    "Gujarati": "gu",
    "Hindi": "hi",
    "Kannada": "kn",
    "Kashmiri": "ks",
    "Konkani": "kok",
    "Maithili": "mai",
    "Malayalam": "ml",
    "Manipuri": "mni",
    "Marathi": "mr",
    "Nepali": "ne",
    "Odia": "or",
    "Punjabi": "pa",
    "Santhali": "sat",
    "Sindhi": "sd",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
    "French": "fr",
    "German": "de",
    "Arabic": "ar",
    "Spanish": "es",
}

TRANSLATIONS = {
    "en": {
        "title": "CareerUpskillers | AI Job Hub",
        "tagline": "Your AI-powered career launchpad",
        "description": "Smart Job Search | Interview Prep | Free Certifications",
        "job_finder": "Job Finder",
        "interview_prep": "Interview Preparation",
        "free_courses": "Free Courses",
        "find_jobs": "Find Jobs",
        "generate_link": "Generate Interview Prep Link",
        "find_courses": "Find Courses",
        "job_title": "Job Title / Keywords",
        "location": "Preferred Location",
        "country": "Country",
        "experience": "Experience Level",
        "date_posted": "Date Posted",
        "search_course": "Search Course / Skill / Job Title",
    },
    "hi": {
        "title": "कैरियर अपस्किलर्स | एआई जॉब हब",
        "tagline": "आपका एआई-संचालित करियर लॉन्चपैड",
        "description": "स्मार्ट जॉब सर्च | साक्षात्कार तैयारी | मुफ्त प्रमाणपत्र",
        "job_finder": "जॉब खोजक",
        "interview_prep": "साक्षात्कार तैयारी",
        "free_courses": "मुफ्त पाठ्यक्रम",
        "find_jobs": "नौकरियाँ खोजें",
        "generate_link": "साक्षात्कार तैयारी लिंक बनाएँ",
        "find_courses": "पाठ्यक्रम खोजें",
        "job_title": "नौकरी शीर्षक / कीवर्ड",
        "location": "पसंदीदा स्थान",
        "country": "देश",
        "experience": "अनुभव स्तर",
        "date_posted": "पोस्ट की तारीख",
        "search_course": "पाठ्यक्रम / कौशल / नौकरी शीर्षक खोजें",
    },
    "ta": {
        "title": "கரியர் அப்ஸ்கிலர்ஸ் | ஏஐ வேலை மையம்",
        "tagline": "உங்கள் ஏஐ-இயக்கப்பட்ட தொழில் தொடக்கப்புள்ளி",
        "description": "புத்திசாலி வேலை தேடல் | நேர்காணல் தயாரிப்பு | இலவச சான்றிதழ்கள்",
        "job_finder": "வேலை தேடுபவர்",
        "interview_prep": "நேர்காணல் தயாரிப்பு",
        "free_courses": "இலவச படிப்புகள்",
        "find_jobs": "வேலைகளைத் தேடு",
        "generate_link": "நேர்காணல் தயாரிப்பு இணைப்பை உருவாக்கு",
        "find_courses": "படிப்புகளைத் தேடு",
        "job_title": "வேலை தலைப்பு / முக்கிய சொற்கள்",
        "location": "விருப்பமான இடம்",
        "country": "நாடு",
        "experience": "அனுபவ நிலை",
        "date_posted": "பதிவு தேதி",
        "search_course": "படிப்பு / திறன் / வேலை தலைப்பு தேடு",
    },
    # Add more translations as needed
}

# ----------------- SETUP -----------------
# Set page config ONCE at the top (must be the first Streamlit command)
st.set_page_config(page_title="CareerUpskillers | AI Job Hub", page_icon="🌟", layout="centered")

# Language selection
lang = st.sidebar.selectbox("Select Language / भाषा चुनें / Sprache wählen", list(LANGUAGES.keys()), index=0)
t = TRANSLATIONS.get(LANGUAGES[lang], TRANSLATIONS["en"])  # Default to English

# Hide Streamlit default elements
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ----------------- BRANDING -----------------
st.markdown(f"""
<div style='text-align:center; padding:10px 0;'>
    <h1 style='color:#1f2937;'>🚀 {t["title"]}</h1>
    <h4 style='color:#374151;'>{t["tagline"]}</h4>
    <p style='font-size:16px;'>{t["description"]}</p>
</div>
""", unsafe_allow_html=True)

# ----------------- TABS -----------------
tab1, tab2, tab3 = st.tabs([f"🌐 {t['job_finder']}", f"🎯 {t['interview_prep']}", f"🎓 {t['free_courses']}"])

# ----------------- TAB 1: JOB FINDER -----------------
with tab1:
    st.header(f"🌐 {t['job_finder']}")

    PORTALS_BY_COUNTRY = {
        "India": [
            ("LinkedIn", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
            ("Naukri", lambda k, l, e, d: f"https://www.naukri.com/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-') if l != 'Remote' else 'india'}"),
            ("Indeed", lambda k, l, e, d: f"https://www.indeed.co.in/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
            ("Shine", lambda k, l, e, d: f"https://www.shine.com/job-search/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}")
        ],
        "USA": [
            ("LinkedIn", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
            ("USAJobs", lambda k, l, e, d: f"https://www.usajobs.gov/Search/Results?k={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
            ("Indeed", lambda k, l, e, d: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
        ]
    }

    with st.form("job_form"):
        col1, col2 = st.columns(2)
        with col1:
            keyword = st.text_input(t["job_title"], "Data Scientist")
            location = st.text_input(t["location"], "Remote")
            country = st.selectbox(t["country"], list(PORTALS_BY_COUNTRY.keys()))
        with col2:
            experience = st.selectbox(t["experience"], ["Any", "Entry", "Mid", "Senior", "Executive"])
            date_posted = st.selectbox(t["date_posted"], ["Any time", "Past month", "Past week", "Past 24 hours"])
        submitted = st.form_submit_button(f"🔍 {t['find_jobs']}")

    if submitted:
        time_map = {
            "Any time": "", "Past month": "r2592000",
            "Past week": "r604800", "Past 24 hours": "r86400"
        }
        exp_map = {
            "Any": "", "Entry": "2", "Mid": "3", "Senior": "4", "Executive": "5"
        }
        d_filter = time_map[date_posted]
        e_filter = exp_map[experience]

        st.subheader(f"🔗 Job Search Links in {country}")
        for name, url_func in PORTALS_BY_COUNTRY[country]:
            url = url_func(keyword, location, e_filter, d_filter)
            st.markdown(f"""
            <a href="{url}" target="_blank" style="display:inline-block; padding:10px 20px; background:#4CAF50; color:white; border-radius:5px; text-decoration:none; margin-bottom:5px;">
                🔍 Search on {name}
            </a>
            """, unsafe_allow_html=True)

# ----------------- TAB 2: INTERVIEW PREPARATION -----------------
with tab2:
    st.header(f"🎯 {t['interview_prep']}")

    with st.form("interview_form"):
        col1, col2 = st.columns(2)
        with col1:
            role = st.text_input(t["job_title"], "Data Analyst")
            country = st.selectbox(t["country"], ["India", "USA", "UK", "Canada", "Germany", "UAE", "Australia"])
        with col2:
            platform = st.selectbox("Choose Platform", [
                "LeetCode", "HackerRank", "GeeksforGeeks", "Glassdoor", "Pramp", 
                "IndiaBix", "AmbitionBox", "Final Round AI", "Big Interview", "iScalePro"
            ])
        interview_submit = st.form_submit_button(f"🔗 {t['generate_link']}")

    if interview_submit:
        query = urllib.parse.quote_plus(role + " " + country)
        PLATFORM_LINKS = {
            "LeetCode": f"https://leetcode.com/problemset/all/?search={query}",
            "HackerRank": f"https://www.hackerrank.com/interview/interview-preparation-kit",
            "GeeksforGeeks": f"https://www.geeksforgeeks.org/?s={query}",
            "Glassdoor": f"https://www.glassdoor.com/Interview/{query}-interview-questions-SRCH_KO0,{len(query)}.htm",
            "Pramp": f"https://www.pramp.com/#interview-prep",
            "IndiaBix": f"https://www.indiabix.com/interview/questions-and-answers/?search={query}",
            "AmbitionBox": f"https://www.ambitionbox.com/interviews?title={query}",
            "Final Round AI": "https://www.finalroundai.com/ai-mock-interview",
            "Big Interview": "https://www.biginterview.com/",
            "iScalePro": "https://www.iscalepro.com/jobseekers/"
        }

        link = PLATFORM_LINKS.get(platform)
        if link:
            st.markdown(f"""
            <a href="{link}" target="_blank" style="display:inline-block; padding:12px 24px; background:#2563eb; color:white; border-radius:5px; text-decoration:none;">
                🚀 Prep on {platform}
            </a>
            """, unsafe_allow_html=True)

# ----------------- TAB 3: FREE COURSES -----------------
with tab3:
    st.header(f"🎓 {t['free_courses']}")

    with st.form("course_form"):
        search = st.text_input(t["search_course"], "AI for Business")
        course_submit = st.form_submit_button(f"🎯 {t['find_courses']}")

    if course_submit:
        query = urllib.parse.quote_plus(search)

        st.subheader("🧠 Tech Giants")
        tech = [
            ("Google", f"https://grow.google/certificates/?q={query}"),
            ("IBM", f"https://skillsbuild.org/learn?search={query}"),
            ("Amazon AWS", f"https://explore.skillbuilder.aws/learn?searchTerm={query}"),
            ("Microsoft (via LinkedIn)", "https://www.linkedin.com/learning/"),
            ("Meta", f"https://www.facebook.com/business/learn/courses?search={query}")
        ]
        for name, url in tech:
            st.markdown(f"<a href='{url}' target='_blank' style='display:block; background:#3b82f6; color:white; padding:10px; border-radius:5px; margin-bottom:5px;'>📘 {name}</a>", unsafe_allow_html=True)

        # Add more sections as in your original code...

# ----------------- FOOTER -----------------
st.markdown("""
<hr style='margin-top:40px;'>
<div style='text-align:center; font-size:16px; color:gray;'>
    🚀 Powered by <strong>CareerUpskillers</strong> |
    <a href='https://www.linkedin.com/company/careerupskillers' target='_blank'>LinkedIn</a> • 
    <a href='https://twitter.com/careerupskill' target='_blank'>Twitter</a> • 
    <a href='https://instagram.com/careerupskillers' target='_blank'>Instagram</a> • 
    <a href='https://youtube.com/@careerupskillers' target='_blank'>YouTube</a>
</div>
""", unsafe_allow_html=True)
