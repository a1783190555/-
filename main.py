# =============================================================================
# 文件: main.py
# 功能: 主程序入口
# =============================================================================

from src.crawler import QiShuiMusicCrawler
from src.converter import AudioConverter
from src.config import Config

def main():
    print("=== 汽水音乐爬虫 ===")
    print()
    print("选择操作模式:")
    print("1. 爬取新音乐并自动转换")
    print("2. 只转换现有的MP4文件")
    
    try:
        choice = input("请选择 (1/2): ").strip()
        
        if choice == "1":
            # 爬取新音乐
            crawler = QiShuiMusicCrawler()
            
            try:
                share_url = input("请输入汽水音乐分享链接: ").strip()
                if not share_url:
                    share_url = "https://qishui.douyin.com/s/iaVudjjq/"  # 默认测试链接
                
                success = crawler.crawl_and_download(share_url)
                
                if success:
                    print("\n🎉 处理完成！")
                else:
                    print("\n💥 处理失败！")
                    
            finally:
                crawler.close()
        
        elif choice == "2":
            # 转换现有文件
            converter = AudioConverter()
            success_count = converter.batch_convert(Config.DOWNLOAD_DIR)
            
            if success_count > 0:
                print(f"\n🎉 成功转换 {success_count} 个文件！")
            else:
                print("\n💥 没有文件被转换！")
        
        else:
            print("❌ 无效选择")
            
    except KeyboardInterrupt:
        print("\n\n👋 程序已取消")
    except Exception as e:
        print(f"\n❌ 程序错误: {e}")

if __name__ == "__main__":
    main()