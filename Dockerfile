######## Kynan #######

FROM python:3.10

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        neofetch \
        apt-utils \
        libmediainfo0v5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY installer.sh .

RUN bash installer.sh

# changing workdir
WORKDIR "/root/naya1503"

# start the bot.
CMD ["bash", "start"]
