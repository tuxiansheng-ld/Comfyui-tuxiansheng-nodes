import os
import sys
import json
from typing import Optional
from comfy_api.latest import io

# 处理相对导入
try:
    from ..utils.kimi_table_to_json import KimiTableToJSON
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.kimi_table_to_json import KimiTableToJSON


class KimiTableToJSONNode(io.ComfyNode):
    """
    Kimi 表格转 JSON 节点
    使用 Kimi API 将表格图片按照 JSON 模板提取为结构化数据
    
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
            node_id="KimiTableToJSONNode",
            display_name="Kimi Table To JSON",
            category="tuxiansheng/kimi",
            inputs=[
                io.String.Input(
                    "image_base64",
                    multiline=True,
                    default="",
                    lazy=True,
                ),
                io.String.Input(
                    "json_template",
                    multiline=True,
                    default="{}",
                    lazy=True,
                ),
                io.String.Input(
                    "api_key",
                    multiline=False,
                    default="",
                    lazy=True,
                    tooltip="Kimi API 密钥（可选，留空则从环境变量 KIMI_API_KEY 获取）",
                ),
                io.Float.Input(
                    "temperature",
                    default=0.1,
                    min=0.0,
                    max=1.0,
                    step=0.01,
                    lazy=True,
                ),
                io.Int.Input(
                    "max_tokens",
                    default=4000,
                    min=100,
                    max=10000,
                    lazy=True,
                )
            ],
            outputs=[
                io.String.Output(display_name="JSON Data"),  # JSON 数据字符串
                io.String.Output(display_name="Raw Response"),  # 原始响应内容
                io.String.Output(display_name="Token Usage"),  # Token 使用情况（JSON格式）
            ],
        )

    @classmethod
    def check_lazy_status(cls, image_base64, json_template, api_key, temperature, max_tokens):
        """
        控制惰性输入的评估时机
        
        总是需要评估所有输入参数
        """
        return ["image_base64", "json_template", "api_key", "temperature", "max_tokens"]

    @classmethod
    def execute(cls, image_base64, json_template, api_key, temperature, max_tokens) -> io.NodeOutput:
        """
        执行节点逻辑
        
        Parameters:
        -----------
        image_base64: str
            图片的 base64 编码字符串（可以包含或不包含 data:image 前缀）
        json_template: str
            JSON 数据模板字符串
        api_key: str
            Kimi API 密钥（可选，为空则从环境变量读取）
        temperature: float
            温度参数，控制输出随机性 (0-1)
        max_tokens: int
            最大生成 token 数
            
        Returns:
        --------
        NodeOutput
            包含 JSON 数据字符串、原始响应、Token 使用情况
        """
        try:
            # 验证输入
            if not image_base64:
                raise ValueError("图片 base64 字符串不能为空")
            
            if not json_template:
                raise ValueError("JSON 模板不能为空")
            
            # 获取 API 密钥：优先使用用户输入，否则从环境变量获取
            kimi_api_key = None
            if api_key and api_key.strip():
                # 用户输入了 API 密钥
                kimi_api_key = api_key.strip()
                print(f"[KimiTableToJSONNode] 使用用户提供的 API 密钥")
            else:
                # 从环境变量获取
                kimi_api_key = os.getenv("KIMI_API_KEY")
                if kimi_api_key:
                    print(f"[KimiTableToJSONNode] 从环境变量 KIMI_API_KEY 获取 API 密钥")
                else:
                    raise ValueError("未提供 API 密钥，且环境变量 KIMI_API_KEY 未设置")
            
            # 初始化 Kimi 客户端
            extractor = KimiTableToJSON(api_key=kimi_api_key)
            
            # 解析 JSON 模板
            try:
                template_obj = json.loads(json_template)
            except json.JSONDecodeError as e:
                raise ValueError(f"JSON 模板格式错误: {str(e)}")
            
            # 直接使用 base64 方法，无需创建临时文件
            result = extractor.extract_table_data_from_base64(
                image_base64=image_base64,
                json_template=template_obj,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # 提取结果
            json_data = result.get("json_data")
            raw_content = result.get("raw_content", "")
            usage = result.get("usage", {})
            
            # 将 JSON 数据转换为字符串
            if json_data:
                json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
            else:
                json_str = ""
                raw_content = "数据提取失败: 无法解析 JSON 数据"
            
            # 将 usage 转换为字符串
            usage_str = json.dumps(usage, ensure_ascii=False, indent=2)
            
            print(f"[KimiTableToJSONNode] 提取成功")
            print(f"[KimiTableToJSONNode] Token 使用: {usage_str}")
            
            return io.NodeOutput(json_str, raw_content, usage_str)
        
        except Exception as e:
            error_msg = f"节点执行失败: {str(e)}"
            print(f"[KimiTableToJSONNode] {error_msg}")
            return io.NodeOutput("", error_msg, "{}")


# 节点映射配置
NODE_CLASS_MAPPINGS = {
    "KimiTableToJSONNode": KimiTableToJSONNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "KimiTableToJSONNode": "Kimi Table To JSON"
}
