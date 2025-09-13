## Previous images (home-assistant/devcontainer and ludeeus/devcontainer) lacked manifests.
## Use the official Microsoft devcontainers Python image as a stable base.
FROM mcr.microsoft.com/devcontainers/python:3.13

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
	PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

# Copy requirement spec early for layer caching
COPY requirements_dev.txt /tmp/requirements_dev.txt

# Install OS packages useful for Home Assistant & imaging/audio features
RUN apt-get update && apt-get install -y --no-install-recommends \
	libjpeg-dev zlib1g-dev libturbojpeg0-dev libffi-dev libssl-dev \
	bluez libbluetooth-dev libudev-dev build-essential \
	&& rm -rf /var/lib/apt/lists/*

## Create venv as the vscode user to avoid slow chown
USER vscode
RUN python -m venv /workspace/.venv && \
	. /workspace/.venv/bin/activate && \
	pip install --upgrade pip && \
	pip install --no-cache-dir -r /tmp/requirements_dev.txt

ENV PATH="/workspace/.venv/bin:${PATH}"

# Auto-activate venv for interactive shells
RUN echo '\n# Auto-activate integration dev venv\nif [ -d /workspace/.venv ]; then . /workspace/.venv/bin/activate; fi' >> /home/vscode/.bashrc

USER root

EXPOSE 8123 5020

# Default shell; use tasks or manual hass start
CMD ["bash"]
