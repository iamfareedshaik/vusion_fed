# Use the official Ubuntu base image
FROM ubuntu:latest

# Update and install dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y git python3-virtualenv libssl-dev libffi-dev build-essential libpython3-dev python3-minimal authbind virtualenv iptables

# Create a new user 'cowrie' with no password
RUN adduser --disabled-password --gecos "" cowrie

# Switch to user 'cowrie'
USER cowrie
WORKDIR /home/cowrie

# Download and setup Cowrie
RUN git clone https://github.com/iamfareedshaik/cowrie.git && \
    cd cowrie && \
    virtualenv cowrie-env && \
    . cowrie-env/bin/activate && \
    pip install --upgrade pip && \
    pip install --upgrade -r requirements.txt && \
    pip install watchdog requests

# Copy the default configuration
RUN cp cowrie/etc/cowrie.cfg.dist cowrie/etc/cowrie.cfg

# Create the log directory and set permissions
RUN mkdir -p /home/cowrie/cowrie/var/log/cowrie && \
    chmod -R 755 /home/cowrie/cowrie/var/log/cowrie

# Copy the honeypotScript.py into the container
COPY honeypotScript.py /home/cowrie/honeypotScript.py

# Create a script to run both Cowrie and the Python script
RUN echo '#!/bin/bash\n\
. /home/cowrie/cowrie/cowrie-env/bin/activate\n\
cowrie/bin/cowrie start -n &\n\
python3 /home/cowrie/honeypotScript.py\n' > /home/cowrie/start.sh && \
    chmod +x /home/cowrie/start.sh

# Expose ports
EXPOSE 2222 2223

# Set the entry point to the script
ENTRYPOINT ["/home/cowrie/start.sh"]
