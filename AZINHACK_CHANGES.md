# AZINHACK submission preparation changes

This archive has been prepared for evaluation from the supplied KisanSaathi project.

## Project/code presentation changes

- Replaced the lengthy top-level README with an evaluator-first project description, architecture, TinyFish explanation, quick start, verification commands and limitations.
- Preserved the former full README as `README_DETAILED_REFERENCE.md`, removing placeholder contributor names and internal member ownership labels.
- Added a localized 3-step explainer on the Farmer Support page so judges can see the Search → Fetch workflow without confusing it with a generic search box.
- Corrected Farmer Support page metadata and tightened the frontend HTTPS/government-domain URL check.
- Removed internal `Member A/B/C/D` ownership comments from code and documentation where present.

## Evaluation assets

- `submission/DEMO_RUNBOOK.md`
- `submission/JUDGE_WALKTHROUGH.md`
- `submission/SOCIAL_POST_DRAFT.md`
- `submission/RUBRIC_READINESS_CHECKLIST.md`
- `submission/TEAM_CONTRIBUTIONS_WORKSHEET.md`
- `VERIFICATION_REPORT.md` and `TEST_RESULTS.txt`

## Important boundaries

- No credentials are included. Configure `TINYFISH_API_KEY` privately on the machine used for the live demo.
- Automated tests use mocked responses where documented; this package does not claim that a live TinyFish run was completed during packaging.
- Team names and genuine individual contributions were not provided with the archive, so none are invented. Complete the team worksheet before public release.
- Confirm originality/eligibility with organisers if project components predate this event.
