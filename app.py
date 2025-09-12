#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字节跳动职位监控 Web 应用
提供职位数据的可视化展示和搜索功能
"""

import json
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from collections import Counter

app = Flask(__name__)

# 环境变量配置
DATA_DIR = os.getenv('DATA_DIR', os.path.join(os.path.dirname(__file__), 'data'))
CACHE_FILE = os.path.join(DATA_DIR, 'bytedance_jobs_cache.json')
EXCEL_FILE = os.path.join(DATA_DIR, 'bytedance_jobs_tracker.xlsx')

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

# Flask配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

def load_job_data():
    """加载职位数据"""
    # 确保数据目录存在
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if not os.path.exists(CACHE_FILE):
        print(f"数据文件不存在: {CACHE_FILE}")
        return {'campus': [], 'intern': [], 'experienced': []}
    
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"成功加载数据: {sum(len(jobs) for jobs in data.values())} 个职位")
            return data
    except Exception as e:
        print(f"加载数据失败: {e}")
        return {'campus': [], 'intern': [], 'experienced': []}

def get_statistics(data):
    """获取数据统计信息"""
    stats = {
        'total': sum(len(jobs) for jobs in data.values()),
        'by_type': {k: len(v) for k, v in data.items()},
        'recent_jobs': 0,
        'cities': Counter(),
        'departments': Counter()
    }
    
    # 统计最近发布的职位（7天内）
    from datetime import datetime, timedelta
    week_ago = datetime.now() - timedelta(days=7)
    
    for job_type, jobs in data.items():
        for job in jobs:
            # 统计最近职位
            try:
                pub_time = datetime.strptime(job.get('publish_time', ''), '%Y-%m-%d')
                if pub_time >= week_ago:
                    stats['recent_jobs'] += 1
            except:
                pass
            
            # 统计城市分布
            city_list = job.get('city_list', [])
            if isinstance(city_list, list):
                for city in city_list:
                    if isinstance(city, dict) and 'name' in city:
                        stats['cities'][city['name']] += 1
            
            # 统计部门分布
            department = job.get('department', '')
            if department:
                stats['departments'][department] += 1
    
    # 添加排序后的热门城市和部门
    stats['top_cities'] = stats['cities'].most_common(10)
    stats['top_departments'] = stats['departments'].most_common(10)
    
    return stats

@app.route('/health')
def health_check():
    """健康检查端点"""
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}, 200

@app.route('/')
def index():
    """首页"""
    data = load_job_data()
    stats = get_statistics(data)
    return render_template('index.html', stats=stats)

@app.route('/jobs/<job_type>')
def jobs(job_type):
    """职位列表页面"""
    if job_type not in ['campus', 'intern', 'experienced']:
        return "Invalid job type", 404
    
    data = load_job_data()
    jobs = data.get(job_type, [])
    
    # 获取搜索参数
    search = request.args.get('search', '').strip()
    city = request.args.get('city', '').strip()
    department = request.args.get('department', '').strip()
    
    # 过滤职位
    filtered_jobs = jobs
    if search:
        filtered_jobs = [job for job in filtered_jobs 
                        if search.lower() in job.get('title', '').lower() 
                        or search.lower() in job.get('description', '').lower()]
    
    if city:
        filtered_jobs = [job for job in filtered_jobs 
                        if any(c.get('name', '') == city for c in job.get('city_list', []))]
    
    if department:
        filtered_jobs = [job for job in filtered_jobs 
                        if department in job.get('department', '')]
    
    # 获取可用的城市和部门选项
    all_cities = set()
    all_departments = set()
    for job in jobs:
        city_list = job.get('city_list', [])
        if isinstance(city_list, list):
            for c in city_list:
                if isinstance(c, dict) and 'name' in c:
                    all_cities.add(c['name'])
        
        dept = job.get('department', '')
        if dept:
            all_departments.add(dept)
    
    job_type_names = {
        'campus': '校园招聘',
        'intern': '实习招聘', 
        'experienced': '社会招聘'
    }
    
    return render_template('jobs.html', 
                         jobs=filtered_jobs,
                         job_type=job_type,
                         job_type_name=job_type_names[job_type],
                         all_cities=sorted(all_cities),
                         all_departments=sorted(all_departments),
                         current_search=search,
                         current_city=city,
                         current_department=department)

@app.route('/api/jobs/<job_type>')
def api_jobs(job_type):
    """API接口：获取职位数据"""
    if job_type not in ['campus', 'intern', 'experienced']:
        return jsonify({'error': 'Invalid job type'}), 404
    
    data = load_job_data()
    return jsonify(data.get(job_type, []))

@app.route('/api/stats')
def api_stats():
    """API接口：获取统计数据"""
    data = load_job_data()
    stats = get_statistics(data)
    return jsonify(stats)

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """API接口：刷新数据"""
    try:
        import subprocess
        import sys
        
        # 在后台运行数据抓取脚本
        result = subprocess.run(
            [sys.executable, 'by.py'],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': '数据刷新成功',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'message': f'数据刷新失败: {result.stderr}',
                'timestamp': datetime.now().isoformat()
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'message': '数据刷新超时，请稍后再试',
            'timestamp': datetime.now().isoformat()
        }), 408
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'数据刷新出错: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    # 开发环境启动
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host=host, port=port)