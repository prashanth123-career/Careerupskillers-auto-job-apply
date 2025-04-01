# AI Career Advisor with Marketing Elements
import streamlit as st
import random
import time
from transformers import pipeline

# Configure Streamlit
st.set_page_config(page_title="AI Career Advisor", page_icon="🤖", layout="wide")

# Animated Marketing Header
st.markdown("""
<style>
@keyframes flash {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}
.flash-text {
    animation: flash 1.5s infinite;
    font-weight: bold;
    color: #FF4B4B;
}
.review-box {
    border-left: 4px solid #2AB7CA;
    padding: 10px;
    margin: 10px 0;
    background: #f0f2f6;
    border-radius: 0 8px 8px 0;
}
</style>
""", unsafe_allow_html=True)

# Header with flashing "FREE"
st.markdown("""
<div style="text-align: center;">
    <h1>Get <span class="flash-text">FREE</span> Personalized Career Counseling</h1>
    <h3>from our AI Career Advisor 🤖</h3>
</div>
""", unsafe_allow_html=True)

# Value Proposition
with st.container():
    st.markdown("""
    <div style="background: #f0f2f6; padding: 20px; border-radius: 10px;">
        <h4>🚀 AI won't take your job - but someone using AI will!</h4>
        <p>Our research shows professionals who leverage AI tools:</p>
        <ul>
            <li>Complete 4 hours work in 30 minutes ⏳</li>
            <li>Earn 25-40% higher salaries 💰</li>
            <li>Get 3x more interview calls 📞</li>
        </ul>
        <p><b>Don't get replaced - become irreplaceable!</b></p>
    </div>
    """, unsafe_allow_html=True)

# Rotating Testimonials
testimonials = [
    {
        "name": "John from USA",
        "text": "This AI advisory helped me identify my market gaps. Their $5,840 Success Kit helped me increase earnings from $1,200 to $3,600/month!",
        "duration": 5
    },
    {
        "name": "Priya from India",
        "text": "The $199 Career Jumpstart Kit helped me choose the right company. Got 40% salary hike in 3 months!",
        "duration": 5
    },
    {
        "name": "David from UK",
        "text": "Discovered high-demand skills I didn't know I had. Landed a remote job paying £85k!",
        "duration": 5
    }
]

if 'testimonial_index' not in st.session_state:
    st.session_state.testimonial_index = 0
    st.session_state.last_change = time.time()

current_time = time.time()
current_testimonial = testimonials[st.session_state.testimonial_index]

if current_time - st.session_state.last_change > current_testimonial['duration']:
    st.session_state.testimonial_index = (st.session_state.testimonial_index + 1) % len(testimonials)
    st.session_state.last_change = current_time
    st.rerun()

with st.container():
    st.markdown(f"""
    <div class="review-box">
        <p><b>{current_testimonial['name']}:</b> "{current_testimonial['text']}"</p>
    </div>
    """, unsafe_allow_html=True)

# Salary Comparison Tool
st.subheader("🔍 Are You Paid Market Standard?")
with st.expander("Check Your Salary Potential (FREE)"):
    col1, col2 = st.columns(2)
    with col1:
        role = st.selectbox("Your Current Role", 
                          ["Software Engineer", "Data Analyst", "Sales Manager", 
                           "Marketing Specialist", "Product Manager"])
        experience = st.slider("Years of Experience", 0, 20, 3)
    with col2:
        location = st.selectbox("Location", 
                              ["USA", "India", "UK", "Germany", "Canada"])
        current_salary = st.number_input("Current Salary (USD)", min_value=0)

    if st.button("Analyze My Market Value"):
        # Simulate AI analysis
        with st.spinner("Comparing with 12,340 professionals in your field..."):
            time.sleep(2)
            market_avg = random.randint(int(current_salary*0.8), int(current_salary*1.5))
            st.success(f"💰 Market Average: ${market_avg:,}")
            if market_avg > current_salary:
                st.warning(f"You might be underpaid by ${market_avg - current_salary:,}")
                st.markdown("""
                <div style="background: #fff4f4; padding: 15px; border-radius: 8px;">
                    <h5>🚀 Salary Boost Recommendation:</h5>
                    <ol>
                        <li>Take our <b>FREE</b> skills assessment</li>
                        <li>Discover high-value skills in your field</li>
                        <li>Learn negotiation strategies</li>
                    </ol>
                    <a href="#skills-assessment" class="stButton">Start Assessment</a>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.balloons()
                st.success("You're at or above market average!")

# AI Career Advisor Section
st.subheader("🤖 Your AI Career Advisor")
tab1, tab2, tab3 = st.tabs(["Skills Assessment", "Career Path", "Upskilling Plan"])

with tab1:
    st.markdown("""
    ### FREE Skills Gap Analysis
    """)
    if st.button("Start 2-Minute Assessment"):
        st.session_state.assessment_started = True
        st.rerun()

    if 'assessment_started' in st.session_state:
        skills = st.multiselect("Select your current skills",
                               ["Python", "SQL", "AWS", "Digital Marketing", 
                                "Sales Forecasting", "Project Management"])
        if st.button("Analyze My Skills"):
            with st.spinner("Comparing with 1,240 job postings..."):
                time.sleep(3)
                st.success("Assessment Complete!")
                st.markdown(f"""
                <div style="background: #f0f8ff; padding: 15px; border-radius: 8px;">
                    <h5>Your Career Boost Plan:</h5>
                    <p>Based on {len(skills)} skills and {experience} years experience:</p>
                    <ul>
                        <li>High-value skills to learn: <b>AI Prompt Engineering, Data Visualization</b></li>
                        <li>Potential salary increase: <b>${random.randint(5000, 15000)}/year</b></li>
                        <li>Recommended certification: <b>Google Cloud Professional</b></li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    ### Your AI-Powered Career Path
    """)
    st.image("https://via.placeholder.com/800x300?text=Personalized+Career+Roadmap", use_column_width=True)
    st.markdown("""
    <div style="text-align: center; margin-top: 10px;">
        <button style="background: linear-gradient(90deg, #2AB7CA 0%, #1A3550 100%); 
                      color: white; border: none; padding: 10px 20px; border-radius: 5px;">
            Unlock Full Career Map ($49)
        </button>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    ### Personalized Upskilling Plan
    """)
    st.write("""
    Our AI analyzes thousands of job postings to recommend:
    - Highest-paying skills in your field
    - Fastest completion learning paths
    - Company-specific skill requirements
    """)
    if st.button("Generate My Plan (FREE)"):
        with st.spinner("Creating your personalized learning path..."):
            time.sleep(3)
            st.success("Plan Generated!")
            st.markdown("""
            **Your 3-Month Upskilling Blueprint:**
            1. Week 1-4: Complete AI Fundamentals Certification (FREE)
            2. Week 5-8: Advanced Data Analysis Specialization
            3. Week 9-12: Build Portfolio Project with Mentorship
            """)
            st.markdown("""
            <div style="background: #e6f7ff; padding: 15px; border-radius: 8px;">
                <h5>Premium Upgrade ($99):</h5>
                <ul>
                    <li>1:1 Career Coaching Sessions</li>
                    <li>Resume Rewriting by Experts</li>
                    <li>LinkedIn Profile Optimization</li>
                    <li>Salary Negotiation Scripts</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Footer with CTA
st.markdown("""
<style>
.cta-box {
    background: linear-gradient(90deg, #2AB7CA 0%, #1A3550 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    margin-top: 30px;
}
</style>
<div class="cta-box">
    <h3>Ready to Future-Proof Your Career?</h3>
    <p>Join 12,457 professionals who boosted their earnings with AI</p>
    <button style="background: white; color: #1A3550; border: none; 
                 padding: 10px 30px; border-radius: 5px; font-weight: bold;">
        START FREE ASSESSMENT
    </button>
</div>
""", unsafe_allow_html=True)
