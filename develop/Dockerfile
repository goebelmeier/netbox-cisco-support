FROM netboxcommunity/netbox:${NETBOX_VER-v3.0-1.4.1}

# These lines are only required if your plugin has its own static files.
COPY develop/configuration/configuration.py /etc/netbox/config/configuration.py
COPY develop/configuration/logging.py /etc/netbox/config/logging.py
COPY develop/configuration/plugins.py /etc/netbox/config/plugins.py

# -------------------------------------------------------------------------------------
# Install Netbox Plugin
# -------------------------------------------------------------------------------------
RUN mkdir -p /source
COPY . /source

#RUN pip install -r requirements.txt
RUN cd /source && \
    /opt/netbox/venv/bin/python3 setup.py develop
