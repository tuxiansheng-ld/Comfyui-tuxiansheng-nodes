"""
Kimi API 工具类 - 根据图片表格内容和JSON模板提取结构化数据
"""
import os
import sys
import json
from typing import Optional, Dict, Any, Union

# 处理相对导入，支持直接运行和作为模块导入
try:
    from .kimi_client import KimiClient
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.kimi_client import KimiClient


class KimiTableToJSON:
    """使用 Kimi API 将图片表格按照 JSON 模板提取为结构化数据的工具类"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 Kimi API 客户端
        
        Args:
            api_key: Kimi API 密钥，如果不提供则从环境变量 KIMI_API_KEY 读取
        """
        # 使用 KimiClient 作为底层客户端
        self.client = KimiClient(api_key=api_key)
        # 默认使用视觉模型
        self.client.set_model("moonshot-v1-8k-vision-preview")
    
    def set_model(self, model: str):
        """
        设置使用的模型版本
        
        Args:
            model: 模型名称 (moonshot-v1-8k-vision-preview, moonshot-v1-32k-vision-preview 等)
        """
        self.client.set_model(model)
    
    def extract_table_data(
        self,
        image_path: str,
        json_template: Union[str, Dict, list],
        custom_prompt: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 4000
    ) -> Dict[str, Any]:
        """
        根据 JSON 模板从图片表格中提取数据
        
        Args:
            image_path: 图片文件路径
            json_template: JSON 数据模板，可以是:
                - 字符串: JSON 格式的字符串
                - 字典: Python 字典对象
                - 列表: Python 列表对象
            custom_prompt: 自定义提示词，如果不提供则使用默认提示词
            temperature: 温度参数，控制输出随机性 (0-1)，建议使用低温度保证准确性
            max_tokens: 最大生成 token 数
            
        Returns:
            包含提取的 JSON 数据和原始响应的字典
        """
        # 将 JSON 模板转换为字符串
        if isinstance(json_template, (dict, list)):
            template_str = json.dumps(json_template, ensure_ascii=False, indent=2)
        else:
            template_str = json_template
        
        # 构建默认提示词
        if custom_prompt is None:
            custom_prompt = f"""请仔细分析这张图片中的表格内容，然后按照以下 JSON 数据模板提取表格数据。

【JSON 数据模板】
```json
{template_str}
```

【提取要求】
1. 严格按照 JSON 模板的结构提取数据
2. 准确识别表格中的每一行数据
3. 确保字段名与模板完全一致
4. 数值类型的数据保持为字符串格式（与模板一致）
5. 如果某个字段在图片中不存在，使用空字符串 ""

【输出要求】
请只返回提取后的 JSON 数据，不要包含任何其他说明文字。
JSON 数据必须是有效的、可解析的格式。"""
        
        # 系统提示词
        system_prompt = "你是一个专业的数据提取专家，擅长从图片表格中准确提取结构化数据。你必须严格按照给定的 JSON 模板格式返回数据。"
        
        # 使用 KimiClient 调用 API
        result = self.client.chat(
            prompt=custom_prompt,
            image_paths=image_path,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # 提取 JSON 数据
        json_data = self._extract_json(result["content"])
        
        return {
            "json_data": json_data,
            "raw_content": result["content"],
            "raw_response": result["raw_response"],
            "image_path": image_path,
            "usage": result["usage"]
        }
    
    def extract_from_template_file(
        self,
        image_path: str,
        template_file_path: str,
        custom_prompt: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 4000
    ) -> Dict[str, Any]:
        """
        从 JSON 模板文件读取模板，然后提取图片数据
        
        Args:
            image_path: 图片文件路径
            template_file_path: JSON 模板文件路径
            custom_prompt: 自定义提示词
            temperature: 温度参数
            max_tokens: 最大 token 数
            
        Returns:
            包含提取的 JSON 数据和原始响应的字典
        """
        # 读取 JSON 模板文件
        with open(template_file_path, 'r', encoding='utf-8') as f:
            json_template = json.load(f)
        
        # 调用提取方法
        return self.extract_table_data(
            image_path=image_path,
            json_template=json_template,
            custom_prompt=custom_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def _extract_json(self, content: str) -> Union[Dict, list, None]:
        """
        从 API 响应内容中提取 JSON 数据
        
        Args:
            content: API 返回的文本内容
            
        Returns:
            提取的 JSON 数据（字典或列表）
        """
        # 尝试提取代码块中的 JSON
        json_str = None
        
        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            json_str = content[start:end].strip()
        elif "```" in content:
            start = content.find("```") + 3
            end = content.find("```", start)
            json_str = content[start:end].strip()
        else:
            json_str = content.strip()
        
        # 尝试解析 JSON
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"警告: JSON 解析失败 - {e}")
            print(f"原始内容: {json_str[:200]}...")
            return None
    
    def save_json(self, json_data: Union[Dict, list], output_path: str):
        """
        保存 JSON 数据到文件
        
        Args:
            json_data: JSON 数据
            output_path: 输出文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    def batch_extract(
        self,
        image_paths: list,
        json_template: Union[str, Dict, list],
        output_dir: str,
        custom_prompt: Optional[str] = None
    ) -> list:
        """
        批量从多张表格图片中提取数据
        
        Args:
            image_paths: 图片文件路径列表
            json_template: JSON 数据模板
            output_dir: 输出目录
            custom_prompt: 自定义提示词
            
        Returns:
            提取结果列表
        """
        results = []
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        for i, image_path in enumerate(image_paths):
            try:
                # 提取数据
                result = self.extract_table_data(image_path, json_template, custom_prompt)
                
                # 生成输出文件名
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                output_path = os.path.join(output_dir, f"{base_name}.json")
                
                # 保存 JSON
                if result["json_data"]:
                    self.save_json(result["json_data"], output_path)
                    
                    results.append({
                        "image_path": image_path,
                        "output_path": output_path,
                        "success": True,
                        "data": result["json_data"]
                    })
                    
                    print(f"✓ 已提取: {image_path} -> {output_path}")
                else:
                    results.append({
                        "image_path": image_path,
                        "output_path": None,
                        "success": False,
                        "error": "JSON 解析失败"
                    })
                    print(f"✗ 提取失败: {image_path} - JSON 解析失败")
                
            except Exception as e:
                results.append({
                    "image_path": image_path,
                    "output_path": None,
                    "success": False,
                    "error": str(e)
                })
                print(f"✗ 提取失败: {image_path}, 错误: {str(e)}")
        
        return results


# 使用示例
if __name__ == "__main__":
    
    # 尝试加载 .env 文件中的环境变量
    try:
        from dotenv import load_dotenv
        # 计算 .env 文件路径（项目根目录）
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
        else:
            # 如果指定路径不存在，尝试加载当前目录的 .env
            load_dotenv()
    except ImportError:
        # 如果没有安装 python-dotenv，使用默认的环境变量
        pass
    
    # 初始化工具类
    extractor = KimiTableToJSON()
    
    # 示例1: 使用字典作为模板
    print("\n" + "="*70)
    print("示例1: 使用字典模板提取数据")
    print("="*70)
    
    # 定义 JSON 模板（与 style1.json 格式一致）
    template = {
        "data": [
            {
                "size": "S",
                "back_length": "42",
                "shoulder_width": "35",
                "bust": "92",
                "hem": "88",
                "sleeve_length": "63"
            }
        ]
    }
    
    # 提取数据（需要实际的图片路径）
    # result = extractor.extract_table_data(
    #     image_path="table_image.jpg",
    #     json_template=template
    # )
    # 
    # if result["json_data"]:
    #     print("提取的数据:")
    #     print(json.dumps(result["json_data"], ensure_ascii=False, indent=2))
    #     
    #     # 保存到文件
    #     extractor.save_json(result["json_data"], "extracted_data.json")
    #     print("\n数据已保存到 extracted_data.json")
    # else:
    #     print("数据提取失败")
    
    # 示例2: 从模板文件读取
    print("\n" + "="*70)
    print("示例2: 从 JSON 模板文件提取数据")
    print("="*70)
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_file = os.path.join(project_root, "table_template", "style2.json")
    
    result = extractor.extract_from_template_file(
        image_path="D:\\data\\comfyui-image\\转换2.png",
        template_file_path=template_file
    )
    
    if result["json_data"]:
        print("提取的数据:")
        print(json.dumps(result["json_data"], ensure_ascii=False, indent=2))
        print(f"\nToken 使用: {result['usage']}")
    
    print("\n提示: 请提供实际的图片路径来测试数据提取功能")
