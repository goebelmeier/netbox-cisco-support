ARG python_ver=3.9
FROM python:${python_ver}

ARG netbox_ver=master

# Play nicely with Docker logging
ENV PYTHONUNBUFFERED 1

# Don't generate .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir -p /opt && pip install --no-cache-dir --upgrade pip

# -------------------------------------------------------------------------------------
# Install NetBox
# -------------------------------------------------------------------------------------
RUN      git clone --single-branch --branch ${netbox_ver} https://github.com/netbox-community/netbox.git /opt/netbox/
WORKDIR  /opt/netbox/
RUN      pip install --no-cache-dir -r /opt/netbox/requirements.txt

# Make the django-debug-toolbar always visible when DEBUG is enabled,
# except when we're running Django unit-tests.
RUN echo "import sys" >> /opt/netbox/netbox/netbox/settings.py && \
    echo "TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'" >> /opt/netbox/netbox/netbox/settings.py && \
    echo "DEBUG_TOOLBAR_CONFIG = {'SHOW_TOOLBAR_CALLBACK': lambda _: DEBUG and not TESTING }" >> /opt/netbox/netbox/netbox/settings.py

# Work around https://github.com/rq/django-rq/issues/421
RUN pip install --no-cache-dir django-rq==2.3.2

# -------------------------------------------------------------------------------------
# Install Netbox Plugin
# -------------------------------------------------------------------------------------
RUN mkdir -p /source
WORKDIR /source
COPY . /source

#RUN pip install -r requirements.txt
RUN python setup.py develop

WORKDIR /opt/netbox/netbox/
