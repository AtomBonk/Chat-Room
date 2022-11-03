FROM python:3.8
WORKDIR /usr/src/app
COPY . .
EXPOSE 4333
CMD [ "python", "chat-server.py" ]