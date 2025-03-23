FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /image_processing_pipeline

COPY . .

RUN pip3 install -r requirements.txt

RUN chmod +x start.sh

ENTRYPOINT ["./start.sh"]