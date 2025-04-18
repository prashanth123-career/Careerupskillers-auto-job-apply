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

# ----------------- SETUP -----------------
st.set_page_config(page_title="CareerUpskillers | AI Job Hub", page_icon="🌟", layout="centered")

# Language selection
lang = st.sidebar.selectbox("Select Language", list(LANGUAGES.keys()), index=0)
t = TRANSLATIONS.get(LANGUAGES[lang], TRANSLATIONS["en"])  # Default to English if not found
# Show links to our other apps
st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Explore Our AI Tools")
st.sidebar.markdown("🔹 [🧠 AI Email Summarizer](https://careerupskillersemail-summarizer-eflb3octoua7tbdwqdbygd.streamlit.app/)")
st.sidebar.markdown("🔹 [🚀 AI Career Advisor](https://careerupskillers-ai-advisor-d8vugggkkncjpxirbrcbx6.streamlit.app/)")
st.sidebar.markdown("🔹 [📊 AI AutoML & Data Visualization](https://careerupskillersdatalabpro-arfr7sam9pvhahj8fx2vak.streamlit.app/)")
st.sidebar.markdown("🔹 [🛡️ AI CyberSecurity Suite](https://careerupskillerscyberdefence-nceptjghsdpqyiddiimryl.streamlit.app/)")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 Launch Your Own AI Career App for ₹499")
st.sidebar.markdown("""
🚀 Build your own AI-powered career app just like this one – No coding needed!

🔗 **[Pay ₹499 & Get Instant Download](https://pages.razorpay.com/pl_Q9haRTHXpyB9SS/view)**

💼 What's Included:
- Full Job Finder & Chatbot App Code
- Proposal Generator, Fake News Detector
- Freelance Strategy & Client Outreach Templates
- AI Career Roadmap & State-wise Lead Database

📥 **Get the AI Starter Kit instantly after payment**
""", unsafe_allow_html=True)

# Hide Streamlit default elements
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)



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

tab1, tab2, tab3, tab4 = st.tabs([
    f"🌐 {t['job_finder']}", 
    f"🎯 {t['interview_prep']}", 
    f"🎓 {t['free_courses']}", 
    f"💼 Freelance & Remote Jobs"
])

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
st.markdown("""
<div style='background-color:#fffde7; border:2px solid #fdd835; border-radius:10px; padding:20px; margin-top:30px;'>

<h3 style='color:#f57f17;'>🚨 2025 Layoffs Are Real. Don't Wait!</h3>
<p style='font-size:16px; color:#555;'>
Big tech companies are cutting jobs aggressively across the globe:
</p>

<ul style='font-size:15px; color:#444;'>
  <li>🛑 <b>Microsoft</b> is laying off 1,900+ staff in 2025 – <a href='https://timesofindia.indiatimes.com/world/us/microsoft-amazon-the-washington-post-and-other-us-companies-laying-off-in-2025/articleshow/117155852.cms' target='_blank'>Read More</a></li>
  <li>🛑 <b>Amazon, Intel & Morgan Stanley</b> are reducing headcount – <a href='https://www.ndtvprofit.com/business/layoffs-2025-amazon-intel-morgan-stanley-among-companies-cutting-jobs-this-year' target='_blank'>Read More</a></li>
  <li>🛑 <b>HPE, SAP, Google</b> and others are affected – <a href='https://indianexpress.com/article/technology/tech-layoffs-march-2025-it-layoffs-9919985/' target='_blank'>Read More</a></li>
</ul>

<p style='margin-top:10px; font-size:16px;'>
🎥 <b>Watch the layoff trend videos:</b><br>
<a href='https://youtu.be/WZW0xbzUHj8?si=TsObXAUIumP3n53s' target='_blank'>🔹 Layoffs Explained</a> |
<a href='https://youtu.be/vM8Chmkd22o?si=wIGD24ZegI8rj6Zg' target='_blank'>🔹 Tech Job Cuts</a> |
<a href='https://youtu.be/uq_ba4Prjps?si=KW2odA2izyFDsNw6' target='_blank'>🔹 Real Layoff Stories</a> |
<a href='https://youtu.be/3ZmtSdAjxCM?si=h7W4AaezK_6xaBQd' target='_blank'>🔹 Layoffs 2025 Insights</a>
</p>

<hr style='margin:15px 0;'>

<h4 style='color:#1b5e20;'>💬 Real Success Story:</h4>
<p style='font-size:15px; color:#333; font-style:italic;'>
"I lost my job in Nov 2024. I was depressed and clueless. But after joining CareerUpskillers and buying the ₹499 AI Kit, I started freelancing with AI tools. Now I earn ₹90K–₹1.7L/month from global clients!"<br>
– <b>Rahul Verma, Ex-Employee at HPE</b>
</p>

<p style='font-size:16px; color:#000; font-weight:bold;'>
🔥 Grab your <span style='color:#d32f2f;'>₹499 AI Premium Kit</span> – Automate tasks, build your AI career, and earn globally!
</p>

<a href='https://pages.razorpay.com/pl_Q9haRTHXpyB9SS/view' target='_blank' style='display:inline-block; padding:10px 20px; background:#1976d2; color:#fff; font-weight:bold; border-radius:6px; text-decoration:none; font-size:16px;'>🚀 Buy Now – Limited Time Offer</a>

</div>
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
            st.markdown("""
<div style='background-color:#fffde7; border:2px solid #fdd835; border-radius:10px; padding:20px; margin-top:30px;'>

<h3 style='color:#f57f17;'>😨 Tired of Rejections? Interviews Got You Nervous?</h3>

<p style='font-size:16px; color:#555;'>
🔸 Most candidates fail interviews not because they lack skills – but because they lack <b>smart preparation</b>.<br>
🔸 If you're still Googling "top 10 interview questions", you're already behind.
</p>

<h4 style='color:#1b5e20;'>🎯 What's Inside the ₹499 AI Interview Kit?</h4>
<ul style='font-size:15px; color:#333;'>
  <li>📄 150+ Real Company Interview Questions (TCS, Accenture, Google, Amazon...)</li>
  <li>🎥 Curated YouTube Playlists by Role (Data Analyst, Developer, Marketing...)</li>
  <li>🧠 Behavioral, Resume & Salary Negotiation Training</li>
  <li>🚀 Daily AI-generated Mock Questions & Custom Prep Links</li>
</ul>

<hr style='margin:15px 0;'>

<h4 style='color:#1b5e20;'>💬 Real User Testimonial:</h4>
<p style='font-size:15px; color:#333; font-style:italic;'>
"I got rejected in 5 interviews in Jan 2025. But once I used the ₹499 AI Interview Kit from CareerUpskillers, I got an offer from Infosys in 18 days! This changed my life!"<br>
– <b>Meenakshi R., Hyderabad</b>
</p>

<p style='font-size:16px; color:#000; font-weight:bold;'>
🎁 Don’t let interviews scare you. <span style='color:#d32f2f;'>Master them with AI!</span>
</p>

<a href='https://pages.razorpay.com/pl_Q9haRTHXpyB9SS/view' target='_blank' style='display:inline-block; padding:10px 20px; background:#1976d2; color:#fff; font-weight:bold; border-radius:6px; text-decoration:none; font-size:16px;'>🎯 Buy ₹499 Interview Kit</a>

</div>
""", unsafe_allow_html=True)

# ----------------- TAB 3: FREE COURSES -----------------
with tab3:
    st.header(f"🎓 {t['free_courses']}")

    with st.form("course_form"):
        search = st.text_input(t["search_course"], "AI for Business")
        course_submit = st.form_submit_button(f"🎯 {t['find_courses']}")

    if course_submit:
        query = urllib.parse.quote_plus(search)

        # ----------- Section 1: Free Courses -----------
        st.subheader("🎓 Free Courses")
        free_courses = [
            ("Coursera Free", f"https://www.coursera.org/search?query={query}&price=1"),
            ("edX Free Courses", f"https://www.edx.org/search?q={query}&price=Free"),
            ("Harvard Online", f"https://pll.harvard.edu/catalog?search_api_fulltext={query}&f%5B0%5D=course_feature_free%3A1"),
            ("YouTube Tutorials", f"https://www.youtube.com/results?search_query=free+{query}+course")
        ]
        for name, url in free_courses:
            st.markdown(f"<a href='{url}' target='_blank' style='display:block; background:#6366f1; color:white; padding:10px; border-radius:5px; margin-bottom:5px;'>📘 {name}</a>", unsafe_allow_html=True)

        # ----------- Section 2: Free Courses with Certification -----------
        st.subheader("📜 Free Courses with Certification")
        certified_courses = [
            ("Google Career Certificates", f"https://grow.google/certificates/?q={query}"),
            ("IBM SkillsBuild", f"https://skillsbuild.org/learn?search={query}"),
            ("Meta Blueprint", f"https://www.facebook.com/business/learn/courses?search={query}"),
            ("AWS Skill Builder", f"https://explore.skillbuilder.aws/learn?searchTerm={query}"),
            ("Google Cloud Skills Boost", f"https://www.cloudskillsboost.google/catalog?search={query}")
        ]
        for name, url in certified_courses:
            st.markdown(f"<a href='{url}' target='_blank' style='display:block; background:#10b981; color:white; padding:10px; border-radius:5px; margin-bottom:5px;'>📜 {name}</a>", unsafe_allow_html=True)

        # ----------- Section 3: Free Hands-on Platforms -----------
        st.subheader("🛠️ Free Platforms for Hands-on Experience")
        platforms = [
            ("GitHub Learning Lab", "https://lab.github.com/"),
            ("Microsoft Learn", f"https://learn.microsoft.com/en-us/training/browse/?terms={query}"),
            ("Kaggle Courses", f"https://www.kaggle.com/learn/search?q={query}"),
            ("Codecademy Free", f"https://www.codecademy.com/catalog/all?query={query}&level=free"),
            ("DataCamp Free", f"https://www.datacamp.com/search?q={query}")
        ]
        for name, url in platforms:
            st.markdown(f"<a href='{url}' target='_blank' style='display:block; background:#f97316; color:white; padding:10px; border-radius:5px; margin-bottom:5px;'>🛠️ {name}</a>", unsafe_allow_html=True)
st.markdown("""
<div style='background-color:#e8f5e9; border:2px solid #43a047; border-radius:10px; padding:20px; margin-top:30px;'>

<h3 style='color:#2e7d32;'>🎓 Learning for Free? Here's How to Start Earning</h3>

<p style='font-size:16px; color:#444;'>
👏 You're taking a great first step with free courses. But if you're serious about building <b>an AI-powered career</b>, it's time to get real-world tools that <b>pay the bills</b>.
</p>

<h4 style='color:#1b5e20;'>🔥 Limited-Time Bonus – ₹499 AI Career Kit:</h4>
<ul style='font-size:15px; color:#333;'>
  <li>💼 10+ Freelance-Ready AI Projects (Chatbot, Face Recognition, Resume Parser...)</li>
  <li>📊 ₹90,000 – ₹1.7L Salary Insights for Each Role</li>
  <li>🧠 Personalized Career Roadmap + Job Links</li>
  <li>🎯 Interview + Resume Masterclass (with PDF checklists)</li>
</ul>

<hr style='margin:15px 0;'>

<h4 style='color:#1b5e20;'>🗣️ Real Story from Our Students:</h4>
<p style='font-size:15px; color:#333; font-style:italic;'>
"In Nov 2024, I got laid off. After 30 days with the CareerUpskillers AI Kit, I landed a freelance project worth ₹65,000. From watching free videos to earning – this kit bridged the gap." <br>
– <b>Arjun V., B.Tech (ECE), Chennai</b>
</p>

<p style='font-size:16px; color:#000; font-weight:bold;'>
🚀 You’ve started learning. Now it’s time to start earning.
</p>

<a href='https://pages.razorpay.com/pl_Q9haRTHXpyB9SS/view' target='_blank' style='display:inline-block; padding:10px 20px; background:#1976d2; color:#fff; font-weight:bold; border-radius:6px; text-decoration:none; font-size:16px;'>💼 Buy ₹499 AI Career Kit</a>

</div>
""", unsafe_allow_html=True)

            # ----------------- TAB 4: FREELANCE & REMOTE JOBS -----------------
with tab4:
    st.header("💼 Freelance & Remote Jobs")

    with st.form("freelance_form"):
        keyword = st.text_input("🛠️ Skill / Job Title", "Python Developer")
        job_type = st.selectbox("💼 Job Type", ["Freelance", "Remote", "Both"])
        region = st.selectbox("🌍 Region", ["Global", "India", "USA", "UK", "Canada", "Germany", "UAE"])
        submit = st.form_submit_button("🔎 Find Jobs")

    if submit:
        q = urllib.parse.quote_plus(keyword)

        st.subheader("🚀 Job Boards with Smart Links")

        platforms = []

        if job_type in ["Freelance", "Both"]:
            platforms += [
                ("Upwork", f"https://www.upwork.com/search/jobs/?q={q}"),
                ("Fiverr", f"https://www.fiverr.com/search/gigs?query={q}"),
                ("Freelancer", f"https://www.freelancer.com/jobs/{q}"),
                ("PeoplePerHour", f"https://www.peopleperhour.com/freelance-jobs?q={q}"),
                ("Toptal", "https://www.toptal.com/freelance-jobs"),
                ("Guru", f"https://www.guru.com/d/jobs/skill/{q}/"),
            ]

        if job_type in ["Remote", "Both"]:
            region_map = {
                "Global": "",
                "India": "&location=India",
                "USA": "&location=United+States",
                "UK": "&location=United+Kingdom",
                "Canada": "&location=Canada",
                "Germany": "&location=Germany",
                "UAE": "&location=United+Arab+Emirates"
            }

            region_filter = region_map.get(region, "")
            platforms += [
                ("Remote OK", f"https://remoteok.com/remote-{q}-jobs"),
                ("We Work Remotely", f"https://weworkremotely.com/remote-jobs/search?term={q}"),
                ("AngelList Talent", f"https://angel.co/jobs?remote=true&keyword={q}{region_filter}"),
                ("Jobspresso", f"https://jobspresso.co/?s={q}"),
                ("Remotive", f"https://remotive.io/remote-jobs/search/{q}"),
                ("Outsourcely", f"https://www.outsourcely.com/remote-jobs/search?q={q}")
            ]

        for name, url in platforms:
            st.markdown(
                f"<a href='{url}' target='_blank' style='display:block; background:#0f766e; color:white; padding:10px; border-radius:5px; margin-bottom:5px;'>🌍 {name}</a>",
                unsafe_allow_html=True
            )

        # Google fallback
        st.markdown("---")
        st.markdown(f"<a href='https://www.google.com/search?q={q}+{job_type}+jobs+{region}' target='_blank' style='display:block; background:#dc2626; color:white; padding:10px; border-radius:5px;'>🔍 Search on Google Jobs</a>", unsafe_allow_html=True)
st.markdown("""
<div style='background-color:#fff8e1; border:2px solid #f9a825; border-radius:10px; padding:20px; margin-top:30px;'>

<h3 style='color:#ef6c00;'>🚀 Can't Find the Right Job? Create Your Own Opportunities</h3>

<p style='font-size:16px; color:#444;'>
Whether you're job hunting, switching careers, or stuck in endless applications, here's a fact:
<b>AI freelancers are earning ₹50K – ₹1.5L/month by building tools from home.</b>
</p>

<h4 style='color:#bf360c;'>🎁 Introducing the ₹499 AI Career Kit (90% Off)</h4>
<ul style='font-size:15px; color:#333;'>
  <li>✅ 10+ Freelance-Ready AI Projects (Chatbot, Resume Parser, Fake News Detector, etc.)</li>
  <li>📈 Tools to automate your job search, interview prep & applications</li>
  <li>🧾 AI-generated proposals & cover letters</li>
  <li>💸 Ideal for Upwork, Fiverr, LinkedIn & Internshala freelancing</li>
</ul>

<hr style='margin:15px 0;'>

<p style='font-size:15px; color:#333; font-style:italic;'>
"After applying for 70+ jobs with no response, I switched to freelancing with this kit. Now earning ₹1.2L/month working from home."  
<br>– <b>Sana Rahman, MBA, Hyderabad</b>
</p>

<p style='font-size:16px; color:#000; font-weight:bold;'>
Don't wait for a job – start your AI freelancing journey today.
</p>

<a href='https://pages.razorpay.com/pl_Q9haRTHXpyB9SS/view' target='_blank' style='display:inline-block; padding:10px 20px; background:#1976d2; color:#fff; font-weight:bold; border-radius:6px; text-decoration:none; font-size:16px;'>💼 Get the ₹499 AI Career Kit</a>

</div>
""", unsafe_allow_html=True)

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
