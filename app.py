# minimal_app.py
import streamlit as st
from streamlit_oauth import OAuth2Component

st.set_page_config(page_title="Minimal OAuth Test", layout="wide")

CLIENT_ID = st.secrets.get("OAUTH_CLIENT_ID", "")
CLIENT_SECRET = st.secrets.get("OAUTH_CLIENT_SECRET", "")
AUTHORIZE_URL = st.secrets.get("OAUTH_AUTHORIZE_URL", "")
TOKEN_URL = st.secrets.get("OAUTH_TOKEN_URL", "")
REFRESH_TOKEN_URL = st.secrets.get("OAUTH_REFRESH_TOKEN_URL", "")
REVOKE_TOKEN_URL = st.secrets.get("OAUTH_REVOKE_TOKEN_URL", "")
REDIRECT_URI = st.secrets.get("OAUTH_REDIRECT_URI", "")
SCOPE = "openid profile email"

oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'token' not in st.session_state:
    st.session_state.token = None

def show_login():
    st.title("Minimal OAuth Test")
    st.write(f"Redirect URI: {REDIRECT_URI}")
    result = oauth2.authorize_button("Login with Google", REDIRECT_URI, SCOPE)
    
    if result and 'token' in result:
        st.session_state.token = result.get('token')
        st.session_state.auth = True
        userinfo = oauth2.get_user_info(result.get('token'))
        st.session_state.user = userinfo
        st.write("Login successful, redirecting...")
        st.rerun()
    else:
        st.write("Please log in to continue.")

def main():
    if not st.session_state.auth:
        show_login()
        return
    
    st.write("Welcome to the dashboard!")
    st.write(f"Hello, {st.session_state.user.get('name', 'User')}!")

if __name__ == "__main__":
    main()
