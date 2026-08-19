# Production Observability

Flask service with Prometheus metrics, health checks, Docker and Kubernetes configuration.

## Run

```bash
pip install -r requirements.txt
python app.py
```

Endpoints:

- `/`
- `/health`
- `/ready`
- `/error`
- `/metrics`

## Docker

```bash
docker compose up --build
```

Prometheus: `http://localhost:9090`

API metrics: `http://localhost:5000/metrics`

## Kubernetes

```bash
kubectl apply -f k8s/
```

Day 304 / 365
