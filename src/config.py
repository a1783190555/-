# =============================================================================
# 文件: src/config.py
# 功能: 配置管理
# =============================================================================

class Config:
    """配置类"""
    
    # 下载设置
    DOWNLOAD_DIR = "downloads"
    OUTPUT_FORMAT = "mp3"
    KEEP_ORIGINAL = False
    AUTO_CONVERT = True
    
    # 音频质量设置
    BITRATE = "320k"
    SAMPLE_RATE = 44100
    CHANNELS = 2
    
    # Selenium设置
    USE_SELENIUM = True
    HEADLESS = True
    WINDOW_SIZE = "1920,1080"
    
    # 请求设置
    MAX_RETRIES = 3
    TIMEOUT = 30
    DELAY_SECONDS = 2
    
    # 用户代理
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    @classmethod
    def get_headers(cls):
        """获取请求头"""
        return {
            'User-Agent': cls.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }