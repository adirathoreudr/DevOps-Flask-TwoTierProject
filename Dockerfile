FROM python:3.9-slim 

WORKDIR /app


RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev pkg-config curl && \
rm -rf /var/lib/apt/lists/* 

COPY requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

COPY . .

# Generate model using the container's sklearn version (eliminates version mismatch warnings)
RUN python model/train_model.py

EXPOSE 5000

CMD ["python", "app.py"]