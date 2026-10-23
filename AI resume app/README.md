# AI Resume & Cover Letter Generator (Gemini API)

A simple Streamlit app with a clean, ChatGPT-style interface. Upload your resume,
paste a job description, and Google Gemini tailors both a resume and a cover
letter for that job — edit them right in the browser and download as PDF.

## Features
- Upload resume as PDF, DOCX, or TXT
- Paste any job description
- Gemini rewrites/tailors your resume for that specific job (never invents fake experience)
- Gemini writes a matching, personalized cover letter
- Edit both documents directly in the app before downloading
- Download both as clean PDF files
- API key can live in a `.env` file so you never have to paste it in the browser
- Uses Google's official `google-genai` SDK (the current recommended library)

---

## Step-by-step Setup (Windows / VS Code)

### 1. Unzip the project
Unzip this folder somewhere simple, e.g. `C:\Users\<you>\Documents\gemini-resume-app`.
**Make sure you don't end up with a folder inside an identical folder**
(check that `app.py` is directly inside the folder you open in VS Code — not one
level deeper).

### 2. Open the folder in VS Code
`File > Open Folder...` and select the unzipped `gemini-resume-app` folder.
Open a terminal inside VS Code (``Terminal > New Terminal``).

### 3. Create and activate a virtual environment
```powershell
python -m venv venv
venv\Scripts\activate
```
You should see `(venv)` appear at the start of your terminal prompt.

### 4. Install dependencies
```powershell
python -m pip install -r requirements.txt
```
> We use `python -m pip` instead of plain `pip` — see the Troubleshooting
> section below if you ever see "Application Control policy has blocked this file".

### 5. Get a free Gemini API key
1. Go to **https://aistudio.google.com/app/apikey**
2. Sign in with your Google account
3. Click **Create API Key** (a free tier is available — no credit card needed
   for basic usage/testing, within Google's quota limits)
4. Copy the key

### 6. Add your Gemini API key to the project
1. In this project folder, copy `.env.example` to a new file named exactly `.env`
2. Open `.env` and paste your real key:
   ```
   GEMINI_API_KEY=your-real-gemini-key-here
   ```
3. Save the file. The app will pick it up automatically — you won't need to
   paste your key into the browser at all.

   (Alternative: skip the `.env` file and just paste your key into the sidebar
   text box every time you run the app — either works.)

### 7. Run the app
```powershell
python -m streamlit run app.py
```
Your browser should open automatically at `http://localhost:8501`.

---

## Project Structure
```
gemini-resume-app/
├── app.py              # Main Streamlit app (UI + flow)
├── utils.py            # Resume text extraction, Gemini API call, PDF generation
├── requirements.txt    # Python dependencies
├── .env.example         # Template for your API key — copy to .env
├── .gitignore
├── .streamlit/
│   └── config.toml      # Clean theme settings
└── README.md
```

---

## Troubleshooting

**"Could not open requirements file"**
You're in the wrong folder. Run `dir` (or `ls`) and confirm `app.py` and
`requirements.txt` are listed before running any command. `cd` into the
correct folder first.

**"Program 'pip.exe' / 'streamlit.exe' failed to run: An Application Control
policy has blocked this file"**
This is a Windows security policy (common on managed/work laptops) blocking
`.exe` files from running directly. Fix: always call tools through Python
instead of calling the `.exe` directly:
```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

**`ModuleNotFoundError: No module named 'google'` (or any other module)**
This means `pip install -r requirements.txt` never actually completed in the
right folder/environment. Make sure `(venv)` is shown in your prompt, `cd` into
the folder with `requirements.txt`, then re-run:
```powershell
python -m pip install -r requirements.txt
```

**Authentication error (401/403)**
Your API key was rejected. Checklist:
- Copy the full key fresh from https://aistudio.google.com/app/apikey
  (no extra spaces or missing characters)
- Confirm the key hasn't been deleted in AI Studio
- If a key has ever been shared/screenshotted, delete it and generate a new one —
  treat any exposed key as compromised

**429 Rate limit / RESOURCE_EXHAUSTED**
The free tier has request-per-minute and per-day limits. Wait a minute and
try again, or reduce how often you click Generate.

**PDF text extraction comes back empty**
Your resume PDF is likely a scanned image rather than real text. Save/paste
your resume content as a `.txt` file instead and upload that.

**Want to use a different Gemini model?**
Add this line to your `.env` file:
```
GEMINI_MODEL=gemini-2.5-pro
```
(or any other model name available to your account/region).

---

## Security Notes
- Never commit your `.env` file or share your API key in screenshots/chats —
  anyone with it can use your account's quota.
- `.env` is already excluded via `.gitignore` so it won't accidentally get
  committed if you put this project in Git.
- The key is only used locally to call the Gemini API — it is not sent
  anywhere else and not stored by the app itself.
