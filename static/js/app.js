// 字节跳动职位监控 Web 应用 JavaScript

// 全局变量
let isLoading = false;

// DOM 加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 初始化应用
function initializeApp() {
    // 初始化工具提示
    initTooltips();
    
    // 初始化搜索功能
    initSearch();
    
    // 初始化滚动效果
    initScrollEffects();
    
    // 初始化数据刷新
    initDataRefresh();
    
    console.log('字节跳动职位监控 Web 应用已初始化');
}

// 初始化工具提示
function initTooltips() {
    // 如果 Bootstrap 可用，初始化工具提示
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// 初始化搜索功能
function initSearch() {
    const searchForm = document.querySelector('form');
    if (searchForm) {
        // 实时搜索建议（防抖）
        const searchInput = document.getElementById('search');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    // 这里可以添加实时搜索建议功能
                    console.log('搜索关键词:', this.value);
                }, 300);
            });
        }
        
        // 表单提交时显示加载状态
        searchForm.addEventListener('submit', function() {
            showLoading();
        });
    }
}

// 初始化滚动效果
function initScrollEffects() {
    // 平滑滚动到锚点
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // 滚动时的导航栏效果
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (navbar) {
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                // 向下滚动，隐藏导航栏
                navbar.style.transform = 'translateY(-100%)';
            } else {
                // 向上滚动，显示导航栏
                navbar.style.transform = 'translateY(0)';
            }
        }
        
        lastScrollTop = scrollTop;
    });
}

// 初始化数据刷新
function initDataRefresh() {
    // 添加刷新按钮功能
    const refreshBtn = document.getElementById('refreshData');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            refreshData();
        });
    }
    
    // 定期检查数据更新（可选）
    // setInterval(checkDataUpdate, 300000); // 每5分钟检查一次
}

// 显示加载状态
function showLoading(element = null) {
    if (isLoading) return;
    
    isLoading = true;
    
    if (element) {
        const originalText = element.innerHTML;
        element.innerHTML = '<span class="loading"></span> 加载中...';
        element.disabled = true;
        
        // 存储原始文本以便恢复
        element.dataset.originalText = originalText;
    }
    
    // 显示全局加载指示器
    showGlobalLoading();
}

// 隐藏加载状态
function hideLoading(element = null) {
    isLoading = false;
    
    if (element && element.dataset.originalText) {
        element.innerHTML = element.dataset.originalText;
        element.disabled = false;
        delete element.dataset.originalText;
    }
    
    // 隐藏全局加载指示器
    hideGlobalLoading();
}

// 显示全局加载指示器
function showGlobalLoading() {
    let loadingOverlay = document.getElementById('loadingOverlay');
    if (!loadingOverlay) {
        loadingOverlay = document.createElement('div');
        loadingOverlay.id = 'loadingOverlay';
        loadingOverlay.innerHTML = `
            <div class="d-flex justify-content-center align-items-center h-100">
                <div class="text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">加载中...</span>
                    </div>
                    <div class="mt-2">正在加载数据...</div>
                </div>
            </div>
        `;
        loadingOverlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.9);
            z-index: 9999;
            display: none;
        `;
        document.body.appendChild(loadingOverlay);
    }
    loadingOverlay.style.display = 'block';
}

// 隐藏全局加载指示器
function hideGlobalLoading() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
    }
}

// 刷新数据
function refreshData() {
    showLoading();
    
    // 模拟数据刷新
    setTimeout(() => {
        location.reload();
    }, 1000);
}

// 检查数据更新
function checkDataUpdate() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            // 检查数据是否有更新
            console.log('数据统计:', data);
        })
        .catch(error => {
            console.error('检查数据更新失败:', error);
        });
}

// 格式化数字
function formatNumber(num) {
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'k';
    }
    return num.toString();
}

// 格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) {
        return '今天';
    } else if (diffDays === 2) {
        return '昨天';
    } else if (diffDays <= 7) {
        return `${diffDays} 天前`;
    } else {
        return date.toLocaleDateString('zh-CN');
    }
}

// 复制到剪贴板
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('已复制到剪贴板', 'success');
        }).catch(() => {
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

// 备用复制方法
function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showToast('已复制到剪贴板', 'success');
    } catch (err) {
        showToast('复制失败', 'error');
    }
    
    document.body.removeChild(textArea);
}

// 显示提示消息
function showToast(message, type = 'info') {
    // 创建提示元素
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 10000; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // 自动移除
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 3000);
}

// 导出函数供全局使用
window.ByteDanceJobMonitor = {
    showLoading,
    hideLoading,
    refreshData,
    formatNumber,
    formatDate,
    copyToClipboard,
    showToast
};