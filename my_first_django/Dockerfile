
FROM python:3.10-bullseye

WORKDIR /app
COPY requirements.txt /app/
# COPY Django-5.0.6-py3-none-any.whl /app/
RUN pip install --no-cache-dir -r requirements.txt \
    --trusted-host pypi.org --trusted-host pypi.python.org  --trusted-host files.pythonhosted.org

COPY . /app/
EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["supervisord", "-c", "/app/supervisord.conf"] # 一個容器內執行多個進程
