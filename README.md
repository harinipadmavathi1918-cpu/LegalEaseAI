# ⚖️ LegalEase — AI-Powered Legal Document Generator

Generate professional legal documents (Employment Contracts, NDAs, Leases, etc.)
using Google's Gemini model, with editable previews and multi-format export.

## 🧱 Stack
- **Backend:** FastAPI + Google Generative AI (`gemini-1.5-flash`)
- **Frontend:** Streamlit
- **Export:** python-docx (DOCX), fpdf2 (PDF), plain text (TXT)

## 📁 Structure
```
legalease/
├── backend/
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   ├── export_utils.py
│   └── ai_core/
│       ├── gemini_generator.py
│       └── prompts.py
└── frontend/
    └── app.py
```

## 🚀 Setup in VS Code

### 1. Prerequisites
- Python 3.10+
- A Gemini API key → https://aistudio.google.com/app/apikey

### 2. Clone / create the folder
Open VS Code → **File → Open Folder →** create `legalease/` and paste all files above.

### 3. Create virtual environment
```bash
# macOS / Linux
python -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure `.env`
Edit `.env` and paste your key:
```
GEMINI_API_KEY=AIzaSy...your_key...
GEMINI_MODEL=gemini-1.5-flash
BACKEND_URL=http://127.0.0.1:8000
```

## ▶️ Run the App

Open **two VS Code terminals**:

**Terminal 1 — Backend**
```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
Visit http://127.0.0.1:8000/docs for interactive API docs.

**Terminal 2 — Frontend**
```bash
streamlit run frontend/app.py
```
Browser opens at http://localhost:8501

## 🧪 Test Flow

1. In Streamlit sidebar → click **Check backend health** (should be ✅).
2. Fill in the form:
   - Document Type: `Employment Contract`
   - Party A: `Acme Corp.`
   - Party B: `Jane Doe`
   - Effective Date: `2025-01-01`
   - Jurisdiction: `State of California, USA`
   - Key Terms: `Salary $120,000/year, 40 hrs/week, 2-year confidentiality, 30-day notice.`
3. Click **✨ Generate Document** → preview appears.
4. Edit if needed → Download **TXT / DOCX / PDF**.

### API test with curl
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "document_type": "Non-Disclosure Agreement (NDA)",
    "party_a": "Acme Corp.",
    "party_b": "John Smith",
    "effective_date": "2025-01-01",
    "jurisdiction": "State of New York, USA",
    "key_terms": "Mutual NDA, 3 years, excludes public info.",
    "additional_notes": ""
  }'
```

## 🐛 Troubleshooting

| Issue | Fix |
|---|---|
| `GEMINI_API_KEY is not set` | Fill `.env` and restart backend |
| `Cannot reach backend` in Streamlit | Ensure `uvicorn` is running on port 8000 |
| `502 Gemini generation failed` | Check API key quota at aistudio.google.com |
| PDF has garbled chars | Non-Latin characters are auto-replaced; stick to English |
| `ModuleNotFoundError: backend` | Run uvicorn/streamlit from the **project root** |

## 📦 Deployment (optional)

- **Backend:** Render / Railway / Fly.io → `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- **Frontend:** Streamlit Community Cloud → point to `frontend/app.py`, set `BACKEND_URL` env var to your deployed backend URL.

---

⚠️ **Disclaimer:** LegalEase produces template documents only. Always have a qualified legal professional review before use.