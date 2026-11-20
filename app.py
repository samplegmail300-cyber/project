"""
Doctor AI - Main Streamlit application.
Homepage, navigation and integrated chatbot.
"""

import html

import streamlit as st
from chatbot import get_bot_response
from symptoms import check_symptoms, SUPPORTED_SYMPTOMS
from diseases import get_disease_names, get_disease_info

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Doctor AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# 2. APP SETTINGS
# --------------------------------------------------

APP_TITLE = "Doctor AI"
APP_SUBTITLE = "Your Intelligent Healthcare Assistant"

NAV_OPTIONS = [
    "🏠 Home",
    "🤖 AI Chatbot",
    "🩺 Symptom Checker",
    "📚 Disease Information",
    "ℹ️ About",
]

# Each feature: (icon, title, description, page to open, button text)
FEATURES = [
    (
        "🤖",
        "AI Chatbot",
        "Chat with a friendly assistant and ask general health questions "
        "in plain language.",
        "🤖 AI Chatbot",
        "Open Chatbot →",
    ),
    (
        "🩺",
        "Symptom Checker",
        "Select your symptoms and learn which common conditions they "
        "may be related to.",
        "🩺 Symptom Checker",
        "Check Symptoms →",
    ),
    (
        "📚",
        "Disease Information",
        "Read simple explanations about common diseases, their causes "
        "and prevention.",
        "📚 Disease Information",
        "Explore Diseases →",
    ),
    (
        "💡",
        "Health Guidance",
        "Get general wellness tips and advice on when to see a "
        "healthcare professional.",
        "ℹ️ About",
        "Learn More →",
    ),
]

HOW_IT_WORKS = [
    (
        "Ask or select",
        "Type a health question, pick your symptoms, or choose a "
        "condition you want to learn about.",
    ),
    (
        "Get simple information",
        "Doctor AI shares general, easy-to-read health information "
        "and self-care tips.",
    ),
    (
        "Talk to a professional",
        "Use the guidance to decide when to visit a doctor. Doctor AI "
        "never replaces one.",
    ),
]

CHAT_SUGGESTIONS = [
    "I have a fever",
    "How can I stay healthy?",
    "What helps a sore throat?",
    "I have a headache",
]

AVATARS = {"user": "🙂", "assistant": "🩺"}

# Disease page sections: (key in info, icon, title, colour style)
DISEASE_SECTIONS = [
    ("symptoms", "🌡️", "Common Symptoms", "c-symptoms"),
    ("causes", "🔍", "Possible Causes", "c-causes"),
    ("prevention", "🛡️", "Prevention Tips", "c-prevention"),
    ("when_to_consult", "👩‍⚕️", "When to Consult a Doctor", "c-doctor"),
]


# --------------------------------------------------
# 3. CUSTOM CSS
# --------------------------------------------------

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    :root {
        --primary: #0b6e99;
        --primary-dark: #084c6b;
        --primary-deep: #063a54;
        --accent: #12a4a4;
        --accent-soft: #e3f6f5;
        --light-bg: #f2f8fb;
        --card-border: #d6e6ee;
        --text-dark: #1d3557;
        --text-muted: #5b6f82;
        --danger: #d64545;
        --shadow: 0 8px 24px rgba(8, 76, 107, 0.10);
    }

    /* ---------- Page background and fonts ---------- */
    .stApp {
        font-family: 'Poppins', 'Segoe UI', sans-serif;
        background:
            radial-gradient(circle at 0% 0%, #dff1f7 0, transparent 38%),
            radial-gradient(circle at 100% 100%, #dcf5f1 0, transparent 38%),
            #f6fafc;
    }

    .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    .stApp p, .stApp li, .stApp label, .stApp button {
        font-family: 'Poppins', 'Segoe UI', sans-serif;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        animation: fadeUp 0.5s ease both;
    }

    .block-container h1,
    .block-container h2,
    .block-container h3,
    .block-container h4 {
        color: var(--text-dark);
    }

    .block-container p,
    .block-container li,
    .block-container label {
        color: var(--text-dark);
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #063a54 0%, #0b6e99 62%, #12a4a4 100%);
    }

    section[data-testid="stSidebar"] * {
        color: #eaf6fa;
    }

    .side-logo {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 0.4rem 0.2rem 0.2rem 0.2rem;
    }

    .side-logo-icon {
        width: 46px;
        height: 46px;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.18);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
    }

    .side-title {
        font-size: 1.25rem;
        font-weight: 700;
        line-height: 1.1;
    }

    .side-sub {
        font-size: 0.75rem;
        opacity: 0.85;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"],
    section[data-testid="stSidebar"] div[role="radiogroup"] {
        width: 100%;
        gap: 0.4rem;
    }

    section[data-testid="stSidebar"] [data-testid="stRadioGroup"] {
        align-items: stretch;
    }

    section[data-testid="stSidebar"] [data-testid="stRadioGroup"] > div {
        width: 100%;
    }

    /* Hide the small link icon Streamlit adds next to headings */
    [data-testid="stHeaderActionElements"] {
        display: none;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 12px;
        padding: 0.55rem 0.8rem;
        display: flex;
        align-items: center;
        width: 100% !important;
        box-sizing: border-box;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(4px);
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        background: #ffffff;
        border-color: #ffffff;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18);
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) * {
        color: var(--primary-dark);
        font-weight: 600;
    }

    /* ---------- Hero (home page) ---------- */
    .hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #063a54 0%, #0b6e99 55%, #12a4a4 100%);
        border-radius: 24px;
        padding: 3rem 2rem 2.6rem 2rem;
        text-align: center;
        color: white;
        margin-bottom: 1.6rem;
        box-shadow: 0 14px 34px rgba(8, 76, 107, 0.28);
    }

    .hero::before,
    .hero::after {
        content: "";
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.08);
    }

    .hero::before {
        width: 280px;
        height: 280px;
        top: -100px;
        right: -60px;
    }

    .hero::after {
        width: 190px;
        height: 190px;
        bottom: -80px;
        left: -50px;
    }

    .hero h1 {
        position: relative;
        margin: 0;
        font-size: 2.9rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        color: white !important;
    }

    .hero p {
        position: relative;
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.93) !important;
    }

    .hero-badges {
        position: relative;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.6rem;
        margin-top: 1.3rem;
    }

    .hero-badge {
        background: rgba(255, 255, 255, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.32);
        color: white;
        padding: 0.3rem 0.95rem;
        border-radius: 999px;
        font-size: 0.85rem;
        backdrop-filter: blur(4px);
    }

    /* ---------- Page banner (other pages) ---------- */
    .page-banner {
        display: flex;
        align-items: center;
        gap: 1.1rem;
        background: linear-gradient(135deg, #063a54 0%, #0b6e99 60%, #12a4a4 100%);
        border-radius: 20px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 10px 26px rgba(8, 76, 107, 0.22);
    }

    .page-icon {
        flex-shrink: 0;
        width: 64px;
        height: 64px;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.18);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.2rem;
    }

    .page-banner h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        color: white !important;
    }

    .page-banner p {
        margin: 0.2rem 0 0 0;
        color: rgba(255, 255, 255, 0.92) !important;
    }

    /* ---------- Section titles ---------- */
    .section-title {
        color: var(--text-dark);
        font-weight: 700;
        margin: 1.8rem 0 0.9rem 0;
    }

    /* ---------- Stats strip ---------- */
    .stats {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 1rem 0 0.4rem 0;
    }

    .stat {
        background: white;
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 1rem 0.8rem;
        text-align: center;
        box-shadow: var(--shadow);
    }

    .stat-num {
        font-size: 1.9rem;
        font-weight: 700;
        line-height: 1.2;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    .stat-label {
        color: var(--text-muted);
        font-size: 0.85rem;
    }

    /* ---------- Feature cards ---------- */
    .feature-card {
        background: white;
        border: 1px solid var(--card-border);
        border-top: 4px solid var(--accent);
        border-radius: 18px;
        padding: 1.5rem 1.2rem;
        min-height: 310px;
        text-align: center;
        box-shadow: var(--shadow);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .feature-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 14px 28px rgba(11, 110, 153, 0.20);
    }

    .feature-icon {
        width: 66px;
        height: 66px;
        margin: 0 auto 0.7rem auto;
        border-radius: 20px;
        background: linear-gradient(135deg, var(--accent-soft), #dcedf6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.1rem;
    }

    .feature-card h3 {
        color: var(--primary);
        font-size: 1.15rem;
        margin: 0.3rem 0 0.5rem 0;
    }

    .feature-card p {
        color: var(--text-muted);
        font-size: 0.93rem;
        margin: 0;
    }

    /* ---------- How it works ---------- */
    .steps {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
    }

    .step {
        background: white;
        border: 1px solid var(--card-border);
        border-radius: 18px;
        padding: 1.3rem 1.3rem;
        box-shadow: var(--shadow);
    }

    .step-num {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        color: white;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.7rem;
    }

    .step h4 {
        margin: 0 0 0.3rem 0;
        color: var(--primary-dark);
    }

    .step p {
        margin: 0;
        color: var(--text-muted);
        font-size: 0.92rem;
    }

    /* ---------- Emergency + disclaimer ---------- */
    .emergency {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: linear-gradient(135deg, #fff2f2, #ffe6e6);
        border: 1px solid #f4b8b8;
        border-left: 6px solid var(--danger);
        border-radius: 16px;
        padding: 1rem 1.3rem;
        margin-top: 1.6rem;
        color: #7a1f1f;
    }

    .emergency-icon {
        font-size: 2rem;
    }

    .emergency strong {
        color: #a02020;
    }

    .disclaimer {
        background: #fff8e6;
        border-left: 5px solid #f0a202;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        color: #5c4400;
        margin-top: 1.2rem;
        box-shadow: 0 2px 8px rgba(240, 162, 2, 0.12);
    }

    .disclaimer strong {
        color: #8a5a00;
    }

    /* ---------- Placeholder ---------- */
    .placeholder {
        background: rgba(255, 255, 255, 0.7);
        border: 2px dashed var(--card-border);
        border-radius: 18px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        color: var(--text-dark);
        margin-top: 1rem;
    }

    .placeholder .big-icon {
        font-size: 3.5rem;
    }

    .placeholder h2 {
        color: var(--text-dark);
    }

    .placeholder p {
        color: var(--text-muted);
    }

    /* ---------- Disease information ---------- */
    .disease-head {
        background: white;
        border: 1px solid var(--card-border);
        border-left: 6px solid var(--accent);
        border-radius: 18px;
        padding: 1.4rem 1.6rem;
        box-shadow: var(--shadow);
        margin: 1rem 0 1.2rem 0;
    }

    .disease-head h2 {
        margin: 0 0 0.4rem 0;
        color: var(--primary-dark);
    }

    .disease-head p {
        margin: 0;
        color: var(--text-muted);
    }

    .info-card {
        background: white;
        border: 1px solid var(--card-border);
        border-radius: 18px;
        padding: 1.2rem 1.4rem;
        box-shadow: var(--shadow);
        margin-bottom: 1rem;
    }

    .info-card h3 {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0 0 0.7rem 0;
        font-size: 1.05rem;
    }

    .info-card ul {
        margin: 0;
        padding-left: 1.1rem;
    }

    .info-card li {
        margin-bottom: 0.35rem;
        font-size: 0.94rem;
    }

    .c-symptoms  { border-top: 5px solid #f08a4b; }
    .c-causes    { border-top: 5px solid #8e6bd8; }
    .c-prevention { border-top: 5px solid #2fb67a; }
    .c-doctor    { border-top: 5px solid #d64545; }

    /* ---------- Buttons ---------- */
    .stButton {
        margin-top: 0.5rem;
    }

    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(11, 110, 153, 0.25);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .stButton button:hover {
        color: white;
        border: none;
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(11, 110, 153, 0.35);
    }

    .stButton button p {
        color: white !important;
    }

    /* ---------- Inputs, chat and alerts ---------- */
    div[data-baseweb="select"] > div {
        border-radius: 12px;
        background: white;
        border-color: var(--card-border);
    }

    [data-testid="stAlert"] {
        border-radius: 14px;
    }

    [data-testid="stChatMessage"] {
        background: white;
        border: 1px solid var(--card-border);
        border-radius: 18px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
        box-shadow: 0 3px 12px rgba(8, 76, 107, 0.07);
    }

    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, #e3f2fa, #e4f8f6);
        border-color: #bfe0ec;
    }

    [data-testid="stChatInput"] {
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(8, 76, 107, 0.12);
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px;
    }

    /* ---------- Footer ---------- */
    .footer {
        text-align: center;
        color: var(--text-muted);
        font-size: 0.85rem;
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid var(--card-border);
    }

    /* ---------- Mobile ---------- */
    @media (max-width: 768px) {
        .hero h1 {
            font-size: 2.1rem;
        }

        .hero p {
            font-size: 1rem;
        }

        .stats {
            grid-template-columns: repeat(2, 1fr);
        }

        .steps {
            grid-template-columns: 1fr;
        }

        .feature-card {
            min-height: auto;
            margin-bottom: 0.8rem;
        }

        .page-banner h1 {
            font-size: 1.4rem;
        }
    }
</style>
"""


# --------------------------------------------------
# 4. REUSABLE UI FUNCTIONS
# --------------------------------------------------

def load_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_html(markup):
    """
    Show a piece of HTML.
    We join the lines into one line so Markdown never turns
    indented HTML into a code block.
    """
    one_line = " ".join(line.strip() for line in markup.splitlines())
    st.markdown(one_line, unsafe_allow_html=True)


def html_list(items):
    """Turn a Python list into an HTML bullet list (text is escaped)."""
    rows = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f"<ul>{rows}</ul>"


def go_to(page_name):
    """Used by buttons to switch the sidebar page."""
    st.session_state.nav_page = page_name


def show_header():
    """Big hero banner (home page)."""
    render_html(
        f"""
        <div class="hero">
            <h1>🩺 {APP_TITLE}</h1>
            <p>{APP_SUBTITLE}</p>
            <div class="hero-badges">
                <span class="hero-badge">✅ Free to use</span>
                <span class="hero-badge">📖 Educational</span>
                <span class="hero-badge">🚨 Emergency alerts</span>
                <span class="hero-badge">🔒 No login needed</span>
            </div>
        </div>
        """
    )


def show_page_banner(icon, title, subtitle):
    """Smaller banner at the top of every other page."""
    render_html(
        f"""
        <div class="page-banner">
            <div class="page-icon">{icon}</div>
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
        </div>
        """
    )


def show_disclaimer():
    st.markdown(
        """
        <div class="disclaimer">
            <strong>⚠️ Medical Disclaimer:</strong>
            Doctor AI is an educational university project and is
            <strong>not</strong> a substitute for professional medical
            advice, diagnosis or treatment. Always consult a qualified
            healthcare professional about medical concerns. In an
            emergency, contact local emergency services immediately.
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_placeholder(icon, title, message):
    render_html(
        f"""
        <div class="placeholder">
            <div class="big-icon">{icon}</div>
            <h2>{title}</h2>
            <p>{message}</p>
        </div>
        """
    )


def show_footer():
    st.markdown(
        '<div class="footer">Doctor AI • University Semester Project • '
        "Built with Python &amp; Streamlit</div>",
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# 5. HOME PAGE
# --------------------------------------------------

def home_page():
    show_header()

    st.markdown(
        '<h2 class="section-title">👋 Welcome to Doctor AI</h2>',
        unsafe_allow_html=True,
    )

    st.write(
        "Doctor AI is a university project that aims to make general "
        "health information easy to find and easy to understand. "
        "Describe how you feel, explore common conditions and learn "
        "simple health tips, all in one friendly place."
    )

    # Small numbers strip (numbers are counted from your own data)
    stats = [
        (str(len(SUPPORTED_SYMPTOMS)), "Symptoms covered"),
        (str(len(get_disease_names())), "Conditions explained"),
        ("24/7", "Always available"),
        ("Free", "No login needed"),
    ]
    stat_cards = "".join(
        f'<div class="stat"><div class="stat-num">{number}</div>'
        f'<div class="stat-label">{label}</div></div>'
        for number, label in stats
    )
    render_html(f'<div class="stats">{stat_cards}</div>')

    st.markdown(
        '<h2 class="section-title">✨ What You Can Do</h2>',
        unsafe_allow_html=True,
    )

    columns = st.columns(len(FEATURES))

    for index, (column, feature) in enumerate(zip(columns, FEATURES)):
        icon, title, description, page, button_text = feature
        with column:
            render_html(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                """
            )
            st.button(
                button_text,
                key=f"feature_button_{index}",
                on_click=go_to,
                args=(page,),
                width="stretch",
            )

    st.markdown(
        '<h2 class="section-title">🧭 How It Works</h2>',
        unsafe_allow_html=True,
    )

    step_cards = "".join(
        f'<div class="step"><div class="step-num">{number}</div>'
        f"<h4>{html.escape(title)}</h4><p>{html.escape(text)}</p></div>"
        for number, (title, text) in enumerate(HOW_IT_WORKS, start=1)
    )
    render_html(f'<div class="steps">{step_cards}</div>')

    render_html(
        """
        <div class="emergency">
            <div class="emergency-icon">🚨</div>
            <div>
                <strong>In an emergency, do not wait.</strong>
                Chest pain, trouble breathing, fainting or severe bleeding
                need immediate medical help. Call your local emergency
                number or go to the nearest hospital.
            </div>
        </div>
        """
    )

    show_disclaimer()


# --------------------------------------------------
# 6. AI CHATBOT PAGE
# --------------------------------------------------

def add_exchange(user_text):
    """Save the user's message and the chatbot's reply in the history."""
    st.session_state.messages.append({"role": "user", "content": user_text})
    reply = get_bot_response(user_text)
    st.session_state.messages.append({"role": "assistant", "content": reply})


def clear_chat():
    st.session_state.messages = []


def chatbot_page():
    show_page_banner(
        "🤖",
        "Doctor AI Chatbot",
        "Ask general health questions and get simple, friendly answers.",
    )

    st.warning(
        "Medical disclaimer: This chatbot is a student project and "
        "provides general health information only. It cannot diagnose "
        "diseases or recommend medicines. In an emergency, contact "
        "local emergency services immediately."
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Welcome message and quick questions when the chat is empty
    if not st.session_state.messages:
        with st.chat_message("assistant", avatar=AVATARS["assistant"]):
            st.write(
                "Hello! 👋 I am Doctor AI. You can ask me about "
                "fever, headache, cough, cold, sore throat, "
                "stomach pain, or healthy lifestyle tips."
            )

        st.caption("💬 Try one of these questions:")
        suggestion_columns = st.columns(len(CHAT_SUGGESTIONS))
        for index, (column, question) in enumerate(
            zip(suggestion_columns, CHAT_SUGGESTIONS)
        ):
            with column:
                st.button(
                    question,
                    key=f"suggestion_{index}",
                    on_click=add_exchange,
                    args=(question,),
                    width="stretch",
                )

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=AVATARS[message["role"]]):
            st.write(message["content"])

    # Button to clear the conversation
    if st.session_state.messages:
        st.button("🗑️ Clear chat", key="clear_chat", on_click=clear_chat)

    # Chat input
    user_text = st.chat_input(
        "Type your health question here..."
    )

    if user_text:
        add_exchange(user_text)

        # Refresh page to display both messages
        st.rerun()


# --------------------------------------------------
# 7. SYMPTOM CHECKER PAGE
# --------------------------------------------------

def symptom_checker_page():
    show_page_banner(
        "🩺",
        "Symptom Checker",
        "Select your symptoms to learn about conditions that may be related.",
    )

    st.warning(
        "This tool is for educational purposes only. "
        "It cannot diagnose diseases or replace a doctor."
    )

    # Let the user select multiple symptoms
    selected_symptoms = st.multiselect(
        "Select your symptoms:",
        options=SUPPORTED_SYMPTOMS,
        placeholder="Choose one or more symptoms...",
    )

    # Check symptoms when button is clicked
    if st.button("🔍 Check Symptoms", type="primary", width="stretch"):

        result = check_symptoms(selected_symptoms)

        st.divider()

        if not selected_symptoms:
            # Friendly message: please select symptoms
            st.info(result)
        elif "medical emergency" in result[:80].lower():
            # Emergency message stands out in red
            st.error(result)
        else:
            with st.container(border=True):
                st.markdown(result)


# --------------------------------------------------
# 8. DISEASE INFORMATION PAGE
# --------------------------------------------------

def disease_information_page():
    show_page_banner(
        "📚",
        "Disease Information",
        "Explore simple educational information about common health conditions.",
    )

    # Get all available disease names
    disease_names = get_disease_names()

    # Let the user select a condition
    selected_disease = st.selectbox(
        "Select a health condition:",
        disease_names,
        index=None,
        placeholder="Choose a condition...",
    )

    # Nothing selected yet: show a friendly hint
    if not selected_disease:
        show_placeholder(
            "📖",
            "Pick a condition to begin",
            "Choose a health condition from the list above to read "
            "its symptoms, causes, prevention tips and when to see a doctor.",
        )
        return

    # Display information when a condition is selected
    info = get_disease_info(selected_disease)

    if not info:
        st.error("Information not available.")
        return

    render_html(
        f"""
        <div class="disease-head">
            <h2>{html.escape(info["name"])}</h2>
            <p>{html.escape(info["description"])}</p>
        </div>
        """
    )

    # Show the four sections as cards, two per row
    for row_start in range(0, len(DISEASE_SECTIONS), 2):
        columns = st.columns(2)
        row_sections = DISEASE_SECTIONS[row_start:row_start + 2]

        for column, (key, icon, title, style) in zip(columns, row_sections):
            with column:
                render_html(
                    f"""
                    <div class="info-card {style}">
                        <h3><span>{icon}</span>{title}</h3>
                        {html_list(info[key])}
                    </div>
                    """
                )

    st.info(info["disclaimer"])


# --------------------------------------------------
# 9. ABOUT PAGE
# --------------------------------------------------

def about_page():
    show_page_banner(
        "ℹ️",
        "About Doctor AI",
        "An educational health information assistant for everyone.",
    )

    st.write(
        "Doctor AI is an educational health information "
        "assistant designed to provide basic health guidance."
    )

    st.subheader("🎯 Our Purpose")
    st.write(
        "Our goal is to make basic health information "
        "easy to understand and accessible to everyone."
    )

    st.subheader("✨ Main Features")
    st.markdown("""
    - AI Chatbot for general health questions
    - Symptom Checker for general health information
    - Disease Information about common conditions
    - Basic health guidance
    - Emergency warning information
    """)

    st.subheader("⚠️ Medical Disclaimer")
    st.warning(
        "Doctor AI is an educational project only. "
        "It does not provide medical diagnosis or treatment. "
        "Always consult a qualified healthcare professional "
        "for medical advice."
    )

    st.caption("Developed as a University Semester Project.")


# --------------------------------------------------
# 10. PAGE NAVIGATION
# --------------------------------------------------

PAGES = {
    "🏠 Home": home_page,
    "🤖 AI Chatbot": chatbot_page,
    "🩺 Symptom Checker": symptom_checker_page,
    "📚 Disease Information": disease_information_page,
    "ℹ️ About": about_page,
}


# --------------------------------------------------
# 11. MAIN FUNCTION
# --------------------------------------------------

def main():

    load_css()

    # Remember which page is open (buttons on the home page can change it)
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = NAV_OPTIONS[0]

    with st.sidebar:
        render_html(
            f"""
            <div class="side-logo">
                <div class="side-logo-icon">🩺</div>
                <div>
                    <div class="side-title">{APP_TITLE}</div>
                    <div class="side-sub">{APP_SUBTITLE}</div>
                </div>
            </div>
            """
        )

        st.divider()

        st.radio(
            "Navigation",
            NAV_OPTIONS,
            key="nav_page",
            label_visibility="collapsed",
        )

        st.divider()

        st.caption(
            "⚠️ For educational use only. Not medical advice."
        )

    # Display selected page
    PAGES[st.session_state.nav_page]()

    show_footer()


# Start application
main()
