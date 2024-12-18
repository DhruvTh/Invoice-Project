FROM python:3.11.9

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 supervisor portaudio19-dev libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libatspi2.0-0 libxcomposite1 libxdamage1 -y

RUN apt install lsb-release curl gpg -y

RUN apt-get update

RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# RUN pip install fastapi uvicorn Pillow requests python-dotenv ffmpeg-python numpy psutil python-multipart pillow-heif openai cached_property einops  langchain langchain-openai langchain-core langchain-mistralai duckduckgo-search langchain-google-genai

# RUN pip install tavily-python google-cloud-aiplatform validators unstructured[all-docs] playwright qdrant-client PyPDF2

ARG GEMINI_API_KEY 
ARG CLAUDEAI_API_KEY 
ARG OPENAI_API_KEY 
ARG MONGO_CONNECTION_STR

ENV OPENAI_API_KEY=${OPENAI_API_KEY}  
ENV CLAUDEAI_API_KEY=${CLAUDEAI_API_KEY}  
ENV GEMINI_API_KEY=${GEMINI_API_KEY}  
ENV MONGO_CONNECTION_STR=${MONGO_CONNECTION_STR}

RUN mkdir /root/app

WORKDIR /root/app

ADD ./ /root/app

RUN pip install -r requirements.txt


ENTRYPOINT ["python", "main.py"]