import streamlit as st
import streamlit.components.v1 as components
import requests
import os

st.set_page_config(page_title="CROSSCURRENT", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');
    
    /* Hide Streamlit UI Chrome (Share/Deploy/Header/Footer) */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    
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

    /* Logo Responsive Styles */
    .logo-left {
        position: fixed; top: 20px; left: 25px; z-index: 999999;
    }
    .logo-left img { height: 80px; filter: drop-shadow(0 0 15px rgba(212,255,0,0.3)); }
    .logo-center {
        position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 999999;
    }
    .logo-center img { height: 150px; filter: drop-shadow(0 0 15px rgba(212,255,0,0.3)); }
    .logo-right {
        position: fixed; top: 20px; right: 25px; z-index: 999999;
    }
    .logo-right img { height: 80px; filter: drop-shadow(0 0 15px rgba(212,255,0,0.3)); }

    @media (max-width: 768px) {
        .logo-left  { top: 8px; left: 10px; }
        .logo-left img  { height: 40px; }
        .logo-center { top: 8px; }
        .logo-center img { height: 75px; }
        .logo-right { top: 8px; right: 10px; }
        .logo-right img { height: 40px; }

        /* On mobile, reduce spacing above game content */
        .game-mobile-spacer { display: none !important; }
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
    <div class="logo-left">
        <img src="{API_URL}/static/images/cas.png">
    </div>
    <div class="logo-center">
        <img src="{API_URL}/static/images/illume.png">
    </div>
    <div class="logo-right">
        <img src="{API_URL}/static/images/tree.png">
    </div>
    """, unsafe_allow_html=True)

def login_page():
    render_logos()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #D4FF00 !important; text-shadow: 0 0 10px rgba(212, 255, 0, 0.3); text-align: center;'>CROSSCURRENT</h1>", unsafe_allow_html=True)
    
    # Check if admin access via query param: ?admin=true
    query_params = st.query_params
    is_admin_mode = query_params.get("admin", "") == "true"
    
    if is_admin_mode:
        st.subheader("Admin Login")
        admin_username = st.text_input("Admin Username")
        admin_password = st.text_input("Admin Password", type="password")
        if st.button("Login as Admin"):
            if admin_username and admin_password:
                try:
                    res = requests.post(f"{API_URL}/admin/login", json={"username": admin_username, "password": admin_password})
                    if res.status_code == 200:
                        st.session_state.user = admin_username
                        st.session_state.is_admin = True
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                except Exception as e:
                    st.error(f"Backend not available. Error: {e}")
    else:
        st.subheader("Join the Competition")
        username = st.text_input("Enter your username to play:")
        event_password = st.text_input("Enter event password:", type="password")
        if st.button("Start Playing"):
            if username and event_password:
                if event_password != "crosscurrent_2026":
                    st.error("Invalid Password.")
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

def game_page():
    render_logos()
    st.markdown('<div class="game-mobile-spacer"><br><br></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([4, 2, 1])
    with col1:
        st.markdown(f"<p style='color: #D4FF00; font-family: Orbitron, sans-serif; font-size: 0.9em; letter-spacing: 2px; margin:0;'>PLAYER: {st.session_state.user}</p>", unsafe_allow_html=True)
    with col3:
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.is_admin = False
            st.rerun()

    # Read the HTML file for the crossword component
    html_path = os.path.join(os.path.dirname(__file__), "static", "crossword.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # Inject username into html to send to backend on completion
    html_content = html_content.replace("var current_username = '';", f"var current_username = '{st.session_state.user}';")
    html_content = html_content.replace("var api_url = '';", f"var api_url = '{API_URL}';")
    
    # Use srcdoc iframe with allowfullscreen so the fullscreen button works on mobile
    import base64
    encoded = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
    st.markdown(
        f'<iframe id="crossword-frame" src="data:text/html;base64,{encoded}" '
        f'width="100%" height="900" '
        f'allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true" '
        f'frameborder="0" style="border:none;"></iframe>'
        f'<style>@media (max-width: 768px) {{ #crossword-frame {{ height: 85vh !important; }} }}</style>',
        unsafe_allow_html=True
    )

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
