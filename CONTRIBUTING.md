# Contributing to grapple-db

This repository contains a community-maintained database of known GitHub Actions
supply chain incidents. You don't need to understand the Grapple app code to
contribute here — just add a YAML entry and open a PR.

## Adding an incident

1. Fork this repository
2. Edit `database.yml`
3. Add your entry following the format below
4. Run `python validate.py` to check your entry is valid
5. Open a pull request

## Entry format

```yaml
- action: owner/action-name         # required: owner/repo format
  date: 2025-03-14                  # required: disclosure date (YYYY-MM-DD)
  severity: critical                # required: critical / high / medium / low
  cve: CVE-2025-30066               # optional: CVE identifier if assigned
  title: "Short description"        # required: one line, max 120 chars
  affected_repos_estimate: 23000    # optional: estimated number of affected repos
  description: |                    # required: what happened, how, impact (min 50 chars)
    Full explanation of the incident.
    What was compromised, how the attack worked, what data was exposed.
  affected_refs:                    # required: which refs were affected
    - type: all_tags_before         # all tags created before a given date
      date: 2025-03-14
  references:                       # required: at least one link
    - https://github.com/advisories/GHSA-xxxx-xxxx-xxxx
```

### `affected_refs` types

| Type | When to use | Required fields |
|---|---|---|
| `all_tags_before` | All tags were overwritten / compromised before a date | `date` |
| `tag` | A specific tag was compromised | `value` (e.g. `v4.2.0`) |
| `branch` | A specific branch was compromised | `value` (e.g. `main`) |
| `sha_range` | A range of commits was affected | `from`, `to` (full SHAs) |

### Severity levels

| Level | Meaning |
|---|---|
| `critical` | Arbitrary code execution in CI, secret exfiltration, confirmed active exploitation |
| `high` | Significant vulnerability, exploitation plausible but not confirmed at scale |
| `medium` | Vulnerability present, limited exploitability or no confirmed exploitation |
| `low` | Minor issue, informational, or theoretical risk only |

## What qualifies as an incident

- Confirmed supply chain compromise (malicious code injected into the action)
- Confirmed secret exfiltration from CI pipelines
- Confirmed tag/branch overwrite with malicious content

**Does not qualify:**
- Vulnerabilities in the software the action wraps (e.g. a CVE in a bundled library)
- Actions with weak defaults but no confirmed exploitation
- Abandoned / unmaintained actions without a known incident

## Validation

Before opening a PR, run locally:

```bash
pip install PyYAML jsonschema
python validate.py
```

CI will run the same check on your PR. A PR with validation errors will not be merged.

## Sources

Good places to find documented incidents:
- [GitHub Advisory Database](https://github.com/advisories?query=ecosystem%3Aactions)
- [OSV.dev](https://osv.dev/list?ecosystem=GitHub+Actions)
- CVE entries at [cve.org](https://www.cve.org/)
