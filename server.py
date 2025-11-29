from flask import Flask, request, Response
import requests

app = Flask(__name__)


@app.route("/")
def root():
    # Simple health check
    return "Mission Control RSS Proxy OK", 200


@app.route("/rss")
def rss_proxy():
    target_url = request.args.get("url")
    if not target_url:
        return Response("Missing 'url' query parameter", status=400)

    try:
        # Fetch the RSS feed
        upstream = requests.get(target_url, timeout=10)
    except requests.RequestException as exc:
        return Response(f"Upstream fetch error: {exc}", status=502)

    # Pass through the body, but make sure content-type + CORS are good
    content_type = upstream.headers.get("Content-Type", "application/xml; charset=utf-8")

    resp = Response(
        upstream.content,
        status=upstream.status_code,
        content_type=content_type,
    )

    # Allow your PWA to call this from any origin
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"

    return resp


if __name__ == "__main__":
    # Local dev: python server.py
    # Render will use gunicorn (see start command below), not this.
    import os

    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
