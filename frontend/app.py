"""LegalEase Streamlit frontend."""

import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="LegalEase — AI Legal Document Generator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- Custom Interactive CSS ----------------
st.markdown(
    """
    <style>
        /* 1. Premium Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@500;700&display=swap');

        /* 2. Live Animated Background */
        .stApp {
            background: linear-gradient(-45deg, #09090b, #1e1b4b, #2e1065, #09090b);
            background-size: 400% 400%;
            animation: gradientBG 20s ease infinite;
            font-family: 'Outfit', sans-serif;
            overflow-x: hidden;
        }
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* 3. Floating Background Orbs */
        .bg-orb {
            position: fixed; border-radius: 50%; filter: blur(90px); z-index: -1; opacity: 0.4;
            animation: float 15s infinite ease-in-out;
        }
        .orb1 { width: 400px; height: 400px; background: #a855f7; top: -10%; left: -10%; }
        .orb2 { width: 300px; height: 300px; background: #3b82f6; bottom: -10%; right: -5%; animation-delay: -7s; }
        .orb3 { width: 250px; height: 250px; background: #ec4899; top: 40%; left: 50%; animation-delay: -3s; opacity: 0.2; }
        @keyframes float {
            0% { transform: translateY(0px) scale(1); }
            50% { transform: translateY(-40px) scale(1.1); }
            100% { transform: translateY(0px) scale(1); }
        }

        /* 4. Interactive Cursor Glow */
        #cursor-glow {
            position: fixed;
            width: 500px; height: 500px;
            background: radial-gradient(circle, rgba(168, 85, 247, 0.15) 0%, transparent 60%);
            border-radius: 50%;
            pointer-events: none;
            transform: translate(-50%, -50%);
            z-index: 9999;
            transition: transform 0.1s ease-out;
            mix-blend-mode: screen;
        }

        /* 5. Premium Hero Header */
        .hero-section {
            text-align: center;
            padding: 3rem 2rem;
            margin-bottom: 2rem;
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
        }
        .hero-section::before {
            content: "";
            position: absolute; top: 0; left: 0; right: 0; height: 2px;
            background: linear-gradient(90deg, transparent, #a855f7, #3b82f6, #a855f7, transparent);
            animation: borderShine 3s linear infinite;
        }
        @keyframes borderShine {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        .hero-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 4rem !important;
            font-weight: 700 !important;
            background: linear-gradient(135deg, #ffffff, #a855f7, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem !important;
            letter-spacing: -1px;
        }
        .hero-subtitle {
            color: #94a3b8 !important;
            font-size: 1.2rem;
            font-weight: 300;
            margin-bottom: 1.5rem;
        }
        .hero-badge {
            display: inline-block;
            background: rgba(168, 85, 247, 0.15);
            color: #d8b4fe;
            padding: 0.4rem 1.2rem;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 600;
            border: 1px solid rgba(168, 85, 247, 0.3);
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        /* 6. Glassmorphism Form Elements (FIXED FOR TEXT VISIBILITY) */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea, div[data-baseweb="select"] > div {
            background-color: #1e1b4b !important; /* Solid dark background */
            border: 1px solid rgba(168, 85, 247, 0.4) !important;
            color: #ffffff !important; /* White text */
            border-radius: 12px !important;
        }
        
        /* Ensure placeholder is visible but not too bright */
        ::placeholder {
            color: #94a3b8 !important;
            opacity: 0.8 !important;
        }

        /* Ensure focused input stays dark with a glow */
        .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus, div[data-baseweb="select"] > div:focus {
            background-color: #2e1065 !important; /* Slightly brighter dark purple on focus */
            border-color: #a855f7 !important;
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.5) !important;
            color: #ffffff !important;
        }

        /* 7. Labels */
        .stTextInput label, .stSelectbox label, .stTextArea label {
            color: #f8fafc !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }

        /* 8. Next-Level Buttons */
        div[data-testid="stFormSubmitButton"] > button,
        div[data-testid="stButton"] > button,
        .stDownloadButton > button {
            background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899) !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 2rem !important;
            box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4) !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            position: relative;
            overflow: hidden;
            width: 100% !important;
        }

        /* FORCE THE TEXT TO BE WHITE AND VISIBLE INSIDE BUTTONS */
        div[data-testid="stFormSubmitButton"] > button > div > p,
        div[data-testid="stButton"] > button > div > p,
        .stDownloadButton > button > div > p {
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 1.05rem !important;
            font-family: 'Outfit', sans-serif !important;
            letter-spacing: 0.5px !important;
            margin: 0 !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
        }

        /* Button Hover Effects */
        div[data-testid="stFormSubmitButton"] > button:hover,
        div[data-testid="stButton"] > button:hover,
        .stDownloadButton > button:hover {
            transform: translateY(-4px) scale(1.02) !important;
            box-shadow: 0 15px 35px rgba(168, 85, 247, 0.6) !important;
        }

        /* 9. Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: rgba(10, 10, 15, 0.6) !important;
            backdrop-filter: blur(25px) !important;
            border-right: 1px solid rgba(255,255,255,0.05) !important;
        }

        /* 10. Custom Scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #09090b; }
        ::-webkit-scrollbar-thumb { background: #a855f7; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #c084fc; }

        /* 11. Document Preview Box */
        .doc-preview {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 2rem;
            white-space: pre-wrap;
            font-family: 'Georgia', serif;
            font-size: 1rem;
            line-height: 1.7;
            color: #e2e8f0 !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
    </style>
    
    <!-- Background Orbs & Cursor Element -->
    <div class="bg-orb orb1"></div>
    <div class="bg-orb orb2"></div>
    <div class="bg-orb orb3"></div>
    <div id="cursor-glow"></div>
    """,
    unsafe_allow_html=True,
)

# ---------------- Session State ----------------
if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "doc_type_saved" not in st.session_state:
    st.session_state.doc_type_saved = ""

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("## ⚖️ LegalEase")
    st.caption("AI-powered legal document generator")
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.write(
        "LegalEase creates professional legal drafts using Google's Gemini model. "
        "Fill in the form, click **Generate**, edit the preview, and download as "
        "**TXT**, **DOCX**, or **PDF**."
    )
    st.markdown("---")
    st.markdown("### 🔌 Backend")
    st.code(BACKEND_URL, language="text")
    if st.button("Check backend health"):
        try:
            r = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if r.status_code == 200:
                st.success("Backend is online ✅")
            else:
                st.error(f"Backend returned {r.status_code}")
        except Exception as e:
            st.error(f"Cannot reach backend: {e}")

# ---------------- Premium Hero Header ----------------
st.markdown(
    """
    <div class="hero-section">
        <div class="hero-badge">⚡ Powered by Gemini 3.1 Flash-Lite</div>
        <h1 class="hero-title">LegalEase</h1>
        <p class="hero-subtitle">Generate professional legal documents instantly with AI.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- Input Form ----------------
DOC_TYPES = [
    "Employment Contract",
    "Non-Disclosure Agreement (NDA)",
    "Residential Lease Agreement",
    "Commercial Lease Agreement",
    "Freelance Services Agreement",
    "Consulting Agreement",
    "Partnership Agreement",
    "Sales Agreement",
    "Privacy Policy",
    "Terms of Service",
]

with st.form("legalease_form", clear_on_submit=False):
    col1, col2 = st.columns(2)

    with col1:
        document_type = st.selectbox("📄 Document Type", DOC_TYPES, index=0)
        party_a = st.text_input(
            "👤 Party A",
            placeholder="e.g. Acme Corp., a Delaware corporation",
        )
        effective_date = st.text_input(
            "📅 Effective Date",
            placeholder="e.g. 2025-01-01",
        )

    with col2:
        jurisdiction = st.text_input(
            "🌍 Governing Jurisdiction",
            placeholder="e.g. State of California, USA",
        )
        party_b = st.text_input(
            "👤 Party B",
            placeholder="e.g. Jane Doe, an individual",
        )
        additional_notes = st.text_input(
            "🗒️ Additional Notes (optional)",
            placeholder="Any extra instructions for the AI",
        )

    key_terms = st.text_area(
        "🔑 Key Terms & Conditions",
        placeholder=(
            "e.g. Salary $120,000/year; 40 hours/week; 2-year confidentiality; "
            "30-day termination notice; IP assignment to employer."
        ),
        height=140,
    )

    submitted = st.form_submit_button("✨ Generate Document")

# ---------------- Handle Generation ----------------
if submitted:
    missing = [
        name
        for name, val in [
            ("Party A", party_a),
            ("Party B", party_b),
            ("Effective Date", effective_date),
            ("Jurisdiction", jurisdiction),
            ("Key Terms", key_terms),
        ]
        if not val or not val.strip()
    ]
    if missing:
        st.error(f"Please fill in: {', '.join(missing)}")
    else:
        with st.spinner("Drafting your document with Gemini…"):
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/generate",
                    json={
                        "document_type": document_type,
                        "party_a": party_a.strip(),
                        "party_b": party_b.strip(),
                        "effective_date": effective_date.strip(),
                        "jurisdiction": jurisdiction.strip(),
                        "key_terms": key_terms.strip(),
                        "additional_notes": (additional_notes or "").strip(),
                    },
                    timeout=120,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.document_text = data["content"]
                    st.session_state.doc_type_saved = data["document_type"]
                    st.success(
                        f"✅ {data['document_type']} generated using `{data['model']}`."
                    )
                else:
                    try:
                        detail = resp.json().get("detail", resp.text)
                    except Exception:
                        detail = resp.text
                    st.error(f"Backend error ({resp.status_code}): {detail}")
            except requests.exceptions.Timeout:
                st.error("Request timed out. Gemini may be slow — try again.")
            except Exception as e:
                st.error(f"Could not reach backend: {e}")

# ---------------- Preview + Edit ----------------
if st.session_state.document_text:
    st.markdown("---")
    st.markdown(f"### 📝 Preview — {st.session_state.doc_type_saved or 'Document'}")

    edited_text = st.text_area(
        "Edit the document below before exporting:",
        value=st.session_state.document_text,
        height=520,
        key="editor",
    )
    st.session_state.document_text = edited_text

    with st.expander("🔍 Styled Preview"):
        safe = (
            edited_text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        st.markdown(f'<div class="doc-preview">{safe}</div>', unsafe_allow_html=True)

    # ---------- Export ----------
    st.markdown("### ⬇️ Export")
    base_name = (
        (st.session_state.doc_type_saved or "document")
        .lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
    )

    c1, c2, c3 = st.columns(3)
    for col, fmt, label, mime in [
        (c1, "txt", "Download .TXT", "text/plain"),
        (
            c2,
            "docx",
            "Download .DOCX",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
        (c3, "pdf", "Download .PDF", "application/pdf"),
    ]:
        with col:
            try:
                r = requests.post(
                    f"{BACKEND_URL}/export",
                    json={
                        "content": edited_text,
                        "filename": base_name,
                        "format": fmt,
                    },
                    timeout=60,
                )
                if r.status_code == 200:
                    st.download_button(
                        label=label,
                        data=r.content,
                        file_name=f"{base_name}.{fmt}",
                        mime=mime,
                        use_container_width=True,
                    )
                else:
                    st.button(label, disabled=True, use_container_width=True)
            except Exception:
                st.button(label, disabled=True, use_container_width=True)

    if st.button("🗑️ Clear document"):
        st.session_state.document_text = ""
        st.session_state.doc_type_saved = ""
        st.rerun()

# ---------------- Footer ----------------
st.markdown("---")
st.caption(
    "⚠️ LegalEase generates template documents for informational purposes only. "
    "Always have a qualified legal professional review before use."
)

# ---------------- Inject Interactive JavaScript (Runs after page load) ----------------
st.components.v1.html(
    """
    <script>
        // 1. Cursor Glow Tracking
        document.addEventListener('mousemove', function(e) {
            var glow = window.parent.document.getElementById('cursor-glow');
            if (glow) {
                glow.style.left = e.clientX + 'px';
                glow.style.top = e.clientY + 'px';
            }
        });

        // 2. 3D Tilt Effect on Forms and Preview
        function applyTilt() {
            const elements = window.parent.document.querySelectorAll('div[data-testid="stForm"], .doc-preview');
            elements.forEach(el => {
                el.addEventListener('mousemove', (e) => {
                    const rect = el.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;
                    const rotateX = ((y - centerY) / centerY) * -2; // Subtle tilt
                    const rotateY = ((x - centerX) / centerX) * 2;
                    el.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
                    el.style.transition = 'transform 0.1s ease-out';
                });
                el.addEventListener('mouseleave', () => {
                    el.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg)`;
                    el.style.transition = 'transform 0.5s ease-out';
                });
            });
        }

        // 3. Ripple Click Effect on Buttons
        function applyRipple() {
            const buttons = window.parent.document.querySelectorAll('div[data-testid="stFormSubmitButton"] > button, div[data-testid="stButton"] > button');
            buttons.forEach(btn => {
                btn.addEventListener('click', function(e) {
                    const rect = this.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    const ripple = window.parent.document.createElement('span');
                    ripple.style.position = 'absolute';
                    ripple.style.width = '20px';
                    ripple.style.height = '20px';
                    ripple.style.background = 'rgba(255, 255, 255, 0.6)';
                    ripple.style.borderRadius = '50%';
                    ripple.style.transform = 'translate(-50%, -50%) scale(0)';
                    ripple.style.left = x + 'px';
                    ripple.style.top = y + 'px';
                    ripple.style.animation = 'rippleAnim 0.6s ease-out';
                    ripple.style.pointerEvents = 'none';
                    this.appendChild(ripple);
                    setTimeout(() => ripple.remove(), 600);
                });
            });
        }

        // Add Ripple Keyframe dynamically to parent document
        const styleSheet = window.parent.document.createElement("style");
        styleSheet.innerText = '@keyframes rippleAnim { to { transform: translate(-50%, -50%) scale(15); opacity: 0; } }';
        window.parent.document.head.appendChild(styleSheet);

        // Ensure DOM is loaded before applying scripts
        setTimeout(() => {
            applyTilt();
            applyRipple();
        }, 1500);
    </script>
    """,
    height=0,
    width=0,
)