FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# 先升级 pip、setuptools、wheel
RUN python -m pip install --upgrade pip setuptools wheel

# 再安装依赖
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]