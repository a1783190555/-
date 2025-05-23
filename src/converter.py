# =============================================================================
# 文件: src/converter.py
# 功能: 音频格式转换
# =============================================================================

import os
import shutil
from pathlib import Path
from moviepy import AudioFileClip
from .config import Config
from typing import Optional

class AudioConverter:
    """音频转换器"""
    
    def __init__(self, output_format: str = None, bitrate: str = None):
        self.output_format = output_format or Config.OUTPUT_FORMAT
        self.bitrate = bitrate or Config.BITRATE
    
    def convert_audio(self, input_file: str, keep_original: bool = None) -> Optional[str]:
        """转换音频格式"""
        if keep_original is None:
            keep_original = Config.KEEP_ORIGINAL
            
        try:
            output_file = input_file.replace('.mp4', f'.{self.output_format}')
            
            print(f"🔄 开始转换音频格式: {os.path.basename(input_file)} -> {self.output_format.upper()}")
            
            # 使用MoviePy转换
            audio_clip = AudioFileClip(input_file)
            
            # 尝试不同的参数组合
            try:
                audio_clip.write_audiofile(output_file, bitrate=self.bitrate)
            except TypeError:
                try:
                    audio_clip.write_audiofile(output_file)
                except TypeError:
                    audio_clip.write_audiofile(output_file, logger=None)
            
            audio_clip.close()
            
            print(f"✅ 音频转换完成: {os.path.basename(output_file)}")
            
            # 删除原文件
            if not keep_original:
                os.remove(input_file)
                print(f"🗑️ 已删除原文件: {os.path.basename(input_file)}")
            
            return output_file
            
        except Exception as e:
            print(f"❌ 音频转换失败: {e}")
            
            # 备用方案：重命名文件
            return self._fallback_rename(input_file, keep_original)
    
    def _fallback_rename(self, input_file: str, keep_original: bool) -> Optional[str]:
        """备用方案：重命名文件"""
        try:
            print("🔄 使用备用方案：重命名文件")
            output_file = input_file.replace('.mp4', f'.{self.output_format}')
            shutil.copy2(input_file, output_file)
            
            if not keep_original:
                os.remove(input_file)
                print(f"🗑️ 已删除原文件: {os.path.basename(input_file)}")
            
            print(f"✅ 文件已重命名: {os.path.basename(output_file)}")
            print("⚠️ 注意：这只是重命名，不是真正的格式转换")
            return output_file
            
        except Exception as e:
            print(f"❌ 备用方案失败: {e}")
            return None
    
    def batch_convert(self, input_dir: str) -> int:
        """批量转换目录中的MP4文件"""
        input_path = Path(input_dir)
        
        if not input_path.exists():
            print(f"❌ 目录不存在: {input_dir}")
            return 0
        
        # 查找所有MP4文件
        mp4_files = list(input_path.glob("*.mp4"))
        
        if not mp4_files:
            print(f"❌ 在 {input_dir} 中未找到MP4文件")
            return 0
        
        print(f"📁 找到 {len(mp4_files)} 个MP4文件")
        
        success_count = 0
        for i, mp4_file in enumerate(mp4_files, 1):
            print(f"\n--- 转换文件 {i}/{len(mp4_files)} ---")
            if self.convert_audio(str(mp4_file)):
                success_count += 1
        
        print(f"\n🎉 批量转换完成！成功: {success_count}/{len(mp4_files)}")
        return success_count