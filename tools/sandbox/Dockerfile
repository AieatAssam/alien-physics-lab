# Sandbox for agent-written predictors. Run with --network none --read-only.
FROM python:3.12-slim
RUN pip install --no-cache-dir numpy==2.1.3 \
 && useradd --uid 1001 --create-home runner
USER runner
WORKDIR /tmp
