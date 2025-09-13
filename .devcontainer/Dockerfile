## The previously referenced image ghcr.io/home-assistant/devcontainer:stable no longer publishes a manifest.
## Use the maintained Home Assistant integration development image instead.
FROM ghcr.io/ludeeus/devcontainer:latest

# Install development dependencies
COPY requirements_dev.txt /tmp/requirements_dev.txt
RUN pip install --no-cache-dir -r /tmp/requirements_dev.txt && rm /tmp/requirements_dev.txt
