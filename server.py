from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route("/rss")
def rss_proxy():
    url = request.args.get("url")
    if not url:
        return Response("Missing url parameter", status=400)

    try:
        # Simple fetch with a polite UA
        upstream = requests.get(
            url,
            headers={"User-Agent": "MissionControlRSS/1.0"},
            timeout=10,
        )
    except requests.RequestException as e:
        return Response(f"Upstream error: {e}", status=502)

    # Pass through content, but add CORS header
    headers = {
        "Content-Type": upstream.headers.get("Content-Type", "application/xml"),
        "Access-Control-Allow-Origin": "*",
    }

    return Response(upstream.content, status=upstream.status_code, headers=headers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
