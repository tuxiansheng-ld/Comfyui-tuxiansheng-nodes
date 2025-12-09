import os
import sys
from comfy_api.latest import io

# 处理模块导入 - 确保父目录在 sys.path 中
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 直接导入模块，不经过 utils.__init__
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "html_screenshotter",
        os.path.join(parent_dir, "utils", "html_screenshotter.py")
    )
    html_screenshotter_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(html_screenshotter_module)
    HTMLScreenshotter = html_screenshotter_module.HTMLScreenshotter
except Exception as e:
    print(f"[HTMLScreenshotterNode] 导入失败: {e}")
    import traceback
    traceback.print_exc()
    raise


class HTMLScreenshotterNode(io.ComfyNode):
    """
    HTML 截图节点
    将 HTML 字符串渲染为图片
    
    Class methods
    -------------
    define_schema (io.Schema):
        定义节点元数据、输入输出参数
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        """
        定义节点架构
        """
        return io.Schema(
            node_id="HTMLScreenshotterNode",
            display_name="HTML Screenshot",
            category="tuxiansheng/tables",
            inputs=[
                io.String.Input(
                    "html_content",
                    multiline=True,
                    default="",
                    lazy=True,
                    tooltip="HTML 内容字符串",
                ),
                io.Int.Input(
                    "width",
                    default=800,
                    min=100,
                    max=10000,
                    lazy=True,
                    tooltip="截图宽度（像素）",
                ),
                io.Int.Input(
                    "height",
                    default=600,
                    min=100,
                    max=10000,
                    lazy=True,
                    tooltip="截图高度（像素）",
                ),
            ],
            outputs=[
                io.Image.Output(display_name="Screenshot"),  # 截图图片
            ],
        )

    @classmethod
    def check_lazy_status(cls, html_content, width, height):
        """
        控制惰性输入的评估时机
        
        总是需要评估所有输入参数
        """
        return ["html_content", "width", "height"]

    @classmethod
    def execute(cls, html_content, width, height) -> io.NodeOutput:
        """
        执行节点逻辑
        
        Parameters:
        -----------
        html_content: str
            HTML 内容字符串
        width: int
            截图宽度（像素）
        height: int
            截图高度（像素）
            
        Returns:
        --------
        NodeOutput
            包含截图图片（torch.Tensor）
        """
        screenshotter = None
        try:
            # 验证输入
            if not html_content:
                raise ValueError("HTML 内容字符串不能为空")
            
            if width <= 0 or height <= 0:
                raise ValueError(f"宽度和高度必须大于0，当前值: {width}x{height}")
            
            # 初始化截图工具
            # 从环境变量获取 chromedriver 路径
            chromedriver_path = os.getenv('CHROMEDRIVER_PATH', 'chromedriver')
            
            try:
                screenshotter = HTMLScreenshotter(
                    chromedriver_path=chromedriver_path,
                    default_width=width,
                    default_height=height
                )
                
                if not screenshotter.driver:
                    raise RuntimeError("WebDriver 初始化失败，请检查 ChromeDriver 配置")
                
                # 截图并返回 tensor
                screenshot_tensor = screenshotter.capture_from_string_to_tensor(
                    html_string=html_content,
                    width=width,
                    height=height
                )
                
                print(f"[HTMLScreenshotterNode] 截图成功，尺寸: {width}x{height}")
                return io.NodeOutput(screenshot_tensor)
                
            except Exception as e:
                error_msg = f"截图失败: {str(e)}"
                print(f"[HTMLScreenshotterNode] {error_msg}")
                # 返回黑色占位图片
                import torch
                return io.NodeOutput(torch.zeros((1, height, width, 3), dtype=torch.float32))
        
        except Exception as e:
            error_msg = f"节点执行失败: {str(e)}"
            print(f"[HTMLScreenshotterNode] {error_msg}")
            # 返回黑色占位图片
            import torch
            return io.NodeOutput(torch.zeros((1, 600, 800, 3), dtype=torch.float32))
        
        finally:
            # 确保关闭 WebDriver
            if screenshotter:
                try:
                    screenshotter.close()
                except Exception as e:
                    print(f"[HTMLScreenshotterNode] 关闭 WebDriver 失败: {str(e)}")


# 节点映射配置
NODE_CLASS_MAPPINGS = {
    "HTMLScreenshotterNode": HTMLScreenshotterNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "HTMLScreenshotterNode": "HTML Screenshot"
}
