#!/bin/bash
# Railway部署脚本 - 安装playwright浏览器依赖

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browsers..."
playwright install chromium

echo "Installation completed!"