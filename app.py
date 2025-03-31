import streamlit as st
import requests
from streamlit_oauth import OAuth2Component

# Set up the page
st.set_page_config(page_title="Auto Job Apply", page_icon="💼")
st.title("💼 Auto Job Apply App")
st.write("Log in to start applying for jobs automatically!")

# Initialize session state for authentication
if "auth" not in st.session_state:
    st.session_state.auth = False
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None

# Function to show the login page
def show_login():
    # Get OAuth details from Streamlit secrets
    try:
        CLIENT_ID = st.secrets["CLIENT_ID"]
        CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
        AUTHORIZE_URL = st.secrets["OAUTH_AUTHORIZE_URL"]
        TOKEN_URL = st.secrets["OAUTH_TOKEN_URL"]
        REFRESH_TOKEN_URL = st.secrets["OAUTH_REFRESH_TOKEN_URL"]
    except KeyError as e:
        st.error(f"Missing secret: {e}. Please check your Streamlit secrets configuration.")
        return

    # For Google OAuth, the user info endpoint is this
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    # Set the redirect URI based on whether we're on Streamlit Cloud or local
    REDIRECT_URI = "https://careerupskillers-auto-job-apply-jwvlomnmt8edxweekkezzv.streamlit.app"
    if "localhost" in st.secrets.get("BASE_URL", ""):  # Check if running locally
        REDIRECT_URI = "http://localhost:8501"

    # Create the OAuth2Component
    oauth2 = OAuth2Component(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        authorize_endpoint=AUTHORIZE_URL,
        token_endpoint=TOKEN_URL,
        refresh_token_endpoint=REFRESH_TOKEN_URL,
        redirect_uri=REDIRECT_URI
    )

    # Show the login button
    result = oauth2.authorize_button(
        name="Login with Google",
        scope="email profile",  # Request access to email and profile info
        icon="https://www.google.com/favicon.ico",
        redirect_uri=REDIRECT_URI,
        key="google_oauth"
    )

    # If the user logs in successfully, get their info
    if result and 'token' in result:
        st.session_state.token = result.get('token')
        st.session_state.auth = True

        # Use the token to get user info
        headers = {"Authorization": f"Bearer {result.get('token')}"}
        response = requests.get(USER_INFO_URL, headers=headers)

        if response.status_code == 200:
            userinfo = response.json()
            st.session_state.user = userinfo
            st.rerun()  # Refresh the app to show the dashboard
        else:
            st.error(f"Failed to fetch user info. Status code: {response.status_code}. Please try again.")

# Function to show the footer (from your logs)
def footer():
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <p>Built with ❤️ by CareerUpskillers | <a href='https://careerupskillers.com'>Visit Us</a></p>
    </div>
    """, unsafe_allow_html=True)

# Main function to show the dashboard after login
def main():
    # Check authentication
    if not st.session_state.auth:
        show_login()
        return

    # If authenticated, show the dashboard
    st.write(f"Welcome, {st.session_state.user.get('name', 'User')}!")
    st.write(f"Email: {st.session_state.user.get('email', 'N/A')}")
    st.write("You’re logged in! Let’s start applying for jobs.")

    # Add your job application logic here
    st.write("This is where the auto job apply magic will happen! 🪄")

# Run the app
if __name__ == "__main__":
    main()
    footer()
