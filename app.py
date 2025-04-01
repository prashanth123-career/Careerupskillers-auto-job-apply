# -------------------- Streamlit App --------------------
st.markdown("""
<style>
    .branding {background: linear-gradient(90deg, #2AB7CA 0%, #1A3550 100%); color: white; padding: 15px; border-radius: 0 0 12px 12px; text-align: center; font-size: 14px; margin-bottom: 10px;}
    .branding a {color: white; text-decoration: none; margin: 0 8px;}
</style>
<div class="branding">
    © 2025 CareerUpskillers | 
    <a href="https://www.careerupskillers.com/about-1">Privacy</a> | 
    <a href="https://wa.me/917892116728">WhatsApp</a> | 
    <a href="https://www.youtube.com/@Careerupskillers">YouTube</a> | 
    <a href="https://www.facebook.com/share/18gUeR73H6/">Facebook</a> | 
    <a href="https://www.linkedin.com/company/careerupskillers/">LinkedIn</a> | 
    <a href="https://www.instagram.com/careerupskillers?igsh=YWNmOGMwejBrb24z">Instagram</a>
</div>
""", unsafe_allow_html=True)

st.title("💼 All-in-One Job Auto-Applier")
st.markdown("Apply smartly with AI-powered cover letters and resume autofill.")

st.subheader("📄 Upload Your Resume")
resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
resume_text = ""
if resume_file:
    resume_text = parse_resume(resume_file)
    st.success("Resume uploaded and parsed successfully!")

st.subheader("👤 Candidate Details")
designation = st.text_input("Your Designation (e.g., Data Analyst, AI Engineer)")
target_role = st.text_input("Target Role or Job Title (e.g., ML Intern, Business Analyst)")
skills = st.text_input("Your Skills (comma-separated, e.g., Python, ML, SQL)")
experience = st.number_input("Years of Experience", min_value=0.0, max_value=30.0, step=0.1, format="%.1f")

st.text(f"✔️ Example: 3.5 or 5.1 years allowed")

st.subheader("🌍 Job Location Preferences")
current_location = st.text_input("Current Location (City, Country)")
interested_location = st.text_input("Preferred Location for Jobs")
current_salary = st.text_input("Current Salary (Optional)")
expected_salary = st.text_input("Expected Salary")

st.subheader("🔍 Job Search Filters")
keyword = st.text_input("Job Title / Keywords", value="Data Science")
location = st.text_input("Search Location", value="Remote")
use_gpt = st.checkbox("Generate AI-based Cover Letter", value=True)
mode = st.radio("Application Mode", ["Manual Click", "Auto Apply (coming soon)"])

if st.button("Search Jobs"):
    if not designation.strip():
        st.error("❌ Please enter your current designation.")
    elif not target_role.strip():
        st.error("❌ Please enter your target role.")
    elif not skills.strip():
        st.error("❌ Please enter your key skills.")
    elif not current_location.strip():
        st.error("❌ Please enter your current location.")
    elif not interested_location.strip():
        st.error("❌ Please enter your preferred job location.")
    elif not expected_salary.strip():
        st.error("❌ Please enter your expected salary.")
    elif not resume_file:
        st.error("❌ Please upload your resume.")
    else:
        with st.spinner("Searching for jobs..."):
            results = []
            results.extend(scrape_monster(keyword, location))
            results.extend(scrape_angellist(keyword, location))
            results.extend(scrape_internshala(keyword))
            results.extend(scrape_naukri(keyword, location))
            results.extend(scrape_indeed(keyword, location))
            results.extend(scrape_timesjobs(keyword))
            results.extend(scrape_linkedin(keyword, location))

        if results:
            st.subheader("📋 Job Results")
            log = []
            for i, job in enumerate(results):
                st.write(f"**{i+1}. {job['Title']}** at {job['Company']} ({job['Platform']})")
                if use_gpt:
                    cover_letter = generate_cover_letter(resume_text, job['Title'])
                    with st.expander("View AI-Generated Cover Letter"):
                        st.text(cover_letter)
                st.markdown(f"[🖱️ Click to Apply]({job['Link']})")
                log.append({
                    "Title": job['Title'],
                    "Company": job['Company'],
                    "Platform": job['Platform'],
                    "Link": job['Link'],
                    "Experience": experience,
                    "Expected Salary": expected_salary,
                    "Time": datetime.now()
                })

            df = pd.DataFrame(log)
            df.to_csv("applied_jobs_log.csv", index=False)
            st.success("📁 Log saved as applied_jobs_log.csv")

            # send_email_alert(email, len(results))  # Email removed since email input is removed
            # send_whatsapp_alert(phone, len(results))  # WhatsApp removed too
        else:
            st.error("❌ No jobs found on any platform. Try different filters.")
