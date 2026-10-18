# Judge walkthrough and technical Q&A

## 30-second pitch

KisanSaathi is a bilingual farmer-assistance prototype that combines practical farm tools with source-backed support discovery. Its AZINHACK-specific feature uses TinyFish Search to discover relevant pages and TinyFish Fetch to read selected official sources, then presents excerpts with links and uncertainty signals. It does not claim to decide eligibility or replace the implementing department.

## Why TinyFish is part of the product

The user may describe a need (for example, solar-pump assistance) without knowing the exact scheme or which department page contains it. Search discovers candidate pages; Fetch retrieves content so the app can expose useful sections and link directly to the source. The integration is backend-side, so the API key is not placed in browser code.

## Likely judge questions

**Q: Is TinyFish mandatory and where is it used?**  
A: Yes, Farmer Support uses TinyFish Search and Fetch in the real backend path. The relevant files are `backend/app/services/tinyfish.py`, `backend/app/services/schemes.py`, and `backend/app/routers/schemes.py`.

**Q: How do you avoid fabricated scheme claims?**  
A: The interface presents source excerpts and source URLs; it marks unreadable details as unavailable and calls out that state applicability and current status need confirmation. It is not a scheme registry or an eligibility engine.

**Q: How do you constrain source URLs?**  
A: Search results are filtered to HTTPS URLs whose host ends in `.gov.in` or `.nic.in`. The same trust boundary is checked after Fetch so an untrusted final URL is not treated as extracted official content. The frontend repeats a conservative URL check before creating the source link.

**Q: What do your tests prove?**  
A: Automated tests cover local behaviour such as URL boundaries, validation, rate limits, error redaction and partial/unreadable pages using mocks. They do not prove live TinyFish availability or the factual correctness of every extracted scheme statement. The live demonstration verifies the current configured environment.

**Q: What are the key limitations?**  
A: Source extraction may be incomplete; scheme dates and eligibility need authority confirmation; some legacy agriculture data is dated; crop-disease performance on Indian field photos has not been independently measured; weather and irrigation outputs are estimates.

**Q: Is the project entirely new for this hackathon?**  
A: Answer transparently. Identify any earlier KisanSaathi code, explain which event-specific changes the team made, and confirm eligibility with organisers. Do not claim earlier work was produced during the event.

## Evidence to open if asked

- TinyFish transport: `backend/app/services/tinyfish.py`
- Domain filtering and section extraction: `backend/app/services/schemes.py`
- API request/validation/rate limiting: `backend/app/routers/schemes.py`
- Automated tests: `backend/tests/test_schemes.py`
- Test/limitation notes: `VERIFICATION_REPORT.md`
