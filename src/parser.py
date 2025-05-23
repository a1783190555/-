# =============================================================================
# 文件: src/parser.py  
# 功能: 页面解析和数据提取
# =============================================================================

import re
import json
from typing import Optional, Dict, Any

class PageParser:
    """页面解析器"""
    
    def __init__(self):
        self.patterns = [
            r'_ROUTER_DATA\s*=\s*(\{[\s\S]*?\});(?=\s*function|\s*</script>|\s*var|\s*window|\s*$)',
            r'"audioWithLyricsOption":\s*(\{[\s\S]*?\})(?=,|\})',
        ]
    
    def extract_track_info(self, html_content: str) -> Optional[Dict[str, Any]]:
        """从HTML内容中提取音乐信息"""
        print("=== 开始解析页面 ===")
        
        for i, pattern in enumerate(self.patterns):
            print(f"尝试模式 {i+1}...")
            matches = re.findall(pattern, html_content, re.DOTALL)
            
            if matches:
                print(f"✓ 模式 {i+1} 找到 {len(matches)} 个匹配")
                
                for j, match in enumerate(matches):
                    try:
                        data = json.loads(match)
                        audio_info = self._find_audio_info_recursive(data)
                        if audio_info:
                            print(f"✓ 从匹配 {j+1} 中找到音频信息")
                            return audio_info
                    except json.JSONDecodeError:
                        continue
        
        print("❌ 未找到音频信息")
        return None
    
    def _find_audio_info_recursive(self, data: Any, path: str = "root") -> Optional[Dict[str, Any]]:
        """递归查找音频信息"""
        if isinstance(data, dict):
            # 检查是否包含音频信息
            if 'url' in data and ('trackName' in data or 'name' in data):
                track_name = data.get('trackName') or data.get('name', '')
                artist_name = data.get('artistName', '未知艺术家')
                audio_url = data.get('url', '')
                
                if audio_url and ('douyinvod.com' in audio_url or 'mp4' in audio_url):
                    return {
                        'track_name': track_name,
                        'artist_name': artist_name,
                        'audio_url': audio_url,
                        'track_id': data.get('track_id'),
                        'duration': data.get('duration', 0),
                        'cover_url': data.get('cover_url')
                    }
            
            # 递归搜索关键节点
            for key, value in data.items():
                if key in ['audioWithLyricsOption', 'track_page', 'loaderData', 'trackInfo']:
                    result = self._find_audio_info_recursive(value, f"{path}.{key}")
                    if result:
                        return result
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                result = self._find_audio_info_recursive(item, f"{path}[{i}]")
                if result:
                    return result
        
        return None