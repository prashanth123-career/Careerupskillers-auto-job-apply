# 1. Import Streamlit first (required to avoid StreamlitAPIException)
import streamlit as st

# 2. Set page config as the FIRST Streamlit command (only one call allowed)
st.set_page_config(
    page_title="CareerUpskillers | AI Job Hub",
    page_icon="🌟",
    layout="centered"
)

# 3. Other imports
import urllib.parse
import google.generativeai as genai
from PyPDF2 import PdfReader
from datetime import datetime, date
from docx import Document
from fpdf import FPDF
from io import BytesIO
from docx.shared import Pt, RGBColor




# 4. Configure Gemini API using Streamlit secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except KeyError:
    st.error("GOOGLE_API_KEY not found in Streamlit secrets. Please configure it in Streamlit Cloud settings.")
    st.stop()

# ----------------- HELPER FUNCTIONS -----------------
def get_gemini_model():
    """Initialize and return the Gemini model."""
    model_name = 'gemini-1.5-flash'  # Updated model name
    try:
        return genai.GenerativeModel(model_name)
    except Exception as e:
        # If the model is not found, list available models
        st.error(f"Error: Could not load model {model_name}. Details: {str(e)}")
        try:
            models = genai.list_models()
            available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
            st.error(f"Available models: {', '.join(available_models)}")
            st.error("Please update the model name in the code to one of the available models and redeploy.")
        except Exception as list_error:
            st.error(f"Could not list available models: {str(list_error)}")
        st.stop()

def pdf_to_text(pdf_file):
    """Extract text from a PDF resume."""
    try:
        reader = PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += str(page.extract_text() or '')
        return text
    except Exception as e:
        st.error(f"Failed to process PDF: {str(e)}")
        return None

def construct_score_prompt(resume, job_description):
    """Construct prompt for resume match score."""
    return f'''
    Act as an HR Manager with 20 years of experience. Compare the resume with the job description.
    Provide a score from 0 to 10 based on:
    1. Key skills that match.
    2. Missing skills or qualifications.
    Return: "Score: X/10\nMatching Skills: ...\nMissing Skills: ..."
    
    Resume: {resume}
    Job Description: {job_description}
    '''

def construct_improvement_prompt(resume, job_description):
    """Construct prompt for resume improvement suggestions."""
    return f'''
    Act as a career coach with 15 years of experience. Analyze the resume and job description.
    Suggest specific changes to improve the resume to better match the job description.
    Focus on:
    1. Keywords to add.
    2. Skills to emphasize.
    3. Sections to rephrase.
    Return as a list of actionable suggestions.
    
    Resume: {resume}
    Job Description: {job_description}
    '''

def get_result(prompt):
    """Get response from Gemini model."""
    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: Could not process request with Gemini LLM. Details: {str(e)}"        
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
    
# Sub-tabs for Interview Prep, Resume Analysis, and ATS Builder
prep_tab, resume_tab, ats_tab = st.tabs(["Interview Prep Resources", t["resume_analysis"], "🎓 Professional ATS Resume Builder"])
    
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
from docx import Document
from docx.shared import Pt, RGBColor
from fpdf import FPDF
from io import BytesIO

with ats_tab:
    st.subheader("🧩 AI-Powered ATS Resume Builder")
    
    st.markdown("""
    <div style="background-color:#e3f2fd; padding:15px; border-radius:10px; margin-bottom:20px;">
        <b>Pro Tip:</b> Our AI analyzes your resume for ATS optimization, keyword matching, and recruiter appeal.
        Get real-time suggestions to improve your resume's effectiveness.
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state for resume analysis
    if 'resume_analysis' not in st.session_state:
        st.session_state.resume_analysis = None

    with st.form("resume_builder_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📝 Personal Information")
            full_name = st.text_input("Full Name*")
            email = st.text_input("Email*")
            phone = st.text_input("Phone")
            linkedin = st.text_input("LinkedIn URL")
            
            st.markdown("### 🎓 Education & Certifications")
            education = st.text_area("Education*", help="Include degree, institution, and year")
            certifications = st.text_area("Certifications", help="List relevant certifications")
            
        with col2:
            st.markdown("### 💼 Target Role")
            role = st.selectbox("Select your target role*", 
                              ["Data Scientist", "Software Engineer", "Product Manager", 
                               "UX Designer", "Marketing Specialist", "Financial Analyst"])
            
            st.markdown("### 🛠 Skills")
            skills = st.text_area("Skills (comma-separated)*", 
                                help="Include both technical and soft skills relevant to your target role")
            
            st.markdown("### 📌 Optional Sections")
            projects = st.text_area("Key Projects", help="Describe 2-3 key projects with impact")
            languages = st.text_input("Languages", help="List languages you speak")
        
        st.markdown("### 🏢 Work Experience")
        experience = st.text_area("Work Experience*", 
                                help="Include company names, job titles, dates, and bullet points of achievements")
        
        st.markdown("### 🔍 ATS Optimization")
        use_ats_keywords = st.checkbox("Include ATS-friendly keywords", value=True)
        resume_design = st.selectbox("Resume Design", 
                                   ["Modern Professional", "Classic Elegant", "ATS-Optimized Simple"])
        
        submitted = st.form_submit_button("✨ Generate & Analyze Resume")

    if submitted:
        if not all([full_name, email, role, skills, experience, education]):
            st.error("Please fill all required fields (*)")
        else:
            # Build resume text
            resume_content = f"""
            CANDIDATE: {full_name}
            TARGET ROLE: {role}
            CONTACT: {email} | {phone} | {linkedin}
            
            SUMMARY:
            [AI will generate based on your inputs]
            
            SKILLS:
            {skills}
            
            WORK EXPERIENCE:
            {experience}
            
            EDUCATION:
            {education}
            """
            
            if certifications:
                resume_content += f"\nCERTIFICATIONS:\n{certifications}"
            if projects:
                resume_content += f"\nPROJECTS:\n{projects}"
            if languages:
                resume_content += f"\nLANGUAGES:\n{languages}"
            
            # Generate AI analysis
            with st.spinner("🤖 AI is analyzing your resume..."):
                analysis_prompt = f"""
                Analyze this resume for a {role} position and provide specific improvement suggestions:
                1. ATS Optimization: Identify missing keywords from the job category
                2. Structure: Suggest better organization of sections
                3. Impact: Recommend stronger action verbs and quantifiable achievements
                4. Skills Matching: Identify gaps between skills and target role
                5. Summary: Generate a powerful professional summary
                
                Resume Content:
                {resume_content}
                
                Provide output in this format:
                
                ### 🔍 AI Analysis Report
                **ATS Score**: X/10
                **Missing Keywords**: [list]
                **Suggested Improvements**: [bulleted list]
                **Generated Professional Summary**: [text]
                """
                
                st.session_state.resume_analysis = get_result(analysis_prompt)
            
            st.success("✅ ATS-Optimized Resume Generated!")
            
            # Display AI Analysis
            st.markdown("---")
            st.markdown(st.session_state.resume_analysis)
            
            # Generate downloadable resume
            st.markdown("---")
            st.markdown("### 📤 Download Your Resume")
            
            # Generate professional summary if not already in analysis
            summary_prompt = f"Generate a 3-sentence professional summary for a {role} with these skills: {skills}"
            professional_summary = get_result(summary_prompt)
            
            # Create formatted resume text
            formatted_resume = f"""
            {full_name.upper()}
            {email} | {phone} | {linkedin}
            --------------------------------------------------
            
            PROFESSIONAL SUMMARY:
            {professional_summary}
            
            TECHNICAL SKILLS:
            {skills}
            
            PROFESSIONAL EXPERIENCE:
            {experience}
            
            EDUCATION:
            {education}
            """
            
            if certifications:
                formatted_resume += f"\nCERTIFICATIONS:\n{certifications}"
            if projects:
                formatted_resume += f"\nKEY PROJECTS:\n{projects}"
            if languages:
                formatted_resume += f"\nLANGUAGES:\n{languages}"
            
            # PDF Generation - SIMPLIFIED VERSION THAT WORKS
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            # Simple header
            pdf.cell(0, 10, full_name, ln=1)
            pdf.cell(0, 5, f"{email} | {phone} | {linkedin}", ln=1)
            pdf.ln(5)
            
            # Function to safely add text
            def safe_add_text(pdf, text):
                try:
                    pdf.multi_cell(0, 5, text)
                except:
                    # If there's any error, use cleaned text
                    cleaned_text = text.encode('latin1', 'replace').decode('latin1')
                    pdf.multi_cell(0, 5, cleaned_text)
            
            # Add sections
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, "PROFESSIONAL SUMMARY", ln=1)
            pdf.set_font('Arial', '', 11)
            safe_add_text(pdf, professional_summary)
            pdf.ln(3)
            
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, "TECHNICAL SKILLS", ln=1)
            pdf.set_font('Arial', '', 11)
            safe_add_text(pdf, skills)
            pdf.ln(3)
            
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, "PROFESSIONAL EXPERIENCE", ln=1)
            pdf.set_font('Arial', '', 11)
            safe_add_text(pdf, experience)
            pdf.ln(3)
            
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, "EDUCATION", ln=1)
            pdf.set_font('Arial', '', 11)
            safe_add_text(pdf, education)
            pdf.ln(3)
            
            # Optional sections
            if certifications:
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 10, "CERTIFICATIONS", ln=1)
                pdf.set_font('Arial', '', 11)
                safe_add_text(pdf, certifications)
                pdf.ln(3)
            
            if projects:
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 10, "KEY PROJECTS", ln=1)
                pdf.set_font('Arial', '', 11)
                safe_add_text(pdf, projects)
                pdf.ln(3)
            
            if languages:
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 10, "LANGUAGES", ln=1)
                pdf.set_font('Arial', '', 11)
                safe_add_text(pdf, languages)
            
            # Save PDF to buffer with error handling
            pdf_buffer = BytesIO()
            try:
                pdf_bytes = pdf.output(dest='S').encode('latin1', 'replace')
            except:
                pdf_bytes = pdf.output(dest='S').encode('utf-8', 'replace')
            pdf_buffer.write(pdf_bytes)
            pdf_buffer.seek(0)
            
            # Download buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    label="📄 Download PDF",
                    data=pdf_buffer,
                    file_name=f"{full_name.replace(' ', '_')}_Resume.pdf",
                    mime="application/pdf"
                )
            with col2:
                st.download_button(
                    label="📋 Download TXT",
                    data=formatted_resume,
                    file_name=f"{full_name.replace(' ', '_')}_Resume.txt",
                    mime="text/plain"
                )
            
            # Additional AI suggestions
            st.markdown("---")
            st.markdown("### 🚀 Boost Your Application")
            
            with st.expander("📝 AI Cover Letter Generator"):
                st.markdown("Generate a tailored cover letter based on your resume and a job description")
                job_desc = st.text_area("Paste the job description here*", height=150)
                company_name = st.text_input("Company Name")
                hiring_manager = st.text_input("Hiring Manager Name (if known)")
                
                if st.button("Generate Cover Letter"):
                    if not job_desc:
                        st.error("Please paste a job description")
                    else:
                        with st.spinner("Generating tailored cover letter..."):
                            cover_prompt = f"""
                            Write a professional cover letter for {full_name} applying for a {role} position at {company_name}.
                            Tailor it specifically to this job description. Use formal business letter format.
                            
                            Job Requirements:
                            {job_desc}
                            
                            Candidate Information:
                            Name: {full_name}
                            Email: {email}
                            Phone: {phone}
                            
                            Resume Highlights:
                            {professional_summary}
                            
                            Key Skills:
                            {skills}
                            
                            Relevant Experience:
                            {experience}
                            
                            Education:
                            {education}
                            
                            Structure the letter with:
                            1. Professional header with date and address
                            2. Personalized salutation (use {hiring_manager} if provided)
                            3. Strong opening paragraph highlighting relevant qualifications
                            4. 2-3 body paragraphs matching skills to job requirements
                            5. Closing paragraph with call to action
                            6. Professional sign-off
                            """
                            
                            cover_letter = get_result(cover_prompt)
                            st.text_area("Generated Cover Letter", cover_letter, height=400)
                            
                            # Download buttons for cover letter
                            col1, col2 = st.columns(2)
                            with col1:
                                st.download_button(
                                    label="📥 Download TXT Cover Letter",
                                    data=cover_letter,
                                    file_name=f"{full_name.replace(' ', '_')}_Cover_Letter.txt",
                                    mime="text/plain"
                                )
                            with col2:
                                # Create DOCX version of cover letter
                                doc = Document()
                                doc.add_paragraph(cover_letter)
                                
                                cover_buffer = BytesIO()
                                doc.save(cover_buffer)
                                cover_buffer.seek(0)
                                
                                st.download_button(
                                    label="📄 Download DOCX Cover Letter",
                                    data=cover_buffer,
                                    file_name=f"{full_name.replace(' ', '_')}_Cover_Letter.docx",
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                )
            
            with st.expander("🔗 LinkedIn Profile Optimizer"):
                if linkedin:
                    st.markdown(f"Analyzing LinkedIn profile: {linkedin}")
                    with st.spinner("Generating LinkedIn optimization tips..."):
                        linkedin_prompt = f"""
                        Analyze this LinkedIn profile for optimization opportunities:
                        Profile URL: {linkedin}
                        
                        Provide specific recommendations for:
                        1. Profile Headline: Suggest an improved headline for a {role} that includes keywords
                        2. About Section: Outline a compelling summary structure with examples
                        3. Skills Section: List the top 5 skills to highlight for {role}
                        4. Experience: Recommendations for optimizing experience descriptions
                        5. Endorsements: Strategy to get relevant skill endorsements
                        6. Networking: Tips for growing relevant connections
                        
                        Format as:
                        ### LinkedIn Optimization Report for {full_name}
                        **Current Headline**: [if available]
                        **Improved Headline**: [suggestion]
                        
                        **About Section Recommendations**:
                        - [bullet points]
                        
                        **Top Skills to Showcase**:
                        1. [skill 1]
                        2. [skill 2]
                        ...
                        
                        **Experience Optimization**:
                        - [suggestions]
                        
                        **Endorsement Strategy**:
                        - [actionable tips]
                        
                        **Networking Tips**:
                        - [suggestions]
                        """
                        
                        linkedin_analysis = get_result(linkedin_prompt)
                        st.markdown(linkedin_analysis)
                else:
                    st.info("Please add your LinkedIn URL above to get optimization tips")
            
            with st.expander("🔍 Get Tailored Job Description Analysis"):
                job_desc = st.text_area("Paste a job description to get customized matching suggestions", height=150)
                if st.button("Analyze Job Match") and job_desc:
                    with st.spinner("Analyzing job match..."):
                        match_prompt = f"""
                        Analyze how well this resume matches the provided job description.
                        Provide specific recommendations to improve alignment.
                        
                        Candidate: {full_name}
                        Target Role: {role}
                        
                        Resume Content:
                        {resume_content}
                        
                        Job Description:
                        {job_desc}
                        
                        Format your response with:
                        - **Match Score**: X/100 with explanation
                        - **Missing Keywords**: [list from job description]
                        - **Recommended Resume Changes**: [bullet points]
                        - **Suggested Skills to Highlight**: [based on job requirements]
                        - **Cover Letter Talking Points**: [key points to emphasize]
                        """
                        
                        match_analysis = get_result(match_prompt)
                        st.markdown(match_analysis)
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
                        ("Fiverr", "https://go.fiverr.com/visit/?bta=1120398&brand=fp")                      ]

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
        - [Fiverr](https://go.fiverr.com/visit/?bta=1120398&brand=fp) – Start with small gigs.
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

    # Define fake_jobs dictionary at function level
    fake_jobs = {
        "Canada": [
            {"title": "Senior Software Engineer", "company": "Shopify", "location": "Ottawa", "visa": "✔️ Sponsorship available", "salary": "CAD 110,000", "type": "Full-Time"},
            {"title": "Data Scientist", "company": "TD Bank", "location": "Toronto", "visa": "✔️ LMIA approved", "salary": "CAD 95,000", "type": "Full-Time"},
            {"title": "Registered Nurse", "company": "Vancouver Coastal Health", "location": "Vancouver", "visa": "✔️ Provincial Nominee Program", "salary": "CAD 85,000", "type": "Full-Time"}
        ],
        "USA": [
            {"title": "AI Researcher", "company": "Google", "location": "Mountain View", "visa": "✔️ H1B sponsorship", "salary": "$150,000", "type": "Full-Time"},
            {"title": "DevOps Engineer", "company": "Amazon", "location": "Seattle", "visa": "✔️ TN visa possible", "salary": "$135,000", "type": "Full-Time"},
            {"title": "Biomedical Engineer", "company": "Medtronic", "location": "Minneapolis", "visa": "✔️ EB-3 visa", "salary": "$120,000", "type": "Full-Time"}
        ],
        "UK": [
            {"title": "NHS Nurse", "company": "National Health Service", "location": "London", "visa": "✔️ Health & Care visa", "salary": "£35,000", "type": "Full-Time"},
            {"title": "FinTech Developer", "company": "Revolut", "location": "London", "visa": "✔️ Skilled Worker visa", "salary": "£75,000", "type": "Full-Time"},
            {"title": "Civil Engineer", "company": "Arup", "location": "Manchester", "visa": "✔️ Sponsorship available", "salary": "£45,000", "type": "Full-Time"}
        ],
        "Germany": [
            {"title": "Full Stack Developer", "company": "SAP", "location": "Berlin", "visa": "✔️ Blue Card sponsorship", "salary": "€65,000", "type": "Full-Time"},
            {"title": "Mechanical Engineer", "company": "Siemens", "location": "Munich", "visa": "✔️ Work visa available", "salary": "€58,000", "type": "Full-Time"},
            {"title": "Healthcare Worker", "company": "Charité", "location": "Berlin", "visa": "✔️ Fast-track visa", "salary": "€42,000", "type": "Full-Time"}
        ],
        "Netherlands": [
            {"title": "Cloud Architect", "company": "Booking.com", "location": "Amsterdam", "visa": "✔️ Highly Skilled Migrant", "salary": "€80,000", "type": "Full-Time"},
            {"title": "AI Engineer", "company": "Philips", "location": "Eindhoven", "visa": "✔️ Work permit available", "salary": "€75,000", "type": "Full-Time"},
            {"title": "Data Analyst", "company": "Adyen", "location": "Amsterdam", "visa": "✔️ Sponsorship available", "salary": "€60,000", "type": "Full-Time"}
        ],
        "Sweden": [
            {"title": "Game Developer", "company": "King", "location": "Stockholm", "visa": "✔️ Work permit sponsorship", "salary": "SEK 600,000", "type": "Full-Time"},
            {"title": "Data Engineer", "company": "Spotify", "location": "Stockholm", "visa": "✔️ EU Blue Card", "salary": "SEK 550,000", "type": "Full-Time"},
            {"title": "Nurse", "company": "Karolinska Hospital", "location": "Stockholm", "visa": "✔️ Work permit", "salary": "SEK 450,000", "type": "Full-Time"}
        ],
        "Ireland": [
            {"title": "Software Engineer", "company": "Google", "location": "Dublin", "visa": "✔️ Critical Skills Employment Permit", "salary": "€70,000", "type": "Full-Time"},
            {"title": "Cybersecurity Analyst", "company": "Accenture", "location": "Dublin", "visa": "✔️ Work permit available", "salary": "€65,000", "type": "Full-Time"},
            {"title": "Pharmaceutical Researcher", "company": "Pfizer", "location": "Cork", "visa": "✔️ Sponsorship available", "salary": "€60,000", "type": "Full-Time"}
        ],
        "Spain": [
            {"title": "Web Developer", "company": "Amadeus", "location": "Madrid", "visa": "✔️ EU Blue Card", "salary": "€40,000", "type": "Full-Time"},
            {"title": "Tourism Manager", "company": "Meliá Hotels", "location": "Barcelona", "visa": "✔️ Work visa sponsorship", "salary": "€35,000", "type": "Full-Time"},
            {"title": "Renewable Energy Engineer", "company": "Iberdrola", "location": "Bilbao", "visa": "✔️ Sponsorship available", "salary": "€45,000", "type": "Full-Time"}
        ],
        "Denmark": [
            {"title": "Software Developer", "company": "Maersk", "location": "Copenhagen", "visa": "✔️ Fast-Track Scheme", "salary": "DKK 600,000", "type": "Full-Time"},
            {"title": "Wind Energy Engineer", "company": "Vestas", "location": "Aarhus", "visa": "✔️ Work permit", "salary": "DKK 550,000", "type": "Full-Time"},
            {"title": "Nurse", "company": "Rigshospitalet", "location": "Copenhagen", "visa": "✔️ Sponsorship available", "salary": "DKK 400,000", "type": "Full-Time"}
        ],
        "Norway": [
            {"title": "Petroleum Engineer", "company": "Equinor", "location": "Stavanger", "visa": "✔️ Skilled Worker Visa", "salary": "NOK 800,000", "type": "Full-Time"},
            {"title": "Software Engineer", "company": "Schibsted", "location": "Oslo", "visa": "✔️ Work permit", "salary": "NOK 700,000", "type": "Full-Time"},
            {"title": "Healthcare Worker", "company": "Oslo University Hospital", "location": "Oslo", "visa": "✔️ Sponsorship available", "salary": "NOK 500,000", "type": "Full-Time"}
        ],
        "Finland": [
            {"title": "Game Programmer", "company": "Supercell", "location": "Helsinki", "visa": "✔️ Residence Permit", "salary": "€60,000", "type": "Full-Time"},
            {"title": "Data Scientist", "company": "Nokia", "location": "Espoo", "visa": "✔️ EU Blue Card", "salary": "€55,000", "type": "Full-Time"},
            {"title": "Nurse", "company": "HUS Helsinki", "location": "Helsinki", "visa": "✔️ Sponsorship available", "salary": "€40,000", "type": "Full-Time"}
        ],
        "Switzerland": [
            {"title": "Financial Analyst", "company": "UBS", "location": "Zurich", "visa": "✔️ Work Permit B", "salary": "CHF 120,000", "type": "Full-Time"},
            {"title": "Pharmaceutical Scientist", "company": "Novartis", "location": "Basel", "visa": "✔️ Sponsorship available", "salary": "CHF 110,000", "type": "Full-Time"},
            {"title": "Software Engineer", "company": "Google", "location": "Zurich", "visa": "✔️ Work permit", "salary": "CHF 130,000", "type": "Full-Time"}
        ],
        "Austria": [
            {"title": "Mechanical Engineer", "company": "AVL", "location": "Graz", "visa": "✔️ EU Blue Card", "salary": "€55,000", "type": "Full-Time"},
            {"title": "Software Developer", "company": "A1 Telekom", "location": "Vienna", "visa": "✔️ Red-White-Red Card", "salary": "€50,000", "type": "Full-Time"},
            {"title": "Nurse", "company": "Vienna General Hospital", "location": "Vienna", "visa": "✔️ Sponsorship available", "salary": "€40,000", "type": "Full-Time"}
        ]
    }

    # Visa-Sponsored Job Search Section with Filters
    st.subheader("🔎 Search Visa-Sponsored Jobs")
    with st.expander("🔍 Find Jobs Offering Visa Sponsorship", expanded=True):
        col_search1, col_search2, col_search3 = st.columns([2, 2, 1])
        with col_search1:
            job_keyword = st.text_input("Job Title/Keywords", "software developer")
            job_type = st.selectbox("Job Type", ["Full-Time", "Part-Time", "Contract", "Internship"])
        with col_search2:
            sponsor_country = st.selectbox("Country", [
                "Canada", "USA", "UK", "Australia", "Germany", "France",
                "Netherlands", "Sweden", "Ireland", "Spain", "Denmark",
                "Norway", "Finland", "Switzerland", "Austria", "Japan",
                "Singapore", "UAE", "New Zealand"
            ])
            salary_range = st.selectbox("Salary Range", [
                "Any", "$50,000-$80,000", "$80,000-$120,000", "$120,000+"
            ])
        with col_search3:
            st.text("")  # For alignment
            search_clicked = st.button("Search Jobs")
        
        if search_clicked:
            # Filter jobs by job type and salary range
            jobs_to_show = fake_jobs.get(sponsor_country, [
                {"title": "IT Specialist", "company": "TechSolutions", "location": sponsor_country, "visa": "✔️ Work visa sponsorship", "salary": "Competitive", "type": "Full-Time"}
            ])
            if job_type != "Full-Time":
                jobs_to_show = [job for job in jobs_to_show if job["type"] == job_type]
            if salary_range != "Any":
                min_salary = int(salary_range.split("-")[0].replace("$", "").replace(",", ""))
                jobs_to_show = [job for job in jobs_to_show if "Competitive" in job["salary"] or int(job["salary"].split()[0].replace(",", "").replace("CAD", "").replace("£", "").replace("€", "").replace("DKK", "").replace("NOK", "").replace("SEK", "").replace("CHF", "")) >= min_salary]
            
            st.success(f"Showing visa-sponsored {job_type} jobs in {sponsor_country} for '{job_keyword}' (Salary: {salary_range})")
            
            # Display results
            for job in jobs_to_show:
                with st.container():
                    st.markdown(f"""
                    <div style="padding:15px; border-radius:10px; background-color:#f5f5f5; margin-bottom:10px;">
                        <h4>{job['title']}</h4>
                        <p>🏢 <b>{job['company']}</b> | 📍 {job['location']} | 💰 {job['salary']}</p>
                        <p>{job['visa']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    col_btn1, col_btn2 = st.columns([1, 5])
                    with col_btn1:
                        st.button("Apply", key=f"apply_{job['title']}_{job['company']}")
                    with col_btn2:
                        st.button("Save Job", key=f"save_{job['title']}_{job['company']}")
            
            st.markdown("""
            <div style="background-color:#e3f2fd; padding:15px; border-radius:10px; margin-top:20px;">
                <h4>💡 Official Job Portals for Visa-Sponsored Jobs</h4>
                <ul>
                    <li><a href="https://www.jobbank.gc.ca" target="_blank">Canada Job Bank</a></li>
                    <li><a href="https://www.myvisajobs.com" target="_blank">MyVisaJobs (USA)</a></li>
                    <li><a href="https://www.make-it-in-germany.com" target="_blank">Make it in Germany</a></li>
                    <li><a href="https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers" target="_blank">UK Visa Sponsors</a></li>
                    <li><a href="https://www.workindenmark.dk" target="_blank">Work in Denmark</a></li>
                    <li><a href="https://www.nav.no" target="_blank">NAV (Norway)</a></li>
                    <li><a href="https://www.arbetsformedlingen.se" target="_blank">Swedish Public Employment Service</a></li>
                </ul>
                <p><b>Tip:</b> Include "visa sponsorship" in your job search keywords.</p>
            </div>
            """, unsafe_allow_html=True)

    # Interactive Job Map (Placeholder)
    st.subheader("🗺️ Explore Job Locations")
    with st.expander("📍 Job Locations by Country", expanded=False):
        st.markdown("**Available Job Locations** (Interactive map coming soon):")
        selected_country = st.selectbox("View Jobs in", fake_jobs.keys(), key="job_map_country")
        locations = list(set(job["location"] for job in fake_jobs.get(selected_country, [])))
        for loc in locations:
            st.markdown(f"- 📍 {loc} ({selected_country})")

    # Progress Tracker
    st.subheader("📊 Your Visa Journey Progress")
    col_prog1, col_prog2 = st.columns([3, 1])
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

    # Visa Cost Estimator
    st.subheader("💸 Visa Cost Estimator")
    with st.form("visa_cost_form"):
        cost_country = st.selectbox("Select Country", [
            "Canada", "USA", "UK", "Australia", "Germany", "Netherlands",
            "Sweden", "Ireland", "Spain", "Denmark", "Norway", "Finland",
            "Switzerland", "Austria"
        ])
        visa_type = st.selectbox("Visa Type", [
            "Work Permit", "Skilled Worker Visa", "EU Blue Card",
            "H1B Visa", "Highly Skilled Migrant", "Critical Skills Permit",
            "Red-White-Red Card"
        ])
        include_dependents = st.checkbox("Include Dependents")
        cost_submit = st.form_submit_button("Estimate Cost")
    
    if cost_submit:
        # Placeholder cost data (in USD for simplicity)
        cost_data = {
            "Canada": {"Work Permit": 300, "Skilled Worker Visa": 1000},
            "USA": {"H1B Visa": 2500, "Skilled Worker Visa": 2000},
            "UK": {"Skilled Worker Visa": 1500, "EU Blue Card": 1000},
            "Australia": {"Skilled Worker Visa": 1200},
            "Germany": {"EU Blue Card": 800, "Work Permit": 500},
            "Netherlands": {"Highly Skilled Migrant": 700, "EU Blue Card": 800},
            "Sweden": {"Work Permit": 600, "EU Blue Card": 800},
            "Ireland": {"Critical Skills Permit": 900, "Work Permit": 600},
            "Spain": {"EU Blue Card": 700, "Work Permit": 500},
            "Denmark": {"Work Permit": 650, "Skilled Worker Visa": 900},
            "Norway": {"Skilled Worker Visa": 800, "Work Permit": 600},
            "Finland": {"Work Permit": 550, "EU Blue Card": 700},
            "Switzerland": {"Work Permit": 1000},
            "Austria": {"Red-White-Red Card": 800, "EU Blue Card": 700}
        }
        base_cost = cost_data.get(cost_country, {}).get(visa_type, 500)
        total_cost = base_cost * (1.5 if include_dependents else 1)
        st.success(f"Estimated Visa Cost for {visa_type} in {cost_country}: **${total_cost:,.2f} USD**")
        st.markdown("*Note: Costs are approximate and include application fees only. Additional costs (e.g., biometrics, legal fees) may apply.*")

    # Enhanced Eligibility Checker
    st.subheader("🔍 Advanced Visa Eligibility Checker")
    with st.form("enhanced_eligibility"):
        country = st.selectbox("Target Country", [
            "Canada", "USA", "UK", "Australia", "Germany", "France",
            "Netherlands", "Sweden", "Ireland", "Spain", "Denmark",
            "Norway", "Finland", "Switzerland", "Austria", "Japan",
            "Singapore", "UAE", "New Zealand"
        ], key="enhanced_country")
        
        col1, col2 = st.columns(2)
        with col1:
            profession = st.text_input("Your Profession", "Software Developer")
            education = st.selectbox("Education Level", [
                "High School", "Bachelor's", "Master's", "PhD"
            ])
        with col2:
            experience = st.select_slider("Years of Experience", 
                                        options=["0-1", "1-3", "3-5", "5-10", "10+"])
            language = st.multiselect("Language Tests", [
                "IELTS", "TOEFL", "TEF", "Goethe-Zertifikat", "JLPT"
            ])
        
        if st.form_submit_button("Check Eligibility Score"):
            score = min(
                100,
                20
                + (len(language) * 15)
                + (10 if education != "High School" else 0)
                + (20 if experience in ["5-10", "10+"] else 10 if experience == "3-5" else 0)
            )
            st.success(f"🎯 Your Eligibility Score for {country}: {score}/100")
            
            st.metric("Your Eligibility Score", f"{score}% match")
            
            # Visual score indicator
            color = "#4CAF50" if score >= 70 else "#FFC107" if score >= 50 else "#F44336"
            st.markdown(f"""
            <style>
                .score-bar {{
                    height: 20px;
                    background: linear-gradient(90deg, {color} {score}%, #f5f5f5 {score}%);
                    border-radius: 10px;
                    margin: 10px 0;
                }}
            </style>
            <div class="score-bar"></div>
            """, unsafe_allow_html=True)
            
            # Interpretation
            if score >= 70:
                st.success("High eligibility! Strong chance for visa approval.")
            elif score >= 50:
                st.warning("Moderate eligibility. Consider improving qualifications.")
            else:
                st.error("Low eligibility. Focus on experience or language skills.")
            
            # Next steps
            st.markdown("**Next Steps:**")
            if score < 70:
                st.markdown("- 🎓 Consider higher education if possible")
                st.markdown("- 🌐 Improve language test scores")
                st.markdown(f"- 💼 Gain more experience in {profession}")
            st.markdown(f"- 📝 Check specific requirements for {country}")

    # Country-Specific Guides with More European Countries
    st.subheader("🌍 Country-Specific Visa Programs")
    
    tab_ca, tab_us, tab_uk, tab_au, tab_de, tab_nl, tab_se, tab_ie, tab_fr, tab_es, tab_dk, tab_no, tab_fi, tab_ch, tab_at = st.tabs([
        "🇨🇦 Canada", "🇺🇸 USA", "🇬🇧 UK", "🇦🇺 Australia", "🇩🇪 Germany",
        "🇳🇱 Netherlands", "🇸🇪 Sweden", "🇮🇪 Ireland", "🇫🇷 France", "🇪🇸 Spain",
        "🇩🇰 Denmark", "🇳🇴 Norway", "🇫🇮 Finland", "🇨🇭 Switzerland", "🇦🇹 Austria"
    ])
    
    with tab_ca:
        st.markdown("""
        ### 🇨🇦 Canada Immigration Programs
        **Top Visa-Sponsored Jobs (2025):**
        - 👨‍💻 Software Developers (NOC 21232) - CAD 85,000 avg
        - 👩‍⚕️ Registered Nurses (NOC 31301) - CAD 78,000 avg
        - 🔧 Electricians (NOC 72200) - CAD 65,000 avg
        
        **Visa Pathways:**
        - **Express Entry**: FSW, CEC, FST (6-8 months processing)
        - **Provincial Nominee Programs (PNP)**: Alberta, BC, Ontario
        - **Work Permits**: LMIA required for most
        
        **2025 Updates:**
        - Tech Talent Strategy for fast-track tech visas
        - Increased healthcare worker quotas
        
        **Resources:**
        - [Job Bank](https://www.jobbank.gc.ca)
        - [Express Entry](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry.html)
        """)
        st.download_button(
            label="📥 Canada Visa Checklist",
            data="Canada Visa Checklist: Language Test, ECA, Proof of Funds, Police Clearance, Medical Exam, Job Offer, Express Entry Profile",
            file_name="canada_visa_checklist.txt"
        )

    with tab_us:
        st.markdown("""
        ### 🇺🇸 USA Work Visa Options
        **Top Visa-Sponsored Jobs:**
        - 💻 Computer Occupations - $120,000 avg
        - 🏥 Healthcare (RNs, Physicians) - $100,000 avg
        - 🎓 University Faculty - $80,000 avg
        
        **Visa Types:**
        - H1B: Specialty Occupations
        - L1: Intracompany Transfers
        - TN: NAFTA Professionals
        - EB-3: Skilled Workers
        
        **2025 Updates:**
        - H1B registration fee: $250
        - Premium processing fee: $2,500
        
        **Resources:**
        - [USCIS](https://www.uscis.gov)
        - [MyVisaJobs](https://www.myvisajobs.com)
        """)
        st.download_button(
            label="📥 USA Visa Checklist",
            data="USA Visa Checklist: Job Offer, LCA, Form I-129, Qualifications, DS-160, Visa Fee, Embassy Interview",
            file_name="usa_visa_checklist.txt"
        )

    with tab_uk:
        st.markdown("""
        ### 🇬🇧 UK Skilled Worker Visa
        **Shortage Occupations:**
        - 👩‍⚕️ Healthcare (Nurses, Doctors) - £35,000 avg
        - 👨‍🔬 STEM (Engineers, Data Scientists) - £50,000 avg
        - 👨‍🏫 Education (Teachers) - £30,000 avg
        
        **Requirements:**
        - Job offer from licensed sponsor
        - Salary ≥ £26,200
        - English B1 level
        
        **2025 Changes:**
        - Immigration Salary List replaces SOL
        - Health & Care Worker visa fee reduced
        
        **Resources:**
        - [UK Visas](https://www.gov.uk/skilled-worker-visa)
        - [Sponsor List](https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers)
        """)
        st.download_button(
            label="📥 UK Visa Checklist",
            data="UK Visa Checklist: CoS, English Proficiency, Maintenance Funds, TB Test, Application Form, IHS Surcharge, Biometrics",
            file_name="uk_visa_checklist.txt"
        )

    with tab_au:
        st.markdown("""
        ### 🇦🇺 Australia Visa Options
        **Skilled Migration:**
        - 189: Independent
        - 190: State Nominated
        - 491: Regional
        
        **2025 Priority:**
        - Healthcare Workers - AUD 80,000 avg
        - Tech (Cybersecurity) - AUD 100,000 avg
        - Trades (Electricians) - AUD 70,000 avg
        
        **Points Test:**
        - Age: max 30 points
        - English: max 20 points
        - Experience: max 15 points
        
        **Resources:**
        - [Home Affairs](https://immi.homeaffairs.gov.au)
        - [SkillSelect](https://skillselect.gov.au)
        """)
        st.download_button(
            label="📥 Australia Visa Checklist",
            data="Australia Visa Checklist: Skills Assessment, IELTS/TOEFL, EOI, Police Clearance, Medical Exam, Proof of Funds, ITA",
            file_name="australia_visa_checklist.txt"
        )

    with tab_de:
        st.markdown("""
        ### 🇩🇪 Germany Work Visas
        **Top Visa-Sponsored Jobs:**
        - 💻 IT Specialists - €60,000 avg
        - 🔧 Engineers - €55,000 avg
        - 🩺 Healthcare Professionals - €50,000 avg
        
        **Visa Options:**
        - EU Blue Card: €58,400+ salary
        - Opportunity Card: Job seeker visa
        - Skilled Worker Visa: Recognized qualifications
        
        **2025 Updates:**
        - Faster qualification recognition
        - Opportunity Card eligibility expanded
        
        **Resources:**
        - [Make it in Germany](https://www.make-it-in-germany.com)
        - [Stepstone](https://www.stepstone.de)
        """)
        st.download_button(
            label="📥 Germany Visa Checklist",
            data="Germany Visa Checklist: Qualifications, Job Offer, Language Proof, Health Insurance, Accommodation, Application Form, Biometrics",
            file_name="germany_visa_checklist.txt"
        )

    with tab_nl:
        st.markdown("""
        ### 🇳🇱 Netherlands Work Visas
        **Top Visa-Sponsored Jobs:**
        - 👨‍💻 Software Developers - €65,000 avg
        - 🩺 Healthcare Workers - €50,000 avg
        - 🔬 R&D Scientists - €60,000 avg
        
        **Visa Pathways:**
        - Highly Skilled Migrant: €4,752/month
        - Orientation Year: For graduates
        - EU Blue Card: €5,670/month
        
        **2025 Updates:**
        - Increased tech/green energy demand
        - 30% ruling tax benefit extended
        
        **Resources:**
        - [IND](https://ind.nl/en/work/working_in_the_netherlands)
        - [Indeed NL](https://www.indeed.nl)
        """)
        st.download_button(
            label="📥 Netherlands Visa Checklist",
            data="Netherlands Visa Checklist: Job Offer, Salary Proof, Qualifications, Health Insurance, Application Form, Biometrics",
            file_name="netherlands_visa_checklist.txt"
        )

    with tab_se:
        st.markdown("""
        ### 🇸🇪 Sweden Work Visas
        **Top Visa-Sponsored Jobs:**
        - 💻 Game Developers - SEK 600,000 avg
        - 👩‍💻 Data Engineers - SEK 550,000 avg
        - 🩺 Nurses - SEK 450,000 avg
        
        **Visa Pathways:**
        - Work Permit: Job offer required
        - EU Blue Card: SEK 59,600/month
        - Job Seeker Visa: Pilot for 2025
        
        **2025 Updates:**
        - Tech sector growth in Stockholm
        - Fast-track for shortage occupations
        
        **Resources:**
        - [Arbetsförmedlingen](https://www.arbetsformedlingen.se)
        - [Migrationsverket](https://www.migrationsverket.se)
        """)
        st.download_button(
            label="📥 Sweden Visa Checklist",
            data="Sweden Visa Checklist: Job Offer, Qualifications, Language Proof, Health Insurance, Application Form, Biometrics",
            file_name="sweden_visa_checklist.txt"
        )

    with tab_ie:
        st.markdown("""
        ### 🇮🇪 Ireland Work Visas
        **Top Visa-Sponsored Jobs:**
        - 💻 Software Engineers - €70,000 avg
        - 🔒 Cybersecurity Specialists - €65,000 avg
        - 🩺 Healthcare Professionals - €55,000 avg
        
        **Visa Pathways:**
        - Critical Skills Employment Permit
        - General Employment Permit
        - EU Blue Card: €60,000+
        
        **2025 Updates:**
        - Dublin tech hub expansion
        - Healthcare worker quotas increased
        
        **Resources:**
        - [Jobs Ireland](https://www.jobsireland.ie)
        - [Irish Immigration](https://www.irishimmigration.ie)
        """)
        st.download_button(
            label="📥 Ireland Visa Checklist",
            data="Ireland Visa Checklist: Job Offer, Qualifications, Language Proof, Application Form, Biometrics, Visa Fee",
            file_name="ireland_visa_checklist.txt"
        )

    with tab_fr:
        st.markdown("""
        ### 🇫🇷 France Work Visas
        **Top Visa-Sponsored Jobs:**
        - 👨‍💻 Tech Professionals - €55,000 avg
        - 🏨 Hospitality Managers - €45,000 avg
        - 👩‍🏫 Researchers - €50,000 avg
        
        **Visa Pathways:**
        - Talent Passport: Skilled professionals
        - Tech Visa: Startup employees
        - EU Blue Card: €53,836+
        
        **2025 Updates:**
        - Paris tech startup growth
        - Simplified Talent Passport process
        
        **Resources:**
        - [Pôle Emploi](https://www.pole-emploi.fr)
        - [France Visas](https://france-visas.gouv.fr)
        """)
        st.download_button(
            label="📥 France Visa Checklist",
            data="France Visa Checklist: Job Offer, Qualifications, Language Proof, Health Insurance, Application Form, Biometrics",
            file_name="france_visa_checklist.txt"
        )

    with tab_es:
        st.markdown("""
        ### 🇪🇸 Spain Work Visas
        **Top Visa-Sponsored Jobs:**
        - 💻 Web Developers - €40,000 avg
        - 🏨 Tourism Managers - €35,000 avg
        - 🔬 Renewable Energy Engineers - €45,000 avg
        
        **Visa Pathways:**
        - EU Blue Card: €33,908+
        - Highly Qualified Professional Visa
        - Work Permit: Employer-sponsored
        
        **2025 Updates:**
        - Renewable energy sector growth
        - Digital nomad visa expansion
        
        **Resources:**
        - [InfoJobs](https://www.infojobs.net)
        - [Exteriores](https://www.exteriores.gob.es)
        """)
        st.download_button(
            label="📥 Spain Visa Checklist",
            data="Spain Visa Checklist: Job Offer, Qualifications, Language Proof, Health Insurance, Application Form, Biometrics",
            file_name="spain_visa_checklist.txt"
        )

    with tab_dk:
        st.markdown("""
        ### 🇩🇰 Denmark Work Visas
        **Top Visa-Sponsored Jobs:**
        - 💻 Software Developers - DKK 600,000 avg
        - 🔧 Wind Energy Engineers - DKK 550,000 avg
        - 🩺 Nurses - DKK 400,000 avg
        
        **Visa Pathways:**
        - Fast-Track Scheme: Quick processing
        - Positive List: Shortage occupations
        - EU Blue Card: DKK 468,000+
        
        **2025 Updates:**
        - Green tech sector expansion
        - Simplified family reunification
        
        **Resources:**
        - [Work in Denmark](https://www.workindenmark.dk)
        - [New to Denmark](https://www.nyidanmark.dk)
        """)
        st.download_button(
            label="📥 Denmark Visa Checklist",
            data="Denmark Visa Checklist: Job Offer, Qualifications, Language Proof, Health Insurance, Application Form, Biometrics",
            file_name="denmark_visa_checklist.txt"
        )

    with tab_no:
        st.markdown("""
        ### 🇳🇴 Norway Work Visas
        **Top Visa-Sponsored Jobs:**
        - 🔧 Petroleum Engineers - NOK 800,000 avg
        - 💻 Software Engineers - NOK 700,000 avg
        - 🩺 Healthcare Workers - NOK 500,000 avg
        
        **Visa Pathways:**
        - Skilled Worker Visa: Job offer required
        - Job Seeker Visa: For professionals
        - EU Blue Card: NOK 600,000+
        
        **2025 Updates:**
        - Energy sector hiring surge
        - Digital application portal launch
        
        **Resources:**
        - [NAV](https://www.nav.no)
        - [UDI](https://www.udi.no)
        """)
        st.download_button(
            label="📥 Norway Visa Checklist",
            data="Norway Visa Checklist: Job Offer, Qualifications, Language Proof, Health Insurance, Application Form, Biometrics",
            file_name="norway_visa_checklist.txt"
        )

    with tab_fi:
        st.markdown("""
        ### 🇫🇮 Finland Work Visas
        **Top Visa-Sponsored Jobs:**
        - 💻 Game Programmers - €60,000 avg
        - 👩‍💻 Data Scientists - €55,000 avg
        - 🩺 Nurses - €40,000 avg
        
        **Visa Pathways:**
        - Residence Permit: Job offer
        - EU Blue Card: €48,000+
        - Specialist Visa: High-skill roles
        
        **2025 Updates:**
        - Helsinki tech hub growth
        - Healthcare worker recruitment
        
        **Resources:**
        - [Work in Finland](https://www.workinfinland.com)
        - [Migri](https://migri.fi)
        """)
        st.download_button(
            label="📥 Finland Visa Checklist",
            data="Finland Visa Checklist: Job Offer, Qualifications, Language Proof, Health Insurance, Application Form, Biometrics",
            file_name="finland_visa_checklist.txt"
        )

    with tab_ch:
        st.markdown("""
        ### 🇨🇭 Switzerland Work Visas
        **Top Visa-Sponsored Jobs:**
        - 💸 Financial Analysts - CHF 120,000 avg
        - 🔬 Pharmaceutical Scientists - CHF 110,000 avg
        - 💻 Software Engineers - CHF 130,000 avg
        
        **Visa Pathways:**
        - Work Permit B: Employer-sponsored
        - Work Permit L: Short-term
        - EU Blue Card: CHF 100,000+
        
        **2025 Updates:**
        - Finance and pharma hiring surge
        - Streamlined permit process
        
        **Resources:**
        - [Ch.ch](https://www.ch.ch)
        - [Swiss Jobs](https://www.jobs.ch)
        """)
        st.download_button(
            label="📥 Switzerland Visa Checklist",
            data="Switzerland Visa Checklist: Job Offer, Qualifications, Language Proof, Health Insurance, Application Form, Biometrics",
            file_name="switzerland_visa_checklist.txt"
        )

    with tab_at:
        st.markdown("""
        ### 🇦🇹 Austria Work Visas
        **Top Visa-Sponsored Jobs:**
        - 🔧 Mechanical Engineers - €55,000 avg
        - 💻 Software Developers - €50,000 avg
        - 🩺 Nurses - €40,000 avg
        
        **Visa Pathways:**
        - Red-White-Red Card: Skilled workers
        - EU Blue Card: €47,000+
        - Job Seeker Visa: 6 months
        
        **2025 Updates:**
        - Tech and healthcare demand
        - Simplified RWR Card process
        
        **Resources:**
        - [Migration.gv.at](https://www.migration.gv.at)
        - [Karriere.at](https://www.karriere.at)
        """)
        st.download_button(
            label="📥 Austria Visa Checklist",
            data="Austria Visa Checklist: Job Offer, Qualifications, Language Proof, Health Insurance, Application Form, Biometrics",
            file_name="austria_visa_checklist.txt"
        )

    # Visa Application Milestones
    st.subheader("✅ Track Your Visa Application")
    with st.form("visa_milestone_form"):
        milestone = st.selectbox("Add Milestone", [
            "Job Offer Secured",
            "Credentials Assessed",
            "Language Test Passed",
            "Visa Application Submitted",
            "Residence Permit Received",
            "Flight Booked"
        ])
        milestone_date = st.date_input("Date")
        milestone_submit = st.form_submit_button("Add Milestone")
    if milestone_submit:
        if milestone not in [m['name'] for m in st.session_state.visa_milestones]:
            st.session_state.visa_milestones.append({
                "name": milestone,
                "date": milestone_date.strftime("%Y-%m-%d"),
                "completed": True
            })
            st.success(f"Milestone '{milestone}' added!")
        
        st.markdown("**Your Visa Journey**")
        for m in st.session_state.visa_milestones:
            st.markdown(f"- ✅ {m['name']} ({m['date']})")

    # Enhanced AI-Powered Visa Guidance
    st.subheader("🤖 Ask AI for Visa Guidance")
    with st.form("visa_guidance_form"):
        visa_query = st.text_area("Ask a Visa Question (e.g., 'What visa for a nurse in Canada?')", 
                                height=100,
                                placeholder="Type your question about visas, work permits, or immigration...")
        visa_query_submit = st.form_submit_button("Get AI Advice")
    if visa_query_submit and visa_query.strip():
        visa_prompt = f"""Act as an immigration expert with 15 years of experience. Provide a concise, structured answer for the following visa-related question about {sponsor_country}.
        Format:
        - **Visa Types**: List relevant visas
        - **Requirements**: Key eligibility criteria
        - **Processing Time**: Estimated duration
        - **Challenges**: Common issues and solutions
        Question: {visa_query}"""
        with st.spinner("Analyzing your visa question..."):
            visa_answer = get_result(visa_prompt)
            st.markdown(f"**AI Visa Advice**:\n\n{visa_answer}")

    # Recent Updates
    st.subheader("🆕 2025 Visa and Job Updates")
    st.markdown("""
    - **Australia**: Core Skills Occupation List launches May 2025
    - **Germany**: Opportunity Card allows 12-month job search
    - **Canada**: 825 PNP invitations in April 2025
    - **UK**: Immigration Salary List replaces SOL
    - **Denmark**: Green tech hiring surge
    - **Norway**: Digital visa portal launch
    - **Switzerland**: Streamlined permit process
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
