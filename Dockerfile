# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 python:3.9

# Install linux packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    nano \
    tree && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root group and user
RUN groupadd --gid 10001 app && \
    useradd --uid 10001 --gid app --shell /bin/bash --create-home app

# Switch to the user's home directory
WORKDIR /home/app

# Create a python virtual environment within the docker container
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
# "Activate" the virtual environment by prepending the venv executable path to the PATH variable
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the necessary files
COPY . src/

# Install python packages (now within the virtual environment)
RUN pip install --upgrade pip && \
    pip install ./src && \
    rm -rf src

# Switch to the non-root user
USER 10001

ENTRYPOINT ["ghget"]
CMD ["--help"]
