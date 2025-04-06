import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Global Job Finder Pro", page_icon="💼", layout="centered")

# ================== DATA CONFIGURATION ==================
LOCATIONS_BY_COUNTRY = {
    "India": [
        "Bangalore", "Mumbai", "Delhi NCR", "Hyderabad", "Chennai",
        "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Remote",
        "Anywhere in India"
    ],
    "USA": [
        "New York", "San Francisco", "Austin", "Seattle", "Chicago",
        "Boston", "Los Angeles", "Remote", "Anywhere in USA"
    ],
    "UK": [
        "London", "Manchester", "Edinburgh", "Birmingham", "Bristol",
        "Leeds", "Remote", "Anywhere in UK"
    ],
    "Canada": [
        "Toronto", "Vancouver", "Montreal", "Ottawa", "Calgary",
        "Edmonton", "Remote", "Anywhere in Canada"
    ],
    "Germany": [
        "Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne",
        "Stuttgart", "Remote", "Anywhere in Germany"
    ],
    "UAE": [
        "Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Remote",
        "Anywhere in UAE"
    ]
}

COUNTRIES = list(LOCATIONS_BY_COUNTRY.keys()) + ["Global"]

INDUSTRIES = [
    "All Industries", "Technology", "Healthcare", "Engineering",
    "Finance", "Education", "Government", "Creative/Design",
    "Remote Work", "Visa Sponsorship"
]

# ================== JOB PORTAL CONFIGURATION ==================
JOB_PORTALS = {
    "India": [
        {
            "name": "LinkedIn India",
            "template": lambda k,l,e,d: (
                f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}"
                f"&location={urllib.parse.quote(l)}"
                f"&f_TPR={d}&f_E={e}"
            ),
            "filters": {
                "experience": {"Entry": "2", "Mid": "3", "Senior": "4", "Executive": "5"},
                "date": {"Past 24 hours": "r86400", "Past week": "r604800", "Past month": "r2592000"}
            },
            "industries": ["All Industries"]
        },
        {
            "name": "Naukri (Tech)",
            "template": lambda k,l,e,d: (
                f"https://www.naukri.com/{k.lower().replace(' ','-')}-jobs"
                f"{'-in-' + l.lower().replace(' ','-') if l not in ['Remote', 'Anywhere in India'] else ''}"
                f"?experience={e}&jobAge={d}"
            ),
            "filters": {
                "experience": {"Entry": "1", "Mid": "2", "Senior": "3", "Executive": "4"},
                "date": {"Past 24 hours": "1", "Past week": "7", "Past month": "30"}
            },
            "industries": ["Technology"]
        }
    ],
    "USA": [
        {
            "name": "LinkedIn USA",
            "template": lambda k,l,e,d: (
                f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}"
                f"&location={urllib.parse.quote(l)}"
                f"&f_TPR={d}&f_E={e}"
            ),
            "filters": {
                "experience": {"Entry": "2", "Mid": "3", "Senior": "4", "Executive": "5"},
                "date": {"Past 24 hours": "r86400", "Past week": "r604800", "Past month": "r2592000"}
            },
            "industries": ["All Industries"]
        },
        {
            "name": "Indeed USA",
            "template": lambda k,l,e,d: (
                f"https://www.indeed.com/jobs?q={urllib.parse.quote(k)}"
                f"&l={urllib.parse.quote(l)}"
                f"&fromage={d}&explvl={e}_level"
            ),
            "filters": {
                "experience": {"Entry": "entry", "Mid": "mid", "Senior": "senior", "Executive": "executive"},
                "date": {"Past 24 hours": "1", "Past week": "7", "Past month": "30"}
            },
            "industries": ["All Industries"]
        }
    ],
    "Global": [
        {
            "name": "LinkedIn Global",
            "template": lambda k,l,e,d: (
                f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(k)}"
                f"&location={urllib.parse.quote(l)}"
                f"&f_TPR={d}&f_E={e}"
            ),
            "filters": {
                "experience": {"Entry": "2", "Mid": "3", "Senior": "4", "Executive": "5"},
                "date": {"Past 24 hours": "r86400", "Past week": "r604800", "Past month": "r2592000"}
            },
            "industries": ["All Industries"]
        }
    ]
}

# ================== UI COMPONENTS ==================
def get_filter_values(portal, experience, date_posted):
    """Get portal-specific filter values"""
    exp_map = portal["filters"]["experience"]
    date_map = portal["filters"]["date"]
    
    exp_val = exp_map.get(experience, "")
    date_val = date_map.get(date_posted, "")
    
    return exp_val, date_val

def show_portal_card(portal, keyword, location, exp_val, date_val):
    """Display a job portal card with proper parameter handling"""
    try:
        # Handle "Anywhere in" locations
        clean_location = location.replace("Anywhere in ", "")
        if "Anywhere" in location:
            clean_location = clean_location + " (All Locations)"
            
        url = portal['template'](
            k=keyword,
            l=clean_location,
            e=exp_val,
            d=date_val
        )
    except Exception as e:
        st.error(f"Error generating URL for {portal['name']}: {str(e)}")
        return

    st.markdown(f"""
    <div style='background-color:#f8f9fa; padding:20px; border-radius:10px; 
                margin-bottom:20px; border-left: 4px solid #0077b5;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        <div style='display: flex; align-items: center; margin-bottom: 15px;'>
            <h3 style='margin: 0; color: #1a237e;'>📌 {portal['name']}</h3>
        </div>
        
        <div style='margin-bottom: 15px; color: #455a64;'>
            <b>📍 Location:</b> {location}<br>
            <b>🎯 Experience:</b> {experience or 'Any'}<br>
            <b>📅 Posted:</b> {date_posted or 'Any time'}
        </div>
        
        <a href='{url}' target='_blank' 
           style='background-color: #0077b5; color: white; padding: 10px 20px;
                  border-radius: 6px; text-decoration: none; display: inline-block;
                  transition: background-color 0.3s; font-weight: 500;'
           onmouseover="this.style.backgroundColor='#0056b3'" 
           onmouseout="this.style.backgroundColor='#0077b5'">
           🔍 Search Jobs
        </a>
    </div>
    """, unsafe_allow_html=True)

# ================== MAIN APP ==================
st.title("🌍 Global Job Finder Pro")
st.markdown("🔍 Smart job search with location-specific portals and precise filters")

with st.form("job_search_form"):
    col1, col2 = st.columns([1, 1])
    
    with col1:
        country = st.selectbox("Select Country", COUNTRIES, index=0)
        location = st.selectbox(
            "Location",
            LOCATIONS_BY_COUNTRY.get(country, ["Global"]),
            index=0
        )
        industry = st.selectbox("Industry", INDUSTRIES, index=0)
        
    with col2:
        keyword = st.text_input("Job Title/Keywords", "Software Engineer")
        experience = st.selectbox(
            "Experience Level",
            ["Any", "Entry", "Mid", "Senior", "Executive"],
            index=2
        )
        date_posted = st.selectbox(
            "Date Posted",
            ["Any time", "Past 24 hours", "Past week", "Past month"],
            index=0
        )
    
    submitted = st.form_submit_button("🚀 Find Jobs")

if submitted:
    st.subheader(f"🔎 {industry} Jobs in {location}")
    st.caption(f"Showing {experience} level jobs posted {date_posted.lower()}")
    
    # Get relevant portals
    portals = JOB_PORTALS.get(country, JOB_PORTALS["Global"])
    
    # Filter by industry
    if industry != "All Industries":
        portals = [p for p in portals if industry in p["industries"]]
    
    # Show results
    for portal in portals:
        exp_val, date_val = get_filter_values(portal, experience, date_posted)
        show_portal_card(portal, keyword, location, exp_val, date_val)
    
    # Show results count
    if portals:
        st.success(f"✅ Found {len(portals)} specialized job sources for your search!")
    else:
        st.warning("⚠️ No job portals found matching your criteria. Try broader filters.")
