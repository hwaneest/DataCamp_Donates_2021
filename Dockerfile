FROM python:3.8
ENV PYTHONUNBUFFERED True
EXPOSE 8080
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY requirements.txt ./requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
CMD streamlit run --server.port 8080 --server.enableCORS false app/main.py
