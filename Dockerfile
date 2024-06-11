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
    pip install --upgrade -r requirements.txt

# Copy the default configuration
RUN cp cowrie/etc/cowrie.cfg.dist cowrie/etc/cowrie.cfg

# Expose ports
EXPOSE 2222 2223

# Set the volume for log files
VOLUME ["/home/admin/logfiles"]

# Start Cowrie and copy log files to the specified directory
CMD ["sh", "-c", "cowrie/bin/cowrie start -n && cp /home/cowrie/cowrie/var/log/cowrie/cowrie.json /home/admin/logfiles"]