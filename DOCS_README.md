# Failure Forensics documentation site

MkDocs Material site in the same layout as the CMPUT 401 KneadTech docs.

## Add to the repository

Copy `mkdocs.yml`, `requirements-docs.txt`, `docs/` and `.github/workflows/docs.yml` into the root of
`UndergraduateArtificialIntelligenceClub/Failure-Forensics` and merge `.gitignore` lines.

Then in GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
The next push to `main` publishes to
https://undergraduateartificialintelligenceclub.github.io/Failure-Forensics/

## Preview locally

    pip install -r requirements-docs.txt
    mkdocs serve

## Updating

- Sprint plans, user stories, story map, roles and sprint report skeletons were generated from the Jira backlog (KAN) on 31 Oct 2026. Jira is the source of truth; edit the pages by hand from now on.
- Fill in names on `docs/teamwork/roles.md`, the team canvas, and each sprint's progress report and meeting minutes as you go.
