import os
import json
import torch
from PIL import Image
from comfy_api.latest import io


class TableStyleConfigNode(io.ComfyNode):
    """
    表格样式配置节点
    读取配置文件，提供模板选择和尺寸设置功能
    
    Class methods
    -------------
    define_schema (io.Schema):
        定义节点元数据、输入输出参数
    """

    @classmethod
    def _load_config(cls):
        """加载配置文件"""
        try:
            # 获取配置文件路径
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(current_dir, "config", "size_table_style_conf.json")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get("styles", [])
        except Exception as e:
            print(f"[TableStyleConfigNode] 加载配置失败: {str(e)}")
            return []

    @classmethod
    def _get_style_names(cls):
        """获取所有样式名称列表"""
        styles = cls._load_config()
        if not styles:
            return ["默认样式"]
        return [style.get("name", f"样式{i+1}") for i, style in enumerate(styles)]

    @classmethod
    def define_schema(cls) -> io.Schema:
        """
        定义节点架构
        """
        # 获取样式名称列表用于下拉框
        style_names = cls._get_style_names()
        
        return io.Schema(
            node_id="TableStyleConfigNode",
            display_name="Table Style Config",
            category="tuxiansheng/tables",
            inputs=[
                io.Combo.Input(
                    "style_name",
                    options=style_names,
                    default=style_names[0] if style_names else "默认样式",
                ),
                io.Int.Input(
                    "custom_width",
                    default=0,
                    min=0,
                    max=10000,
                    lazy=True,
                ),
                io.Int.Input(
                    "custom_height",
                    default=0,
                    min=0,
                    max=10000,
                    lazy=True,
                )
            ],
            outputs=[
                io.String.Output(display_name="HTML Template"),  # HTML模板字符串
                io.String.Output(display_name="JSON Template"),  # JSON数据模板字符串
                io.Int.Output(display_name="Width"),     # 宽度
                io.Int.Output(display_name="Height"),     # 高度
                io.Image.Output(display_name="Preview"),  # 预览图片
                io.Int.Output(display_name="Crop Width"),  # 建议裁剪宽度
                io.Int.Output(display_name="Crop Height"),  # 建议裁剪高度
            ],
        )

    @classmethod
    def check_lazy_status(cls, style_name, custom_width, custom_height):
        """
        控制惰性输入的评估时机
        
        只有当需要自定义尺寸时才评估宽高参数
        """
        # 总是需要评估宽高参数以支持 fallback 逻辑
        return ["custom_width", "custom_height"]

    @classmethod
    def execute(cls, style_name, custom_width, custom_height) -> io.NodeOutput:
        """
        执行节点逻辑
        
        Parameters:
        -----------
        style_name: str
            选择的样式模板名称
        custom_width: int
            自定义宽度（0表示使用配置值）
        custom_height: int
            自定义高度（0表示使用配置值）
            
        Returns:
        --------
        NodeOutput
            包含HTML模板、JSON模板、宽度、高度、预览图片、建议裁剪宽度、建议裁剪高度
        """
        # 加载配置
        styles = cls._load_config()
        
        # 查找选中的样式配置
        selected_style = None
        for style in styles:
            if style.get("name") == style_name:
                selected_style = style
                break
        
        # 如果未找到配置，返回默认值
        if not selected_style:
            print(f"[TableStyleConfigNode] 未找到样式: {style_name}")
            # 返回默认的黑色预览图片
            default_preview = torch.zeros((1, 100, 100, 3), dtype=torch.float32)
            return io.NodeOutput("", "", 800, 600, default_preview, 800, 600)
        
        # 读取HTML模板
        html_content = ""
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            html_path = os.path.join(current_dir, selected_style.get("html_template", ""))
            if os.path.exists(html_path):
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
            else:
                print(f"[TableStyleConfigNode] HTML模板文件不存在: {html_path}")
        except Exception as e:
            print(f"[TableStyleConfigNode] 读取HTML模板失败: {str(e)}")
        
        # 读取JSON数据模板
        json_content = ""
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_path = os.path.join(current_dir, selected_style.get("json_data_template", ""))
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    json_content = f.read()
            else:
                print(f"[TableStyleConfigNode] JSON模板文件不存在: {json_path}")
        except Exception as e:
            print(f"[TableStyleConfigNode] 读取JSON模板失败: {str(e)}")
        
        # 确定输出的宽高：优先使用用户输入，如果为0则使用配置值
        output_width = custom_width if custom_width > 0 else selected_style.get("sugguest_width", 800)
        output_height = custom_height if custom_height > 0 else selected_style.get("sugguest_height", 600)
        
        # 读取预览图片
        preview_image = None
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            preview_path = selected_style.get("preview_image", "")
            
            if preview_path:
                preview_full_path = os.path.join(current_dir, preview_path)
                if os.path.exists(preview_full_path):
                    # 读取图片并转换为 ComfyUI 需要的格式
                    img = Image.open(preview_full_path)
                    # 转换为 RGB 模式（如果是 RGBA 或其他模式）
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    # 转换为 numpy 数组，并归一化到 0-1 范围
                    import numpy as np
                    img_array = np.array(img).astype(np.float32) / 255.0
                    # 转换为 PyTorch tensor，格式: [batch, height, width, channels]
                    preview_image = torch.from_numpy(img_array).unsqueeze(0)
                    print(f"[TableStyleConfigNode] 加载预览图片: {preview_full_path}")
                else:
                    print(f"[TableStyleConfigNode] 预览图片文件不存在: {preview_full_path}")
                    # 创建一个默认的黑色图片 (1, 100, 100, 3)
                    preview_image = torch.zeros((1, 100, 100, 3), dtype=torch.float32)
            else:
                print(f"[TableStyleConfigNode] 配置中未指定预览图片")
                # 创建一个默认的黑色图片
                preview_image = torch.zeros((1, 100, 100, 3), dtype=torch.float32)
        except Exception as e:
            print(f"[TableStyleConfigNode] 读取预览图片失败: {str(e)}")
            # 创建一个默认的黑色图片
            preview_image = torch.zeros((1, 100, 100, 3), dtype=torch.float32)
        
        # 获取配置文件中的建议裁剪尺寸
        crop_width = selected_style.get("sugguest_width", 800)
        crop_height = selected_style.get("sugguest_height", 600)
        
        return io.NodeOutput(html_content, json_content, output_width, output_height, preview_image, crop_width, crop_height)


# 节点映射配置
NODE_CLASS_MAPPINGS = {
    "TableStyleConfigNode": TableStyleConfigNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TableStyleConfigNode": "Table Style Config"
}
