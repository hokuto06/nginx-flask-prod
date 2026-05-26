# HANDOFF — nginx-flask-prod

> **Note**: This file documents an active security remediation session.
> Remove or archive it once Phase 2 is complete and all items below are resolved.

_Generated: 2026-05-25_
_Auditor: Claude Sonnet 4.6 (repo-audit-toolkit)_

---

## Repository State

| Field | Value |
|-------|-------|
| Remote | https://github.com/hokuto06/nginx-flask-prod |
| Branch | `main` (only branch) |
| HEAD | `65d7947` |
| Working tree | Clean — nothing uncommitted |
| Ahead of origin | 0 — fully pushed |

---

## Completed This Session

### Commit `1cd7f63` — Remove tracked secrets and runtime artifacts
_2026-05-25_

| Item | Action |
|------|--------|
| `django_blog_front/settings.py` | Hardcoded `SECRET_KEY` removed; replaced with `env("SECRET_KEY")` via django-environ (was already wired, just commented out) |
| `django_blog_front/db.sqlite3` | Untracked with `git rm --cached` — file still on disk, no longer in git index |
| `django-api/venv/` (4,477 files) | Untracked with `git rm -r --cached` — venv still on disk, no longer in git index |
| `.gitignore` | Added: `*.sqlite`, `*.sqlite3`, `venv/`, `*/venv/` |
| `app/.env.example` | Created — documents `FLASK_SECRET_KEY` |
| `django-api/.env.example` | Created — documents `SECRET_KEY`, DB creds, AWS creds |
| `django_blog_front/.env.example` | Created — documents `SECRET_KEY` |

### Commit `65d7947` — Improve deployment and operational documentation
_2026-05-25_

| Item | Action |
|------|--------|
| `README.md` | Rewritten: correct docker compose command, per-service `.env` setup, `[restart]`/`[rebuild]` deploy convention, certbot renewal, secrets table, port map |
| `.github/workflows/deploy.yml` | Header comment added explaining commit-tag convention and required GitHub secrets |
| `docker-compose.yml` | Letsencrypt double-mount annotated — explains the `:ro` host mount vs local certbot bind mount |

---

## Active Branches

Only `main`. No feature branches were created during this session.

---

## Pending Changes (not yet implemented)

These were designed and proposed but **not committed**. Implementation requires
a separate session and, for some items, server-side `.env` changes before pushing.

### Phase 2A — `ALLOWED_HOSTS` hardening
**Files:** `django-api/django_api_blog/settings.py:20`, `django_blog_front/django_blog_front/settings.py:20`

```python
# Current (both files)
ALLOWED_HOSTS = ["*"]

# Target
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])
```

**Server prerequisite** — must be in each service's `.env` on EC2 **before** push:
```
ALLOWED_HOSTS=estebanmartins.com.ar,blog.estebanmartins.com.ar,localhost
```

**Risk:** If env var is missing on server at restart time, Django defaults to
`["localhost"]` and all inbound requests return HTTP 400. Verify `.env` via SSH
before pushing.

---

### Phase 2B — CORS tightening
**File:** `django-api/django_api_blog/settings.py:54`

```python
# Current
CORS_ALLOW_ALL_ORIGINS = True

# Target
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
```

**Server prerequisite** — `django-api/.env` must contain:
```
CORS_ALLOWED_ORIGINS=https://estebanmartins.com.ar,https://blog.estebanmartins.com.ar
```

**Risk:** Low — affects browser cross-origin requests only. Server-to-server
and curl calls are not blocked. Can be rolled back by reverting `settings.py`
and running `[restart]`.

---

### Phase 2C — Restart policies
**File:** `docker-compose.yml`

Add `restart: unless-stopped` to `flask`, `api`, `blog-front`, `nginx`, `certbot`.

**Risk:** None. Additive only. Means containers survive EC2 reboots without
manual `docker compose up -d`.

---

### Phase 2D1 — Docker non-root (Flask only)
**File:** `app/Dockerfile`

```dockerfile
RUN addgroup --system app && adduser --system --ingroup app app
USER app
```

Flask has no live source-code volume mount in production — safe to do without
volume ownership changes. Requires `[rebuild]`.

---

### Phase 2D2 — Docker non-root (Django services)
**Files:** `django-api/Dockerfile`, `django_blog_front/Dockerfile`, `docker-compose.yml`

**Deferred.** Both Django services use live source-code mounts
(`./django-api:/app`) owned by the host `ubuntu` user (UID 1000).
Creating a container system user requires matching the host UID or changing
the volume mount strategy. Do not implement without planning the `chown`
approach or removing live mounts.

---

## Known Risks

### Burned SECRET_KEY in git history
`django-insecure-vx*^$h9#fbg3a_fg=p+^*+)*zamsn_6%wqg+-k-g@5cqmss@94`

This key is permanently in the public git history of `django_blog_front`.
It was removed from the codebase in commit `1cd7f63` but **git history was not
rewritten** (intentional — no force push, no `git filter-repo`). The key is
effectively public.

**Action required:**
- Generate a new key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Place it in `django_blog_front/.env` on the EC2 server
- Restart the `blog-front` container: `docker compose restart blog-front`
- The old key must never be used again

If this was not done yet, **do it now**. Active Django sessions signed with the
old key will be invalidated on restart (users must log in again — acceptable).

### `db.sqlite3` in git history
`django_blog_front/db.sqlite3` was committed at `e2527700` (2025-06-09,
"enviando sqlite a prod") and is permanently in public history. It contains
Django ORM data as of that commit. No history rewrite was performed.

History cleanup (e.g. `git filter-repo --path django_blog_front/db.sqlite3 --invert-paths`)
is a future option but requires force-push and coordination with any forks or
CI/CD keys. Not urgent — the file is old data, not credentials.

### `venv/` in git history
`django-api/venv/` was in git history before commit `1cd7f63`. History was not
rewritten — the objects remain. This only affects clone/fetch size for users
who pull full history. No security impact.

---

## Recommended Next Steps

In order of priority:

1. **[Server — immediate]** Verify `django_blog_front/.env` on EC2 contains a
   fresh `SECRET_KEY`. Rotate the burned key if not already done.

2. **[Next commit]** Phase 2C — restart policies. Zero risk, single file change,
   push with `[restart]`.

3. **[Next commit, after server .env prep]** Phase 2A + 2B — `ALLOWED_HOSTS`
   and CORS. Prepare `.env` on server first, then push, then verify in browser.

4. **[Separate commit]** Phase 2D1 — Flask non-root Dockerfile.

5. **[Separate commit, after D1]** Phase 2D2 — Django non-root, once volume
   ownership strategy is decided.

6. **[Future]** Consider `git filter-repo` to remove `db.sqlite3` and `venv/`
   from history. Coordinate with any CI/CD webhooks before force-pushing.

---

## Commands to Resume Work

```bash
# Navigate to the cloned repo (already on disk)
cd ~/repo-audit-toolkit/tmp/nginx-flask-prod

# Confirm clean state
git status
git log --oneline -5

# Pull latest from origin before making changes
git pull origin main

# Re-run the full audit toolkit (for updated baseline after changes)
bash ~/repo-audit-toolkit/scripts/run_audit.sh \
  ~/repo-audit-toolkit/tmp/nginx-flask-prod

# View current audit reports
ls ~/repo-audit-toolkit/reports/
cat ~/repo-audit-toolkit/reports/FINAL_SUMMARY.md
```

---

## Rollback Procedures

### Roll back a pushed commit (last resort — requires force push)
```bash
# Identify the commit to revert to
git log --oneline -10

# Create a revert commit (safe, no history rewrite)
git revert <commit-sha>
git push origin main
```

### Roll back individual file changes without touching history
```bash
# Restore a specific file to a previous commit's version
git checkout <commit-sha> -- path/to/file
git commit -m "Revert <file> to <commit-sha>"
git push origin main
```

### Roll back ALLOWED_HOSTS change without redeploying code
```bash
# SSH to EC2 and edit .env directly — no rebuild needed
ssh ubuntu@<EC2_HOST>
echo "ALLOWED_HOSTS=*" >> /home/ubuntu/nginx-flask-prod/django-api/.env
docker compose restart api
```

---

## Operational Dependencies

### On the EC2 server (`/home/ubuntu/nginx-flask-prod/`)

| File | Required by | Status |
|------|-------------|--------|
| `app/.env` | Flask (`FLASK_SECRET_KEY`) | Must exist — not in repo |
| `django-api/.env` | django-api (`SECRET_KEY`, DB creds, AWS creds) | Must exist — not in repo |
| `django_blog_front/.env` | blog-front (`SECRET_KEY`) | **Verify contains fresh key** |
| `./letsencrypt/` | Nginx + certbot (TLS certs) | Managed by certbot locally |
| `./nginx/conf.d/` | nginx-proxy | Tracked in repo |

### GitHub Secrets (Settings → Secrets → Actions)

| Secret | Purpose |
|--------|---------|
| `SSH_PRIVATE_KEY` | ed25519 key for EC2 SSH in deploy workflow |
| `EC2_HOST` | Server IP/hostname |
| `EC2_USER` | SSH user (typically `ubuntu`) |

### AWS (used by django-api at runtime)

| Service | Usage |
|---------|-------|
| SES (us-east-1) | Flask app sends email via boto3 |
| DynamoDB (us-east-1) | Flask app reads `email_received` table |
| S3 | django-api stores post media (bucket in `AWS_STORAGE_BUCKET_NAME`) |

Credentials for SES/DynamoDB come from the EC2 instance role or `app/.env`.
Credentials for S3 come from `django-api/.env`.

### DNS

| Domain | Service |
|--------|---------|
| `estebanmartins.com.ar` | Nginx → Flask landing |
| `blog.estebanmartins.com.ar` | Nginx → blog-front |
| (multiple subdomains) | Nginx virtual hosts in `nginx/conf.d/` |

### Docker

```bash
# Check running containers on EC2
docker compose ps

# View logs for a specific service
docker compose logs -f blog-front

# Restart a single service after .env change (no rebuild)
docker compose restart blog-front

# Rebuild and restart after Dockerfile change
docker compose up -d --build blog-front
```

### Commit-tag deploy convention

| Tag in commit message | Effect on EC2 |
|----------------------|---------------|
| `[restart]` | `docker compose down && docker compose up -d` |
| `[rebuild]` | `docker compose up -d --build` |
| _(none)_ | `git pull` only |

---

## Audit Toolkit Location

The toolkit used to generate this audit lives at:

```
~/repo-audit-toolkit/
  scripts/run_audit.sh       # runs all four scans
  scripts/inventory.sh
  scripts/secrets_scan.sh
  scripts/docker_audit.sh
  scripts/git_hygiene.sh
  scripts/generate_summary.py
  reports/                   # last scan results (nginx-flask-prod)
  tmp/nginx-flask-prod/      # cloned repo
```

To audit a different repository:
```bash
bash ~/repo-audit-toolkit/scripts/run_audit.sh /path/to/other-repo
```
