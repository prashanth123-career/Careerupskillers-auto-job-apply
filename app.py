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
    "te": {
        "title": "కెరీర్ అప్‌స్కిల్లర్స్ | ఏఐ ఉద్యోగ హబ్",
        "tagline": "మీ ఏఐ ఆధారిత కెరీర్ ప్రారంభ వేదిక",
        "description": "స్మార్ట్ జాబ్ సెర్చ్ | ఇంటర్వ్యూ తయారీ | ఉచిత సర్టిఫికేట్‌లు",
        "job_finder": "ఉద్యోగ శోధకుడు",
        "interview_prep": "ఇంటర్వ్యూ తయారీ",
        "free_courses": "ఉచిత కోర్సులు",
        "find_jobs": "ఉద్యోగాలను కనుగొనండి",
        "generate_link": "ఇంటర్వ్యూ లింక్ రూపొందించండి",
        "find_courses": "కోర్సులను కనుగొనండి",
        "job_title": "ఉద్యోగ శీర్షిక / కీవర్డ్‌లు",
        "location": "ఇష్టమైన ప్రదేశం",
        "country": "దేశం",
        "experience": "అనుభవ స్థాయి",
        "date_posted": "పోస్ట్ చేసిన తేదీ",
        "search_course": "కోర్సు / నైపుణ్యం / ఉద్యోగ శీర్షికను శోధించండి",
        "experience_options": ["ఏదైనా", "ఎంట్రీ", "మధ్యస్థం", "సీనియర్", "ఎగ్జిక్యూటివ్"],
        "date_posted_options": ["ఏ సమయంలోనైనా", "గత నెల", "గత వారం", "గత 24 గంటలు"],
    },
    "ml": {
        "title": "കരിയർ അപ്‌സ്‌കില്ലേഴ്‌സ് | എഐ ജോബ് ഹബ്",
        "tagline": "നിങ്ങളുടെ എഐ അധിഷ്ഠിത കരിയർ ആരംഭം",
        "description": "സ്മാർട്ട് ജോബ് തിരയൽ | ഇന്റർവ്യൂ തയ്യാറെടുപ്പ് | സൗജന്യ സർട്ടിഫിക്കറ്റുകൾ",
        "job_finder": "ജോബ് ഫൈൻഡർ",
        "interview_prep": "ഇന്റർവ്യൂ തയ്യാറെടുപ്പ്",
        "free_courses": "സൗജന്യ കോഴ്സുകൾ",
        "find_jobs": "ജോലികൾ കണ്ടെത്തുക",
        "generate_link": "ഇന്റർവ്യൂ ലിങ്ക് സൃഷ്ടിക്കുക",
        "find_courses": "കോഴ്സുകൾ കണ്ടെത്തുക",
        "job_title": "ജോബ് ടൈറ്റിൽ / കീവേഡുകൾ",
        "location": "പ്രിയപ്പെട്ട സ്ഥലം",
        "country": "രാജ്യം",
        "experience": "അനുഭവനില",
        "date_posted": "പോസ്റ്റ് ചെയ്ത തീയതി",
        "search_course": "കോഴ്സ് / കഴിവ് / ജോബ് ടൈറ്റിൽ തിരയുക",
        "experience_options": ["ഏതെങ്കിലും", "എൻട്രി", "മധ്യ", "സീനിയർ", "എക്‌സിക്യൂട്ടീവ്"],
        "date_posted_options": ["ഏത് സമയത്തും", "കഴിഞ്ഞ മാസം", "കഴിഞ്ഞ ആഴ്ച", "കഴിഞ്ഞ 24 മണിക്കൂർ"],
    },
    "fr": {
        "title": "CareerUpskillers | Centre d'emploi IA",
        "tagline": "Votre tremplin de carrière alimenté par l'IA",
        "description": "Recherche d'emploi intelligente | Préparation à l'entretien | Certifications gratuites",
        "job_finder": "Chercheur d'emploi",
        "interview_prep": "Préparation à l'entretien",
        "free_courses": "Cours gratuits",
        "find_jobs": "Trouver des emplois",
        "generate_link": "Générer le lien de préparation à l'entretien",
        "find_courses": "Trouver des cours",
        "job_title": "Intitulé du poste / Mots-clés",
        "location": "Emplacement préféré",
        "country": "Pays",
        "experience": "Niveau d'expérience",
        "date_posted": "Date de publication",
        "search_course": "Rechercher un cours / une compétence / un poste",
        "experience_options": ["Tout", "Débutant", "Intermédiaire", "Confirmé", "Cadre"],
        "date_posted_options": ["N'importe quand", "Le mois dernier", "La semaine dernière", "Les dernières 24 heures"],
    },
    "de": {
        "title": "CareerUpskillers | KI-Job-Hub",
        "tagline": "Ihre KI-gestützte Karriereplattform",
        "description": "Intelligente Jobsuche | Interviewvorbereitung | Kostenlose Zertifikate",
        "job_finder": "Jobsuche",
        "interview_prep": "Interview-Vorbereitung",
        "free_courses": "Kostenlose Kurse",
        "find_jobs": "Jobs finden",
        "generate_link": "Interview-Link generieren",
        "find_courses": "Kurse finden",
        "job_title": "Jobtitel / Schlüsselwörter",
        "location": "Bevorzugter Standort",
        "country": "Land",
        "experience": "Erfahrungslevel",
        "date_posted": "Veröffentlichungsdatum",
        "search_course": "Kurs / Fähigkeit / Jobtitel suchen",
        "experience_options": ["Beliebig", "Einsteiger", "Mittel", "Senior", "Führungskraft"],
        "date_posted_options": ["Jederzeit", "Letzter Monat", "Letzte Woche", "Letzte 24 Stunden"],
    },
    "ar": {
        "title": "CareerUpskillers | مركز الوظائف بالذكاء الاصطناعي",
        "tagline": "منصتك لإطلاق مهنتك بالذكاء الاصطناعي",
        "description": "بحث ذكي عن الوظائف | التحضير للمقابلات | شهادات مجانية",
        "job_finder": "الباحث عن عمل",
        "interview_prep": "التحضير للمقابلة",
        "free_courses": "دورات مجانية",
        "find_jobs": "ابحث عن وظائف",
        "generate_link": "إنشاء رابط التحضير للمقابلة",
        "find_courses": "ابحث عن الدورات",
        "job_title": "المسمى الوظيفي / الكلمات الرئيسية",
        "location": "الموقع المفضل",
        "country": "الدولة",
        "experience": "مستوى الخبرة",
        "date_posted": "تاريخ النشر",
        "search_course": "ابحث عن دورة / مهارة / وظيفة",
        "experience_options": ["أي", "مبتدئ", "متوسط", "كبير", "تنفيذي"],
        "date_posted_options": ["في أي وقت", "الشهر الماضي", "الأسبوع الماضي", "آخر 24 ساعة"],
    },
}

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
            ("Indeed", lambda k, l, e, d: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
            ("Monster", lambda k, l, e, d: f"https://www.monster.com/jobs/search/?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}")
        ],
        "UK": [
            ("LinkedIn", lambda k, l, e, d: f"https://uk.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
            ("Reed", lambda k, l, e, d: f"https://www.reed.co.uk/jobs/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
            ("TotalJobs", lambda k, l, e, d: f"https://www.totaljobs.com/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}"),
            ("CV-Library", lambda k, l, e, d: f"https://www.cv-library.co.uk/search-jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
        ],
        "UAE": [
            ("LinkedIn", lambda k, l, e, d: f"https://ae.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
            ("Bayt", lambda k, l, e, d: f"https://www.bayt.com/en/uae/jobs/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
            ("NaukriGulf", lambda k, l, e, d: f"https://www.naukrigulf.com/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
            ("GulfTalent", lambda k, l, e, d: f"https://www.gulftalent.com/uae/jobs/title/{k.lower().replace(' ', '-')}")
        ],
        "Germany": [
            ("LinkedIn", lambda k, l, e, d: f"https://de.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
            ("StepStone", lambda k, l, e, d: f"https://www.stepstone.de/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}.html"),
            ("XING", lambda k, l, e, d: f"https://www.xing.com/jobs/search?q={urllib.parse.quote(k)}"),
            ("Monster DE", lambda k, l, e, d: f"https://www.monster.de/jobs/suche/?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}")
        ],
        "Australia": [
            ("LinkedIn", lambda k, l, e, d: f"https://au.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
            ("Seek", lambda k, l, e, d: f"https://www.seek.com.au/{k.lower().replace(' ', '-')}-jobs/in-{l.lower().replace(' ', '-')}"),
            ("Adzuna", lambda k, l, e, d: f"https://www.adzuna.com.au/search?q={urllib.parse.quote(k)}&loc={urllib.parse.quote(l)}"),
            ("CareerOne", lambda k, l, e, d: f"https://www.careerone.com.au/jobs?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}")
        ],
        "New Zealand": [
            ("Seek NZ", lambda k, l, e, d: f"https://www.seek.co.nz/{k.lower().replace(' ', '-')}-jobs/in-{l.lower().replace(' ', '-')}"),
            ("TradeMe Jobs", lambda k, l, e, d: f"https://www.trademe.co.nz/a/jobs/search?search_string={urllib.parse.quote(k)}"),
            ("MyJobSpace", lambda k, l, e, d: f"https://www.myjobspace.co.nz/jobs?q={urllib.parse.quote(k)}")
        ],
        "Russia": [
            ("hh.ru", lambda k, l, e, d: f"https://hh.ru/search/vacancy?text={urllib.parse.quote(k)}&area=113"),
            ("SuperJob", lambda k, l, e, d: f"https://www.superjob.ru/vacancy/search/?keywords={urllib.parse.quote(k)}"),
            ("Rabota.ru", lambda k, l, e, d: f"https://www.rabota.ru/vacancy?query={urllib.parse.quote(k)}")
        ],
        "China": [
            ("51Job", lambda k, l, e, d: f"https://search.51job.com/list/000000,000000,0000,00,9,99,{urllib.parse.quote(k)},2,1.html"),
            ("Zhaopin", lambda k, l, e, d: f"https://sou.zhaopin.com/?jl=530&kw={urllib.parse.quote(k)}"),
            ("Liepin", lambda k, l, e, d: f"https://www.liepin.com/zhaopin/?key={urllib.parse.quote(k)}")
        ],
        "Japan": [
            ("Daijob", lambda k, l, e, d: f"https://www.daijob.com/en/jobs/search?keyword={urllib.parse.quote(k)}"),
            ("Jobs in Japan", lambda k, l, e, d: f"https://jobsinjapan.com/jobs/?search={urllib.parse.quote(k)}"),
            ("GaijinPot", lambda k, l, e, d: f"https://jobs.gaijinpot.com/index/index/search?keywords={urllib.parse.quote(k)}")
        ]
    }

    with st.form("job_form"):
        col1, col2 = st.columns(2)
        with col1:
            keyword = st.text_input(t["job_title"], "Data Scientist")
            location = st.text_input(t["location"], "Remote")
            manual_mode = st.checkbox("Manually select country", value=True)
            if manual_mode:
                country = st.selectbox(t["country"], list(PORTALS_BY_COUNTRY.keys()))
            else:
                import geocoder
                user_location = geocoder.ip('me')
                detected_country = user_location.country if user_location else "India"
                country = detected_country if detected_country in PORTALS_BY_COUNTRY else "India"
                st.markdown(f"**🌍 Detected Country:** {country}")
        with col2:
            experience = st.selectbox(t["experience"], t["experience_options"])
            date_posted = st.selectbox(t["date_posted"], t["date_posted_options"])
        submitted = st.form_submit_button(t["find_jobs"])

    if submitted:
        time_map = {
            t["date_posted_options"][0]: "",
            t["date_posted_options"][1]: "r2592000",
            t["date_posted_options"][2]: "r604800",
            t["date_posted_options"][3]: "r86400"
        }
        exp_map = {
            t["experience_options"][0]: "",
            t["experience_options"][1]: "2",
            t["experience_options"][2]: "3",
            t["experience_options"][3]: "4",
            t["experience_options"][4]: "5"
        }
        d_filter = time_map[date_posted]
        e_filter = exp_map[experience]

        st.subheader(f"🔗 Job Search Links in {country}")
        for name, url_func in PORTALS_BY_COUNTRY.get(country, PORTALS_BY_COUNTRY["India"]):
            url = url_func(keyword, location, e_filter, d_filter)
            st.markdown(
                f'<a href="{url}" target="_blank" style="display:inline-block; padding:10px 20px; background:#4CAF50; color:white; border-radius:5px; text-decoration:none; margin-bottom:5px;">'
                f'Search on {name}</a>',
                unsafe_allow_html=True
            )

        # Google Jobs fallback
        google_jobs_url = f"https://www.google.com/search?q={urllib.parse.quote(keyword + ' jobs in ' + location)}"
        st.markdown(
            f'<a href="{google_jobs_url}" target="_blank" style="display:inline-block; padding:10px 20px; background:#4285F4; color:white; border-radius:5px; text-decoration:none; margin-bottom:5px;">'
            f'Search on Google Jobs</a>',
            unsafe_allow_html=True
        )

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
