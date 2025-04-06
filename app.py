import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Mega Job Finder Pro", page_icon="💼", layout="centered")

# ================== DATA CONFIGURATION ==================
ALL_INDIAN_LOCATIONS = [
    "Bangalore", "Mumbai", "Delhi NCR", "Hyderabad", "Chennai",
    "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow",
    "Surat", "Kochi", "Coimbatore", "Nagpur", "Indore",
    "Patna", "Bhopal", "Visakhapatnam", "Vadodara", "Remote",
    "Anywhere in India"
]

COUNTRIES = ["India", "USA", "UK", "Canada", "Australia", "Germany", "UAE", "Global"]

INDUSTRIES = [
    "All Industries", "Technology", "Healthcare", "Engineering",
    "Finance", "Education", "Government", "Creative/Design",
    "Remote Work", "Visa Sponsorship"
]

EXP_LEVELS = ["Any", "Entry", "Mid", "Senior", "Executive"]
DATE_POSTED = ["Any time", "Past 24 hours", "Past week", "Past month"]

# ================== JOB PORTAL CONFIGURATION ==================
JOB_PORTALS = {
    "India": [
        {
            "name": "LinkedIn (India)",
            "template": lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}",
            "filters": ["location", "experience", "date"],
            "icon": "🔵"
        },
        {
            "name": "Naukri",
            "template": lambda k, l, e, d: f"https://www.naukri.com/{k.lower().replace(' ', '-')}-jobs-in-{l.lower().replace(' ', '-') if l != 'Remote' else 'india'}?experience={e}&jobAge={d}",
            "filters": ["location", "experience", "date"],
            "icon": "🟡"
        },
        {
            "name": "Indeed India",
            "template": lambda k, l, e, d: f"https://www.indeed.co.in/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}&fromage={d}&explvl={e}_level",
            "filters": ["location", "experience", "date"],
            "icon": "🔴"
        },
        {
            "name": "Monster India",
            "template": lambda k, l, e, d: f"https://www.monsterindia.com/srp/results?query={urllib.parse.quote(k)}&locations={urllib.parse.quote(l)}&experienceRanges={e}~{e}&jobAge={d}",
            "filters": ["location", "experience", "date"],
            "icon": "🟢"
        }
    ],
    "Global": [
        {
            "name": "LinkedIn Global",
            "template": lambda k, l, e, d: f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}&location={urllib.parse.quote(l)}&f_TPR={d}&f_E={e}",
            "filters": ["location", "experience", "date"],
            "icon": "🔵"
        },
        {
            "name": "Indeed Worldwide",
            "template": lambda k, l, e, d: f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}&l={urllib.parse.quote(l)}&fromage={d}&explvl={e}_level",
            "filters": ["location", "experience", "date"],
            "icon": "🔴"
        }
    ]
}

# ================== FILTER MAPPINGS ==================
EXP_MAP = {
    "Any": "",
    "Entry": "1",
    "Mid": "2",
    "Senior": "3",
    "Executive": "4"
}

DATE_MAP = {
    "Any time": "",
    "Past 24 hours": "1",
    "Past week": "7",
    "Past month": "30"
}

# ================== UI COMPONENTS ==================
def show_job_card(portal, keyword, location, exp_val, date_val):
    """Display a job portal card with applied filters"""
    try:
        url = portal['template'](
            k=keyword,
            l=location if location != "Anywhere in India" else "India",
            e=exp_val,
            d=date_val
        )
        st.markdown(f"""
        <div style='background-color:#f8f9fa; padding:15px; border-radius:10px; margin-bottom:15px; 
                    border-left: 4px solid #0077b5; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                <span style='font-size: 24px; margin-right: 12px;'>{portal.get('icon', '🔗')}</span>
                <h4 style='margin: 0; color: #1a237e;'>{portal['name']}</h4>
            </div>
            <div style='margin-bottom: 12px; color: #455a64;'>
                {f"<b>Location:</b> {location}<br>" if 'location' in portal['filters'] else ""}
                {f"<b>Experience:</b> {exp_val if exp_val else 'Any'}<br>" if 'experience' in portal['filters'] else ""}
                {f"<b>Posted:</b> {date_val} days ago<br>" if date_val and 'date' in portal['filters'] else ""}
            </div>
            <a href='{url}' target='_blank' 
               style='background-color: #0077b5; color: white; padding: 8px 16px; 
                      border-radius: 5px; text-decoration: none; display: inline-block; 
                      transition: all 0.3s; border: none; cursor: pointer;'
               onmouseover="this.style.backgroundColor='#0056b3'" 
               onmouseout="this.style.backgroundColor='#0077b5'">
                Search Jobs →
            </a>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating URL for {portal['name']}: {str(e)}")

# ================== MAIN APP ==================
st.title("💼 Mega Job Finder Pro")
st.markdown("🔍 Advanced job search with precision filters across 50+ portals")

with st.form("job_search_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        keyword = st.text_input("Job Title/Keywords", "Software Engineer")
        industry = st.selectbox("Industry", INDUSTRIES, index=0)
        country = st.selectbox("Country", COUNTRIES, index=0)
        
    with col2:
        location = st.selectbox("Location", ALL_INDIAN_LOCATIONS if country == "India" else ["Global"], 
                               index=0 if country != "India" else 0)
        experience = st.selectbox("Experience Level", EXP_LEVELS, index=2)
        date_posted = st.selectbox("Date Posted", DATE_POSTED, index=0)
    
    submitted = st.form_submit_button("🚀 Find Jobs")

if submitted:
    # Combine keyword with industry if industry is specified
    search_keyword = keyword
    if industry != "All Industries":
        search_keyword = f"{industry} {keyword}".strip()
    
    st.subheader(f"🔎 {industry} Jobs in {location if country == 'India' else country}")
    st.caption(f"Showing {experience.lower()} level jobs posted {date_posted.lower()}")
    
    # Convert filters
    exp_val = EXP_MAP[experience]
    date_val = DATE_MAP[date_posted]
    search_location = location if country == "India" else country
    
    # Show relevant portals
    portals = JOB_PORTALS.get(country, JOB_PORTALS["Global"])
    
    for portal in portals:
        show_job_card(portal, search_keyword, search_location, exp_val, date_val)
    
    # Additional Resources
    st.markdown("---")
    st.subheader("📌 Additional Job Search Tools")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Popular Alternatives:**
        - [Google Jobs](https://www.google.com/search?q=jobs)
        - [Glassdoor](https://www.glassdoor.com)
        - [AngelList](https://angel.co/jobs)
        - [Government Jobs](https://www.india.gov.in/spotlight/government-jobs)
        """)
        
    with col2:
        st.markdown("""
        **Pro Tips:**
        1. Use exact job titles for better matches
        2. Combine location + remote filters
        3. Set up daily email alerts
        4. Use multiple portals for maximum coverage
        """)
    
    st.success(f"✅ Found {len(portals)} premium job sources for your search!")
