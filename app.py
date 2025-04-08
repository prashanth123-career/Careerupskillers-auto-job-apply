import streamlit as st
import urllib.parse

# ----------------- LANGUAGE SUPPORT -----------------
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
    "French": "fr",
    "German": "de",
    "Arabic": "ar",
    # Add more languages as needed
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
        "experience_options": ["Any", "Entry", "Mid", "Senior", "Executive"],
        "date_posted_options": ["Any time", "Past month", "Past week", "Past 24 hours"],
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
        "experience_options": ["कोई भी", "प्रारंभिक", "मध्य", "वरिष्ठ", "कार्यकारी"],
        "date_posted_options": ["कभी भी", "पिछला महीना", "पिछला सप्ताह", "पिछले 24 घंटे"],
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
        "experience_options": ["எதுவும்", "ஆரம்பம்", "நடுத்தரம்", "மூத்தவர்", "நிர்வாகி"],
        "date_posted_options": ["எப்போது வேண்டுமானாலும்", "கடந்த மாதம்", "கடந்த வாரம்", "கடந்த 24 மணி நேரம்"],
    },
    # Add more languages as needed
}

# ----------------- SETUP -----------------
st.set_page_config(page_title="CareerUpskillers | AI Job Hub", page_icon="🌟", layout="centered")

# Language selection
lang = st.sidebar.selectbox("Select Language", list(LANGUAGES.keys()), index=0)
t = TRANSLATIONS.get(LANGUAGES[lang], TRANSLATIONS["en"])  # Default to English if not found

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
            experience = st.selectbox(t["experience"], t["experience_options"])
            date_posted = st.selectbox(t["date_posted"], t["date_posted_options"])
        submitted = st.form_submit_button(f"🔍 {t['find_jobs']}")

    if submitted:
        time_map = {
            t["date_posted_options"][0]: "",  # "Any time" or equivalent
            t["date_posted_options"][1]: "r2592000",  # "Past month"
            t["date_posted_options"][2]: "r604800",   # "Past week"
            t["date_posted_options"][3]: "r86400"     # "Past 24 hours"
        }
        exp_map = {
            t["experience_options"][0]: "",  # "Any"
            t["experience_options"][1]: "2", # "Entry"
            t["experience_options"][2]: "3", # "Mid"
            t["experience_options"][3]: "4", # "Senior"
            t["experience_options"][4]: "5"  # "Executive"
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
    
    # Expanded preparation matrix
    with st.form("interview_form"):
        col1, col2 = st.columns([1, 2])
        with col1:
            role = st.text_input(t["job_title"], "Data Analyst", key="int_role")
            country = st.selectbox(t["country"], ["India", "USA", "UK", "Canada"], key="int_country")
            exp_level = st.selectbox(t["experience"], t["experience_options"])
        
        with col2:
            prep_type = st.selectbox("Preparation Type", [
                "Technical Questions", 
                "Behavioral Questions",
                "Case Studies",
                "Salary Negotiation",
                "Resume Tips"
            ])
            
            company = st.text_input("Target Company (optional)", placeholder="Google, TCS, etc.")
        
        submitted = st.form_submit_button(f"🔗 {t['generate_link']}")

    if submitted:
        # Create smart Google search queries
        base_query = f"{role} {prep_type} {exp_level} {company} {country}"
        encoded_query = urllib.parse.quote_plus(base_query)
        
        st.subheader("🔍 Best Preparation Resources")
        
        # Curated resource matrix
        RESOURCE_MATRIX = {
            "Technical Questions": {
                "India": "https://www.indiabix.com",
                "Global": "https://leetcode.com"
            },
            "Behavioral Questions": {
                "India": "https://www.ambitionbox.com/interviews",
                "Global": "https://www.themuse.com/advice/behavioral-interview-questions"
            },
            # Add more categories
        }
        
        # Show curated resources first
        main_resource = RESOURCE_MATRIX.get(prep_type, {}).get("India" if country == "India" else "Global")
        if main_resource:
            st.markdown(f"""
            <div style="padding:15px; background:#e8f5e9; border-radius:10px; margin-bottom:20px;">
                <h4>🎯 Recommended Resource</h4>
                <a href="{main_resource}" target="_blank" style="color:#2e7d32; font-weight:bold;">
                    Best {prep_type} Guide for {country} → 
                </a>
            </div>
            """, unsafe_allow_html=True)
        
        # Smart Google fallback
        st.markdown(f"""
        <div style="padding:15px; background:#fff3e0; border-radius:10px;">
            <h4>🔎 More Resources via Smart Search</h4>
            <a href="https://www.google.com/search?q={encoded_query}+filetype:pdf" target="_blank">
                📄 Find PDF Guides
            </a><br>
            <a href="https://www.google.com/search?q={encoded_query}+site:youtube.com" target="_blank">
                🎥 Video Tutorials
            </a><br>
            <a href="https://www.google.com/search?q={encoded_query}+forum" target="_blank">
                💬 Discussion Forums
            </a>
        </div>
        """, unsafe_allow_html=True)

        # Preparation checklist
        st.subheader("✅ Personalized Checklist")
        checklist_items = {
            "Technical Questions": ["Review core concepts", "Practice coding problems", "Study system design"],
            "Behavioral Questions": ["Prepare STAR stories", "Research company values", "Practice timing"],
            # Add more categories
        }.get(prep_type, [])
        
        for item in checklist_items:
            st.checkbox(item, key=f"check_{item}")

# ----------------- TAB 3: FREE COURSES -----------------
with tab3:
    st.header(f"🎓 {t['free_courses']}")

    # Expanded curated course database
    COURSE_DATABASE = {
        "AI/ML": [
            ("Google", "https://cloudskillsboost.google/journeys/118", "ML Fundamentals", "8h", "✅"),
            ("Microsoft", "https://learn.microsoft.com/ai", "AI Principles", "6h", "✅"),
            ("IBM", "https://cognitiveclass.ai/learn/ai", "AI Foundations", "10h", "✅"),
        ],
        "Programming": [
            ("FreeCodeCamp", "https://www.freecodecamp.org/learn", "Python Basics", "4h", "✅"),
            ("Harvard", "https://cs50.harvard.edu/x/", "CS50: Intro to CS", "10w", "✅"),
            ("Codecademy", "https://codecademy.com/learn/intro-to-javascript", "JavaScript Basics", "6h", "✅"),
        ],
        "Soft Skills": [
            ("Coursera", "https://www.coursera.org/learn/learning-how-to-learn", "Learning How to Learn", "8h", "✅"),
            ("edX", "https://www.edx.org/course/essential-soft-skills", "Essential Soft Skills", "5h", "✅"),
            ("Udemy", "https://udemy.com/course/communication-skills-masterclass", "Communication Mastery", "3h", "✅"),
        ],
        "Cloud Computing": [
            ("AWS", "https://www.aws.training", "AWS Cloud Practitioner Essentials", "6h", "✅"),
            ("Google Cloud", "https://cloud.google.com/training", "Cloud Digital Leader", "7h", "✅"),
            ("Microsoft", "https://learn.microsoft.com/azure-fundamentals", "Azure Fundamentals", "5h", "✅"),
        ],
        "Sales": [
            ("HubSpot", "https://academy.hubspot.com/courses/sales", "Sales Training", "4h", "✅"),
            ("Coursera", "https://coursera.org/specializations/sales-training", "Sales Strategies", "12h", "✅"),
            ("Alison", "https://alison.com/course/diploma-in-sales-skills", "Sales Diploma", "8h", "✅"),
        ]
    }

    with st.form("course_form"):
        col1, col2 = st.columns([3, 2])
        with col1:
            search_query = st.text_input(t["search_course"], "Sales")
        with col2:
            category = st.selectbox("Category", ["All"] + list(COURSE_DATABASE.keys()))
        submitted = st.form_submit_button(f"🎯 {t['find_courses']}")

    if submitted:
        st.subheader("🏅 Verified Courses in Application")
        found = False
        
        # Search through all categories
        for cat, courses in COURSE_DATABASE.items():
            if category != "All" and cat != category:
                continue
                
            category_header = False  # Control category headings
            
            for provider, url, title, duration, cert in courses:
                if search_query.lower() in title.lower() or search_query.lower() in cat.lower():
                    if not category_header:
                        st.markdown(f"### {cat} Courses")
                        category_header = True
                        found = True
                    
                    # Course card with enhanced styling
                    st.markdown(f"""
                    <div style="padding:15px; border:1px solid #e0e0e0; border-radius:10px; margin:10px 0;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h4 style="margin:0; color:#1a73e8;">{title}</h4>
                                <p style="margin:5px 0; color:#5f6368;">🏢 {provider} | ⏳ {duration} | Certificate: {cert}</p>
                            </div>
                            <a href="{url}" target="_blank" 
                               style="background:#1a73e8; color:white; padding:8px 20px; 
                                      border-radius:5px; text-decoration:none; font-weight:500;">
                                Enroll Now
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        if not found:
            st.warning("No matching courses found. Try broadening your search terms.")

        # Enhanced learning paths
        st.subheader("🗺 Career Learning Paths")
        paths = {
            "AI/ML": "1. Math Basics → 2. Python Programming → 3. ML Fundamentals → 4. Deep Learning → 5. NLP Specialization",
            "Programming": "1. Programming Basics → 2. Algorithms → 3. Version Control → 4. Project Development → 5. Open Source Contributions",
            "Soft Skills": "1. Communication → 2. Time Management → 3. Critical Thinking → 4. Leadership → 5. Negotiation",
            "Cloud Computing": "1. Cloud Basics → 2. IaaS/PaaS → 3. Security & DevOps → 4. Certification Prep → 5. Cloud Architecture",
            "Sales": "1. Sales Fundamentals → 2. CRM Tools → 3. Negotiation Tactics → 4. Client Management → 5. Sales Leadership"
        }

        selected_path = paths.get(category, "General Skills Development Path")
        st.markdown(f"""
        <div style="padding:20px; background:#f8f9fa; border-radius:10px; margin-top:15px;
                    border-left: 4px solid #1a73e8;">
            <h4 style="margin:0 0 10px 0; color:#202124;">{category if category != 'All' else 'General'} Career Path</h4>
            <p style="margin:0; color:#5f6368; line-height:1.6;">{selected_path}</p>
        </div>
        """, unsafe_allow_html=True)
