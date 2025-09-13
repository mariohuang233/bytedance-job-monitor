#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字节跳动职位监控系统 - 简化版Flask应用
不依赖Playwright，使用requests直接调用API
"""

import json
import logging
import os
import threading
import time
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_file
from by_simple import SimpleJobMonitor, TASK_CONFIGS, OUTPUT_FILENAME, JSON_CACHE_FILENAME

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Flask应用配置
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'bytedance-jobs-monitor-simple')

# 全局变量
monitor_instance = None
monitor_thread = None
monitor_status = {
    'running': False,
    'last_run': None,
    'next_run': None,
    'total_jobs': 0,
    'error_message': None
}

def load_cached_data():
    """加载缓存数据"""
    try:
        if JSON_CACHE_FILENAME.exists():
            with open(JSON_CACHE_FILENAME, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"加载缓存数据失败: {e}")
    return {}

def run_monitor_task():
    """运行监控任务"""
    global monitor_status
    
    try:
        monitor_status['running'] = True
        monitor_status['error_message'] = None
        
        logging.info("开始执行监控任务...")
        
        monitor = SimpleJobMonitor(tasks=TASK_CONFIGS, filename=OUTPUT_FILENAME)
        result = monitor.run(silent_mode=True)
        
        monitor_status['last_run'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        monitor_status['total_jobs'] = result.get('total_jobs', 0)
        
        logging.info(f"监控任务完成: {result}")
        
    except Exception as e:
        error_msg = f"监控任务执行失败: {str(e)}"
        logging.error(error_msg)
        monitor_status['error_message'] = error_msg
    
    finally:
        monitor_status['running'] = False

@app.route('/')
def index():
    """主页"""
    return render_template('base.html')

@app.route('/api/status')
def get_status():
    """获取监控状态"""
    return jsonify(monitor_status)

@app.route('/api/data')
def get_data():
    """获取职位数据"""
    try:
        data = load_cached_data()
        
        # 统计信息
        stats = {
            'total_jobs': sum(len(jobs) for jobs in data.values()),
            'categories': {}
        }
        
        for category, jobs in data.items():
            stats['categories'][category] = len(jobs)
        
        return jsonify({
            'success': True,
            'data': data,
            'stats': stats,
            'last_updated': monitor_status.get('last_run')
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/run', methods=['POST'])
def run_monitor():
    """手动运行监控任务"""
    global monitor_thread
    
    if monitor_status['running']:
        return jsonify({
            'success': False,
            'message': '监控任务正在运行中...'
        })
    
    try:
        monitor_thread = threading.Thread(target=run_monitor_task)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        return jsonify({
            'success': True,
            'message': '监控任务已启动'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download')
def download_excel():
    """下载Excel文件"""
    try:
        if OUTPUT_FILENAME.exists():
            return send_file(
                OUTPUT_FILENAME,
                as_attachment=True,
                download_name=f'bytedance_jobs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            )
        else:
            return jsonify({
                'success': False,
                'error': 'Excel文件不存在，请先运行监控任务'
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': 'simple-1.0.0',
        'dependencies': {
            'playwright': False,  # 简化版不依赖Playwright
            'requests': True,
            'pandas': True,
            'openpyxl': True
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'API端点不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': '服务器内部错误'
    }), 500

if __name__ == '__main__':
    # 启动时运行一次监控任务
    logging.info("启动时执行初始监控任务...")
    initial_thread = threading.Thread(target=run_monitor_task)
    initial_thread.daemon = True
    initial_thread.start()
    
    # 启动Flask应用
    port = int(os.environ.get('PORT', 8080))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )