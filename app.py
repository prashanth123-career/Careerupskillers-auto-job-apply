import streamlit as st
import urllib.parse
import google.generativeai as genai
from PyPDF2 import PdfReader

# Configure Gemini API using Streamlit secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# Initialize Gemini model
def get_gemini_model():
    return genai.GenerativeModel('gemini-pro')

# Extract text from PDF resume
def pdf_to_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# Construct prompt for resume match score
def construct_score_prompt(resume, job_description):
    prompt = f'''
    Act as an HR Manager with 20 years of experience. Compare the resume provided below with the job description given below.
    Provide a score from 0 to 10 on how well the resume matches the job based on:
    1. Key skills that match.
    2. Missing skills or qualifications.
    The score should be a number between 0 and 10, where 0 means little to no match and 10 means a perfect match.
    Return the response in the format: "Score: X/10\nMatching Skills: ...\nMissing Skills: ..."
    
    Resume: {resume}
    Job Description: {job_description}
    '''
    return prompt

# Construct prompt for resume improvement suggestions
def construct_improvement_prompt(resume, job_description):
    prompt = f'''
    Act as a career coach with 15 years of experience. Analyze the resume and job description below.
    Suggest specific changes to improve the resume to better match the job description.
    Focus on:
    1. Keywords to add.
    2. Skills to emphasize.
    3. Any sections to rephrase for better impact.
    Return the response as a list of actionable suggestions.
    
    Resume: {resume}
    Job Description: {job_description}
    '''
    return prompt

# Get response from Gemini model
def get_result(prompt):
    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: Could not process the request with Gemini LLM. Details: {str(e)}"

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
        "resume_analysis": "Resume Analysis",
        "upload_resume": "Upload Your Resume (PDF)",
        "analyze_resume": "Analyze Resume",
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
        "resume_analysis": "रिज्यूमे विश्लेषण",
        "upload_resume": "अपना रिज्यूमे अपलोड करें (PDF)",
        "analyze_resume": "रिज्यूमे का विश्लेषण करें",
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
        "resume_analysis": "ரெஸ்யூமே பகுப்பாய்வு",
        "upload_resume": "உங்கள் ரெஸ்யூமேவை பதிவேற்றவும் (PDF)",
        "analyze_resume": "ரெஸ்யூமேவை பகுப்பாய்வு செய்யவும்",
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
        "resume_analysis": "రెజ్యూమ్ విశ్లేషణ",
        "upload_resume": "మీ రెజ్యూమ్‌ను అప్‌లోడ్ చేయండి (PDF)",
        "analyze_resume": "రెజ్యూమ్ విశ్లేషించండి",
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
        "resume_analysis": "റെസ്യൂം വിശകലനം",
        "upload_resume": "നിന്റെ റെസ്യൂം അപ്‌ലോഡ് ചെയ്യുക (PDF)",
        "analyze_resume": "റെസ്യൂം വിശകലനം ചെയ്യുക",
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
        "resume_analysis": "Analyse de CV",
        "upload_resume": "Téléchargez votre CV (PDF)",
        "analyze_resume": "Analyser le CV",
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
        "resume_analysis": "Lebenslauf-Analyse",
        "upload_resume": "Laden Sie Ihren Lebenslauf hoch (PDF)",
        "analyze_resume": "Lebenslauf analysieren",
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
        "resume_analysis": "تحليل السيرة الذاتية",
        "upload_resume": "قم بتحميل سيرتك الذاتية (PDF)",
        "analyze_resume": "تحليل السيرة الذاتية",
    },
}

# ----------------- SETUP -----------------
st.set_page_config(page_title="CareerUpskillers | AI Job Hub", page_icon="🌟", layout="centered")

# Language selection
lang = st.sidebar.selectbox("Select Language", list(LANGUAGES.keys()), index=0)
t = TRANSLATIONS.get(LANGUAGES[lang], TRANSLATIONS["en"])  # Default to English if not found
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

# ----------------- BRANDING -----------------
st.markdown(f"""
<div style='text-align:center; padding:10px 0;'>
    <h1 style='color:#1f2937;'>🚀 {t["title"]}</h1>
    <h4 style='color:#374151;'>{t["tagline"]}</h4>
    <p style='font-size:16px;'>{t["description"]}</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    f"🌐 {t['job_finder']}", 
    f"🎯 {t['interview_prep']}", 
    f"🎓 {t['free_courses']}", 
    f"💼 Freelance & Remote Jobs",
    f"🌍 International Jobs"  # You can add this to your translations if needed
])
# ----------------- TAB 1: JOB FINDER -----------------
with tab1:
    st.header(f"🌐 {t['job_finder']}")
    PORTALS_BY_COUNTRY = {
    "India": [
        ("LinkedIn", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("Naukri", lambda k, l, e, d: f"https://www.naukri.com/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-') if l != 'Remote' else 'india'}"),
        ("Indeed", lambda k, l, e, d: f"https://www.indeed.co.in/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Shine", lambda k, l, e, d: f"https://www.shine.com/job-search/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("Apna", lambda k, l, e, d: f"https://www.apna.co/jobs/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("CutShort", lambda k, l, e, d: f"https://cutshort.io/jobs?search={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Hirect", lambda k, l, e, d: f"https://hirect.in/"),
        ("Instahyre", lambda k, l, e, d: f"https://www.instahyre.com/"),
        ("Foundit (Monster)", lambda k, l, e, d: f"https://www.foundit.in/search/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}")
    ],
    "USA": [
        ("LinkedIn", lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}"),
        ("USAJobs", lambda k, l, e, d: f"https://www.usajobs.gov/Search/Results?k={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Indeed", lambda k, l, e, d: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Monster", lambda k, l, e, d: f"https://www.monster.com/jobs/search/?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}"),
        ("ZipRecruiter", lambda k, l, e, d: f"https://www.ziprecruiter.com/jobs-search?search={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Glassdoor", lambda k, l, e, d: f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={urllib.parse.quote(k)}&locT=C&locId={urllib.parse.quote(l)}"),
        ("AngelList", lambda k, l, e, d: f"https://angel.co/jobs"),
        ("Built In", lambda k, l, e, d: f"https://builtin.com/jobs"),
        ("Dice", lambda k, l, e, d: f"https://www.dice.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "UK": [
        ("LinkedIn", lambda k, l, e, d: f"https://uk.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Reed", lambda k, l, e, d: f"https://www.reed.co.uk/jobs/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("TotalJobs", lambda k, l, e, d: f"https://www.totaljobs.com/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}"),
        ("CV-Library", lambda k, l, e, d: f"https://www.cv-library.co.uk/search-jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Adzuna UK", lambda k, l, e, d: f"https://www.adzuna.co.uk/search?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}"),
        ("CWJobs", lambda k, l, e, d: f"https://www.cwjobs.co.uk/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}"),
        ("Jobsite UK", lambda k, l, e, d: f"https://www.jobsite.co.uk/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}")
    ],
    "UAE": [
        ("LinkedIn", lambda k, l, e, d: f"https://ae.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Bayt", lambda k, l, e, d: f"https://www.bayt.com/en/uae/jobs/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("NaukriGulf", lambda k, l, e, d: f"https://www.naukrigulf.com/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("GulfTalent", lambda k, l, e, d: f"https://www.gulftalent.com/uae/jobs/title/{k.lower().replace(' ', '-')}"),
        ("Laimoon", lambda k, l, e, d: f"https://laimoon.com/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}"),
        ("Dubai Careers", lambda k, l, e, d: f"https://www.dubaicareers.ae/en/search?search={urllib.parse.quote(k)}")
    ],
    "Germany": [
        ("LinkedIn", lambda k, l, e, d: f"https://de.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("StepStone", lambda k, l, e, d: f"https://www.stepstone.de/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}.html"),
        ("XING", lambda k, l, e, d: f"https://www.xing.com/jobs/search?q={urllib.parse.quote(k)}"),
        ("Monster DE", lambda k, l, e, d: f"https://www.monster.de/jobs/suche/?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}"),
        ("Arbeitsagentur", lambda k, l, e, d: f"https://www.arbeitsagentur.de/jobsuche/suche?was={urllib.parse.quote(k)}&wo={urllib.parse.quote(l)}"),
        ("Indeed DE", lambda k, l, e, d: f"https://de.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Kimeta", lambda k, l, e, d: f"https://www.kimeta.de/jobs/{k.lower().replace(' ', '-')}/in-{l.lower().replace(' ', '-')}")
    ],
    "Australia": [
        ("LinkedIn", lambda k, l, e, d: f"https://au.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Seek", lambda k, l, e, d: f"https://www.seek.com.au/{k.lower().replace(' ', '-')}-jobs/in-{l.lower().replace(' ', '-')}"),
        ("Adzuna", lambda k, l, e, d: f"https://www.adzuna.com.au/search?q={urllib.parse.quote(k)}&loc={urllib.parse.quote(l)}"),
        ("CareerOne", lambda k, l, e, d: f"https://www.careerone.com.au/jobs?q={urllib.parse.quote(k)}&where={urllib.parse.quote(l)}"),
        ("Jora", lambda k, l, e, d: f"https://au.jora.com/j?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Australian JobSearch", lambda k, l, e, d: f"https://jobsearch.gov.au/job/search?occupation={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}")
    ],
    "New Zealand": [
        ("Seek NZ", lambda k, l, e, d: f"https://www.seek.co.nz/{k.lower().replace(' ', '-')}-jobs/in-{l.lower().replace(' ', '-')}"),
        ("TradeMe Jobs", lambda k, l, e, d: f"https://www.trademe.co.nz/a/jobs/search?search_string={urllib.parse.quote(k)}"),
        ("MyJobSpace", lambda k, l, e, d: f"https://www.myjobspace.co.nz/jobs?q={urllib.parse.quote(k)}"),
        ("NZ Careers", lambda k, l, e, d: f"https://www.careers.govt.nz/jobs-database/?q={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Student Job Search", lambda k, l, e, d: f"https://www.sjs.co.nz/student-jobs?search={urllib.parse.quote(k)}")
    ],
    "Russia": [
        ("hh.ru", lambda k, l, e, d: f"https://hh.ru/search/vacancy?text={urllib.parse.quote(k)}&area=113"),
        ("SuperJob", lambda k, l, e, d: f"https://www.superjob.ru/vacancy/search/?keywords={urllib.parse.quote(k)}"),
        ("Rabota.ru", lambda k, l, e, d: f"https://www.rabota.ru/vacancy?query={urllib.parse.quote(k)}"),
        ("Careerist.ru", lambda k, l, e, d: f"https://careerist.ru/vacancies/?q={urllib.parse.quote(k)}"),
        ("TrudVsem", lambda k, l, e, d: f"https://trudvsem.ru/vacancy/search?text={urllib.parse.quote(k)}")
    ],
    "China": [
        ("51Job", lambda k, l, e, d: f"https://search.51job.com/list/000000,000000,0000,00,9,99,{urllib.parse.quote(k)},2,1.html"),
        ("Zhaopin", lambda k, l, e, d: f"https://sou.zhaopin.com/?jl=530&kw={urllib.parse.quote(k)}"),
        ("Liepin", lambda k, l, e, d: f"https://www.liepin.com/zhaopin/?key={urllib.parse.quote(k)}"),
        ("Boss Zhipin", lambda k, l, e, d: f"https://www.zhipin.com/web/geek/job?query={urllib.parse.quote(k)}"),
        ("Lagou", lambda k, l, e, d: f"https://www.lagou.com/jobs/list_{urllib.parse.quote(k)}")
    ],
    "Japan": [
        ("Daijob", lambda k, l, e, d: f"https://www.daijob.com/en/jobs/search?keyword={urllib.parse.quote(k)}"),
        ("Jobs in Japan", lambda k, l, e, d: f"https://jobsinjapan.com/jobs/?search={urllib.parse.quote(k)}"),
        ("GaijinPot", lambda k, l, e, d: f"https://jobs.gaijinpot.com/index/index/search?keywords={urllib.parse.quote(k)}"),
        ("Wantedly", lambda k, l, e, d: f"https://www.wantedly.com/projects?q={urllib.parse.quote(k)}"),
        ("CareerCross", lambda k, l, e, d: f"https://www.careercross.com/en/job-search?keywords={urllib.parse.quote(k)}"),
        ("En Japan", lambda k, l, e, d: f"https://www.en-japan.com/search/?keyword={urllib.parse.quote(k)}")
    ],
    "Canada": [
        ("LinkedIn", lambda k, l, e, d: f"https://ca.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Canada", lambda k, l, e, d: f"https://ca.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Job Bank", lambda k, l, e, d: f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={urllib.parse.quote(k)}&locationstring={urllib.parse.quote(l)}"),
        ("Workopolis", lambda k, l, e, d: f"https://www.workopolis.com/jobsearch/find-jobs?query={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Eluta", lambda k, l, e, d: f"https://www.eluta.ca/search?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "Brazil": [
        ("LinkedIn", lambda k, l, e, d: f"https://br.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Brazil", lambda k, l, e, d: f"https://br.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Catho", lambda k, l, e, d: f"https://www.catho.com.br/vagas/{k.lower().replace(' ', '-')}/"),
        ("InfoJobs", lambda k, l, e, d: f"https://www.infojobs.com.br/empregos.aspx?Palabra={urllib.parse.quote(k)}"),
        ("Vagas", lambda k, l, e, d: f"https://www.vagas.com.br/vagas-de-{k.lower().replace(' ', '-')}")
    ],
    "France": [
        ("LinkedIn", lambda k, l, e, d: f"https://fr.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed France", lambda k, l, e, d: f"https://fr.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("APEC", lambda k, l, e, d: f"https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles={urllib.parse.quote(k)}"),
        ("Pôle Emploi", lambda k, l, e, d: f"https://candidat.pole-emploi.fr/offres/recherche?motsCles={urllib.parse.quote(k)}"),
        ("Welcome to the Jungle", lambda k, l, e, d: f"https://www.welcometothejungle.com/fr/jobs?query={urllib.parse.quote(k)}")
    ],
    "Singapore": [
        ("LinkedIn", lambda k, l, e, d: f"https://sg.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Singapore", lambda k, l, e, d: f"https://sg.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("JobStreet", lambda k, l, e, d: f"https://www.jobstreet.com.sg/en/job-search/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}/"),
        ("JobsDB", lambda k, l, e, d: f"https://sg.jobsdb.com/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-')}"),
        ("MyCareersFuture", lambda k, l, e, d: f"https://www.mycareersfuture.gov.sg/search?search={urllib.parse.quote(k)}")
    ],
        "France": [
        ("LinkedIn", lambda k, l, e, d: f"https://fr.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed France", lambda k, l, e, d: f"https://fr.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("APEC", lambda k, l, e, d: f"https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles={urllib.parse.quote(k)}"),
        ("Pôle Emploi", lambda k, l, e, d: f"https://candidat.pole-emploi.fr/offres/recherche?motsCles={urllib.parse.quote(k)}"),
        ("Welcome to the Jungle", lambda k, l, e, d: f"https://www.welcometothejungle.com/fr/jobs?query={urllib.parse.quote(k)}")
    ],
    "Netherlands": [
        ("LinkedIn", lambda k, l, e, d: f"https://nl.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Netherlands", lambda k, l, e, d: f"https://www.indeed.nl/vacatures?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Nationale Vacaturebank", lambda k, l, e, d: f"https://www.nationalevacaturebank.nl/vacatures/{k.lower().replace(' ', '-')}"),
        ("Vacature.nl", lambda k, l, e, d: f"https://www.vacature.nl/vacatures/{k.lower().replace(' ', '-')}"),
        ("Undutchables", lambda k, l, e, d: f"https://www.undutchables.nl/jobs/?search={urllib.parse.quote(k)}")
    ],
    "Spain": [
        ("LinkedIn", lambda k, l, e, d: f"https://es.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Spain", lambda k, l, e, d: f"https://www.indeed.es/trabajo?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("InfoJobs", lambda k, l, e, d: f"https://www.infojobs.net/{k.lower().replace(' ', '-')}/em-i.htm"),
        ("Tecnoempleo", lambda k, l, e, d: f"https://www.tecnoempleo.com/{k.lower().replace(' ', '-')}-trabajo"),
        ("JobFluent", lambda k, l, e, d: f"https://www.jobfluent.com/es-es/empleos-{k.lower().replace(' ', '-')}")
    ],
    "Italy": [
        ("LinkedIn", lambda k, l, e, d: f"https://it.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Italy", lambda k, l, e, d: f"https://it.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("InfoJobs Italia", lambda k, l, e, d: f"https://www.infojobs.it/{k.lower().replace(' ', '-')}/offerte-di-lavoro"),
        ("Monster Italia", lambda k, l, e, d: f"https://www.monster.it/lavoro/cerca/?q={urllib.parse.quote(k)}"),
        ("Glassdoor Italia", lambda k, l, e, d: f"https://www.glassdoor.it/Lavoro/{k.lower().replace(' ', '-')}-lavoro-SRCH_KO0,23.htm")
    ],
    "Sweden": [
        ("LinkedIn", lambda k, l, e, d: f"https://se.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Sweden", lambda k, l, e, d: f"https://se.indeed.com/jobb?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Arbetsförmedlingen", lambda k, l, e, d: f"https://arbetsformedlingen.se/platsbanken/annonser?q={urllib.parse.quote(k)}"),
        ("CareerBuilder SE", lambda k, l, e, d: f"https://www.careerbuilder.se/jobs/{k.lower().replace(' ', '-')}"),
        ("Academic Work", lambda k, l, e, d: f"https://www.academicwork.se/jobb/{k.lower().replace(' ', '-')}")
    ],
    "Switzerland": [
        ("LinkedIn", lambda k, l, e, d: f"https://ch.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Switzerland", lambda k, l, e, d: f"https://ch.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("JobScout24", lambda k, l, e, d: f"https://www.jobscout24.ch/de/jobs/{k.lower().replace(' ', '-')}"),
        ("Jobs.ch", lambda k, l, e, d: f"https://www.jobs.ch/de/stellenangebote/?term={urllib.parse.quote(k)}"),
        ("JobRoom", lambda k, l, e, d: f"https://www.job-room.ch/joboffers?search={urllib.parse.quote(k)}")
    ],
    "Poland": [
        ("LinkedIn", lambda k, l, e, d: f"https://pl.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Poland", lambda k, l, e, d: f"https://pl.indeed.com/praca?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Pracuj.pl", lambda k, l, e, d: f"https://www.pracuj.pl/praca/{k.lower().replace(' ', '%20')}"),
        ("BulldogJob", lambda k, l, e, d: f"https://bulldogjob.pl/companies/jobs/s/role,{k.lower().replace(' ', '-')}"),
        ("No Fluff Jobs", lambda k, l, e, d: f"https://nofluffjobs.com/pl/?criteria=keyword%3D{urllib.parse.quote(k)}")
    ],
    "Portugal": [
        ("LinkedIn", lambda k, l, e, d: f"https://pt.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Portugal", lambda k, l, e, d: f"https://pt.indeed.com/empregos?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("NetEmpregos", lambda k, l, e, d: f"https://www.net-empregos.com/procurar?q={urllib.parse.quote(k)}"),
        ("Sapo Emprego", lambda k, l, e, d: f"https://emprego.sapo.pt/ofertas-emprego/{k.lower().replace(' ', '-')}"),
        ("Talent Portugal", lambda k, l, e, d: f"https://www.talent.com/jobs?k={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}")
    ],
    "Belgium": [
        ("LinkedIn", lambda k, l, e, d: f"https://be.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Belgium", lambda k, l, e, d: f"https://be.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("VDAB", lambda k, l, e, d: f"https://www.vdab.be/vindeenjob/vacatures?keyword={urllib.parse.quote(k)}"),
        ("StepStone BE", lambda k, l, e, d: f"https://www.stepstone.be/zoeken/?ke={urllib.parse.quote(k)}"),
        ("Jobat", lambda k, l, e, d: f"https://www.jobat.be/nl/jobs/{k.lower().replace(' ', '-')}")
    ],
    "Austria": [
        ("LinkedIn", lambda k, l, e, d: f"https://at.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Austria", lambda k, l, e, d: f"https://at.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Karriere.at", lambda k, l, e, d: f"https://www.karriere.at/jobs/{k.lower().replace(' ', '-')}"),
        ("AMS", lambda k, l, e, d: f"https://www.ams.at/arbeitsuchende/jobsuche?search={urllib.parse.quote(k)}"),
        ("Jobwohnen", lambda k, l, e, d: f"https://www.jobwohnen.at/jobs?search={urllib.parse.quote(k)}")
    ],
    "Norway": [
        ("LinkedIn", lambda k, l, e, d: f"https://no.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Norway", lambda k, l, e, d: f"https://no.indeed.com/jobb?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Finn.no", lambda k, l, e, d: f"https://www.finn.no/job/fulltime/search.html?q={urllib.parse.quote(k)}"),
        ("Nav.no", lambda k, l, e, d: f"https://www.nav.no/arbeid/stillinger?q={urllib.parse.quote(k)}"),
        ("Jobbnorge", lambda k, l, e, d: f"https://www.jobbnorge.no/search?q={urllib.parse.quote(k)}")
    ],
    "Denmark": [
        ("LinkedIn", lambda k, l, e, d: f"https://dk.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Denmark", lambda k, l, e, d: f"https://dk.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Jobindex", lambda k, l, e, d: f"https://www.jobindex.dk/jobsoegning?q={urllib.parse.quote(k)}"),
        ("WorkinDenmark", lambda k, l, e, d: f"https://www.workindenmark.dk/Search-Results?search={urllib.parse.quote(k)}"),
        ("Ofir", lambda k, l, e, d: f"https://www.ofir.dk/soeg-job?search={urllib.parse.quote(k)}")
    ],
    "Finland": [
        ("LinkedIn", lambda k, l, e, d: f"https://fi.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Finland", lambda k, l, e, d: f"https://fi.indeed.com/ty%C3%B6paikat?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("Monster Finland", lambda k, l, e, d: f"https://www.monster.fi/tyopaikat/hae/?q={urllib.parse.quote(k)}"),
        ("TE-palvelut", lambda k, l, e, d: f"https://paikat.te-palvelut.fi/tpt/?searchPhrase={urllib.parse.quote(k)}"),
        ("Oikotie", lambda k, l, e, d: f"https://www.oikotie.fi/tyopaikat?words={urllib.parse.quote(k)}")
    ],
    "Ireland": [
        ("LinkedIn", lambda k, l, e, d: f"https://ie.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed Ireland", lambda k, l, e, d: f"https://ie.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("IrishJobs", lambda k, l, e, d: f"https://www.irishjobs.ie/Jobs/{k.lower().replace(' ', '-')}-Jobs"),
        ("Jobs.ie", lambda k, l, e, d: f"https://www.jobs.ie/ApplyForJob.aspx?url=SearchJobs&keywords={urllib.parse.quote(k)}"),
        ("RecruitIreland", lambda k, l, e, d: f"https://www.recruitireland.com/jobs/{k.lower().replace(' ', '-')}")
    ],

    "South Africa": [
        ("LinkedIn", lambda k, l, e, d: f"https://za.linkedin.com/jobs/search?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}"),
        ("Indeed South Africa", lambda k, l, e, d: f"https://za.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}"),
        ("CareerJunction", lambda k, l, e, d: f"https://www.careerjunction.co.za/jobs/keywords/{k.lower().replace(' ', '-')}"),
        ("PNet", lambda k, l, e, d: f"https://www.pnet.co.za/jobs/{k.lower().replace(' ', '-')}"),
        ("JobMail", lambda k, l, e, d: f"https://www.jobmail.co.za/jobs/{k.lower().replace(' ', '-')}")
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
                try:
                    import geocoder
                    user_location = geocoder.ip('me')
                    detected_country = user_location.country if user_location else "India"
                    country = detected_country if detected_country in PORTALS_BY_COUNTRY else "India"
                    st.markdown(f"**🌍 Detected Country:** {country}")
                except Exception as e:
                    country = "India"
                    st.warning(f"Could not detect location: {str(e)}. Defaulting to India.")
        with col2:
            experience = st.selectbox(t["experience"], t["experience_options"])
            date_posted = st.selectbox(t["date_posted"], t["date_posted_options"])
        submitted = st.form_submit_button(t["find_jobs"])

    if submitted:
        if not keyword.strip() or not location.strip():
            st.error("Please enter a job title and location.")
        else:
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

            google_jobs_url = f"https://www.google.com/search?q={urllib.parse.quote(keyword + ' jobs in ' + location)}"
            st.markdown(
                f'<a href="{google_jobs_url}" target="_blank" style="display:inline-block; padding:10px 20px; background:#4285F4; color:white; border-radius:5px; text-decoration:none; margin-bottom:5px;">'
                f'Search on Google Jobs</a>',
                unsafe_allow_html=True
            )

    st.markdown("""
    <div style='background-color:#fffde7; border:2px solid #fdd835; border-radius:10px; padding:20px; margin-top:30px;'>
        <h3 style='color:#f57f17;'>🚨 2025 Layoffs Are Real. Don't Wait!</h3>
        <p style='font-size:16px; color:#555;'>Big tech companies are cutting jobs aggressively across the globe:</p>
        <ul style='font-size:15px; color:#444;'>
            <li>🛑 <b>Microsoft</b> is laying off 1,900+ staff in 2025 – <a href='https://timesofindia.indiatimes.com/world/us/microsoft-amazon-the-washington-post-and-other-us-companies-laying-off-in-2025/articleshow/117155852.cms' target='_blank'>Read More</a></li>
            <li>🛑 <b>Amazon, Intel & Morgan Stanley</b> are reducing headcount – <a href='https://www.ndtvprofit.com/business/layoffs-2025-amazon-intel-morgan-stanley-among-companies-cutting-jobs-this-year' target='_blank'>Read More</a></li>
            <li>🛑 <b>HPE, SAP, Google</b> and others are affected – <a href='https://indianexpress.com/article/technology/tech-layoffs-march-2025-it-layoffs-9919985/' target='_blank'>Read More</a></li>
        </ul>
        <p style='margin-top:10px; font-size:16px;'>🎥 <b>Watch the layoff trend videos:</b><br><a href='https://youtu.be/WZW0xbzUHj8?si=TsObXAUIumP3n53s' target='_blank'>🔹 Layoffs Explained</a> | <a href='https://youtu.be/vM8Chmkd22o?si=wIGD24ZegI8rj6Zg' target='_blank'>🔹 Tech Job Cuts</a> | <a href='https://youtu.be/uq_ba4Prjps?si=KW2odA2izyFDsNw6' target='_blank'>🔹 Real Layoff Stories</a> | <a href='https://youtu.be/3ZmtSdAjxCM?si=h7W4AaezK_6xaBQd' target='_blank'>🔹 Layoffs 2025 Insights</a></p>
        <hr style='margin:15px 0;'>
        <h4 style='color:#1b5e20;'>💬 Real Success Story:</h4>
        <p style='font-size:15px; color:#333; font-style:italic;'>"I lost my job in Nov 2024. I was depressed and clueless. But after joining CareerUpskillers and buying the ₹499 AI Kit, I started freelancing with AI tools. Now I earn ₹90K–₹1.7L/month from global clients!"<br>– <b>Rahul Verma, Ex-Employee at HPE</b></p>
        <p style='font-size:16px; color:#000; font-weight:bold;'>🔥 Grab your <span style='color:#d32f2f;'>₹499 AI Premium Kit</span> – Automate tasks, build your AI career, and earn globally!</p>
        <a href='https://pages.razorpay.com/pl_Q9haRTHXpyB9SS/view' target='_blank' style='display:inline-block; padding:10px 20px; background:#1976d2; color:#fff; font-weight:bold; border-radius:6px; text-decoration:none; font-size:16px;'>🚀 Buy Now – Limited Time Offer</a>
    </div>
    """, unsafe_allow_html=True)

# ----------------- TAB 2: INTERVIEW PREPARATION (Updated with Resume Analysis) -----------------
with tab2:
    st.header(f"🎯 {t['interview_prep']}")
    
    # Sub-tabs for Interview Prep and Resume Analysis
    prep_tab, resume_tab = st.tabs(["Interview Prep Resources", t["resume_analysis"]])
    
    # Interview Prep Resources (Enhanced Functionality)
    with prep_tab:
        # Initialize session state for confidence tracker
        if 'interview_practice_count' not in st.session_state:
            st.session_state.interview_practice_count = 0
        if 'star_stories' not in st.session_state:
            st.session_state.star_stories = []

        # Confidence Tracker
        st.markdown(f"💪 **Interview Confidence**: {st.session_state.interview_practice_count} practice sessions completed")
        progress = min(st.session_state.interview_practice_count / 10, 1.0)  # Max at 10 sessions
        st.progress(progress)
        if st.session_state.interview_practice_count >= 10:
            st.success("🎉 Badge Earned: 10 Questions Mastered!")

        # Updated form with company-specific trending questions
        with st.form("interview_form"):
            col1, col2 = st.columns([1, 2])
            with col1:
                role = st.text_input(t["job_title"], "Data Analyst", key="int_role")
                country = st.selectbox(t["country"], list(PORTALS_BY_COUNTRY.keys()), key="int_country")
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
            if not role.strip():
                st.error("Please enter a job title.")
            else:
                base_query = f"{role} {prep_type} {exp_level} {company} {country}"
                encoded_query = urllib.parse.quote_plus(base_query)
                
                st.subheader("🔍 Best Preparation Resources")
                
                # Updated resource matrix with region-specific resources
                RESOURCE_MATRIX = {
                    "Technical Questions": {
                        "India": "https://www.indiabix.com",
                        "USA": "https://leetcode.com",
                        "Global": "https://www.hackerrank.com"
                    },
                    "Behavioral Questions": {
                        "India": "https://www.ambitionbox.com/interviews",
                        "USA": "https://www.themuse.com/advice/behavioral-interview-questions",
                        "Global": "https://www.vault.com/career-advice/interviewing"
                    },
                    "Case Studies": {
                        "India": "https://www.mbauniverse.com",
                        "USA": "https://www.caseinterview.com",
                        "Global": "https://www.preplounge.com"
                    },
                    "Salary Negotiation": {
                        "India": "https://www.payscale.com",
                        "USA": "https://www.glassdoor.com",
                        "Global": "https://www.salary.com"
                    },
                    "Resume Tips": {
                        "India": "https://www.naukri.com",
                        "USA": "https://www.resume.com",
                        "Global": "https://www.zety.com"
                    }
                }
                
                region_key = country if country in ["India", "USA"] else "Global"
                main_resource = RESOURCE_MATRIX.get(prep_type, {}).get(region_key)
                if main_resource:
                    st.markdown(f"""
                    <div style="padding:15px; background:#e8f5e9; border-radius:10px; margin-bottom:20px;">
                        <h4>🎯 Recommended Resource</h4>
                        <a href="{main_resource}" target="_blank" style="color:#2e7d32; font-weight:bold;">
                            Best {prep_type} Guide for {country} → 
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                
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

                # Trending Interview Questions
                st.subheader("🔥 Trending Interview Questions")
                trending_questions = {
                    "Data Analyst": [
                        "Explain the difference between supervised and unsupervised learning.",
                        "How do you handle missing data in a dataset?",
                        "Describe a time you used data visualization to influence a decision."
                    ],
                    "Software Engineer": [
                        "Reverse a linked list in-place.",
                        "Design a REST API for a booking system.",
                        "How do you optimize a slow-performing application?"
                    ],
                    "Product Manager": [
                        "How would you prioritize features for a new app?",
                        "Describe a failed project and what you learned.",
                        "Walk us through your process for launching a product."
                    ]
                }
                role_key = role if role in trending_questions else "Data Analyst"
                for q in trending_questions[role_key]:
                    st.markdown(f"- {q}")

                # Personalized Checklist
                checklist_items = {
                    "Technical Questions": ["Review core concepts", "Practice 5 coding problems", "Study system design"],
                    "Behavioral Questions": ["Prepare 3 STAR stories", "Research company values", "Practice timing"],
                    "Case Studies": ["Practice problem-solving", "Review case frameworks", "Mock interviews"],
                    "Salary Negotiation": ["Research market salary", "Prepare counter-offers", "Practice negotiation"],
                    "Resume Tips": ["Update skills section", "Tailor to job", "Proofread"]
                }.get(prep_type, [])
                st.subheader("✅ Personalized Checklist")
                for item in checklist_items:
                    st.checkbox(item, key=f"check_{item}")

                # Downloadable Interview Prep Roadmap
                roadmap_content = f"Interview Prep Roadmap for {role} ({exp_level})\n\n"
                roadmap_content += f"Target Company: {company or 'Any'}\nCountry: {country}\nPreparation Type: {prep_type}\n\n"
                roadmap_content += "Checklist:\n" + "\n".join([f"- [ ] {item}" for item in checklist_items])
                roadmap_content += f"\n\nRecommended Resource: {main_resource}\n"
                roadmap_content += f"Trending Questions:\n" + "\n".join([f"- {q}" for q in trending_questions[role_key]])
                st.download_button(
                    label="📥 Download Prep Roadmap",
                    data=roadmap_content,
                    file_name=f"{role}_Interview_Roadmap.txt",
                    mime="text/plain"
                )

        # AI-Powered Mock Interview Simulator
        st.subheader("🤖 AI Mock Interview Simulator")
        with st.form("mock_interview_form"):
            mock_role = st.text_input("Enter Role for Mock Interview", role, key="mock_role")
            mock_question_type = st.selectbox("Question Type", ["Technical", "Behavioral"], key="mock_question_type")
            mock_submit = st.form_submit_button("Generate Mock Question")
        
        if mock_submit:
            st.session_state.interview_practice_count += 1
            mock_prompt = f"""
            Act as an experienced interviewer. Generate one {mock_question_type.lower()} interview question for a {mock_role} role at {exp_level} level.
            Ensure the question is realistic, specific, and relevant to 2025 job trends.
            Return only the question as a single sentence.
            """
            mock_question = get_result(mock_prompt)
            st.markdown(f"**Question**: {mock_question}")
            
            with st.form("mock_answer_form"):
                user_answer = st.text_area("Your Answer", height=150, key="mock_answer")
                feedback_submit = st.form_submit_button("Get AI Feedback")
            
            if feedback_submit and user_answer.strip():
                feedback_prompt = f"""
                Act as a career coach with 15 years of experience. Review the user's answer to the following {mock_question_type.lower()} interview question for a {mock_role} role: "{mock_question}".
                User Answer: "{user_answer}"
                Provide concise feedback focusing on:
                1. Clarity and structure
                2. Relevance to the question
                3. Suggestions for improvement
                Return the feedback in a bullet-point format.
                """
                feedback = get_result(feedback_prompt)
                st.markdown("**AI Feedback**")
                st.markdown(feedback)

        # Interactive STAR Method Guide
        st.subheader("🌟 Craft STAR Stories")
        with st.form("star_form"):
            situation = st.text_area("Situation (Describe the context)", height=100)
            task = st.text_area("Task (What was your responsibility?)", height=100)
            action = st.text_area("Action (What did you do?)", height=100)
            result = st.text_area("Result (What was the outcome?)", height=100)
            star_submit = st.form_submit_button("Save STAR Story")
        
        if star_submit and all([situation.strip(), task.strip(), action.strip(), result.strip()]):
            st.session_state.star_stories.append({
                "Situation": situation,
                "Task": task,
                "Action": action,
                "Result": result
            })
            st.success("STAR Story saved!")
            
            # Display saved STAR stories
            if st.session_state.star_stories:
                st.markdown("**Your STAR Stories**")
                for i, story in enumerate(st.session_state.star_stories, 1):
                    st.markdown(f"**Story {i}**")
                    st.markdown(f"- **Situation**: {story['Situation']}")
                    st.markdown(f"- **Task**: {story['Task']}")
                    st.markdown(f"- **Action**: {story['Action']}")
                    st.markdown(f"- **Result**: {story['Result']}")
                    # AI Feedback on STAR Story
                    if st.button("Get AI Feedback", key=f"star_feedback_{i}"):
                        star_feedback_prompt = f"""
                        Act as a career coach. Review the following STAR story for a {mock_role} interview:
                        Situation: {story['Situation']}
                        Task: {story['Task']}
                        Action: {story['Action']}
                        Result: {story['Result']}
                        Provide feedback on structure, impact, and suggestions for improvement in bullet points.
                        """
                        star_feedback = get_result(star_feedback_prompt)
                        st.markdown("**AI Feedback on STAR Story**")
                        st.markdown(star_feedback)

    # Resume Analysis (Enhanced with Interview Question Suggestions)
    with resume_tab:
        st.subheader(t["resume_analysis"])
        with st.form("resume_form"):
            col1, col2 = st.columns([1, 1])
            with col1:
                job_description = st.text_area("Enter the Job Description", height=200, key="resume_job_desc")
            with col2:
                uploaded_file = st.file_uploader(t["upload_resume"], type=['pdf'], key="resume_upload")
            
            analyze_submitted = st.form_submit_button(t["analyze_resume"])

        if analyze_submitted:
            if not job_description:
                st.error("Please enter a job description.")
            elif not uploaded_file:
                st.error("Please upload your resume.")
            else:
                try:
                    # Extract resume text
                    resume_text = pdf_to_text(uploaded_file)
                    
                    # Get match score
                    score_prompt = construct_score_prompt(resume_text, job_description)
                    score_result = get_result(score_prompt)
                    st.subheader("Resume Match Score")
                    st.markdown(score_result)
                    
                    # Get improvement suggestions
                    improvement_prompt = construct_improvement_prompt(resume_text, job_description)
                    improvement_result = get_result(improvement_prompt)
                    st.subheader("Suggestions to Improve Your Resume")
                    st.markdown(improvement_result)
                    
                    # Suggest interview questions based on resume analysis
                    question_prompt = f"""
                    Based on the resume and job description below, suggest 3 interview questions (1 technical, 1 behavioral, 1 role-specific) that the candidate should prepare for.
                    Resume: {resume_text}
                    Job Description: {job_description}
                    Return the questions in a bullet-point format.
                    """
                    suggested_questions = get_result(question_prompt)
                    st.subheader("Recommended Interview Questions to Prepare")
                    st.markdown(suggested_questions)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    # Updated promotional content
    st.markdown("""
    <div style='background-color:#fffde7; border:2px solid #fdd835; border-radius:10px; padding:20px; margin-top:30px;'>
        <h3 style='color:#f57f17;'>\U0001F680 Ace Your 2025 Interviews with AI</h3>
        <p style='font-size:16px; color:#555;'>🔸 Rejections hurt, but <b>smart AI prep</b> can make you unstoppable.<br>🔸 Don’t just memorize answers – master interviews with tools tailored for 2025.</p>
        <h4 style='color:#1b5e20;'>🎯 ₹499 AI Interview Kit – Your Secret Weapon:</h4>
        <ul style='font-size:15px; color:#333;'>
            <li>📄 200+ Real Interview Questions (Amazon, TCS, Microsoft, etc.)</li>
            <li>🎥 Role-Specific Video Playlists (Data Scientist, Developer, PM)</li>
            <li>🧠 AI Mock Interviews + STAR Story Builder</li>
            <li>🚀 Auto-Generated Prep Roadmaps & Salary Negotiation Scripts</li>
        </ul>
        <hr style='margin:15px 0;'>
        <h4 style='color:#1b5e20;'>💬 Real Success Story:</h4>
        <p style='font-size:15px; color:#333; font-style:italic;'>"After 7 rejections, I used the ₹499 AI Kit to prep for a Google interview. Landed a ₹35L offer in Feb 2025!"<br>– <b>Ankit Sharma, Software Engineer, Delhi</b></p>
        <p style='font-size:16px; color:#000; font-weight:bold;'>🎁 Don’t let interviews intimidate you. <span style='color:#d32f2f;'>Crush them with AI!</span></p>
        <a href='https://pages.razorpay.com/pl_Q9haRTHXpyB9SS/view' target='_blank' style='display:inline-block; padding:10px 20px; background:#1976d2; color:#fff; font-weight:bold; border-radius:6px; text-decoration:none; font-size:16px;'>🎯 Buy ₹499 Interview Kit</a>
    </div>
    """, unsafe_allow_html=True)
# ----------------- TAB 3: FREE COURSES -----------------
with tab3:
    st.header(f"🎓 {t['free_courses']}")

    # Expanded mapping of keywords to course categories for 2025 trends
    COURSE_CATEGORY_MAP = {
        "ai": "Artificial Intelligence",
        "machine learning": "Machine Learning",
        "data science": "Data Science",
        "python": "Programming",
        "sql": "Data Analysis",
        "business": "Business",
        "marketing": "Marketing",
        "design": "Design",
        "web development": "Web Development",
        "cloud": "Cloud Computing",
        "cybersecurity": "Cybersecurity",
        "blockchain": "Blockchain",
        "finance": "Finance",
        "accounting": "Accounting",
        "project management": "Project Management",
        "generative ai": "Generative AI",
        "quantum computing": "Quantum Computing",
        "data engineering": "Data Engineering",
        "devops": "DevOps",
        "ui/ux": "UI/UX Design"
    }

    # Expanded curated courses with new categories and badges
    CURATED_COURSES = {
        "Artificial Intelligence": [
            ("AI For Everyone (Coursera) 🏆 Top Rated", "https://www.coursera.org/learn/ai-for-everyone"),
            ("Intro to AI (edX)", "https://www.edx.org/learn/artificial-intelligence"),
            ("AI Basics (Google) ✨ New", "https://www.cloudskillsboost.google/quests/238")
        ],
        "Machine Learning": [
            ("Machine Learning Crash Course (Google)", "https://developers.google.com/machine-learning/crash-course"),
            ("Intro to ML (Kaggle)", "https://www.kaggle.com/learn/intro-to-machine-learning"),
            ("ML Foundations (Coursera)", "https://www.coursera.org/learn/machine-learning")
        ],
        "Data Science": [
            ("Data Science for Beginners (Microsoft)", "https://learn.microsoft.com/en-us/training/paths/data-science/"),
            ("Intro to Data Science (edX)", "https://www.edx.org/learn/data-science"),
            ("Data Science Basics (Coursera)", "https://www.coursera.org/learn/data-science-basics")
        ],
        "Programming": [
            ("Python for Everybody (Coursera) 🏆 Top Rated", "https://www.coursera.org/specializations/python"),
            ("Learn to Code (Codecademy)", "https://www.codecademy.com/learn/learn-python-3"),
            ("CS50 Intro to Programming (Harvard)", "https://pll.harvard.edu/course/cs50-introduction-computer-science")
        ],
        "Generative AI": [
            ("Generative AI Basics (Google) ✨ New", "https://www.cloudskillsboost.google/quests/281"),
            ("Intro to GenAI (Coursera)", "https://www.coursera.org/learn/generative-ai-for-everyone"),
            ("Hugging Face Transformers (DeepLearning.AI)", "https://www.deeplearning.ai/short-courses/hugging-face-transformers/")
        ],
        "Cybersecurity": [
            ("Cybersecurity Fundamentals (IBM)", "https://www.coursera.org/learn/cybersecurity-fundamentals"),
            ("Intro to Cybersecurity (Cisco)", "https://www.netacad.com/courses/cybersecurity/introduction-cybersecurity"),
            ("Google Cybersecurity Certificate", "https://www.coursera.org/professional-certificates/google-cybersecurity")
        ]
    }

    # Initialize session state for progress tracking and learning streak
    if 'course_progress' not in st.session_state:
        st.session_state.course_progress = {}
    if 'learning_streak' not in st.session_state:
        st.session_state.learning_streak = 0
    if 'last_search_date' not in st.session_state:
        st.session_state.last_search_date = None

    # Update learning streak
    from datetime import datetime, date
    today = date.today()
    if st.session_state.last_search_date != today:
        st.session_state.learning_streak += 1
        st.session_state.last_search_date = today
    st.markdown(f"🔥 **Learning Streak**: {st.session_state.learning_streak} days")

    # Popular Skills buttons for quick access
    st.subheader("🔥 Explore Popular Skills")
    popular_skills = ["Artificial Intelligence", "Programming", "Data Science", "Cybersecurity", "Generative AI"]
    cols = st.columns(len(popular_skills))
    for i, skill in enumerate(popular_skills):
        with cols[i]:
            if st.button(skill):
                search = skill
                course_submit = True
            else:
                course_submit = False

    # Updated search form with skill level filter
    with st.form("course_form"):
        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input(t["search_course"], "AI for Business")
        with col2:
            skill_level = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced"])
        course_submit = st.form_submit_button(f"🎯 {t['find_courses']}")

    if course_submit:
        if not search.strip():
            st.error("Please enter a course, skill, or job title.")
        else:
            # Normalize search term and map to category
            search_lower = search.lower().strip()
            category = None
            for keyword, mapped_category in COURSE_CATEGORY_MAP.items():
                if keyword in search_lower:
                    category = mapped_category
                    break
            if not category:
                category = search  # Fallback to original search term
                st.warning(f"No exact match found for '{search}'. Showing results for '{category}'.")

            query = urllib.parse.quote_plus(category)
            st.info(f"🔍 Searching for courses related to: **{category}** (Level: {skill_level})")

            # Course search results in expanders
            with st.expander("🎓 Free Courses", expanded=True):
                free_courses = [
                    ("Coursera Free", f"https://www.coursera.org/search?query={query}&sortBy=RELEVANCE&price=FREE&level={skill_level.lower()}"),
                    ("edX Free Courses", f"https://www.edx.org/search?q={query}&cost=Free&sort=relevance&level={skill_level.lower()}"),
                    ("Harvard Online", f"https://pll.harvard.edu/catalog?keywords={query}&f%5B0%5D=course_feature_free%3A1"),
                    ("YouTube Tutorials", f"https://www.youtube.com/results?search_query=free+{query}+course+for+{skill_level.lower()}")
                ]
                # Add region-specific platforms based on language
                if lang == "Hindi" or lang == "Tamil" or lang == "Telugu" or lang == "Malayalam":
                    free_courses.append(("SWAYAM (India)", f"https://swayam.gov.in/explorer?searchText={query}"))
                if lang == "French":
                    free_courses.append(("FUN-MOOC (France)", f"https://www.fun-mooc.fr/en/courses/?q={query}"))
                for name, url in free_courses:
                    st.markdown(f"<a href='{url}' target='_blank' style='display:block; background:#6366f1; color:white; padding:10px; border-radius:5px; margin-bottom:5px;'>📘 {name}</a>", unsafe_allow_html=True)

            with st.expander("📜 Free Courses with Certification"):
                certified_courses = [
                    ("Google Career Certificates", f"https://grow.google/certificates/?q={query}"),
                    ("IBM SkillsBuild", f"https://skillsbuild.org/learn?search={query}"),
                    ("Meta Blueprint", f"https://www.facebook.com/business/learn/courses?search={query}"),
                    ("AWS Skill Builder", f"https://explore.skillbuilder.aws/learn?searchTerm={query}"),
                    ("Google Cloud Skills Boost", f"https://www.cloudskillsboost.google/catalog?search={query}")
                ]
                for name, url in certified_courses:
                    st.markdown(f"<a href='{url}' target='_blank' style='display:block; background:#10b981; color:white; padding:10px; border-radius:5px; margin-bottom:5px;'>📜 {name}</a>", unsafe_allow_html=True)

            with st.expander("🛠️ Free Platforms for Hands-on Experience"):
                platforms = [
                    ("GitHub Learning Lab", "https://lab.github.com/"),
                    ("Microsoft Learn", f"https://learn.microsoft.com/en-us/training/browse/?terms={query}"),
                    ("Kaggle Courses", f"https://www.kaggle.com/learn/search?q={query}"),
                    ("Codecademy Free", f"https://www.codecademy.com/catalog/all?query={query}&level=free"),
                    ("DataCamp Free", f"https://www.datacamp.com/search?q={query}")
                ]
                for name, url in platforms:
                    st.markdown(f"<a href='{url}' target='_blank' style='display:block; background:#f97316; color:white; padding:10px; border-radius:5px; margin-bottom:5px;'>🛠️ {name}</a>", unsafe_allow_html=True)

            # Curated recommendations with progress tracking
            if category in CURATED_COURSES:
                with st.expander("✨ Curated Recommendations", expanded=True):
                    for name, url in CURATED_COURSES[category]:
                        course_key = f"{category}_{name}"
                        progress = st.session_state.course_progress.get(course_key, "Not Started")
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"<a href='{url}' target='_blank' style='display:block; background:#ff6f61; color:white; padding:10px; border-radius:5px; margin-bottom:5px;'>📚 {name}</a>", unsafe_allow_html=True)
                        with col2:
                            new_progress = st.selectbox("Progress", ["Not Started", "In Progress", "Completed"], index=["Not Started", "In Progress", "Completed"].index(progress), key=course_key)
                            st.session_state.course_progress[course_key] = new_progress

            # Downloadable Learning Plan
            if category in CURATED_COURSES:
                learning_plan = "\n".join([f"- [ ] {name} ({url}) - Status: {st.session_state.course_progress.get(f'{category}_{name}', 'Not Started')}" for name, url in CURATED_COURSES[category]])
                st.download_button(
                    label="📥 Download Learning Plan",
                    data=f"Learning Plan for {category}\n\n{learning_plan}",
                    file_name=f"{category}_Learning_Plan.txt",
                    mime="text/plain"
                )

    # Recently Added Courses
    st.subheader("🆕 Recently Added Courses")
    recent_courses = [
        ("Generative AI for Developers (AWS) ✨ New", "https://explore.skillbuilder.aws/learn/course/external/view/elearning/17476/generative-ai-for-developers"),
        ("Python for Data Analysis (Microsoft)", "https://learn.microsoft.com/en-us/training/paths/data-analysis-python/"),
        ("Cybersecurity Essentials (Cisco) 🏆 Top Rated", "https://www.netacad.com/courses/cybersecurity/cybersecurity-essentials")
    ]
    for name, url in recent_courses:
        st.markdown(f"<a href='{url}' target='_blank' style='display:block; background:#ffeb3b; color:black; padding:10px; border-radius:5px; margin-bottom:5px;'>📚 {name}</a>", unsafe_allow_html=True)

    # Updated promotional content
    st.markdown("""
    <div style='background-color:#e8f5e9; border:2px solid #43a047; border-radius:10px; padding:20px; margin-top:30px;'>
        <h3 style='color:#2e7d32;'>\U0001F393 Turn Free Learning into a High-Paying Career</h3>
        <p style='font-size:16px; color:#444;'>👏 You're mastering skills with free courses – now take the leap to <b>earn ₹50K–₹2L/month</b> with AI-powered freelancing or jobs.</p>
        <h4 style='color:#1b5e20;'>🔥 ₹499 AI Career Kit – Your Shortcut to Success:</h4>
        <ul style='font-size:15px; color:#333;'>
            <li>💼 15+ Freelance-Ready AI Projects (Chatbots, Data Pipelines, AI Apps)</li>
            <li>📊 Real-time Salary Data for 2025 (AI, DevOps, Cybersecurity)</li>
            <li>🧠 Personalized Learning & Career Roadmap</li>
            <li>🎯 Auto-generated Proposals + Job Application Tools</li>
        </ul>
        <hr style='margin:15px 0;'>
        <h4 style='color:#1b5e20;'>🗣️ Success Story:</h4>
        <p style='font-size:15px; color:#333; font-style:italic;'>"I learned Python for free but struggled to get hired. The ₹499 AI Kit helped me build 3 freelance projects. Now I earn ₹1.8L/month on Upwork!"<br>– <b>Priya S., Data Engineer, Bangalore</b></p>
        <p style='font-size:16px; color:#000; font-weight:bold;'>🚀 Don’t just learn – start earning with AI.</p>
        <a href='https://pages.razorpay.com/pl_Q9haRTHXpyB9SS/view' target='_blank' style='display:inline-block; padding:10px 20px; background:#1976d2; color:#fff; font-weight:bold; border-radius:6px; text-decoration:none; font-size:16px;'>💼 Buy ₹499 AI Career Kit</a>
    </div>
    """, unsafe_allow_html=True)
# ----------------- TAB 4: FREELANCE & REMOTE JOBS (Updated with More Platforms) -----------------
with tab4:
    st.header(f"💼 Freelance & Remote Jobs")

    tab_a, tab_b, tab_c = st.tabs(["🔍 Search Jobs", "🚀 For Beginners", "💰 Pay Insights"])

    with tab_a:
        with st.form("freelance_form"):
            col1, col2 = st.columns(2)
            with col1:
                keyword = st.text_input("🛠️ Skill / Job Title", "Python Developer")
                job_type = st.selectbox("💼 Job Type", ["Freelance", "Remote", "Hybrid", "AI Gigs", "Micro-Tasks"])
            with col2:
                region = st.selectbox("🌍 Region", ["Global", "USA", "UK", "India", "EU", "Latin America", "Asia-Pacific"])
                subregion = None
                if region == "UK":
                    subregion = st.selectbox("🏴 UK Region", ["All UK", "England", "Scotland", "Wales", "Northern Ireland"])
                experience = st.selectbox("📈 Experience Level", ["Any", "Entry", "Mid", "Senior"])
            submit = st.form_submit_button("🔎 Find Jobs")

        if submit:
            if not keyword.strip():
                st.error("Please enter a skill or job title.")
            else:
                q = urllib.parse.quote_plus(keyword)
                st.subheader("🚀 Job Boards with Smart Links")

                platforms = []
                exp_filter = {
                    "Any": "",
                    "Entry": "&experience=entry",
                    "Mid": "&experience=mid",
                    "Senior": "&experience=senior"
                }.get(experience, "")

                # Region filter logic
                if region == "Global":
                    region_filter = ""
                elif region == "UK" and subregion and subregion != "All UK":
                    region_filter = f"&location={urllib.parse.quote(subregion)}"
                else:
                    region_filter = f"&location={urllib.parse.quote(region)}"

                # Job type specific platforms
                if job_type == "Freelance":
                    platforms += [
                        ("Upwork", f"https://www.upwork.com/nx/search/jobs/?q={q}{region_filter}{exp_filter}"),
                        ("Freelancer", f"https://www.freelancer.com/jobs/{q.replace('+', '-')}/"),
                        ("Toptal", f"https://www.toptal.com/talent/apply?skill={q}"),
                        ("Guru", f"https://www.guru.com/d/jobs/q/{q}/"),
                        ("PeoplePerHour", f"https://www.peopleperhour.com/freelance-jobs?keywords={q}")
                    ]
                elif job_type == "Remote":
                    platforms += [
                        ("We Work Remotely", f"https://weworkremotely.com/remote-jobs/search?term={q}"),
                        ("Remote OK", f"https://remoteok.com/remote-jobs?search={q}"),
                        ("FlexJobs", f"https://www.flexjobs.com/search?search={q}&location={region}"),
                        ("JustRemote", f"https://justremote.co/remote-jobs?search={q}"),
                        ("Remote.co", f"https://remote.co/remote-jobs/search/?search={q}")
                    ]
                elif job_type == "Hybrid":
                    platforms += [
                        ("LinkedIn", f"https://www.linkedin.com/jobs/search?keywords={q}{region_filter}&f_WT=1"),
                        ("Indeed", f"https://www.indeed.com/jobs?q={q}&l={region}&wt=hybrid"),
                        ("Monster", f"https://www.monster.com/jobs/search?q={q}&where={region}&wt=hybrid"),
                        ("Glassdoor", f"https://www.glassdoor.com/Job/{q.replace('+', '-')}-jobs-SRCH_KO0,20.htm?workType=hybrid"),
                        ("ZipRecruiter", f"https://www.ziprecruiter.com/jobs-search?search={q}&location={region}&workType=hybrid")
                    ]
                elif job_type == "AI Gigs":
                    platforms += [
                        ("OpenAI Jobs", f"https://openai.com/careers/search?query={q}"),
                        ("Anthropic Jobs", f"https://www.anthropic.com/careers"),
                        ("PromptBase", f"https://promptbase.com/marketplace?query={q}"),
                        ("AI-Jobs.net", f"https://ai-jobs.net/?search={q}{region_filter}"),
                        ("Hugging Face Jobs", f"https://huggingface.co/careers#open-positions")
                    ]
                elif job_type == "Micro-Tasks":
                    platforms += [
                        ("Amazon Mechanical Turk", f"https://www.mturk.com/worker"),
                        ("Clickworker", f"https://www.clickworker.com/clickworker-job-offers/?query={q}"),
                        ("Appen", f"https://connect.appen.com/qrp/public/jobs?keywords={q}"),
                        ("Microworkers", f"https://www.microworkers.com/jobs?search={q}"),
                        ("Fiverr", f"https://www.fiverr.com/search/gigs?query={q}")
                    ]

                # General platforms for all job types
                platforms += [
                    ("LinkedIn", f"https://www.linkedin.com/jobs/search?keywords={q}{region_filter}{exp_filter}"),
                    ("Indeed", f"https://www.indeed.com/jobs?q={q}&l={region}"),
                    ("Google Jobs", f"https://www.google.com/search?q={q}+{job_type}+jobs+{region}")
                ]

                for name, url in platforms:
                    st.markdown(
                        f'<a href="{url}" target="_blank" style="display:inline-block; padding:10px 20px; background:#4CAF50; color:white; border-radius:5px; text-decoration:none; margin-bottom:5px;">'
                        f'Search on {name}</a>',
                        unsafe_allow_html=True
                    )

    with tab_b:
        st.subheader("🚀 Getting Started with Freelancing")
        st.markdown("""
        **New to freelancing? Follow these steps to land your first gig:**
        1. **Build a Profile**: Create a strong profile on platforms like Upwork or Fiverr. Highlight skills and include a portfolio.
        2. **Start Small**: Apply for micro-tasks or small projects to build reviews and credibility.
        3. **Learn to Pitch**: Write clear, tailored proposals. Mention how you’ll solve the client’s problem.
        4. **Upskill**: Take free courses (check Tab 3) to boost your skills in high-demand areas like AI or web development.
        5. **Network**: Join communities on LinkedIn or Discord to connect with clients and other freelancers.
        """)
        st.markdown("""
        **Recommended Platforms for Beginners:**
        - [Fiverr](https://www.fiverr.com) – Start with small gigs.
        - [Upwork](https://www.upwork.com) – Entry-level projects.
        - [Clickworker](https://www.clickworker.com) – Micro-tasks for quick cash.
        - [PeoplePerHour](https://www.peopleperhour.com) – Simple freelance jobs.
        """)

    with tab_c:
        st.subheader("💰 Freelance Pay Insights")
        st.markdown("""
        **Average Hourly Rates (2025, USD):**
        - **Python Developer**: $30–$80 (Entry), $80–$150 (Senior)
        - **AI/ML Engineer**: $50–$120 (Entry), $120–$250 (Senior)
        - **Web Developer**: $25–$60 (Entry), $60–$120 (Senior)
        - **Graphic Designer**: $20–$50 (Entry), $50–$100 (Senior)
        - **Content Writer**: $15–$40 (Entry), $40–$90 (Senior)
        - **Micro-Tasks**: $5–$20/hour (varies by task complexity)
        
        **Tips to Maximize Earnings:**
        - Specialize in high-demand skills (e.g., AI, cloud computing).
        - Work with global clients in regions like the USA or EU for higher pay.
        - Upskill regularly to stay competitive.
        - Use platforms like Payoneer for seamless international payments.
        """)
        st.markdown("""
        **Resources for Pay Research:**
        - [Glassdoor](https://www.glassdoor.com/Salaries/index.htm)
        - [Payscale](https://www.payscale.com/research/US/Job=Freelancer/Salary)
        - [Upwork Market Trends](https://www.upwork.com/research)
        """)
        st.markdown("""
    <div style='background-color:#fff8e1; border:2px solid #f9a825; border-radius:10px; padding:20px; margin-top:30px;'>
        <h3 style='color:#ef6c00;'>\U0001F680 Can't Find the Right Job? Create Your Own Opportunities</h3>
        <p style='font-size:16px; color:#444;'>Whether you're job hunting, switching careers, or stuck in endless applications, here's a fact: <b>AI freelancers are earning ₹50K – ₹1.5L/month by building tools from home.</b></p>
        <h4 style='color:#bf360c;'>🎁 Introducing the ₹499 AI Career Kit (90% Off)</h4>
        <ul style='font-size:15px; color:#333;'>
            <li>✅ 10+ Freelance-Ready AI Projects (Chatbot, Resume Parser, Fake News Detector, etc.)</li>
            <li>📈 Tools to automate your job search, interview prep & applications</li>
            <li>🧾 AI-generated proposals & cover letters</li>
            <li>💸 Ideal for Upwork, Fiverr, LinkedIn & Internshala freelancing</li>
        </ul>
        <hr style='margin:15px 0;'>
        <p style='font-size:15px; color:#333; font-style:italic;'>"After applying for 70+ jobs with no response, I switched to freelancing with this kit. Now earning ₹1.2L/month working from home."<br>– <b>Sana Rahman, MBA, Hyderabad</b></p>
        <p style='font-size:16px; color:#000; font-weight:bold;'>Don't wait for a job – start your AI freelancing journey today.</p>
        <a href='https://pages.razorpay.com/pl_Q9haRTHXpyB9SS/view' target='_blank' style='display:inline-block; padding:10px 20px; background:#1976d2; color:#fff; font-weight:bold; border-radius:6px; text-decoration:none; font-size:16px;'>💼 Get the ₹499 AI Career Kit</a>
    </div>
    """, unsafe_allow_html=True)

    # ----------------- TAB 5: international_jobs
with tab5:
    st.header(f"🌍 {t.get('international_jobs', 'International Job Opportunities')}")
    
    # Initialize session state for visa application progress
    if 'visa_progress' not in st.session_state:
        st.session_state.visa_progress = {}
    if 'visa_milestones' not in st.session_state:
        st.session_state.visa_milestones = []

    # Enhanced Progress Tracker
    st.subheader("📊 Your Visa Journey Progress")
    col_prog1, col_prog2 = st.columns([3,1])
    with col_prog1:
        progress = min(len(st.session_state.visa_milestones) / 5, 1.0)
        st.progress(progress)
    with col_prog2:
        if st.button("Reset Progress", key="reset_progress"):
            st.session_state.visa_milestones = []
            st.rerun()
    
    # Visual Milestone Path
    milestones = [
        ("🔍 Research", "Country selection"),
        ("📝 Preparation", "Docs & tests"),
        ("💼 Job Offer", "Employer secured"),
        ("🖋️ Application", "Visa submitted"),
        ("✅ Approval", "Ready to move")
    ]
    
    cols = st.columns(5)
    for idx, (icon, text) in enumerate(milestones):
        with cols[idx]:
            st.markdown(f"""
            <div style='text-align:center; padding:10px; 
            background-color:{"#e3f2fd" if idx < len(st.session_state.visa_milestones) else "#f5f5f5"};
            border-radius:10px;'>
                <div style='font-size:24px;'>{icon}</div>
                <div>{text}</div>
                {"✓" if idx < len(st.session_state.visa_milestones) else ""}
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced Eligibility Checker
    with st.expander("🔍 Advanced Visa Eligibility Checker", expanded=True):
        with st.form("enhanced_eligibility"):
            country = st.selectbox("Target Country", 
                                 ["Canada", "Australia", "Germany", "UK", "New Zealand", "UAE"],
                                 key="enhanced_country")
            
            col1, col2 = st.columns(2)
            with col1:
                profession = st.text_input("Your Profession", "Software Developer")
                education = st.selectbox("Education Level", 
                                      ["High School", "Bachelor's", "Master's", "PhD"])
            with col2:
                experience = st.select_slider("Years of Experience", 
                                            options=["0-1", "1-3", "3-5", "5-10", "10+"])
                language = st.multiselect("Language Tests", 
                                        ["IELTS", "TOEFL", "TEF", "Goethe-Zertifikat"])
            
            if st.form_submit_button("Check Eligibility Score"):
                # Calculate score logic here
                score = min(100, 20 + (len(language)*15) + (10 if education != "High School" else 0))
                st.metric("Your Eligibility Score", f"{score}% match")
                
                # Visual score indicator
                st.markdown(f"""
                <style>
                    .score-bar {{
                        height: 20px;
                        background: linear-gradient(90deg, #4CAF50 {score}%, #f5f5f5 {score}%);
                        border-radius: 10px;
                        margin: 10px 0;
                    }}
                </style>
                <div class="score-bar"></div>
                """, unsafe_allow_html=True)

    # Overview
    st.subheader("🌐 Global Opportunities for Skilled Workers")
    st.markdown("""
    Countries like **Canada**, **Australia**, and **Germany** are actively seeking skilled professionals in 2025 to fill labor shortages in tech, healthcare, engineering, and trades. Streamlined visa programs make it easier for qualified workers to secure jobs and permanent residency. Follow these steps to get started:
    1. **Secure a Job Offer**: Find a role matching your skills on official job portals.
    2. **Apply for a Visa**: Use employer-sponsored or points-based visa programs.
    3. **Meet Eligibility**: Ensure qualifications, experience, and language skills align with requirements.
    """)

    # Country-Specific Guides
    st.subheader("📌 Country-Specific Opportunities")
    with st.expander("🇨🇦 Canada", expanded=True):
        st.markdown("""
        **Job Opportunities**: High demand for tech (e.g., Software Developers, NOC 21232), healthcare (e.g., Nurses, NOC 31301), and trades (e.g., Electricians, NOC 72200). Average salary: CAD 50,000-60,000.
        **Visa Programs**:
        - **Express Entry (Federal Skilled Worker Program)**: Points-based system (67/100 needed) for permanent residency. Requires 1 year of skilled work experience, CLB 7 language skills, and education credentials.
        - **Provincial Nominee Programs (PNPs)**: Province-specific pathways, adding 600 CRS points.
        - **Canadian Experience Class (CEC)**: For those with 1 year of Canadian work experience.
        **Eligibility**: Age, education, work experience, language (IELTS/TOEFL). No job offer required for FSWP.
        **Process**: Submit Expression of Interest (EOI), receive Invitation to Apply (ITA), apply within 6 months.
        **Tips**:
        - Get credentials assessed (e.g., WES).
        - Explore Job Bank (jobbank.gc.ca) for opportunities.
        - Take IELTS for English or TEF for French.
        **Resources**:
        - [Canada Job Bank](https://www.jobbank.gc.ca)
        - [Express Entry](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry.html)
        """)
        st.download_button(
            label="📥 Canada Visa Checklist",
            data="Canada Visa Application Checklist\n- Credential assessment (WES)\n- Language test (IELTS/TOEFL)\n- Job offer (optional)\n- EOI submission\n- ITA and permanent residency application",
            file_name="Canada_Visa_Checklist.txt",
            mime="text/plain"
        )

    with st.expander("🇦🇺 Australia"):
        st.markdown("""
        **Job Opportunities**: Demand in healthcare (e.g., Nurses, ANZSCO 2544), IT (e.g., Software Engineers, ANZSCO 2613), and engineering (e.g., Civil Engineers, ANZSCO 2332). Unemployment: 3.5%.
        **Visa Programs**:
        - **Skilled Independent Visa (Subclass 189)**: Points-based, no employer needed.
        - **Employer-Sponsored Visa (Subclass 482)**: Requires job offer.
        - **Global Talent Visa**: For exceptional professionals.
        - **Working Holiday Visa (Subclass 417)**: For ages 18-35, temporary work.
        **Eligibility**: Skills on Skilled Occupation List (SOL), 2-5 years experience, English (IELTS 6+).
        **Process**: Submit EOI via SkillSelect, receive ITA, apply for visa. Core Skills Occupation List launches May 2025.
        **Tips**:
        - Check ANZSCO codes for your role.
        - Get skills assessed (e.g., VETASSESS).
        - Use SEEK (seek.com.au) for job search.
        **Resources**:
        - [SEEK Australia](https://www.seek.com.au)
        - [Home Affairs](https://immi.homeaffairs.gov.au)
        """)
        st.download_button(
            label="📥 Australia Visa Checklist",
            data="Australia Visa Application Checklist\n- Skills assessment (VETASSESS)\n- English test (IELTS)\n- Job offer (for Subclass 482)\n- EOI via SkillSelect\n- ITA and visa application",
            file_name="Australia_Visa_Checklist.txt",
            mime="text/plain"
        )

    with st.expander("🇩🇪 Germany"):
        st.markdown("""
        **Job Opportunities**: Shortages in IT, healthcare (e.g., Doctors, Nurses), and engineering. 19,000+ visa-sponsored jobs. Salaries: €45,000-€80,000.
        **Visa Programs**:
        - **EU Blue Card**: For jobs paying €48,300/year (€43,992 for bottleneck professions like IT, healthcare).
        - **Skilled Worker Visa**: Requires recognized degree or 2+ year vocational training, job offer.
        - **Opportunity Card (Chancenkarte)**: 12-month job search visa, requires A1 German or B2 English.
        **Eligibility**: Recognized qualifications, job offer (except Opportunity Card). Age 45+ needs €53,130/year or pension proof.
        **Process**: Apply at German embassy (visa-free entry for Canada, Australia, etc.), then residence permit. Federal Employment Agency approval needed.
        **Tips**:
        - Get qualifications recognized (e.g., ZAB).
        - Use Make It in Germany portal for jobs.
        - Learn basic German (A1/A2) for better integration.
        **Resources**:
        - [Make It in Germany](https://www.make-it-in-germany.com)
        - [Federal Foreign Office](https://www.auswaertiges-amt.de)
        """)
        st.download_button(
            label="📥 Germany Visa Checklist",
            data="Germany Visa Application Checklist\n- Qualification recognition (ZAB)\n- Language test (Goethe-Institut, IELTS)\n- Job offer (except Opportunity Card)\n- Visa application at embassy\n- Residence permit in Germany",
            file_name="Germany_Visa_Checklist.txt",
            mime="text/plain"
        )

    # Other Countries
    with st.expander("🌎 Other Countries with Skill Shortages"):
        st.markdown("""
        Explore opportunities in countries like **New Zealand**, **Ireland**, and **Singapore**, which offer visa programs for skilled workers:
        - **New Zealand**: Skilled Migrant Category Visa. Check [workingin.nz](https://www.workingin.nz).
        - **Ireland**: Critical Skills Employment Permit. Visit [enterprise.gov.ie](https://www.enterprise.gov.ie).
        - **Singapore**: Employment Pass. Explore [mom.gov.sg](https://www.mom.gov.sg).
        """)

    # AI-Powered Visa Guidance
    st.subheader("🤖 Ask AI for Visa Guidance")
    with st.form("visa_guidance_form"):
        visa_query = st.text_area("Ask a Visa Question (e.g., 'What visa for a nurse in Canada?')", height=100)
        visa_query_submit = st.form_submit_button("Get AI Advice")
    if visa_query_submit and visa_query.strip():
        visa_prompt = f"Act as an immigration expert. Provide a concise, accurate answer to the following visa-related question: {visa_query}"
        visa_answer = get_result(visa_prompt)
        st.markdown(f"**AI Answer**: {visa_answer}")

    # Visa Application Milestones
    st.subheader("✅ Track Your Visa Application")
    with st.form("visa_milestone_form"):
        milestone = st.selectbox("Add Milestone", [
            "Job Offer Secured",
            "Credentials Assessed",
            "Language Test Passed",
            "Visa Application Submitted",
            "Residence Permit Received"
        ])
        milestone_submit = st.form_submit_button("Add Milestone")
    if milestone_submit:
        if milestone not in st.session_state.visa_milestones:
            st.session_state.visa_milestones.append(milestone)
            st.success(f"Milestone '{milestone}' added!")
        st.markdown("**Your Milestones**")
        for m in st.session_state.visa_milestones:
            st.markdown(f"- {m}")

    # Recent Updates
    st.subheader("🆕 2025 Visa and Job Updates")
    st.markdown("""
    - **Australia**: Core Skills Occupation List launches May 2025, prioritizing tech and cybersecurity roles.
    - **Germany**: Opportunity Card allows 12-month job search without a job offer, ideal for Indian professionals.
    - **Canada**: Express Entry draws continue, with 825 PNP invitations in April 2025.[](https://immigration.ca/who-qualifies-for-canadian-permanent-residence-skilled-worker-immigration/)
    """)

    # Promotional Content
    st.markdown("""
    <div style='background-color:#e3f2fd; border:2px solid #1976d2; border-radius:10px; padding:20px; margin-top:30px;'>
        <h3 style='color:#0d47a1;'>\U0001F30D Launch Your Global Career with AI</h3>
        <p style='font-size:16px; color:#444;'>🌟 Ready to work abroad? <b>AI tools</b> can help you navigate visas and land high-paying jobs in Canada, Australia, or Germany.</p>
        <h4 style='color:#1565c0;'>🎯 ₹499 Global Career Kit – Your Passport to Success:</h4>
        <ul style='font-size:15px; color:#333;'>
            <li>📋 Visa Application Checklists for 10+ Countries</li>
            <li>💼 50+ Job Search Templates (Cover Letters, LinkedIn Outreach)</li>
            <li>🧠 AI-Powered Visa Eligibility Assessments</li>
            <li>🚀 In-Demand Skills Guide for 2025 (Tech, Healthcare, Engineering)</li>
        </ul>
        <hr style='margin:15px 0;'>
        <h4 style='color:#1565c0;'>💬 Success Story:</h4>
        <p style='font-size:15px; color:#333; font-style:italic;'>"I used the ₹499 Global Career Kit to apply for Canada's Express Entry. Got my ITA in 3 months and now earn CAD 70,000 as a data analyst!"<br>– <b>Rahul V., Data Analyst, Toronto</b></p>
        <p style='font-size:16px; color:#000; font-weight:bold;'>🌍 Don't wait – start your global career today!</p>
        <a href='https://pages.razorpay.com/pl_Q9haRTHXpyB9SS/view' target='_blank' style='display:inline-block; padding:10px 20px; background:#1976d2; color:#fff; font-weight:bold; border-radius:6px; text-decoration:none; font-size:16px;'>🌟 Buy ₹499 Global Career Kit</a>
    </div>
    """, unsafe_allow_html=True)# ----------------- FOOTER -----------------
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
