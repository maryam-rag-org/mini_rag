# Create middleware

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time


# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Tottal HTTP Requests', ['method', 'endpint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Latency', ['method', 'endpoint'])

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request : Request, call_next):
        
        start_time = time.time()

        response = await call_next(request)
        duration = time.time() - start_time
        
        endpoint = request.url.path

        REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(duration)
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=response.status_code).inc()
        
        return response
    
def setup_metrics(app: FastAPI):
    """
        Setup Prometheus metrics middleware and endpoint
    """

    # Add Prometheus middleware
    app.add_middleware(PrometheusMiddleware)

    @app.get("/TjgR_87vhp_bs8KJ", include_in_schema = False) # return the metrics ==> should be private that is why we re-name it from /metrics to random name
    def metrics():
        '''
        return the last metrics calculated
        '''
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)