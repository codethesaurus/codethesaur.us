# Code Thesaurus — Agent Guidelines

These guidelines help coding agents (like Junie, Copilot, OpenCode, etc.) understand the project, its structure, and how to contribute effectively.

## Critical Rules

- **Always follow Test-Driven Development (TDD):** When implementing a new feature or fixing a bug, YOU MUST first provide the test case that reproduces the issue or defines the new behavior. Only then provide the implementation. Tests live in `web/tests/`.
- **Respect read-only mode:** Do not modify files unless explicitly asked.
- **Follow existing style:** Match the project's use of PEP 8, pylint, and `isort --profile black`.
- **No interactive commands:** All terminal commands must be non-interactive.
- **Don't make large assumptions:** If something is unclear, ask before making assumptions.
- **Thesaurus data is sacred:** When editing JSON files under `web/thesauruses/`, always validate them with the management commands below before finishing.

## Project Overview

Code Thesaurus is a polyglot developer reference tool. It compares a programming-language feature (e.g. "Data Types", "Functions", "Control Structures") side-by-side across one or two languages or databases, or displays a single-language "reference sheet." It's aimed at new and experienced programmers alike, so content must be beginner-friendly and technically correct.

Most of the site is driven by JSON data files — the Django app mostly reads them and renders comparison/reference pages; the relational database only stores visit/lookup analytics.

### Key Technologies
- Python 3.14 (per `runtime.txt` and CI; project requires pinned `requirements.txt`)
- Django 6.1 (project package `codethesaurus/`, single app `web/`)
- Bootstrap 5 (CDN) + Font Awesome (CDN) for the frontend
- Pygments (syntax highlighting), django-markdownify (Markdown rendering)
- jsonmerge / jsonschema (thesaurus data handling and validation)
- SQLite for local dev, PostgreSQL in production (via `dj-database-url`)
- Gunicorn (production), WhiteNoise (static files)

## Repository Structure

- `AGENTS.md` — This file (project guidance for agents)
- `codethesaurus/` — Django project settings, root URLs, and custom error handlers (400/403/404/500)
- `web/` — The single Django app:
  - `models.py` — Non-DB classes that parse the thesaurus JSON (`MetaStructure`, `ThesaurusEntry`, `ThesaurusMetaInfo`) plus analytics DB models (`SiteVisit`, `LookupData`, `MissingLookup`)
  - `views.py` — `index`, `about`, `statistics`, `concepts` (comparison/reference pages), `api_reference`, `api_compare`, custom error handlers, and helpers that log visits/lookups/missing items
  - `urls.py` — Routes for the above (see **API** below)
  - `middleware.py` — `DatabaseDownMiddleware`: catches DB `OperationalError` and renders `error500.html`
  - `thesaurus_template_generators.py` — `generate_entry_template()` / `generate_meta_template()` for scaffolding starter JSON
  - `templatetags/templatetags.py` — `concept_card` inclusion tag
  - `templates/` — Django templates (`base.html`, `index.html`, `concepts.html`, `concept_card.html`, `statistics.html`, `about.html`, error pages, `robots.txt`)
  - `static/` — CSS (`app.css`, `pygments_colorful.css`), JS (`checkAvailableStructs.js`, `contributors.js`), images
  - `management/commands/` — `generate_template`, `generate_missing_templates`, `validatemetainfofile`, `validatelanginfofiles`
  - `tests/` — Django unit/integration tests
- `web/thesauruses/` — **The core data repository** (see **Data Model Summary**)
- `docs/` — A separate, nested MkDocs repository (docs.codethesaur.us); not part of the main git repo
- `.github/workflows/` — CI/CD (see **Pre-merge Checks**)
- Deployment files: `Dockerfile`, `docker-compose.yml`, `docker-entrypoint.sh`, `Procfile` (Heroku), `runtime.txt`, `static.json`

### API
- `GET /api/<structure>/<lang>/<version>/` — JSON reference for one language
- `GET /api/<structure>/<lang1>/<version1>/<lang2>/<version2>/` — JSON comparison of two languages

## Local Development

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Apply migrations (creates `db.sqlite3` with analytics tables) | `python manage.py migrate` |
| Create superuser (admin only) | `python manage.py createsuperuser` |
| Run dev server | `python manage.py runserver` |
| Run the whole site with Docker | `docker-compose up` (serves at `http://localhost:8000`) |
| Run all tests | `python manage.py test` |
| Validate meta info | `python manage.py validatemetainfofile` |
| Validate language info files | `python manage.py validatelanginfofiles` |
| Generate a starter language structure file | `python manage.py generate_template` |
| Generate missing structure templates | `python manage.py generate_missing_templates` |

**Note:** The site mostly works without DB data — the database only stores visit/lookup statistics and admin data, so you typically only need `migrate` + `runserver` to develop against thesaurus data.

## Data Model Summary

The thesaurus is a file-based (JSON) data model, not a relational one. All entry points understand it through `ThesaurusMetaInfo` → `MetaStructure` → `ThesaurusEntry` in `web/models.py`.

- **`meta_info.json`** — The root registry: `categories` (currently `langs` and `databases`), `languages` (key → display name for every supported language/database), and `structures` (per-category map of structure key → display name). Editing it requires running `validatemetainfofile`.
- **`_meta/<structure>.json`** — One file per concept area (e.g. `data_types.json`). Defines `meta` (`structure`, `structure_name`) and `categories`, where each category maps concept IDs → human-friendly concept names. These concept IDs must match across all language files.
- **`langs/<lang>/<version>/<structure>.json`** — One file per language/version/structure (26 languages: ada, bash, c, cpp, csharp, clips, clojure, go, haskell, java, javascript, kotlin, lua, nim, objectivec, perl, php, powershell, python, r, ruby, rust, scala, swift, typescript, vbnet). Each has a `meta` block (`language`, `language_version`, `language_name`, `structure`) and a `concepts` block keyed by the concept IDs from `_meta/`.
- **`databases/<db>/<version>/<structure>.json`** — Same pattern for databases (mongodb, mysql, postgresql) using the database structures (`deletions`, `filtering`, `inserts`, `queries`).

**Concept field rules** (validated by `validatelanginfofiles`):
- Each concept is one of: `code`, `code` + `comment`, `not-implemented`, or `not-implemented` + `comment`. Other combinations are invalid.
- `code` — the code snippet; a string or an array of strings (arrays are preferred for multiple ways to do something; use the `comment` to differentiate when to pick which).
- `comment` (singular) — explanatory notes. Never `comments`. Backticks (`` `code` ``) may be used to reference code within comments.
- `"not-implemented": true` (hyphenated) — for concepts that don't exist in that language/version. Never `not_implemented`. **Do not** write an algorithm to emulate a missing feature — mark it not-implemented instead.
- Do **not** include a `categories` section in language files; that is handled by the `_meta` files.
- Code blocks must be technically compilable/runnable if copied — no placeholder prose inside code. Keep explanatory text in `comment`.

**Analytics DB models** (`web/models.py`):
- **SiteVisit** — one row per page view (URL, user agent, referer).
- **LookupData** — one row per comparison/reference lookup, linked to a `SiteVisit` (`entry1`/`entry2` = the pair, or the single language for references).
- **MissingLookup** — records requested languages/structures/concepts that don't exist yet, so maintainers can see gaps. The `/statistics/` page aggregates all three.

## Coding Standards

- **PEP 8**: Follow standard Python style.
- **Path handling**: Use `pathlib.Path` for file-system path manipulation, not `os.path` (though `os.path` remains in legacy code — don't extend the pattern).
- **Management commands**: Use `self.stdout.write()` / `self.stderr.write()` with `self.style` (e.g. `self.style.SUCCESS`, `self.style.ERROR`) instead of `print()`.
- **Logic structure**: Break complex or monolithic methods into smaller, focused, descriptive private methods.
- **Models/helpers**: Reuse the helper methods in `web/models.py` (`ThesaurusMetaInfo`, `ThesaurusEntry` — e.g. `is_concept_complete`, `is_category_incomplete`, `has_any_implemented_in_category`) to keep view logic clean, rather than re-implementing JSON traversal.
- **Linting/formatting**: `pylint` and `isort` are pinned in `requirements.txt`. Keep code clean under both.
- **Naming conventions**: Language/entry keys are lowercase (`python`, `javascript`); JSON files are snake_case (`control_structures.json`).
- **Frontend**: UI changes go in `web/templates/` and `web/static/`. Follow existing CSS patterns in `web/static/css/`. Keep pages responsive and accessible; avoid inline styles; use Bootstrap for consistency.
- **Documentation**: Update the external docs (docs.codethesaur.us, built from the nested `docs/` MkDocs repo) for significant changes to core logic or data structures. Use docstrings for complex logic in `views.py` or management commands.

## Testing Strategy and Contribution

- **Location**: Tests live in `web/tests/` (`test_urls.py`, `test_views.py`, `test_views_extra.py`, `test_models.py`, `test_models_extra.py`, `test_db_models.py`, `test_categories.py`, `test_generators.py`, `test_templatetags.py`, `test_templates.py`, `test_commands.py`, `test_middleware.py`).
- **TDD Requirement**: When fixing bugs, add a reproducer test before applying the fix.
- **Data changes**: JSON edits under `web/thesauruses/**` require the two validation commands to pass (`validatemetainfofile` after `meta_info.json`/`_meta/` changes, `validatelanginfofiles` after language file changes). Add/update validation coverage in `test_commands.py` when the validators change.
- **Scope**: Include model parsing logic, views, templates, URL routing, and management commands.
- **Keep changes minimal** and avoid large refactors in feature tasks. Make small, targeted changes rather than building for hypothetical future needs. Do not rename files without a valid technical reason.
- **Pull requests**: Follow `.github/PULL_REQUEST_TEMPLATE.md` — note any AI bots used and complete the checklist. The project participates in Hacktoberfest; see `CONTRIBUTING.md` for the issue-claiming workflow.

### Adding a new language or database
1. Create a directory under `web/thesauruses/` with the language/database key.
2. Create a version subdirectory (e.g. `3` for Python 3).
3. Add JSON files matching the `_meta` structures — use `python manage.py generate_template` to scaffold.
4. Only implement what actually exists in the language; otherwise use `"not-implemented": true`.
5. Register the language in `meta_info.json` (`languages`) and validate with both validation commands.

## Pre-merge Checks (CI must pass)

- All tests: `python manage.py test` (after `python manage.py migrate`)
- Thesaurus data validation: `python manage.py validatemetainfofile` + `python manage.py validatelanginfofiles`
- All JSON files must be valid (checked by the `json-validate` workflow using a JSON syntax checker)
- Security scan: `bandit -r . -ll -x ./venv,./web/tests,./staticfiles`
- Dependency scans: `pip-audit -r requirements.txt` and `safety check -r requirements.txt` (run by the `security` workflow)
- CodeQL Python analysis (run by the `codeql` workflow)
- Docker build check: `docker compose build` (run by the `check-docker-build` workflow when Docker/deps change)

## Agent-Specific Tips (Junie, Copilot, OpenCode, etc.)

- Search the codebase to infer structure; `web/models.py`, `web/views.py`, and `web/thesaurus_template_generators.py` contain the important reusable code. Reuse those whenever possible.
- Before editing thesaurus data, read the relevant `web/thesauruses/_meta/<structure>.json` file to ensure new data matches the expected keys and categories.
- If a request is about adding new language/concept data, it's almost always a JSON edit + validation, not a code change — read the `docs/` project-architecture and thesaurus-editing pages (docs.codethesaur.us) for the current conventions.
- Don't introduce a build step for frontend JS/CSS; the frontend is server-rendered Django templates with hand-rolled static assets.
- The `docs/` directory is a separate git repo (MkDocs); don't commit documentation changes inside the main repo's history.
- Never edit `db.sqlite3` data as a substitute for thesaurus data, and don't rely on it being populated in CI — tests must not depend on it.