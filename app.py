# ... (previous code remains the same until the Salary Insights section)

    elif choice == "Salary Insights":
        st.header("💰 Salary Comparison")
        
        col1, col2 = st.columns(2)
        with col1:
            job_title = st.text_input("Job Title for Salary Data", "Data Scientist")
        with col2:
            location = st.selectbox("Location", ["Remote", "New York", "San Francisco", "London"])
        
        if st.button("Get Salary Data"):
            salary = get_salary_data(job_title, location)
            st.metric(f"Average Salary for {job_title}", salary)
            
            # Show comparison chart
            salary_data = {
                "Position": ["Data Scientist", "Software Engineer", "Product Manager"],
                "Remote": [120000, 110000, 95000],
                "New York": [140000, 130000, 115000],
                "San Francisco": [150000, 140000, 125000]
            }
            df = pd.DataFrame(salary_data).melt(id_vars="Position", 
                                              var_name="Location", 
                                              value_name="Salary")
            
            fig = px.bar(df[df['Location'] == location], 
                         x="Position", y="Salary",
                         title=f"Salary Comparison in {location}")
            st.plotly_chart(fig, use_container_width=True)
    
    elif choice == "Settings":
        st.header("⚙️ Settings & Preferences")
        settings_section()
    
    # Show application form if triggered
    if 'show_application_form' in st.session_state and st.session_state.show_application_form:
        application_form()

# -------------------- Footer --------------------
def footer():
    st.markdown("""
    <style>
        .footer {
            background: linear-gradient(90deg, #2AB7CA 0%, #1A3550 100%);
            color: white;
            padding: 15px;
            border-radius: 12px 12px 0 0;
            text-align: center;
            font-size: 14px;
            margin-top: 40px;
        }
        .footer a {
            color: white;
            text-decoration: none;
            margin: 0 8px;
        }
    </style>
    <div class="footer">
        © 2025 CareerUpskillers | 
        <a href="https://www.careerupskillers.com/about-1">Privacy</a> | 
        <a href="https://wa.me/917892116728">WhatsApp</a> | 
        <a href="https://www.youtube.com/@Careerupskillers">YouTube</a> | 
        <a href="https://www.facebook.com/share/18gUeR73H6/">Facebook</a> | 
        <a href="https://www.linkedin.com/company/careerupskillers/">LinkedIn</a> | 
        <a href="https://www.instagram.com/careerupskillers?igsh=YWNmOGMwejBrb24z">Instagram</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    footer()
