#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字节跳动职位监控 - 简化版本（无Playwright依赖）
适用于云平台部署，使用requests + 模拟请求方式
"""

import json
import logging
import requests
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

# 文件路径配置
PROJECT_PATH = Path(__file__).parent
DATA_PATH = PROJECT_PATH / "data"
DATA_PATH.mkdir(exist_ok=True)
OUTPUT_FILENAME = DATA_PATH / "bytedance_jobs_tracker.xlsx"
JSON_CACHE_FILENAME = DATA_PATH / "bytedance_jobs_cache.json"

# 任务配置 - 直接使用API接口
TASK_CONFIGS: List[Dict[str, Any]] = [
    {
        'id': 1,
        'name': '实习招聘',
        'sheet_name': 'intern',
        'api_url': 'https://jobs.bytedance.com/api/v1/search/job/posts',
        'params': {
            'keywords': '',
            'category': '6704215864629004552,6704215864591255820,6704216224387041544,6704215924712409352',
            'location': 'CT_125',
            'project': '7481474995534301447,7468181472685164808,7194661644654577981,7194661126919358757',
            'type': '',
            'job_hot_flag': '',
            'current': 1,
            'limit': 2000,
            'functionCategory': '',
            'tag': ''
        }
    },
    {
        'id': 2,
        'name': '校园招聘',
        'sheet_name': 'campus',
        'api_url': 'https://jobs.bytedance.com/api/v1/search/job/posts',
        'params': {
            'keywords': '',
            'category': '6704215864629004552,6704215864591255820,6704216224387041544,6704215924712409352',
            'location': 'CT_125',
            'project': '7525009396952582407',
            'type': '',
            'job_hot_flag': '',
            'current': 1,
            'limit': 2000,
            'functionCategory': '',
            'tag': ''
        }
    },
    {
        'id': 3,
        'name': '社会招聘',
        'sheet_name': 'experienced',
        'api_url': 'https://jobs.bytedance.com/api/v1/search/job/posts',
        'params': {
            'keywords': '',
            'category': '6704215864629004552,6704215864591255820,6704215924712409352,6704216224387041544',
            'location': 'CT_125',
            'project': '',
            'type': '',
            'job_hot_flag': '',
            'current': 1,
            'limit': 600,
            'functionCategory': '',
            'tag': ''
        }
    }
]

class SimpleJobMonitor:
    """简化版职位监控器 - 不依赖Playwright"""
    
    def __init__(self, tasks: List[Dict[str, Any]], filename: Path):
        self.tasks = tasks
        self.filename = filename
        self.session = requests.Session()
        
        # 设置请求头，模拟浏览器
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://jobs.bytedance.com/',
            'Origin': 'https://jobs.bytedance.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        })
    
    def fetch_jobs(self, task_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """获取职位数据 - 带重试机制"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    logging.info(f"重试获取 {task_config['name']} 数据 (第{attempt+1}次)...")
                else:
                    logging.info(f"正在获取 {task_config['name']} 数据...")
                
                # 添加随机延迟避免请求过于频繁
                if attempt > 0:
                    import time
                    time.sleep(retry_delay * attempt)
                
                # 调试：打印请求信息
                full_url = f"{task_config['api_url']}?{'&'.join([f'{k}={v}' for k, v in task_config['params'].items()])}"
                logging.info(f"请求URL: {full_url}")
                
                response = self.session.get(
                    task_config['api_url'],
                    params=task_config['params'],
                    timeout=30
                )
                
                # 调试：打印响应信息
                logging.info(f"响应状态码: {response.status_code}")
                logging.info(f"响应头: {dict(response.headers)}")
                logging.info(f"响应内容前200字符: {response.text[:200]}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        if 'data' in data and 'job_post_list' in data['data']:
                            jobs = data['data']['job_post_list']
                            logging.info(f"✅ {task_config['name']} 获取成功: {len(jobs)} 个职位")
                            return jobs
                        elif 'data' in data and isinstance(data['data'], list):
                            # 兼容不同的API响应格式
                            jobs = data['data']
                            logging.info(f"✅ {task_config['name']} 获取成功: {len(jobs)} 个职位")
                            return jobs
                        else:
                            logging.warning(f"⚠️ {task_config['name']} 数据格式异常: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                            if attempt == max_retries - 1:
                                return []
                            continue
                    except json.JSONDecodeError as e:
                        logging.error(f"❌ {task_config['name']} JSON解析失败: {e}")
                        if attempt == max_retries - 1:
                            return []
                        continue
                        
                elif response.status_code == 429:
                    # 请求频率限制
                    logging.warning(f"⚠️ {task_config['name']} 请求频率限制，等待重试...")
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(10)  # 等待更长时间
                        continue
                    else:
                        logging.error(f"❌ {task_config['name']} 请求频率限制，重试失败")
                        return []
                        
                elif response.status_code in [403, 404]:
                    # 权限或资源不存在错误，不重试
                    logging.error(f"❌ {task_config['name']} 请求失败: {response.status_code} - {response.text[:200]}")
                    return []
                    
                else:
                    logging.error(f"❌ {task_config['name']} 请求失败: {response.status_code}")
                    if attempt == max_retries - 1:
                        return []
                    continue
                    
            except requests.exceptions.Timeout:
                logging.warning(f"⚠️ {task_config['name']} 请求超时")
                if attempt == max_retries - 1:
                    logging.error(f"❌ {task_config['name']} 多次超时，获取失败")
                    return []
                continue
                
            except requests.exceptions.ConnectionError:
                logging.warning(f"⚠️ {task_config['name']} 连接错误")
                if attempt == max_retries - 1:
                    logging.error(f"❌ {task_config['name']} 连接失败")
                    return []
                continue
                
            except Exception as e:
                logging.error(f"❌ {task_config['name']} 获取失败: {e}")
                if attempt == max_retries - 1:
                    return []
                continue
        
        return []
    
    def process_job_data(self, jobs: List[Dict[str, Any]]) -> pd.DataFrame:
        """处理职位数据"""
        processed_jobs = []
        
        for job in jobs:
            try:
                processed_job = {
                    '职位名称': job.get('title', ''),
                    '部门': job.get('department', ''),
                    '工作地点': job.get('city_info', {}).get('city_name', ''),
                    '发布时间': job.get('publish_time', ''),
                    '更新时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    '职位ID': job.get('id', ''),
                    '职位链接': f"https://jobs.bytedance.com/campus/position/{job.get('id', '')}",
                    '工作性质': job.get('job_type', {}).get('name', ''),
                    '学历要求': job.get('requirement', ''),
                    '职位描述': job.get('description', '')[:500] + '...' if len(job.get('description', '')) > 500 else job.get('description', '')
                }
                processed_jobs.append(processed_job)
            except Exception as e:
                logging.warning(f"处理职位数据时出错: {e}")
                continue
        
        return pd.DataFrame(processed_jobs)
    
    def save_to_excel(self, data_frames: Dict[str, pd.DataFrame]):
        """保存到Excel文件"""
        try:
            with pd.ExcelWriter(self.filename, engine='openpyxl') as writer:
                for sheet_name, df in data_frames.items():
                    if not df.empty:
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        
                        # 设置列宽
                        worksheet = writer.sheets[sheet_name]
                        for column in worksheet.columns:
                            max_length = 0
                            column_letter = column[0].column_letter
                            for cell in column:
                                try:
                                    if len(str(cell.value)) > max_length:
                                        max_length = len(str(cell.value))
                                except:
                                    pass
                            adjusted_width = min(max_length + 2, 50)
                            worksheet.column_dimensions[column_letter].width = adjusted_width
            
            logging.info(f"✅ 数据已保存到: {self.filename}")
            
        except Exception as e:
            logging.error(f"❌ 保存Excel文件失败: {e}")
    
    def save_json_cache(self, data_frames: Dict[str, pd.DataFrame]):
        """保存JSON缓存"""
        try:
            cache_data = {}
            for sheet_name, df in data_frames.items():
                if not df.empty:
                    cache_data[sheet_name] = df.to_dict('records')
            
            with open(JSON_CACHE_FILENAME, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            logging.info(f"✅ JSON缓存已保存到: {JSON_CACHE_FILENAME}")
            
        except Exception as e:
            logging.error(f"❌ 保存JSON缓存失败: {e}")
    
    def run(self, silent_mode: bool = False):
        """运行监控任务"""
        logging.info("🚀 开始执行字节跳动职位监控任务 - 简化版本")
        
        data_frames = {}
        total_jobs = 0
        
        for task_config in self.tasks:
            jobs = self.fetch_jobs(task_config)
            
            if jobs:
                df = self.process_job_data(jobs)
                data_frames[task_config['sheet_name']] = df
                total_jobs += len(jobs)
            else:
                # 创建空的DataFrame
                data_frames[task_config['sheet_name']] = pd.DataFrame()
        
        if data_frames:
            self.save_to_excel(data_frames)
            self.save_json_cache(data_frames)
        
        logging.info(f"✅ 任务完成! 共获取 {total_jobs} 个职位")
        
        if not silent_mode:
            try:
                # 尝试发送桌面通知
                import subprocess
                subprocess.run([
                    'osascript', '-e',
                    f'display notification "共获取 {total_jobs} 个职位" with title "字节跳动职位监控"'
                ], check=False)
            except:
                pass
        
        return {
            'success': True,
            'total_jobs': total_jobs,
            'tasks_completed': len(self.tasks),
            'message': f'成功获取 {total_jobs} 个职位'
        }

if __name__ == "__main__":
    try:
        is_silent = "--auto" in sys.argv
        monitor = SimpleJobMonitor(tasks=TASK_CONFIGS, filename=OUTPUT_FILENAME)
        result = monitor.run(silent_mode=is_silent)
        
        if result['success']:
            logging.info("🎉 程序执行成功!")
        else:
            logging.error("❌ 程序执行失败")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logging.info("\n⚠️ 程序被用户中断。")
        sys.exit(0)
    except Exception as e:
        logging.critical(f"\n❌ 程序发生严重错误: {e}", exc_info=True)
        sys.exit(1)