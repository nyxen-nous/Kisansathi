# KisanSaathi — किसान साथी

**A bilingual farmer-assistance prototype connecting practical farm tools with live discovery of official support information.**

KisanSaathi brings together crop-disease screening, mandi-price context, historical crop insights, season planning, weather-aware irrigation estimates, a farmer-to-buyer listing flow, and a TinyFish-powered official-source discovery page. It is designed for the AZINHACK ’26 open-innovation round: there is no fixed problem statement, so the project focuses on a clear farmer problem and demonstrates a functional TinyFish use case.

> **Demo focus for judges:** open **Farmer support**, choose a state and type of support, and demonstrate TinyFish Search → official-domain filtering → TinyFish Fetch → source-backed results. This feature needs a configured TinyFish API key and internet access. Search results are research leads, not official eligibility decisions.

## Why KisanSaathi

Finding useful farm support can require navigating multiple department sites and documents. KisanSaathi aims to reduce that friction by placing several farm decision-support tools in one Hindi/English interface and using TinyFish to discover and read relevant government pages from a farmer’s selected state and support category.

## Features

| Area | What it does | Important boundary |
|---|---|---|
| **Farmer support (TinyFish)** | Searches and extracts relevant information from eligible Indian government domains for irrigation, solar pumps, equipment, crop insurance and income-support queries. | Does not confirm eligibility or guarantee that an application window is open. Always check the linked authority source. |
| **Crop Doctor** | Screens a leaf image using a pretrained classifier and provides general bilingual advice. | Field performance on Indian photographs has not been independently measured; not a confirmed diagnosis. |
| **Mandi Bhav** | Shows dated mandi price observations and helps compare a trader offer with estimated mandi proceeds after user-entered costs. | Default community provider covers five states and can be stale; source date is more important than fetch time. |
| **Crop Insights** | Explores historical crop area and production by state, district, crop, season and year. | Bundled community history is old (around 2012–13); newer data import is optional. |
| **Next Season Planner** | Compares available yield, price and user-entered cost evidence and explains missing inputs. | Rule-based, indicative decision support, not a validated profit prediction. |
| **Weather** | Retrieves current conditions and a 1–7 day forecast when requested. | Open-Meteo model forecast, not an official IMD warning. |
| **Irrigation Planner** | Estimates a seven-day root-zone water balance using forecast rain/ET₀, crop coefficients and typical soil parameters. | Estimates depend on field inputs and generic soil assumptions; not a sensor reading or agronomic certification. |
| **Direct Market** | Lets farmers publish produce listings and buyers register interest, with PIN safeguards and optional OTP workflow. | OTP is console-only in the demo; a real SMS gateway and production privacy controls are required before public launch. |

## TinyFish integration: what is actually implemented

The Farmer support flow uses both TinyFish Search and TinyFish Fetch. The backend owns the API key; the browser never receives it.

1. A farmer selects a state and support category.
2. The backend builds a focused query and calls TinyFish Search.
3. Search results are filtered to HTTPS URLs under `.gov.in` or `.nic.in` (plus a maintained official PM-KUSUM seed source for the solar category).
4. TinyFish Fetch retrieves up to five page results as Markdown.
5. The backend extracts relevant sections where possible and returns the source URL, retrieval time, state-mention signal, and incomplete/possibly outdated warnings.
6. The interface presents excerpts as source material, not as verified claims of benefit or eligibility.

**Relevant code:**

- `backend/app/services/tinyfish.py` — server-side TinyFish transport and error redaction.
- `backend/app/services/schemes.py` — source filtering, extraction and period handling.
- `backend/app/routers/schemes.py` — validated, rate-limited API endpoint.
- `frontend/schemes.html` and `frontend/js/schemes.js` — farmer-facing UI.
- `backend/tests/test_schemes.py` — mocked contract, filtering, validation, partial-page, redirect and error tests.

The automated tests validate these local code paths with mocked API responses. They do **not** prove a live TinyFish request has succeeded using your team’s key. Run the live demo steps below before recording the submission video.

## Quick start for the hackathon demo

**Requirements:** Python 3.11–3.13, Node.js for frontend text/syntax checks, internet access, and a TinyFish API key for the mandatory live feature. On Windows, run commands in PowerShell. Use a fresh environment where possible.

### 1. Create an environment and install dependencies

From the repository root:

```powershell
cd backend
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
Copy-Item .env.example .env
```

For macOS/Linux, use `python3 -m venv .venv`, `source .venv/bin/activate` and `cp .env.example .env` instead. Run backend Python commands from the `backend/` directory.

### 2. Configure TinyFish locally

Open `backend/.env` and set:

```dotenv
TINYFISH_API_KEY=your_actual_tinyfish_key
PRELOAD_MODEL=0
MANDI_AUTO_REFRESH_ENABLED=false
```

Create the key through the TinyFish account portal. Keep `.env` private: do not paste the key into chat, screenshots, source code or GitHub. `PRELOAD_MODEL=0` avoids a background model warm-up for a short TinyFish-focused demo; Crop Doctor may remain unavailable until its model is downloaded. Disabling the in-process mandi scheduler avoids unrelated external calls during the showcase. These are local-demo settings, not recommended universal production defaults.

### 3. Start and verify the app

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open these pages:

- App home: <http://127.0.0.1:8000/>
- **TinyFish feature:** <http://127.0.0.1:8000/schemes.html>
- API docs: <http://127.0.0.1:8000/docs>
- Health check: <http://127.0.0.1:8000/health>

### 4. Run a real demonstration

1. Open `/schemes.html` and choose **Punjab → Solar pumps**.
2. Start the search and wait for the live response.
3. Show the returned official source URL and retrieval time.
4. Expand the benefits, eligibility, application or period sections where the retrieved page provides them.
5. Open the official source in a new tab and compare it with the excerpt.
6. Explain that unreadable sections and uncertain current status are deliberately labelled rather than invented.

If the request fails, use the UI’s error message and inspect the backend terminal. Do not present mocked test results as a live call. Keep a fallback recording only as clearly labelled backup evidence, not as proof of a live run.

## Architecture

```text
Browser (HTML / CSS / JavaScript, Hindi + English)
                     │ REST/JSON
                     ▼
FastAPI backend ── validation / rate limiting / domain checks
  ├── TinyFish Search ── discover pages
  ├── TinyFish Fetch  ── read page content
  ├── SQLAlchemy + SQLite (default local database)
  ├── Crop/price/planning/irrigation services
  └── Weather and optional ML/data providers
```

**Stack:** FastAPI, Pydantic, SQLAlchemy, SQLite by default, plain HTML/CSS/JavaScript, Hugging Face Transformers for the optional crop model, TinyFish Search and Fetch for official-source research, and Open-Meteo for the weather/irrigation forecast path.

## Verification

Run the checks from the repository root:

```powershell
cd backend
python -m compileall -q app scripts tests
python -m pytest -q
Get-ChildItem ..\frontend\js\*.js | ForEach-Object { node --check $_.FullName }
```

The packaging environment collected and passed **133 automated backend tests**. The suite uses mocked external APIs and a fake disease classifier in relevant tests; passing it demonstrates covered local code paths, not external service availability or real-world model/agronomic accuracy. See [`VERIFICATION_REPORT.md`](VERIFICATION_REPORT.md) and [`TEST_RESULTS.txt`](TEST_RESULTS.txt) for the bounded verification record.

## Known limitations and responsible-use notes

- TinyFish results can be incomplete, and extracted content can omit important context. Verify each decision with the linked government authority.
- The scheme page does not confirm active application windows, farmer-specific eligibility, or approval odds.
- Crop Doctor is a screening aid; field-photo accuracy has not been independently evaluated.
- Crop planning is evidence-based and rule-based, not a validated profitability model. The bundled crop-history dataset is dated.
- Mandi source dates may be old even when an API fetch is recent. Synthetic CSV records are for UI testing only.
- Weather is a model forecast, not an official IMD warning. Irrigation figures are estimates using generic soil values.
- Direct Market’s OTP provider writes codes to the backend console; real SMS delivery, production privacy controls and shared rate limiting are not included.
- Do not use the prototype as the sole basis for financial, pesticide or irrigation decisions.

## Repository map

```text
backend/app/              FastAPI routers, schemas, data models and services
backend/scripts/           Data/model setup, import, verification and demo utilities
backend/tests/             Automated regression and behaviour tests
frontend/                  Responsive bilingual pages, styles and JavaScript
 data/                     Synthetic mandi samples and data-source notes
ml/                        Model cache location (weights are downloaded separately)
```

## Submission assets

The `submission/` folder contains a judge walkthrough, demo script, social post draft, rubric checklist, and team-contribution worksheet. Complete the few team-specific items honestly before publishing. The presentation deck is supplied alongside the project archive.

## Detailed references

- [`README_DETAILED_REFERENCE.md`](README_DETAILED_REFERENCE.md) — extended setup, data provenance, API reference and operational notes.
- [`DECISION_SUPPORT_METHODOLOGY.md`](DECISION_SUPPORT_METHODOLOGY.md) — methodology and decision-support limits.
- [`DATA_ACCESS_STATUS.md`](DATA_ACCESS_STATUS.md) — data source/access status.
- [`FRONTEND_DESIGN_NOTES.md`](FRONTEND_DESIGN_NOTES.md) — design intent and usability notes.
- [`AZINHACK_CHANGES.md`](AZINHACK_CHANGES.md) — files touched for TinyFish integration.

## Before publishing

- Add actual team names, roles and genuine contributions to the public repository and presentation; do not invent contributor details.
- Confirm with the organisers that extending a pre-existing project is eligible under their originality rule. Clearly distinguish earlier project work from event-specific work.
- Make sure the GitHub repository is public, the README matches the actual setup, and the video/social post/PPT submitted to the event are the final versions.
