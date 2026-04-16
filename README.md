# grapple-db

Community-maintained database of known GitHub Actions supply chain incidents.

Used by [Grapple](https://github.com/excla1mmm/Grapple) to flag compromised actions in CI/CD workflows. Other tools can use this database independently as a git submodule.

## What's inside

| File | Purpose |
|---|---|
| `database.yml` | Incident records: action name, date, severity, description, affected refs |
| `schema.json` | JSON Schema — defines the valid structure for each entry |
| `validate.py` | Validation script — run by CI on every pull request |
| `CONTRIBUTING.md` | How to add a new incident |

## Current incidents

| Action | Date | Severity | CVE |
|---|---|---|---|
| `tj-actions/changed-files` | 2025-03-14 | critical | CVE-2025-30066 |
| `reviewdog/action-misspell` | 2025-03-14 | critical | — |
| `reviewdog/action-actionlint` | 2025-03-14 | critical | — |
| `reviewdog/action-shellcheck` | 2025-03-18 | critical | — |
| `reviewdog/action-composite-template` | 2025-03-18 | critical | — |
| `reviewdog/action-staticcheck` | 2025-03-18 | critical | — |
| `reviewdog/action-ast-grep` | 2025-03-18 | critical | — |
| `reviewdog/action-typos` | 2025-03-18 | critical | — |
| `reviewdog/action-setup` | 2025-03-19 | high | CVE-2025-30154 |
| `aquasecurity/trivy-action` | 2026-03-15 | critical | — |

## Adding an incident

Open a pull request editing `database.yml`. CI will automatically validate your entry against `schema.json`. See [CONTRIBUTING.md](CONTRIBUTING.md) for the format and severity guidelines.

## Using as a submodule

```bash
git submodule add git@github.com:excla1mmm/grapple-db.git incidents
git submodule update --init --remote
```

The database is then available at `incidents/database.yml`.
