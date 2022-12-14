FROM python:3.8-slim
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt
  
COPY chat-server.py keys.py ./
EXPOSE 4333
CMD [ "python", "chat-server.py" ]