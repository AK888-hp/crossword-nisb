import streamlit as st
import streamlit.components.v1 as components
import requests
import os

st.set_page_config(page_title="CROSSCURRENT", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');
    
    /* Global Font Overrides */
    html, body, [class*="css"], .stApp, p, span, div, label, input, button {
        font-family: 'Rajdhani', sans-serif !important;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 1px;
    }

    /* ILLUME Theme for Streamlit */
    .stApp {
        background: linear-gradient(-45deg, #000000, #081100, #142a00, #000000);
        background-size: 400% 400%;
        animation: aurora 15s ease infinite;
        color: #FFFFFF;
    }
    @keyframes aurora {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    h1 {
        color: #D4FF00 !important;
        text-shadow: 0 0 10px rgba(212, 255, 0, 0.3) !important;
    }
    h1 * {
        color: #D4FF00 !important;
    }
    h2, h3, h4, h5, h6, p, span, div, label {
        color: #FFFFFF;
    }

    .stButton>button {
        background-color: transparent !important;
        color: #D4FF00 !important;
        border: 2px solid #D4FF00 !important;
        border-radius: 0px !important;
        font-weight: 800 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #D4FF00 !important;
        color: #000000 !important;
        box-shadow: 0 0 15px rgba(212, 255, 0, 0.5) !important;
    }
    .stTextInput>div>div>input {
        background-color: #111111 !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 0px !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #D4FF00 !important;
        box-shadow: 0 0 5px rgba(212, 255, 0, 0.3) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #000000;
    }
    .stTabs [data-baseweb="tab"] {
        color: #888888 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #D4FF00 !important;
        border-bottom-color: #D4FF00 !important;
    }
</style>
""", unsafe_allow_html=True)

API_URL = os.environ.get("API_URL", "http://localhost:8000")

def init_session():
    if "user" not in st.session_state:
        st.session_state.user = None
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False

init_session()

def render_logos():
    st.markdown(f"""
    <div style="position: fixed; top: 20px; left: 25px; z-index: 999999;">
        <img src="{API_URL}/static/images/cas.png" style="height: 80px; filter: drop-shadow(0 0 15px rgba(212,255,0,0.3));">
    </div>
    <div style="position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 999999;">
        <img src="{API_URL}/static/images/illume.png" style="height: 150px; filter: drop-shadow(0 0 15px rgba(212,255,0,0.3));">
    </div>
    <div style="position: fixed; top: 20px; right: 25px; z-index: 999999;">
        <img src="{API_URL}/static/images/tree.png" style="height: 80px; filter: drop-shadow(0 0 15px rgba(212,255,0,0.3));">
    </div>
    """, unsafe_allow_html=True)

def login_page():
    render_logos()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #D4FF00 !important; text-shadow: 0 0 10px rgba(212, 255, 0, 0.3); text-align: center;'>CROSSCURRENT</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Player Login", "Admin Login"])
    
    with tab1:
        st.subheader("Join the Competition")
        username = st.text_input("Enter your username to play:")
        event_password = st.text_input("Enter event password:", type="password")
        if st.button("Start Playing"):
            if username and event_password:
                if event_password != "ILLUME_CROSSCURRENT_123":
                    st.error("Invalid Event Password.")
                else:
                    try:
                        res = requests.post(f"{API_URL}/login", json={"username": username})
                        if res.status_code == 200:
                            data = res.json()
                            st.session_state.user = data["username"]
                            st.session_state.is_admin = data.get("is_admin", False)
                            st.rerun()
                        else:
                            st.error("Failed to login.")
                    except Exception as e:
                        st.error(f"Backend not available. Error: {e}")
            else:
                st.warning("Please enter both username and event password.")
                
    with tab2:
        st.subheader("Admin Login")
        admin_username = st.text_input("Admin Username")
        admin_password = st.text_input("Admin Password", type="password")
        if st.button("Login as Admin"):
            if admin_username and admin_password:
                try:
                    res = requests.post(f"{API_URL}/admin/login", json={"username": admin_username, "password": admin_password})
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.user = admin_username
                        st.session_state.is_admin = True
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                except Exception as e:
                    st.error(f"Backend not available. Error: {e}")

def game_page():
    render_logos()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color: #D4FF00 !important; text-shadow: 0 0 10px rgba(212, 255, 0, 0.3); text-align: center;'>CROSSCURRENT: Welcome, {st.session_state.user}!</h1>", unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.is_admin = False
        st.rerun()
        
    st.markdown("### Crossword Puzzle")
    st.write("Click on a box to see the clue. Correct answers will automatically lock in.")

    # Read the HTML file for the crossword component
    html_path = os.path.join(os.path.dirname(__file__), "static", "crossword.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # Inject username into html to send to backend on completion
    html_content = html_content.replace("var current_username = '';", f"var current_username = '{st.session_state.user}';")
    html_content = html_content.replace("var api_url = '';", f"var api_url = '{API_URL}';")
    
    components.html(html_content, height=1200, scrolling=False)

def admin_page():
    render_logos()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #D4FF00 !important; text-shadow: 0 0 10px rgba(212, 255, 0, 0.3); text-align: center;'>Admin Dashboard</h1>", unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.is_admin = False
        st.rerun()
        
    st.header("Leaderboard")
    try:
        res = requests.get(f"{API_URL}/leaderboard")
        if res.status_code == 200:
            scores = res.json()
            if not scores:
                st.info("No scores yet.")
            else:
                for i, score in enumerate(scores):
                    st.write(f"**{i+1}. {score['username']}** - Time: {score['time_seconds']}s")
        else:
            st.error("Failed to fetch leaderboard.")
    except Exception as e:
         st.error("Backend not available.")

# App Routing
if not st.session_state.user:
    login_page()
elif st.session_state.is_admin:
    admin_page()
else:
    game_page()
