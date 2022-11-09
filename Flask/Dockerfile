FROM python:slim
COPY . ./app
WORKDIR /app
RUN chmod 755 main.py
RUN ls -la
RUN pip install -r requirements.txt
ENTRYPOINT ["./main.py"]