# Use a lightweight version of Python 3.10
FROM python:3.10-slim

WORKDIR /app

# OPTIMIZATION: Install CPU-only PyTorch first
# This prevents downloading the 1GB+ GPU version
RUN pip install --default-timeout=1000 --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .

# Now install the rest (it will skip torch because it's already installed)
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data/uploads data/vector_store

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]