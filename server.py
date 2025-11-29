from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.after_request
def add_cors_headers(resp):
    # Allow your Mission Control site (or * if you prefer)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp

@app.route("/rss", methods=["GET", "OPTIONS"])
def rss_proxy():
    # Handle CORS preflight if browser sends OPTIONS
    if request.method == "OPTIONS":
        return Response(status=204)

    url = request.args.get("url")
    if not url:
        return Response("Missing url parameter", status=400)

    try:
        upstream = requests.get(
            url,
            headers={"User-Agent": "MissionControlRSS/1.0"},
            timeout=10,
        )
    except requests.RequestException as e:
        return Response(f"Upstream error: {e}", status=502)

    # Pass through content; CORS headers are added in add_cors_headers()
    content_type = upstream.headers.get("Content-Type", "application/xml")
    return Response(upstream.content, status=upstream.status_code,
                    headers={"Content-Type": content_type})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
