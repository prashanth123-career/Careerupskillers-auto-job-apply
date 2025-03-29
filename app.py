if st.button("Search Jobs") and keyword and platforms:
    st.info("Searching jobs on selected platforms...")
    results = []
    
    for platform in platforms:
        try:
            if platform == "Internshala":
                scraped = scrape_internshala(keyword)
                results += scraped
                st.write(f"✅ Internshala found: {len(scraped)} jobs")
            elif platform == "Naukri":
                scraped = scrape_naukri(keyword, location)
                results += scraped
                st.write(f"✅ Naukri found: {len(scraped)} jobs")
            elif platform == "Indeed":
                scraped = scrape_indeed(keyword, location)
                results += scraped
                st.write(f"✅ Indeed found: {len(scraped)} jobs")
            elif platform == "TimesJobs":
                scraped = scrape_timesjobs(keyword, location)
                results += scraped
                st.write(f"✅ TimesJobs found: {len(scraped)} jobs")
            elif platform == "LinkedIn":
                st.warning("LinkedIn supports only manual click mode. Showing jobs only.")
        except Exception as e:
            st.error(f"❌ Error while scraping {platform}: {e}")

    if results:
        st.success(f"Found {len(results)} jobs across platforms.")
        # (continue with your display logic)
    else:
        st.warning("No jobs found. Try different filters or check logs.")
