# KisanSaathi demo runbook (2:30–3:00)

## Before recording

- Use the actual laptop/network environment planned for the judging demo.
- Configure `TINYFISH_API_KEY` in `backend/.env`; never reveal it on-screen.
- Start the backend and open `http://127.0.0.1:8000/schemes.html`.
- Test one real search and verify that each visible source URL opens.
- Close terminals/tabs that reveal secrets, personal data or unrelated errors.
- If TinyFish is unavailable, do not pretend a mocked result is live. Explain the issue and record a clearly labelled backup walkthrough only if the rules permit it.

## Timed script

**0:00–0:15 — Problem**  
“Farmers may have to navigate several department websites to find assistance information. KisanSaathi brings common farm tools together and makes official-source discovery part of the workflow.”

**0:15–0:35 — Product context**  
Show the homepage briefly. Point out the Hindi/English toggle and the farmer support entry. Do not spend the whole video listing every feature.

**0:35–1:25 — Live TinyFish workflow**  
Open Farmer support. Select **Punjab → Solar pumps** and run the search. Say: “TinyFish Search discovers candidate pages; our backend filters to approved government domains, then TinyFish Fetch reads the selected pages.” Show the actual response and source links.

**1:25–1:55 — Trust and boundaries**  
Expand the extracted benefits/eligibility/application/period fields. Point out retrieval time and the state-applicability status. Open the official source. Explain: “This is a research lead, not an eligibility decision. If content cannot be read or the date is unclear, the interface says so rather than inventing an answer.”

**1:55–2:20 — One other working feature**  
Briefly show a second page only if it is configured and returns honest data. Mark sample data as sample; do not present stale or synthetic prices as current market facts.

**2:20–2:45 — Technical wrap-up**  
Show the TinyFish service path in the repository and the test suite. Explain that tests cover filtering, validation and failure handling with mocked external calls, while the video proves the actual live request.

**2:45–3:00 — Close**  
“KisanSaathi’s goal is to reduce the effort required to find and act on farm information while keeping source links and uncertainty visible.”

## Capture checklist

- Keep pointer movement deliberate and browser zoom readable.
- Show one uninterrupted live TinyFish result.
- Make source title, URL and retrieval time legible.
- Do not show `.env`, API keys, phone numbers, passwords or private farmer data.
- Use captions or clear narration; avoid background music that masks speech.
- Test the final uploaded/unlisted video URL from a signed-out browser if the organisers need public access.
