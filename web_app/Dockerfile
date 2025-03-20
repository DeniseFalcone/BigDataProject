FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /web_app

COPY . .


RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "front_end/app.py", "--server.port=8501", "--server.address=0.0.0.0"]