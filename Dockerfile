FROM python
WORKDIR /work
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./kt_sim.py" ]
