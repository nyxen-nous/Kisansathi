# KisanSaathi — verification record and limitations

**Packaging verification date:** 18 October 2026  
**Scope:** local source checks performed on the prepared archive. This is not a live external-service certification.

## Checks run for this prepared version

| Check | Result | What it means |
|---|---|---|
| `python -m compileall -q app scripts tests` | Passed | Python source files compile in the current environment. |
| `python -m pytest -q` | **133 tests passed** | The automated suite passed in the current environment. Several upstream integrations are mocked by design. |
| `node --check` for every `frontend/js/*.js` file | Passed | JavaScript syntax parses. This does not replace browser interaction testing. |
| EN/HI new TinyFish workflow copy | Present in both language dictionaries | The three new explainer steps have English and Hindi text. The existing frontend text tests also pass as part of pytest. |

## What the automated tests cover

The suite includes local tests for scheme API validation, source-domain filtering, redirects to untrusted domains, missing API configuration, rate limiting, TinyFish transport shape and error redaction, along with other app areas such as crop data handling, irrigation calculations, marketplace protections and bilingual strings. TinyFish, weather and mandi integration tests use mocks or fixtures where indicated by the tests.

A successful test suite means the covered local code paths behave as tested. It does not prove a live TinyFish Search or Fetch request succeeded, that every source page was accurately parsed, or that agricultural predictions are accurate in the field.

## Must verify on the team's demo machine

- [ ] Configure `TINYFISH_API_KEY` in `backend/.env` and run a real TinyFish Search + Fetch request from `/schemes.html`.
- [ ] Confirm the visible source link opens and its content supports the displayed excerpt.
- [ ] Confirm current API error messages appear correctly for missing credentials, network timeout and rate limiting.
- [ ] Perform a browser walkthrough at the display size used for the recording, in Hindi and English.
- [ ] If showing Crop Doctor, download the pinned model and test with a suitable leaf image. Its accuracy on Indian field images has not been independently measured.
- [ ] If showing live mandi or weather data, inspect source dates and disclose that the price provider is a community service and weather is a model forecast, not an official IMD warning.

## Known product limitations

- TinyFish results are research leads. Current availability, eligibility, deadlines and application processes must be confirmed with the relevant implementing authority.
- Extracted sections can be missing or incomplete. The interface indicates unavailable content and retains official source links.
- The default historical crop dataset is old (around 2012–13 unless newer data are imported).
- Crop Doctor is image-level screening and has not been independently evaluated on Indian field photographs.
- Season-planning returns are indicative and rule-based; no validated profitability model is claimed.
- Irrigation estimates use forecast ET₀, crop coefficients and typical soil values rather than live field sensors or independent agronomic validation.
- Mandi observations may be stale even when the fetch is recent. Synthetic sample rows are for UI testing only.
- The Direct Market OTP provider is console-only in the demo; real SMS integration and production privacy controls are required before public deployment.

## Claim discipline

Do not publish a score, accuracy metric, adoption figure, savings estimate or live-integration claim unless the team has direct evidence. Do not treat a mocked test response as proof of a successful external request. The live walkthrough and source inspection should be completed before submitting the demo video.
