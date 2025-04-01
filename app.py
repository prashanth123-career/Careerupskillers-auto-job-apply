import streamlit as st
import urllib.parse

st.set_page_config(page_title="🌍 Global AI Job Finder", page_icon="🌎", layout="centered")

# Company type mappings
COMPANY_TYPES = {
    "Product": "Product-based companies develop their own products/services",
    "Service": "Service-based companies provide IT services to clients",
    "Both": "Show all company types"
}

# ---------------- LinkedIn Smart Filtered Link ----------------
def linkedin_url(keyword, location, time_filter, experience, remote_option, easy_apply, company_type):
    time_map = {
        "Past 24 hours": "r86400",
        "Past week": "r604800",
        "Past month": "r2592000",
        "Any time": ""
    }
    exp_map = {
        "Any": "",
        "Internship": "1",
        "Entry level": "2",
        "Associate": "3",
        "Mid-Senior level": "4",
        "Director": "5"
    }
    remote_map = {
        "Any": "",
        "Remote": "2",
        "On-site": "1",
        "Hybrid": "3"
    }
    
    # Company type filters
    company_filters = {
        "Product": ["tech", "saas", "product", "startup"],
        "Service": ["consulting", "services", "outsourcing", "solution"]
    }

    params = {
        "keywords": f"{keyword} {' '.join(company_filters.get(company_type, []))}",
        "location": location,
        "f_TPR": time_map.get(time_filter, ""),
        "f_E": exp_map.get(experience, ""),
        "f_WT": remote_map.get(remote_option, ""),
        "f_AL": "true" if easy_apply else ""
    }

    return f"https://www.linkedin.com/jobs/search/?{urllib.parse.urlencode({k: v for k, v in params.items() if v})}"

# ---------------- Indeed Smart Filtered Link ----------------
def indeed_url(keyword, location, country, salary=None, company_type="Both"):
    domain_map = {
        "USA": "www.indeed.com",
        "UK": "uk.indeed.com",
        "Canada": "ca.indeed.com",
        "Australia": "au.indeed.com",
        "India": "www.indeed.co.in"
    }
    
    base_url = f"https://{domain_map.get(country, 'www.indeed.com')}/jobs"
    
    # Add company type keywords
    company_keywords = {
        "Product": ["product", "startup", "tech company"],
        "Service": ["consulting", "services", "IT services"]
    }.get(company_type, [])
    
    full_query = f"{keyword} {' '.join(company_keywords)}" if company_type != "Both" else keyword
    
    params = {
        "q": full_query,
        "l": location
    }
    
    if salary and country != "India":
        params["salary"] = salary
    
    return f"{base_url}?{urllib.parse.urlencode(params)}"

# ---------------- UI ----------------
st.title("🌍 Global AI Job Finder")
st.markdown("🔎 Get LinkedIn + top job portals for any country with smart filters!")

with st.form("job_form"):
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("Job Title / Keywords", "Data Scientist")
        location = st.text_input("Preferred Location", "Remote")
        country = st.selectbox("🌐 Country", ["USA", "UK", "India", "Australia", "Canada", "Others"])
        
    with col2:
        company_type = st.selectbox(
            "🏢 Company Type",
            options=list(COMPANY_TYPES.keys()),
            format_func=lambda x: COMPANY_TYPES[x],
            help="Product-based companies build their own products. Service-based provide IT services to clients."
        )
        
        if country != "India":
            salary = st.number_input("💰 Minimum Salary (per year)", min_value=0, value=0, step=10000)
        else:
            salary = None
    
    time_filter = st.selectbox("📅 LinkedIn Date Posted", ["Past 24 hours", "Past week", "Past month", "Any time"])
    experience = st.selectbox("📈 Experience Level", ["Any", "Internship", "Entry level", "Associate", "Mid-Senior level", "Director"])
    remote_option = st.selectbox("🏠 Work Arrangement", ["Any", "Remote", "On-site", "Hybrid"])
    easy_apply = st.checkbox("⚡ Easy Apply only", value=False)
    
    submitted = st.form_submit_button("🔍 Find Jobs")

if submitted:
    st.subheader("🔗 LinkedIn Smart Search")
    linkedin_link = linkedin_url(keyword, location, time_filter, experience, remote_option, easy_apply, company_type)
    st.markdown(f"✅ [Open LinkedIn Search]({linkedin_link})")

    st.subheader(f"🌐 Job Portals in {country}")
    for name, url in generate_job_links(keyword, location, country, salary if salary else None, company_type):
        st.markdown(f"- 🔗 [{name}]({url})")

    # Company type explanation
    with st.expander("ℹ️ About Company Types"):
        st.markdown("""
        **Product-based Companies** 🏭:
        - Develop their own software/products
        - Examples: Google, Microsoft, Adobe
        - Pros: More focus on product innovation, often better compensation
        
        **Service-based Companies** 🤝:
        - Provide IT services to client organizations
        - Examples: TCS, Infosys, Accenture
        - Pros: Exposure to multiple domains, stable projects
        
        Why choose one over another?
        - Product companies offer deeper technical work on specific products
        - Service companies provide broader domain exposure
        - Compensation and work culture varies significantly between types
        """)

    st.success("🎯 All job search links generated successfully!")
