# 纯API版本 - 完全避免浏览器依赖
# 版本: v2.0 - 专为Zeabur平台优化
FROM python:3.11-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV PORT=8080

# 安装基础系统工具（仅curl用于健康检查）
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件（现在requirements.txt就是纯API版本）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码（现在app.py就是纯API版本）
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

# 创建数据目录
RUN mkdir -p /app/data

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["python", "app.py"]

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "app:app"]