FROM python:3.8-slim
ENV PYTHONUNBUFFERED True
EXPOSE 8080
ENV APP_HOME /app
WORKDIR $APP_HOME
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY app/ ./app/
COPY data/ ./data/
COPY requirements.txt .
RUN pip3 install -r requirements.txt
CMD streamlit run --server.port 8080 --server.enableCORS false app/app.py
