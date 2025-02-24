FROM python: 3.11-bookworm

WORKDIR /app
RUN pip install --no-cache-dir -r requrements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

