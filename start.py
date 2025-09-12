#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Railway启动脚本
确保应用能在Railway环境中正常启动
"""

import os
import sys

# 设置环境变量
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('FLASK_DEBUG', 'False')
os.environ.setdefault('PYTHONPATH', '/app')
os.environ.setdefault('DATA_DIR', '/app/data')

# 确保数据目录存在
data_dir = os.environ.get('DATA_DIR', '/app/data')
os.makedirs(data_dir, exist_ok=True)

print(f"启动环境:")
print(f"- FLASK_ENV: {os.environ.get('FLASK_ENV')}")
print(f"- DATA_DIR: {data_dir}")
print(f"- PORT: {os.environ.get('PORT', '8080')}")
print(f"- 数据目录存在: {os.path.exists(data_dir)}")

# 导入并启动应用
if __name__ == '__main__':
    from app import app
    
    port = int(os.environ.get('PORT', 8080))
    print(f"启动Flask应用，端口: {port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )