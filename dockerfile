# Sürətli və yüngül Python imicindən istifadə edirik
FROM python:3.11-slim

# Konteyner daxilində işçi qovluğu təyin edirik
WORKDIR /app

# Python-un çıxışları birbaşa terminala yazdırmasını təmin edirik (.pyc faylları yazılmır)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Əvvəlcə asılılıqları köçürürük (Kəşləmə - Caching mexanizmindən yararlanmaq üçün)
COPY requirements.txt .

# Asılılıqları yükləyirik
RUN pip install --no-cache-dir -r requirements.txt

# Layihənin bütün kodlarını konteynerə köçürürük
COPY . .

# Layihəni işə salmaq üçün komanda (Məsələn, FastAPI üçün uvicorn)
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]