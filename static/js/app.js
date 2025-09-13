// 字节跳动职位监控 Web 应用 JavaScript - 现代化版本

// 全局变量
let isLoading = false;
let animationObserver = null;
let scrollProgress = 0;

// DOM 加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 页面加载动画
window.addEventListener('load', function() {
    // 页面加载完成后的动画
    document.body.classList.add('loaded');
    
    // 添加页面加载完成的CSS
    const style = document.createElement('style');
    style.textContent = `
        body {
            opacity: 0;
            transition: opacity 0.5s ease-in-out;
        }
        body.loaded {
            opacity: 1;
        }
        .fade-in-up {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .fade-in-up.visible {
            opacity: 1;
            transform: translateY(0);
        }
        .stagger-animation:nth-child(1) { transition-delay: 0.1s; }
        .stagger-animation:nth-child(2) { transition-delay: 0.2s; }
        .stagger-animation:nth-child(3) { transition-delay: 0.3s; }
        .stagger-animation:nth-child(4) { transition-delay: 0.4s; }
        .stagger-animation:nth-child(5) { transition-delay: 0.5s; }
    `;
    document.head.appendChild(style);
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
    
    // 初始化动画观察器
    initAnimationObserver();
    
    // 初始化微交互
    initMicroInteractions();
    
    // 初始化导航栏效果
    initNavbarEffects();
    
    // 初始化卡片悬停效果
    initCardEffects();
    
    console.log('字节跳动职位监控 Web 应用已初始化 - 现代化版本');
}

// 初始化动画观察器
function initAnimationObserver() {
    if ('IntersectionObserver' in window) {
        animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    // 为卡片添加交错动画
                    if (entry.target.classList.contains('card')) {
                        entry.target.classList.add('stagger-animation');
                    }
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        // 观察所有卡片和需要动画的元素
        document.querySelectorAll('.card, .fade-in-up').forEach(el => {
            el.classList.add('fade-in-up');
            animationObserver.observe(el);
        });
    }
}

// 初始化微交互
function initMicroInteractions() {
    // 按钮点击波纹效果
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', createRippleEffect);
    });
    
    // 卡片悬停时的倾斜效果
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mousemove', handleCardMouseMove);
        card.addEventListener('mouseleave', handleCardMouseLeave);
    });
    
    // 输入框聚焦效果
    document.querySelectorAll('.form-control, .form-select').forEach(input => {
        input.addEventListener('focus', handleInputFocus);
        input.addEventListener('blur', handleInputBlur);
    });
}

// 创建波纹效果
function createRippleEffect(e) {
    const button = e.currentTarget;
    const ripple = document.createElement('span');
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    `;
    
    // 添加波纹动画CSS（如果还没有）
    if (!document.querySelector('#ripple-styles')) {
        const style = document.createElement('style');
        style.id = 'ripple-styles';
        style.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
            .btn {
                position: relative;
                overflow: hidden;
            }
        `;
        document.head.appendChild(style);
    }
    
    button.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// 卡片鼠标移动效果
function handleCardMouseMove(e) {
    const card = e.currentTarget;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = (y - centerY) / 10;
    const rotateY = (centerX - x) / 10;
    
    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
}

// 卡片鼠标离开效果
function handleCardMouseLeave(e) {
    const card = e.currentTarget;
    card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
}

// 输入框聚焦效果
function handleInputFocus(e) {
    const input = e.currentTarget;
    input.parentElement.classList.add('input-focused');
}

function handleInputBlur(e) {
    const input = e.currentTarget;
    input.parentElement.classList.remove('input-focused');
}

// 初始化导航栏效果
function initNavbarEffects() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    let lastScrollY = window.scrollY;
    
    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        
        // 导航栏背景透明度
        if (currentScrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.backdropFilter = 'blur(20px)';
        } else {
            navbar.style.background = 'var(--white)';
            navbar.style.backdropFilter = 'none';
        }
        
        // 导航栏隐藏/显示
        if (currentScrollY > lastScrollY && currentScrollY > 100) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollY = currentScrollY;
    });
}

// 初始化卡片效果
function initCardEffects() {
    // 为统计卡片添加数字动画
    const statCards = document.querySelectorAll('.card h2');
    statCards.forEach(card => {
        const finalValue = parseInt(card.textContent);
        if (!isNaN(finalValue)) {
            animateNumber(card, 0, finalValue, 1500);
        }
    });
}

// 数字动画
function animateNumber(element, start, end, duration) {
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // 使用缓动函数
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const current = Math.floor(start + (end - start) * easeOutQuart);
        
        element.textContent = current.toLocaleString();
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// 初始化工具提示
function initTooltips() {
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
        const searchInput = document.getElementById('search');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    // 实时搜索建议功能
                    const query = this.value.trim();
                    if (query.length > 2) {
                        showSearchSuggestions(query);
                    } else {
                        hideSearchSuggestions();
                    }
                }, 300);
            });
            
            // 搜索框聚焦动画
            searchInput.addEventListener('focus', function() {
                this.parentElement.style.transform = 'scale(1.02)';
                this.parentElement.style.boxShadow = '0 8px 25px rgba(22, 100, 255, 0.15)';
            });
            
            searchInput.addEventListener('blur', function() {
                this.parentElement.style.transform = 'scale(1)';
                this.parentElement.style.boxShadow = '';
            });
        }
    }
}

// 显示搜索建议
function showSearchSuggestions(query) {
    // 这里可以实现搜索建议功能
    console.log('搜索建议:', query);
}

// 隐藏搜索建议
function hideSearchSuggestions() {
    // 隐藏搜索建议
}

// 初始化滚动效果
function initScrollEffects() {
    // 滚动进度条
    const progressBar = createScrollProgressBar();
    
    // 返回顶部按钮
    const backToTopBtn = createBackToTopButton();
    
    window.addEventListener('scroll', function() {
        const scrolled = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
        progressBar.style.width = scrolled + '%';
        
        // 显示/隐藏返回顶部按钮
        if (window.scrollY > 300) {
            backToTopBtn.style.opacity = '1';
            backToTopBtn.style.transform = 'translateY(0)';
        } else {
            backToTopBtn.style.opacity = '0';
            backToTopBtn.style.transform = 'translateY(20px)';
        }
    });
}

// 创建滚动进度条
function createScrollProgressBar() {
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(90deg, #1664ff, #4285ff);
        z-index: 9999;
        transition: width 0.1s ease;
    `;
    document.body.appendChild(progressBar);
    return progressBar;
}

// 创建返回顶部按钮
function createBackToTopButton() {
    const button = document.createElement('button');
    button.innerHTML = '<i class="fas fa-arrow-up"></i>';
    button.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1664ff, #4285ff);
        border: none;
        color: white;
        font-size: 18px;
        cursor: pointer;
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(22, 100, 255, 0.3);
    `;
    
    button.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    button.addEventListener('mouseenter', () => {
        button.style.transform = 'translateY(-4px) scale(1.1)';
        button.style.boxShadow = '0 8px 20px rgba(22, 100, 255, 0.4)';
    });
    
    button.addEventListener('mouseleave', () => {
        button.style.transform = 'translateY(0) scale(1)';
        button.style.boxShadow = '0 4px 12px rgba(22, 100, 255, 0.3)';
    });
    
    document.body.appendChild(button);
    return button;
}

// 初始化数据刷新
function initDataRefresh() {
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            this.classList.add('loading');
            refreshData();
        });
    }
}

// 显示加载状态
function showLoading(element = null) {
    if (element) {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        spinner.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div>';
        element.appendChild(spinner);
    } else {
        showGlobalLoading();
    }
}

// 隐藏加载状态
function hideLoading(element = null) {
    if (element) {
        const spinner = element.querySelector('.loading-spinner');
        if (spinner) {
            spinner.remove();
        }
    } else {
        hideGlobalLoading();
    }
}

// 显示全局加载
function showGlobalLoading() {
    if (document.querySelector('.global-loading')) return;
    
    const loadingOverlay = document.createElement('div');
    loadingOverlay.className = 'global-loading';
    loadingOverlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        backdrop-filter: blur(5px);
    `;
    
    const spinner = document.createElement('div');
    spinner.style.cssText = `
        width: 40px;
        height: 40px;
        border: 4px solid rgba(22, 100, 255, 0.2);
        border-radius: 50%;
        border-top-color: #1664ff;
        animation: spin 1s linear infinite;
    `;
    
    loadingOverlay.appendChild(spinner);
    document.body.appendChild(loadingOverlay);
}

// 隐藏全局加载
function hideGlobalLoading() {
    const loading = document.querySelector('.global-loading');
    if (loading) {
        loading.style.opacity = '0';
        setTimeout(() => loading.remove(), 300);
    }
}

// 刷新数据
function refreshData() {
    if (isLoading) return;
    
    isLoading = true;
    showGlobalLoading();
    
    fetch('/api/refresh', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('数据刷新成功！', 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showToast('数据刷新失败，请稍后重试', 'error');
        }
    })
    .catch(error => {
        console.error('刷新失败:', error);
        showToast('网络错误，请检查连接', 'error');
    })
    .finally(() => {
        isLoading = false;
        hideGlobalLoading();
        const refreshBtn = document.getElementById('refreshBtn');
        if (refreshBtn) {
            refreshBtn.classList.remove('loading');
        }
    });
}

// 格式化数字
function formatNumber(num) {
    return new Intl.NumberFormat('zh-CN').format(num);
}

// 格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (days === 0) {
        return '今天';
    } else if (days === 1) {
        return '昨天';
    } else if (days < 7) {
        return `${days}天前`;
    } else {
        return date.toLocaleDateString('zh-CN');
    }
}

// 复制到剪贴板
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('已复制到剪贴板', 'success');
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
    
    textArea.remove();
}

// 显示提示消息
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    const colors = {
        success: '#00d4aa',
        error: '#ff6b6b',
        warning: '#ff8c00',
        info: '#1664ff'
    };
    
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type]};
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 500;
    `;
    
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // 动画显示
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
    }, 100);
    
    // 自动隐藏
    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// 导出全局API
window.ByteDanceJobMonitor = {
    showLoading,
    hideLoading,
    refreshData,
    formatNumber,
    formatDate,
    copyToClipboard,
    showToast,
    animateNumber
};