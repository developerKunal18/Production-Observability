import time

from flask import Flask, jsonify, request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
)

ERROR_COUNT = Counter(
    "http_errors_total",
    "Total HTTP errors",
    ["endpoint", "status"],
)


@app.before_request
def start_timer():
    request.start_time = time.perf_counter()


@app.after_request
def record_metrics(response):
    endpoint = request.path
    duration = time.perf_counter() - request.start_time

    REQUEST_COUNT.labels(
        request.method,
        endpoint,
        response.status_code,
    ).inc()

    REQUEST_LATENCY.labels(
        request.method,
        endpoint,
    ).observe(duration)

    if response.status_code >= 400:
        ERROR_COUNT.labels(
            endpoint,
            response.status_code,
        ).inc()

    return response


@app.get("/")
def home():
    return jsonify(
        service="day304-observability",
        message="Service is running",
    )


@app.get("/health")
def health():
    return jsonify(status="healthy")


@app.get("/ready")
def ready():
    return jsonify(status="ready")


@app.get("/error")
def error():
    return jsonify(error="demo error"), 500


@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST,
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
