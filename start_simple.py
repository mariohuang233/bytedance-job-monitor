#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版启动文件 - 不依赖Playwright
适用于Zeabur等云平台部署
"""

import os
import sys
from pathlib import Path

# 设置环境变量
os.environ['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'development')
os.environ['DATA_DIR'] = os.environ.get('DATA_DIR', './data')
os.environ['PYTHONPATH'] = os.environ.get('PYTHONPATH', '.')

# 确保数据目录存在
data_dir = Path(os.environ.get('DATA_DIR', './data'))
data_dir.mkdir(parents=True, exist_ok=True)

print(f"🚀 启动字节跳动职位监控系统 - 简化版本")
print(f"📁 数据目录: {data_dir.absolute()}")
print(f"🌐 运行模式: {os.environ.get('FLASK_ENV', 'development')}")
print(f"🔧 Python版本: {sys.version}")

# 导入并启动Flask应用
from app_simple import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🌍 服务器启动: http://{host}:{port}")
    print(f"🔍 调试模式: {debug}")
    print("=" * 50)
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )