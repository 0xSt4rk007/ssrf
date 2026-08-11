# SSRF Canary

A minimal, generic Flask service for **authorized security testing**.

It provides harmless endpoints that let you verify:

- server-side callbacks
- response-header reflection
- HTTP redirect following
- final redirect destination

It does **not** perform internal network scanning, cloud-metadata access, credential collection, or other active probing.

## Endpoints

| Endpoint | Purpose |
|---|---|
| `/test` | Simple 200 callback with `X-SSRF-Test` |
| `/headers` | Distinctive headers for reflection testing |
| `/redirect` | HTTP 302 redirect to `/final` |
| `/final` | Distinct final destination |
| `/health` | Health check |
| `/` | Endpoint index |

## Local usage

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

The app listens on:

```text
http://127.0.0.1:8000
```

## Render deployment

Create a new Render Web Service from this repository.

Build command:

```text
pip install -r requirements.txt
```

Start command:

```text
gunicorn app:app
```

Render supplies the `PORT` environment variable automatically.

After deployment, suppose Render gives you:

```text
https://ssrf-canary.example.onrender.com
```

Useful URLs are:

```text
https://ssrf-canary.example.onrender.com/test
https://ssrf-canary.example.onrender.com/headers
https://ssrf-canary.example.onrender.com/redirect
https://ssrf-canary.example.onrender.com/final
https://ssrf-canary.example.onrender.com/health
```

## Example authorized SSRF tests

### Server-side callback

Supply `/test` to the authorized target's URL-fetching parameter.

Expected callback response:

```text
HTTP 200
X-SSRF-Test: ssrf-canary-001
```

### Header reflection

Supply `/headers`.

If the target reflects upstream headers, look for:

```text
X-SSRF-Test: mmp-ssrf-001
X-Researcher-Test: canary-001
```

### Redirect following

Supply `/redirect`.

The endpoint returns:

```text
HTTP 302
Location: /final
```

If the target follows redirects, its observed final URL should become:

```text
/final
```

The target should be tested only within the authorization/scope of the relevant disclosure program.

## Evidence

For a report, preserve:

1. Request sent to the target.
2. Target's response.
3. Canary request/response or application logs.
4. Timestamp and unique endpoint used.

Do not put credentials, cookies, or sensitive information into this canary.

## Operational note

If deployed on a free/scale-to-zero platform, the first request may be delayed while the service wakes up. That is normal and should not be interpreted as a failed SSRF test.
