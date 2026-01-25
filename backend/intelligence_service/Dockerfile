# 1. Base Image (Lightweight Python)
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Install System Dependencies (Required for building C extensions if needed)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# --- THE OPTIMIZATION TRICK ---
# 4. Install CPU-only PyTorch explicitly FIRST.
# This prevents downloading the huge NVIDIA CUDA version.
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

# 5. Copy requirements and install the rest
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the Application Code
COPY . .

# 7. Command to run the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]