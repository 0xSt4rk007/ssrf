import os
from flask import Flask, jsonify, make_response, redirect, request

app = Flask(__name__)

@app.get("/")
def index():
    return jsonify({
        "service": "SSRF Canary",
        "status": "ok",
        "endpoints": {
            "basic": "/test",
            "headers": "/headers",
            "redirect": "/redirect",
            "final": "/final",
            "health": "/health"
        }
    })

@app.get("/test")
def test():
    """Simple 200 response for proving a server-side callback."""
    response = make_response("SSRF-CANARY-OK\n", 200)
    response.headers["X-SSRF-Test"] = "ssrf-canary-001"
    response.headers["Cache-Control"] = "no-store"
    return response

@app.get("/headers")
def headers():
    """Returns distinctive, non-sensitive headers for reflection tests."""
    response = make_response("HEADER-REFLECTION-TEST\n", 200)
    response.headers["X-SSRF-Test"] = "mmp-ssrf-001"
    response.headers["X-Researcher-Test"] = "canary-001"
    response.headers["Cache-Control"] = "no-store"
    return response

@app.get("/redirect")
def redirect_test():
    """Real HTTP 302 redirect for testing redirect following."""
    return redirect("/final", code=302)

@app.get("/final")
def final():
    """Distinct final destination for redirect-chain verification."""
    response = make_response("SSRF-CANARY-FINAL\n", 200)
    response.headers["X-SSRF-Final"] = "mmp-final-001"
    response.headers["Cache-Control"] = "no-store"
    return response

@app.get("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
