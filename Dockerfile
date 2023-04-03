FROM python:3.9

RUN mkdir /app
WORKDIR /app

# Install requirements
COPY requirements.txt /app
RUN cd /app  && pip install --no-cache-dir --upgrade -r requirements.txt

# Copy source code
COPY ./src /app/src

# Default container configuration
ENV STORAGE_PATH /storage

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "80"]
