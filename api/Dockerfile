FROM python:3.11
WORKDIR /work
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "flask", "--app", "kill-team-simulator", "run", "--host=0.0.0.0", "--debug" ]
