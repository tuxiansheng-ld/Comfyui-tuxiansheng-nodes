import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class HTMLScreenshotter:
    """
    一个使用无头浏览器将HTML内容按指定尺寸截图的工具类。
    """

    def __init__(self, chromedriver_path=None, default_width=None, default_height=None):
        """
        初始化截图工具，启动一个无头的Chrome浏览器。

        :param chromedriver_path: chromedriver的可执行文件路径。
                                  如果未提供，将尝试从环境变量CHROMEDRIVER_PATH读取。
                                  如果环境变量也未设置，则假定它在系统的PATH中(默认为'chromedriver')。
        :param default_width: 默认截图宽度，如果未提供，将从环境变量DEFAULT_SCREENSHOT_WIDTH读取，默认1920。
        :param default_height: 默认截图高度，如果未提供，将从环境变量DEFAULT_SCREENSHOT_HEIGHT读取，默认1080。
        """
        # 从环境变量或参数获取chromedriver路径
        if chromedriver_path is None:
            chromedriver_path = os.getenv('CHROMEDRIVER_PATH', 'chromedriver')
        
        # 从环境变量或参数获取默认宽高
        self.default_width = default_width or int(os.getenv('DEFAULT_SCREENSHOT_WIDTH', '1920'))
        self.default_height = default_height or int(os.getenv('DEFAULT_SCREENSHOT_HEIGHT', '1080'))
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 无头模式
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--window-size={self.default_width}x{self.default_height}") # 设置默认窗口大小
        
        try:
            # 使用Service对象是Selenium 4.6+推荐的方式
            service = Service(executable_path=chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"初始化WebDriver时出错: {e}")
            print("请确保已安装Chrome浏览器和正确的chromedriver，并提供了正确的路径。")
            self.driver = None

    def capture_from_string(self, html_string: str, output_image: str, width: int = None, height: int = None):
        """
        从HTML内容字符串进行截图。

        :param html_string: HTML内容的字符串。
        :param output_image: 输出图片文件的保存路径 (例如 'screenshot.png')。
        :param width: 截图的期望宽度（像素），如果未提供则使用默认宽度。
        :param height: 截图的期望高度（像素），如果未提供则使用默认高度。
        """
        width = width or self.default_width
        height = height or self.default_height
        if not self.driver:
            print("WebDriver未初始化，无法截图。")
            return

        # 使用data URI加载HTML字符串
        self.driver.get(f"data:text/html;charset=utf-8,{html_string}")
        self._take_screenshot(output_image, width, height)
        print(f"截图已保存到 {output_image}")

    def capture_from_file(self, html_file_path: str, output_image: str, width: int = None, height: int = None):
        """
        从本地HTML文件进行截图。

        :param html_file_path: 本地HTML文件的路径。
        :param output_image: 输出图片文件的保存路径 (例如 'screenshot.png')。
        :param width: 截图的期望宽度（像素），如果未提供则使用默认宽度。
        :param height: 截图的期望高度（像素），如果未提供则使用默认高度。
        """
        width = width or self.default_width
        height = height or self.default_height
        if not self.driver:
            print("WebDriver未初始化，无法截图。")
            return

        # 获取绝对路径并使用 file:// URI
        abs_path = os.path.abspath(html_file_path)
        self.driver.get(f"file:///{abs_path}")
        self._take_screenshot(output_image, width, height)
        print(f"截图已保存到 {output_image}")

    def _take_screenshot(self, output_image: str, width: int, height: int):
        """内部辅助方法，用于设置尺寸并截图。"""
        self.driver.set_window_size(width, height)
        # 根据body的实际尺寸来截图，可以确保内容完整
        # 但如果需要固定尺寸的画布，set_window_size已经足够
        self.driver.save_screenshot(output_image)

    def close(self):
        """
        关闭浏览器实例，释放资源。
        """
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        """支持 with 上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出 with 代码块时自动关闭浏览器"""
        self.close()

# ====================
#     示例用法
# ====================
if __name__ == '__main__':
    # --- 为演示创建一个临时的HTML文件 ---
    html_for_file = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <title>测试页面</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background-color: #f0f8ff; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;}
            .container { text-align: center; padding: 40px; background-color: #ffffff; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 10px; }
            h1 { color: #0056b3; }
            p { color: #333; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>来自文件的截图!</h1>
            <p>这是一个通过HTML文件生成的精美截图。</p>
        </div>
    </body>
    </html>
    """
    with open("test_page.html", "w", encoding="utf-8") as f:
        f.write(html_for_file)

    # --- 使用截图工具类 ---
    # 使用 'with' 语句可以确保浏览器在结束时自动关闭。
    # 如果 chromedriver 不在系统PATH中, 请替换为你的 chromedriver 路径。
    # 例如: 'C:/path/to/your/chromedriver.exe'
    try:
        with HTMLScreenshotter() as screenshotter:
            # 1. 从HTML字符串截图
            html_string = "<h1>你好, 世界!</h1><p style='color: red; font-size: 24px;'>这是一个从HTML字符串生成的截图。</p>"
            screenshotter.capture_from_string(html_string, "string_screenshot.png", width=800, height=400)

            # 2. 从HTML文件截图
            screenshotter.capture_from_file("D:/ComfyUI/custom_nodes/Comfyui-tuxiansheng-nodes/output_table.html", "file_screenshot.png", width=600, height=500)

    except Exception as e:
        print(f"执行过程中发生错误: {e}")

