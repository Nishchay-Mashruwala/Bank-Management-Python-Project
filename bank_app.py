import json
import random
import string
from pathlib import Path
import streamlit as st

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Vault — Banking",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "page" not in st.session_state:
    st.session_state.page = "open"

# ─── Premium CSS + Animations ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --gold:       #c9a84c;
  --gold-light: #e8c97a;
  --gold-dim:   #7a6030;
  --indigo:     #6c63ff;
  --indigo-dim: #3a3580;
  --bg:         #080910;
  --bg2:        #0d0f18;
  --bg3:        #12141f;
  --border:     rgba(255,255,255,0.06);
  --border2:    rgba(255,255,255,0.10);
  --text:       #e8eaf2;
  --muted:      #4a5068;
  --muted2:     #2a2d42;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: var(--bg) !important;
    color: var(--text);
}
.stApp { background: var(--bg) !important; }
.block-container { padding: 2.2rem 3rem !important; max-width: 880px !important; }
.main .block-container { padding-top: 1.8rem !important; }

/* ── Keyframes ── */
@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes shimmer {
  0%   { background-position: -600px 0; }
  100% { background-position: 600px 0; }
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(201,168,76,0.6); }
  50%       { opacity: 0.8; box-shadow: 0 0 0 5px rgba(201,168,76,0); }
}
@keyframes glow-border {
  0%, 100% { border-color: rgba(108,99,255,0.25); }
  50%       { border-color: rgba(108,99,255,0.55); }
}
@keyframes card-in {
  from { opacity: 0; transform: translateY(14px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="stSidebar"] section { padding: 0 !important; }

/* Sidebar inner scroll area */
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

/* ── Logo ── */
.vault-logo {
    padding: 2rem 1.5rem 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 0.25rem;
    animation: fadeIn 0.6s ease both;
}
.vault-logo .wordmark {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.5px;
    line-height: 1;
}
.vault-logo .wordmark em {
    font-style: normal;
    background: linear-gradient(90deg, var(--gold), var(--gold-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.vault-logo .tagline {
    font-size: 0.62rem;
    color: var(--muted2);
    letter-spacing: 0.16em;
    text-transform: uppercase;
    font-weight: 600;
    margin-top: 0.35rem;
}

/* ── Nav section label ── */
.nav-group-label {
    font-size: 0.58rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted2);
    font-weight: 700;
    padding: 1.1rem 1.5rem 0.35rem;
    animation: fadeIn 0.5s ease both;
}

/* ── Nav buttons ── */
[data-testid="stSidebar"] .stButton { margin: 0 !important; }
[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    color: var(--muted) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.86rem !important;
    font-weight: 500 !important;
    padding: 0.58rem 1rem !important;
    text-align: left !important;
    justify-content: flex-start !important;
    transition: all 0.2s cubic-bezier(0.4,0,0.2,1) !important;
    margin: 1px 0 !important;
    letter-spacing: 0.01em !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.04) !important;
    color: #a0a8c0 !important;
    transform: translateX(3px) !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .nav-active .stButton > button {
    background: linear-gradient(90deg, rgba(108,99,255,0.18), rgba(108,99,255,0.06)) !important;
    color: #c8c4ff !important;
    border-color: rgba(108,99,255,0.35) !important;
    box-shadow: inset 0 0 20px rgba(108,99,255,0.08) !important;
}

/* ── Sidebar stat ── */
.sidebar-stat {
    margin: 1.4rem 1rem 0;
    background: rgba(201,168,76,0.05);
    border: 1px solid rgba(201,168,76,0.15);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    animation: fadeIn 0.8s ease both;
}
.sidebar-stat .ss-label {
    font-size: 0.6rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--gold-dim);
    font-weight: 600;
    margin-bottom: 5px;
}
.sidebar-stat .ss-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--gold);
}

/* ── Page entry animation ── */
.page-wrap {
    animation: fadeSlideUp 0.45s cubic-bezier(0.22,1,0.36,1) both;
}

/* ── Page header ── */
.page-header {
    display: flex;
    align-items: flex-start;
    gap: 1.1rem;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}
.page-icon {
    width: 48px; height: 48px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.25rem; flex-shrink: 0;
    position: relative;
}
.page-icon.gold   { background: rgba(201,168,76,0.12); border: 1px solid rgba(201,168,76,0.2); }
.page-icon.teal   { background: rgba(0,200,160,0.1);   border: 1px solid rgba(0,200,160,0.2); }
.page-icon.blue   { background: rgba(80,140,255,0.1);  border: 1px solid rgba(80,140,255,0.2); }
.page-icon.amber  { background: rgba(240,160,48,0.1);  border: 1px solid rgba(240,160,48,0.2); }
.page-icon.red    { background: rgba(255,80,80,0.1);   border: 1px solid rgba(255,80,80,0.2); }
.page-icon.purple { background: rgba(108,99,255,0.12); border: 1px solid rgba(108,99,255,0.2); }
.page-header-text h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.45rem;
    font-weight: 600;
    color: var(--text);
    margin: 0 0 0.25rem;
    letter-spacing: -0.3px;
}
.page-header-text p { color: var(--muted); font-size: 0.84rem; }

/* ── Premium glass card ── */
.vault-card {
    background: linear-gradient(135deg, rgba(20,22,36,0.95) 0%, rgba(14,16,26,0.98) 100%);
    border: 1px solid var(--border2);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
    animation: card-in 0.5s cubic-bezier(0.22,1,0.36,1) both;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
}
/* top shimmer line */
.vault-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(201,168,76,0.4), transparent);
    pointer-events: none;
}
/* ambient glow orb */
.vault-card::after {
    content: '';
    position: absolute; top: -80px; right: -80px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(108,99,255,0.08) 0%, transparent 70%);
    pointer-events: none;
}

/* Credit-card style header band */
.card-band {
    display: flex; justify-content: space-between; align-items: flex-start;
    margin-bottom: 1.6rem;
}
.card-chip {
    width: 36px; height: 28px;
    border-radius: 5px;
    background: linear-gradient(135deg, var(--gold-dim), var(--gold));
    opacity: 0.8;
    position: relative;
    overflow: hidden;
}
.card-chip::after {
    content: '';
    position: absolute; top: 50%; left: 0; right: 0;
    height: 1px; background: rgba(0,0,0,0.3);
    transform: translateY(-50%);
}
.card-network {
    display: flex; gap: -4px;
}
.card-network span {
    width: 22px; height: 22px; border-radius: 50%;
    display: inline-block;
}
.card-network span:first-child  { background: rgba(201,168,76,0.5); margin-right: -8px; }
.card-network span:last-child   { background: rgba(201,168,76,0.3); }

/* ── Account pill ── */
.acct-pill {
    display: inline-flex; align-items: center; gap: 7px;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 100px; padding: 4px 12px;
    font-size: 0.73rem; letter-spacing: 0.12em; color: var(--muted);
    font-family: 'Inter', monospace;
}
.acct-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--gold);
    animation: pulse-dot 2.5s ease-in-out infinite;
}

/* ── Avatar ── */
.avatar {
    width: 50px; height: 50px; border-radius: 50%;
    background: linear-gradient(135deg, rgba(108,99,255,0.25), rgba(108,99,255,0.1));
    border: 2px solid rgba(108,99,255,0.3);
    display: inline-flex; align-items: center; justify-content: center;
    font-family: 'Playfair Display', serif;
    font-weight: 600; font-size: 1rem; color: #b0a8ff;
    margin-right: 1rem; flex-shrink: 0;
    box-shadow: 0 0 20px rgba(108,99,255,0.2);
}

/* ── Stat chips ── */
.stat-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 0; }
.stat-chip {
    flex: 1; min-width: 130px;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 14px; padding: 1rem 1.1rem;
    transition: border-color 0.2s, background 0.2s;
}
.stat-chip:hover {
    background: rgba(255,255,255,0.05);
    border-color: var(--border2);
}
.sc-label {
    font-size: 0.63rem; letter-spacing: 0.09em;
    text-transform: uppercase; color: var(--muted2);
    font-weight: 600; margin-bottom: 6px;
}
.sc-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem; font-weight: 600;
    color: var(--text); letter-spacing: -0.3px;
}
.sc-value.gold   { color: var(--gold); }
.sc-value.teal   { color: #00c8a0; }
.sc-value.indigo { color: #a09aff; }
.sc-value.red    { color: #ff7878; }

/* ── Messages ── */
.msg {
    border-radius: 12px; padding: 0.8rem 1.1rem;
    margin: 0.7rem 0; font-size: 0.88rem; font-weight: 500;
    display: flex; align-items: center; gap: 0.7rem;
    animation: fadeSlideUp 0.3s ease both;
}
.msg-ok   {
    background: rgba(0,200,160,0.07);
    border: 1px solid rgba(0,200,160,0.2);
    color: #00c8a0;
}
.msg-err  {
    background: rgba(255,100,100,0.08);
    border: 1px solid rgba(255,100,100,0.2);
    color: #ff8080;
}
.msg-info {
    background: rgba(108,99,255,0.08);
    border: 1px solid rgba(108,99,255,0.2);
    color: #a09aff;
}
.msg-warn {
    background: rgba(201,168,76,0.08);
    border: 1px solid rgba(201,168,76,0.2);
    color: var(--gold);
}
.msg-icon {
    width: 22px; height: 22px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.7rem; flex-shrink: 0;
    font-weight: 700;
}
.msg-ok   .msg-icon { background: rgba(0,200,160,0.2); }
.msg-err  .msg-icon { background: rgba(255,100,100,0.2); }
.msg-info .msg-icon { background: rgba(108,99,255,0.2); }
.msg-warn .msg-icon { background: rgba(201,168,76,0.2); }

/* ── Section divider ── */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(201,168,76,0.25), transparent);
    margin: 1.4rem 0;
    border: none;
}

/* ── Form inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.7rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:hover,
.stNumberInput > div > div > input:hover {
    border-color: rgba(255,255,255,0.14) !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: rgba(108,99,255,0.5) !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.12), 0 0 20px rgba(108,99,255,0.06) !important;
    background: rgba(108,99,255,0.04) !important;
}
.stTextInput > div > div > input::placeholder,
.stNumberInput > div > div > input::placeholder {
    color: var(--muted2) !important;
}

/* ── Labels ── */
.stTextInput label, .stNumberInput label,
.stCheckbox label span, .stSelectbox label {
    color: var(--muted) !important;
    font-size: 0.77rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
}

/* ── Submit button ── */
.stFormSubmitButton > button {
    background: linear-gradient(135deg, var(--indigo), #8b84ff) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7rem 2rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    width: 100% !important;
    letter-spacing: 0.02em !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    box-shadow: 0 4px 20px rgba(108,99,255,0.35) !important;
    position: relative !important;
}
.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #7c74ff, #a09aff) !important;
    box-shadow: 0 6px 30px rgba(108,99,255,0.5) !important;
    transform: translateY(-2px) !important;
}
.stFormSubmitButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 10px rgba(108,99,255,0.3) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
}

/* ── Checkbox ── */
.stCheckbox { margin-top: 0.25rem; }

/* ── Horizontal rule ── */
hr { border-color: var(--border) !important; }

/* ── Shimmer skeleton (for cards) ── */
.shimmer-line {
    height: 12px; border-radius: 6px;
    background: linear-gradient(90deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.04) 100%);
    background-size: 600px 100%;
    animation: shimmer 1.8s infinite linear;
    margin-bottom: 8px;
}

/* ── Form container glass box ── */
.form-glass {
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    animation: card-in 0.4s cubic-bezier(0.22,1,0.36,1) both;
    box-shadow: 0 8px 40px rgba(0,0,0,0.3);
}

/* ── Glow badge ── */
.glow-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(0,200,160,0.1);
    border: 1px solid rgba(0,200,160,0.25);
    border-radius: 100px;
    padding: 3px 10px;
    font-size: 0.7rem; letter-spacing: 0.06em;
    color: #00c8a0; font-weight: 600;
}
.glow-dot {
    width: 5px; height: 5px; border-radius: 50%;
    background: #00c8a0;
    animation: pulse-dot 2s ease-in-out infinite;
}

/* ── Streamlit alert override ── */
[data-testid="stAlert"] {
    background: rgba(201,168,76,0.07) !important;
    border: 1px solid rgba(201,168,76,0.2) !important;
    border-radius: 12px !important;
    color: var(--gold) !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Database ─────────────────────────────────────────────────────────────────
DATABASE = "data.json"

def load_data():
    path = Path(DATABASE)
    if path.exists():
        try:
            with open(path) as f: return json.load(f)
        except: return []
    return []

def save_data(data):
    try:
        with open(DATABASE, "w") as f: json.dump(data, f, indent=2)
    except IOError as e: st.error(f"Save failed: {e}")

def gen_account():
    chars  = random.choices(string.ascii_uppercase, k=2)
    digits = random.choices(string.digits, k=6)
    parts  = chars + digits; random.shuffle(parts)
    return "".join(parts)

def find_user(data, account_no, pin):
    m = [u for u in data if u["accountNo"] == account_no and u["pin"] == pin]
    return m[0] if m else None

def initials(name):
    p = name.strip().split()
    return (p[0][0] + p[-1][0]).upper() if len(p) >= 2 else name[:2].upper()


# ─── UI helpers ───────────────────────────────────────────────────────────────
def ok(msg):
    st.markdown(f'<div class="msg msg-ok"><div class="msg-icon">✓</div><span>{msg}</span></div>',
                unsafe_allow_html=True)

def err(msg):
    st.markdown(f'<div class="msg msg-err"><div class="msg-icon">✕</div><span>{msg}</span></div>',
                unsafe_allow_html=True)

def hint(msg):
    st.markdown(f'<div class="msg msg-info"><div class="msg-icon">→</div><span>{msg}</span></div>',
                unsafe_allow_html=True)

def warn(msg):
    st.markdown(f'<div class="msg msg-warn"><div class="msg-icon">!</div><span>{msg}</span></div>',
                unsafe_allow_html=True)

def page_header(icon, color, title, subtitle):
    st.markdown(f"""
    <div class="page-header">
      <div class="page-icon {color}">{icon}</div>
      <div class="page-header-text">
        <h2>{title}</h2>
        <p>{subtitle}</p>
      </div>
    </div>""", unsafe_allow_html=True)

def gold_divider():
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

def auth_fields(prefix):
    c1, c2 = st.columns([3, 2])
    with c1: acc = st.text_input("Account Number", key=f"{prefix}_acc", placeholder="e.g. AB123456")
    with c2: pin = st.text_input("PIN", key=f"{prefix}_pin", type="password",
                                  placeholder="4 digits", max_chars=4)
    return acc.strip(), pin.strip()

def nav_btn(label, page_key):
    active = st.session_state.page == page_key
    if active: st.markdown('<div class="nav-active">', unsafe_allow_html=True)
    if st.button(label, key=f"nav_{page_key}"):
        st.session_state.page = page_key
        st.rerun()
    if active: st.markdown('</div>', unsafe_allow_html=True)


# ─── Pages ────────────────────────────────────────────────────────────────────
def page_create(data):
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    page_header("✦", "gold", "Open an account", "Join Vault — takes less than a minute")

    with st.form("create_form", clear_on_submit=True):
        st.markdown('<div class="form-glass">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name", placeholder="e.g. Priya Sharma")
            age  = st.number_input("Age", min_value=1, max_value=120, value=22, step=1)
        with c2:
            email = st.text_input("Email", placeholder="priya@example.com")
            pin   = st.text_input("Choose PIN", type="password", max_chars=4, placeholder="4 digits")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("✦  Create Account")

    if submitted:
        if not name.strip():               err("Full name is required.")
        elif not (18 <= int(age) <= 60):   err("Applicants must be aged 18 – 60.")
        elif "@" not in email:             err("Enter a valid email address.")
        elif not pin.isdigit() or len(pin) != 4: err("PIN must be exactly 4 digits.")
        else:
            acct = gen_account()
            data.append({"name": name.strip(), "age": int(age), "email": email.strip(),
                         "pin": int(pin), "accountNo": acct, "balance": 0})
            save_data(data)
            ok("Account created successfully.")
            st.markdown(f"""
            <div class="vault-card">
              <div class="card-band">
                <div class="card-chip"></div>
                <div class="card-network"><span></span><span></span></div>
              </div>
              <div class="acct-pill" style="margin-bottom:1.2rem;">
                <span class="acct-dot"></span>{acct}
              </div>
              <div style="display:flex;align-items:center;margin-bottom:1.5rem;">
                <div class="avatar">{initials(name)}</div>
                <div>
                  <p style="color:var(--muted2);font-size:0.72rem;letter-spacing:0.08em;
                     text-transform:uppercase;margin-bottom:4px;">Account Holder</p>
                  <p style="font-family:'Playfair Display',serif;font-size:1.2rem;
                     font-weight:600;color:var(--text);margin:0;">{name}</p>
                  <p style="color:var(--muted);font-size:0.8rem;margin:2px 0 0;">{email}</p>
                </div>
                <div style="margin-left:auto;">
                  <span class="glow-badge"><span class="glow-dot"></span>Active</span>
                </div>
              </div>
              <div class="gold-divider" style="margin:0 0 1.2rem;"></div>
              <div class="stat-row">
                <div class="stat-chip">
                  <div class="sc-label">Opening Balance</div>
                  <div class="sc-value gold">₹0</div>
                </div>
                <div class="stat-chip">
                  <div class="sc-label">Account Type</div>
                  <div class="sc-value indigo" style="font-size:1rem;">Savings</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)
            hint("Save your account number — you'll need it every time you log in.")
    st.markdown('</div>', unsafe_allow_html=True)


def page_deposit(data):
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    page_header("↓", "teal", "Deposit funds", "Add money to your account instantly")

    with st.form("dep_form"):
        st.markdown('<div class="form-glass">', unsafe_allow_html=True)
        auth_fields_result = auth_fields("dep")
        gold_divider()
        amount = st.number_input("Amount to Deposit (₹)", min_value=1, max_value=10_000,
                                  step=100, value=1_000)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("↓  Deposit Funds")

    acc, pin = auth_fields_result
    if submitted:
        if not acc or not pin: err("Enter your account number and PIN."); return
        if not pin.isdigit():  err("PIN must be numeric."); return
        user = find_user(data, acc, int(pin))
        if user is None:       err("Invalid account number or PIN."); return
        user["balance"] += int(amount); save_data(data)
        ok(f"₹{int(amount):,} deposited to your account.")
        st.markdown(f"""
        <div class="vault-card">
          <div class="card-band">
            <div class="card-chip"></div>
            <div class="card-network"><span></span><span></span></div>
          </div>
          <p style="color:var(--muted2);font-size:0.72rem;letter-spacing:0.1em;
             text-transform:uppercase;margin-bottom:1rem;">Transaction Summary</p>
          <div class="stat-row">
            <div class="stat-chip">
              <div class="sc-label">Amount Deposited</div>
              <div class="sc-value teal">+₹{int(amount):,}</div>
            </div>
            <div class="stat-chip">
              <div class="sc-label">New Balance</div>
              <div class="sc-value gold">₹{user['balance']:,}</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def page_withdraw(data):
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    page_header("↑", "blue", "Withdraw funds", "Transfer money out of your account")

    with st.form("wd_form"):
        st.markdown('<div class="form-glass">', unsafe_allow_html=True)
        auth_fields_result = auth_fields("wd")
        gold_divider()
        amount = st.number_input("Amount to Withdraw (₹)", min_value=1,
                                  max_value=10_000_000, step=100, value=500)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("↑  Withdraw Funds")

    acc, pin = auth_fields_result
    if submitted:
        if not acc or not pin: err("Enter your account number and PIN."); return
        if not pin.isdigit():  err("PIN must be numeric."); return
        user = find_user(data, acc, int(pin))
        if user is None:       err("Invalid account number or PIN."); return
        if amount > user["balance"]:
            err(f"Insufficient balance — available: ₹{user['balance']:,}"); return
        user["balance"] -= int(amount); save_data(data)
        ok(f"₹{int(amount):,} withdrawn successfully.")
        st.markdown(f"""
        <div class="vault-card">
          <div class="card-band">
            <div class="card-chip"></div>
            <div class="card-network"><span></span><span></span></div>
          </div>
          <p style="color:var(--muted2);font-size:0.72rem;letter-spacing:0.1em;
             text-transform:uppercase;margin-bottom:1rem;">Transaction Summary</p>
          <div class="stat-row">
            <div class="stat-chip">
              <div class="sc-label">Amount Withdrawn</div>
              <div class="sc-value red">−₹{int(amount):,}</div>
            </div>
            <div class="stat-chip">
              <div class="sc-label">Remaining Balance</div>
              <div class="sc-value gold">₹{user['balance']:,}</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def page_details(data):
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    page_header("◈", "purple", "Account details", "View your profile and balance")

    with st.form("det_form"):
        st.markdown('<div class="form-glass">', unsafe_allow_html=True)
        auth_fields_result = auth_fields("det")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("◈  View My Account")

    acc, pin = auth_fields_result
    if submitted:
        if not acc or not pin: err("Enter your account number and PIN."); return
        if not pin.isdigit():  err("PIN must be numeric."); return
        user = find_user(data, acc, int(pin))
        if user is None:       err("Invalid account number or PIN."); return

        st.markdown(f"""
        <div class="vault-card">
          <div class="card-band">
            <div class="card-chip"></div>
            <div class="card-network"><span></span><span></span></div>
          </div>
          <div class="acct-pill" style="margin-bottom:1.4rem;">
            <span class="acct-dot"></span>{user['accountNo']}
          </div>
          <div style="display:flex;align-items:center;margin-bottom:1.6rem;">
            <div class="avatar">{initials(user['name'])}</div>
            <div style="flex:1;">
              <p style="color:var(--muted2);font-size:0.7rem;letter-spacing:0.1em;
                 text-transform:uppercase;margin-bottom:4px;">Account Holder</p>
              <p style="font-family:'Playfair Display',serif;font-size:1.25rem;
                 font-weight:600;color:var(--text);margin:0;">{user['name']}</p>
              <p style="color:var(--muted);font-size:0.82rem;margin:3px 0 0;">{user['email']}</p>
            </div>
            <span class="glow-badge"><span class="glow-dot"></span>Active</span>
          </div>
          <div class="gold-divider" style="margin:0 0 1.3rem;"></div>
          <div class="stat-row">
            <div class="stat-chip">
              <div class="sc-label">Available Balance</div>
              <div class="sc-value gold">₹{user['balance']:,}</div>
            </div>
            <div class="stat-chip">
              <div class="sc-label">Account Age</div>
              <div class="sc-value indigo">{user['age']} yrs</div>
            </div>
            <div class="stat-chip">
              <div class="sc-label">Account Type</div>
              <div class="sc-value" style="font-size:0.95rem;color:var(--muted);">Savings</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def page_update(data):
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    page_header("✎", "amber", "Edit details", "Update your name, email or PIN")
    hint("Leave any field blank to keep its current value. Age, account number and balance cannot be changed.")

    with st.form("upd_form"):
        st.markdown('<div class="form-glass">', unsafe_allow_html=True)
        auth_fields_result = auth_fields("upd")
        gold_divider()
        c1, c2 = st.columns(2)
        with c1:
            new_name  = st.text_input("New Name",  placeholder="Leave blank to keep")
            new_email = st.text_input("New Email", placeholder="Leave blank to keep")
        with c2:
            new_pin = st.text_input("New PIN", type="password", max_chars=4,
                                     placeholder="Leave blank to keep")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("✎  Save Changes")

    acc, pin = auth_fields_result
    if submitted:
        if not acc or not pin: err("Enter your account number and PIN."); return
        if not pin.isdigit():  err("PIN must be numeric."); return
        user = find_user(data, acc, int(pin))
        if user is None:       err("Invalid account number or PIN."); return
        changed = False
        if new_name.strip():
            user["name"] = new_name.strip(); changed = True
        if new_email.strip():
            if "@" not in new_email: err("Enter a valid email address."); return
            user["email"] = new_email.strip(); changed = True
        if new_pin.strip():
            if not new_pin.isdigit() or len(new_pin) != 4:
                err("New PIN must be exactly 4 digits."); return
            user["pin"] = int(new_pin); changed = True
        if changed:
            save_data(data); ok("Your details have been updated.")
        else:
            hint("No changes were submitted.")
    st.markdown('</div>', unsafe_allow_html=True)


def page_delete(data):
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    page_header("✕", "red", "Close account", "Permanently remove your Vault account")
    warn("This action is irreversible. Your account and all data will be permanently deleted.")

    with st.form("del_form"):
        st.markdown('<div class="form-glass">', unsafe_allow_html=True)
        auth_fields_result = auth_fields("del")
        gold_divider()
        confirm = st.checkbox("I understand this is permanent and cannot be undone.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("✕  Close Account Permanently")

    acc, pin = auth_fields_result
    if submitted:
        if not acc or not pin: err("Enter your account number and PIN."); return
        if not pin.isdigit():  err("PIN must be numeric."); return
        if not confirm:        err("Please tick the confirmation checkbox."); return
        user = find_user(data, acc, int(pin))
        if user is None:       err("Invalid account number or PIN."); return
        data.remove(user); save_data(data)
        ok("Your account has been closed. We hope to see you again.")
    st.markdown('</div>', unsafe_allow_html=True)


# ─── App Shell ────────────────────────────────────────────────────────────────
def main():
    data = load_data()

    with st.sidebar:
        st.markdown("""
        <div class="vault-logo">
          <div class="wordmark">Vault<em>.</em></div>
          <div class="tagline">Premium Banking</div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<p class="nav-group-label">Navigation</p>', unsafe_allow_html=True)

        NAV = [
            ("✦   Open Account",   "open"),
            ("↓   Deposit",        "deposit"),
            ("↑   Withdraw",       "withdraw"),
            ("◈   My Account",     "details"),
            ("✎   Edit Details",   "update"),
            ("✕   Close Account",  "delete"),
        ]
        for label, key in NAV:
            nav_btn(label, key)

        st.markdown(f"""
        <div class="sidebar-stat">
          <div class="ss-label">Total Accounts</div>
          <div class="ss-value">{len(data):,}</div>
        </div>""", unsafe_allow_html=True)

    PAGES = {
        "open":     page_create,
        "deposit":  page_deposit,
        "withdraw": page_withdraw,
        "details":  page_details,
        "update":   page_update,
        "delete":   page_delete,
    }
    PAGES[st.session_state.page](data)


if __name__ == "__main__":
    main()