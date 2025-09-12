# 字节跳动职位监控系统 🚀

一个实时监控字节跳动招聘信息的Web应用，支持职位搜索、数据统计和可视化展示。

## ✨ 功能特性

- 📊 **实时数据监控**: 自动抓取字节跳动最新职位信息
- 🔍 **智能搜索**: 支持按职位名称、城市、部门等多维度搜索
- 📈 **数据可视化**: 提供职位分布统计图表
- 📱 **响应式设计**: 完美适配桌面和移动设备
- 🔄 **自动更新**: 支持定时自动抓取最新数据
- 🌐 **云端部署**: 支持多种云平台一键部署

## 🎯 支持的职位类型

- **校园招聘**: 面向应届毕业生的全职岗位
- **实习招聘**: 在校学生实习机会
- **社会招聘**: 面向有工作经验的专业人士

## 🚀 快速开始

### 本地运行

1. **克隆项目**
```bash
git clone https://github.com/your-username/bytedance-job-monitor.git
cd bytedance-job-monitor
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **运行应用**
```bash
python app.py
```

4. **访问应用**
打开浏览器访问 `http://localhost:8080`

### Docker 部署

```bash
# 构建并运行
docker-compose up -d

# 查看状态
docker-compose ps
```

## 🌐 云端部署

### Railway 部署（推荐）

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. 点击上方按钮或访问 [Railway.app](https://railway.app)
2. 连接你的 GitHub 仓库
3. 选择此项目进行部署
4. 等待自动构建完成
5. 获取部署URL并访问

### 其他平台

- **Heroku**: 支持一键部署，查看 [部署指南](DEPLOYMENT.md#heroku-部署)
- **Render**: 免费托管，查看 [部署指南](DEPLOYMENT.md#render-部署)
- **VPS**: 完整的服务器部署方案，查看 [部署指南](DEPLOYMENT.md#vps-手动部署)

## 📊 数据更新

### 手动更新
```bash
python by.py
```

### 自动更新

项目支持多种自动更新方式：

- **Docker Compose**: 内置定时任务容器（推荐）
- **Cron 任务**: 系统级定时任务
- **云平台**: 使用平台提供的定时任务功能

详细配置请参考 [部署指南](DEPLOYMENT.md)

## 🔧 配置说明

### 环境变量

复制 `.env.example` 为 `.env` 并根据需要修改：

```bash
# Flask配置
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key

# 服务器配置
HOST=0.0.0.0
PORT=8080

# 数据配置
DATA_UPDATE_INTERVAL=7200  # 2小时更新一次
```

### 数据存储

- **JSON缓存**: 快速数据访问
- **Excel文件**: 数据备份和分析
- **内存缓存**: 提升响应速度

## 📁 项目结构

```
├── app.py              # Flask主应用
├── by.py               # 数据抓取脚本
├── requirements.txt    # Python依赖
├── Dockerfile         # Docker配置
├── docker-compose.yml # Docker编排
├── Procfile          # Heroku部署配置
├── railway.json      # Railway部署配置
├── static/           # 静态资源
│   ├── css/
│   └── js/
├── templates/        # HTML模板
│   ├── base.html
│   ├── index.html
│   └── jobs.html
└── data/            # 数据存储目录
```

## 🛠️ 技术栈

- **后端**: Python Flask
- **前端**: HTML5, CSS3, JavaScript
- **数据处理**: BeautifulSoup, Pandas
- **可视化**: Chart.js
- **部署**: Docker, Gunicorn
- **样式**: Bootstrap 5

## 📸 界面预览

### 首页统计
- 职位总数统计
- 各类型职位分布
- 热门城市排行
- 热门部门排行

### 职位列表
- 实时搜索过滤
- 分页浏览
- 详细信息展示
- 响应式布局

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🔗 相关链接

- [部署指南](DEPLOYMENT.md)
- [字节跳动招聘官网](https://jobs.bytedance.com/)
- [Railway 部署平台](https://railway.app/)
- [Docker Hub](https://hub.docker.com/)

## 📞 支持

如果你觉得这个项目有用，请给它一个 ⭐️！

有问题或建议？欢迎提交 [Issue](https://github.com/your-username/bytedance-job-monitor/issues)。

---

**免责声明**: 本项目仅用于学习和研究目的，请遵守相关网站的使用条款和robots.txt规定。