FROM python:3.11

# install dependencies
RUN pip install discord-py inflect requests; \
    useradd -m insultbot

ENV SYNC_TREE "false"
ENV LOG_LEVEL 20
ENV BOT_TOKEN ""
ENV BOT_PREFIX "$"
ENV GIST "https://gist.github.com/EldritchGarden/c2318c11c2a6e9726f7b8825518f9662/raw/f39849457e473f9d45363815a94e6dd1da75f024"

USER insultbot
WORKDIR /home/insultbot

COPY --chown=insultbot:insultbot src/ src/

ENTRYPOINT [ "/usr/local/bin/python3", "src/main.py" ]
