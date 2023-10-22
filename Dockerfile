FROM python:3.8-slim
LABEL maintainer="lol@Nope.com"


ARG USERNAME=archivist
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME 
RUN useradd --uid $USER_UID --gid $USER_GID -m $USERNAME


RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install ffmpeg --no-install-recommends

WORKDIR /app


COPY ["README.MD", "main.py", "requirements.txt", "./"]
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt



CMD [ "python", "main.py" ]