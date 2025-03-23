#!/bin/bash

# Start ingestion main in the background
python3 ./ingestion/ingestion_main.py &

# Start processing main in the foreground
python3 ./processing/processing_main.py

# Wait for background processes to finish
wait