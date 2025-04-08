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
    
    # Expanded platform list with icons
    PLATFORMS = {
        "LeetCode": {"icon": "💻", "type": "Coding"},
        "HackerRank": {"icon": "👨💻", "type": "Coding"},
        "GeeksforGeeks": {"icon": "📚", "type": "Technical"},
        "Glassdoor": {"icon": "🏢", "type": "Company Specific"},
        "Pramp": {"icon": "🤝", "type": "Mock Interviews"},
        "InterviewBit": {"icon": "🧠", "type": "Coding"},
        "AmbitionBox": {"icon": "🇮🇳", "type": "India Focused"},
        "Big Interview": {"icon": "🎥", "type": "Mock Interviews"},
        "iScalePro": {"icon": "📈", "type": "Behavioral"},
    }

    with st.expander("🚀 Comprehensive Interview Preparation Suite", expanded=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            role = st.text_input(t["job_title"], "Data Analyst", key="interview_role")
            country = st.selectbox(t["country"], ["India", "USA", "UK", "Canada", "Germany", "UAE", "Australia"], key="interview_country")
            interview_type = st.selectbox("Interview Type", ["Technical", "Behavioral", "Case Study", "System Design"])
        
        with col2:
            st.markdown("### 📚 Preparation Resources")
            platform_type = st.selectbox("Resource Type", ["Coding", "Technical", "Behavioral", "Company Specific", "All"])
            
            # Filter platforms
            filtered_platforms = [k for k, v in PLATFORMS.items() if platform_type == "All" or v["type"] == platform_type]
            selected_platform = st.selectbox("Select Platform", filtered_platforms, format_func=lambda x: f"{PLATFORMS[x]['icon']} {x}")
            
            # Difficulty level
            difficulty = st.select_slider("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])

    # Generate dynamic content
    if st.button(f"🔗 {t['generate_link']}"):
        query = urllib.parse.quote_plus(f"{role} {country} {interview_type}")
        
        # Dynamic content generation
        with st.spinner("🧠 Generating personalized interview plan..."):
            # AI-generated questions (simulated)
            questions = [
                f"Explain the difference between supervised and unsupervised learning in {role} context",
                f"How would you handle missing data in a real-world {role} scenario?",
                f"Case study: Analyze our sales data and suggest optimization strategies",
                f"Behavioral: Describe a time you solved a complex problem as a {role}"
            ][:3]  # Simulated AI response
            
            # Resource links
            PLATFORM_LINKS = {
                "LeetCode": f"https://leetcode.com/problemset/all/?search={query}",
                "Glassdoor": f"https://glassdoor.com/Interview/{query}-questions",
                # Add other platform links
            }

            # Display results
            st.success("🎉 Personalized Interview Plan Generated!")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.subheader("📝 Recommended Questions")
                for i, q in enumerate(questions, 1):
                    st.markdown(f"""
                    <div style="padding:10px; background:#f0f5ff; border-radius:5px; margin-bottom:10px;">
                        {i}. {q}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.subheader("📈 Progress Tracker")
                st.markdown("""
                - Technical Skills: 65% completed
                - Behavioral Prep: 40% completed
                - Mock Interviews: 2/5 completed
                """)

            with col2:
                st.subheader("🎥 Interactive Preparation")
                tab_a, tab_b, tab_c = st.tabs(["📚 Resources", "💡 Tips", "🎤 Mock Interview"])
                
                with tab_a:
                    st.markdown(f"""
                    **🔗 {selected_platform} Resources:**
                    - [Practice Questions]({PLATFORM_LINKS.get(selected_platform, '#')})
                    - [Discussion Forum](https://discuss.{selected_platform.lower()}.com/{query})
                    - [Company-specific Guide](https://{selected_platform.lower()}.com/company-guides)
                    """)
                
                with tab_b:
                    st.markdown("""
                    **🌟 Pro Tips for Success:**
                    - Research the company's recent projects and mention them
                    - Use STAR method for behavioral questions
                    - Practice whiteboarding with time constraints
                    - Prepare 2-3 thoughtful questions for the interviewer
                    """)
                
                with tab_c:
                    st.markdown("""
                    **🎤 AI Mock Interview (Coming Soon)**
                    <div style="border:2px dashed #4CAF50; padding:20px; border-radius:10px; text-align:center;">
                        <p>🎧 Voice-based AI Interview Practice</p>
                        <p>📊 Instant Feedback & Analytics</p>
                        <p>🤖 Real-time Technical Challenge</p>
                        <small>Powered by AI Interview Coach</small>
                    </div>
                    """, unsafe_allow_html=True)

# ----------------- TAB 3: FREE COURSES -----------------
with tab3:
    st.header(f"🎓 {t['free_courses']}")
    
    # Curated course database
    COURSES = [
        {
            "title": "AI For Everyone",
            "provider": "Coursera",
            "link": "https://coursera.org/learn/ai-for-everyone",
            "category": "AI",
            "difficulty": "Beginner",
            "duration": "6 hours",
            "rating": 4.8,
            "certificate": True,
            "skills": ["AI Basics", "Business Strategy"]
        },
        {
            "title": "Data Science Fundamentals",
            "provider": "IBM",
            "link": "https://skillsbuild.org/data-science",
            "category": "Data Science",
            "difficulty": "Intermediate",
            "duration": "20 hours",
            "rating": 4.5,
            "certificate": True,
            "skills": ["Python", "Pandas", "Data Analysis"]
        },
        # Add more courses...
    ]

    with st.form("course_search"):
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            search_query = st.text_input(t["search_course"], "AI for Business")
        with col2:
            category_filter = st.selectbox("Category", ["All", "AI", "Data Science", "Programming", "Soft Skills"])
        with col3:
            difficulty_filter = st.selectbox("Difficulty", ["All", "Beginner", "Intermediate", "Advanced"])
        submitted = st.form_submit_button(f"🎯 {t['find_courses']}")

    if submitted:
        filtered_courses = [
            c for c in COURSES
            if (search_query.lower() in c["title"].lower() or not search_query)
            and (category_filter == "All" or c["category"] == category_filter)
            and (difficulty_filter == "All" or c["difficulty"] == difficulty_filter)
        ]

        st.subheader(f"📚 {len(filtered_courses)} Courses Found")
        
        for course in filtered_courses:
            with st.expander(f"### {course['title']} ({course['provider']})", expanded=True):
                cols = st.columns([1, 3, 1])
                with cols[0]:
                    st.image(f"https://logo.clearbit.com/{course['provider']}.com", width=60)
                with cols[1]:
                    st.markdown(f"""
                    **Provider:** {course['provider']}  
                    **Duration:** {course['duration']}  
                    **Skills:** {", ".join(course['skills'])}  
                    **Certificate:** {'✅ Available' if course['certificate'] else '❌ Not Available'}
                    """)
                with cols[2]:
                    st.markdown(f"""
                    <div style="text-align:center">
                        <div style="font-size:24px; color:#4CAF50;">{course['rating']}★</div>
                        <a href="{course['link']}" target="_blank" style="display:block; padding:8px; background:#4CAF50; color:white; border-radius:5px; text-decoration:none;">
                            Enroll Now
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#f0f5ff; padding:20px; border-radius:10px; margin-top:20px;">
            <h4>🎓 Learning Path Recommendations</h4>
            <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:20px; margin-top:15px;">
                <div style="background:white; padding:15px; border-radius:10px;">
                    <h5>🚀 AI Specialist Path</h5>
                    <p>1. AI Basics → 2. Machine Learning → 3. Deep Learning</p>
                </div>
                <div style="background:white; padding:15px; border-radius:10px;">
                    <h5>📊 Data Analyst Path</h5>
                    <p>1. Excel → 2. SQL → 3. Python → 4. Data Visualization</p>
                </div>
                <div style="background:white; padding:15px; border-radius:10px;">
                    <h5>💼 Business Intelligence Path</h5>
                    <p>1. Power BI → 2. Tableau → 3. Data Storytelling</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
