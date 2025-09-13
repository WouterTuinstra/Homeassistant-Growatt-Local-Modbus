## Previous images (home-assistant/devcontainer and ludeeus/devcontainer) lacked manifests.
## Use the official Microsoft devcontainers Python image as a stable base.
FROM mcr.microsoft.com/devcontainers/python:3.12

# Install development dependencies
COPY requirements_dev.txt /tmp/requirements_dev.txt
RUN pip install --no-cache-dir -r /tmp/requirements_dev.txt && rm /tmp/requirements_dev.txt

# Optional: install Home Assistant core (for richer integration linting) lightweight extras.
RUN pip install --no-cache-dir homeassistant==2025.2.0 || true
