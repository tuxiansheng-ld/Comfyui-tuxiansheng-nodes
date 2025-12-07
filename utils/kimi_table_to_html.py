"""
Kimi API 工具类 - 根据图片表格内容生成 HTML 代码
"""
import os
import json
import base64
import requests
from typing import Optional, Dict, Any


class KimiTableToHTML:
    """使用 Kimi API 将图片表格转换为 HTML 代码的工具类"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 Kimi API 客户端
        
        Args:
            api_key: Kimi API 密钥，如果不提供则从环境变量 KIMI_API_KEY 读取
        """
        self.api_key = api_key or os.getenv("KIMI_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Please provide api_key or set KIMI_API_KEY environment variable.")
        
        self.base_url = "https://api.moonshot.cn/v1"
        self.model = "moonshot-v1-8k"  # 默认使用 8k 版本
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def set_model(self, model: str):
        """
        设置使用的模型版本
        
        Args:
            model: 模型名称 (moonshot-v1-8k, moonshot-v1-32k, moonshot-v1-128k)
        """
        self.model = model
    
    def encode_image(self, image_path: str) -> str:
        """
        将图片编码为 base64 格式
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            base64 编码的图片字符串
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def upload_image(self, image_path: str) -> str:
        """
        上传图片到 Kimi 服务器
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            上传后的文件 ID
        """
        url = f"{self.base_url}/files"
        
        with open(image_path, 'rb') as f:
            files = {
                'file': (os.path.basename(image_path), f, 'image/jpeg')
            }
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
            
        result = response.json()
        return result.get('id')
    
    def table_image_to_html(
        self, 
        image_path: str,
        custom_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 4000
    ) -> Dict[str, Any]:
        """
        将表格图片转换为 HTML 代码
        
        Args:
            image_path: 图片文件路径
            custom_prompt: 自定义提示词，如果不提供则使用默认提示词
            temperature: 温度参数，控制输出随机性 (0-1)
            max_tokens: 最大生成 token 数
            
        Returns:
            包含 HTML 代码和原始响应的字典
        """
        # 上传图片
        file_id = self.upload_image(image_path)
        
        # 构建默认提示词
        if custom_prompt is None:
            custom_prompt = """请仔细分析这张图片中的表格内容，然后生成对应的 HTML 代码。要求：
1. 准确识别表格的行和列结构
2. 保留所有单元格的内容和合并关系
3. 生成规范的 HTML table 代码
4. 添加基本的 CSS 样式使表格美观
5. 确保代码可以直接使用

请只返回完整的 HTML 代码，包含 <style> 标签的样式定义。"""
        
        # 构建请求消息
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的前端开发专家，擅长将表格内容转换为结构化的 HTML 代码。"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"file://{file_id}"
                        }
                    },
                    {
                        "type": "text",
                        "text": custom_prompt
                    }
                ]
            }
        ]
        
        # 调用 Kimi API
        response = self._call_api(messages, temperature, max_tokens)
        
        # 提取 HTML 代码
        html_code = self._extract_html(response)
        
        return {
            "html_code": html_code,
            "raw_response": response,
            "file_id": file_id
        }
    
    def _call_api(
        self, 
        messages: list,
        temperature: float = 0.3,
        max_tokens: int = 4000
    ) -> Dict[str, Any]:
        """
        调用 Kimi API
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大 token 数
            
        Returns:
            API 响应结果
        """
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def _extract_html(self, response: Dict[str, Any]) -> str:
        """
        从 API 响应中提取 HTML 代码
        
        Args:
            response: API 响应结果
            
        Returns:
            提取的 HTML 代码
        """
        if "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
            
            # 尝试提取代码块中的 HTML
            if "```html" in content:
                start = content.find("```html") + 7
                end = content.find("```", start)
                return content[start:end].strip()
            elif "```" in content:
                start = content.find("```") + 3
                end = content.find("```", start)
                return content[start:end].strip()
            else:
                return content.strip()
        
        return ""
    
    def save_html(self, html_code: str, output_path: str):
        """
        保存 HTML 代码到文件
        
        Args:
            html_code: HTML 代码
            output_path: 输出文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_code)
    
    def batch_convert(
        self, 
        image_paths: list,
        output_dir: str,
        custom_prompt: Optional[str] = None
    ) -> list:
        """
        批量转换多张表格图片为 HTML
        
        Args:
            image_paths: 图片文件路径列表
            output_dir: 输出目录
            custom_prompt: 自定义提示词
            
        Returns:
            转换结果列表
        """
        results = []
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        for i, image_path in enumerate(image_paths):
            try:
                # 转换图片
                result = self.table_image_to_html(image_path, custom_prompt)
                
                # 生成输出文件名
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                output_path = os.path.join(output_dir, f"{base_name}.html")
                
                # 保存 HTML
                self.save_html(result["html_code"], output_path)
                
                results.append({
                    "image_path": image_path,
                    "output_path": output_path,
                    "success": True,
                    "file_id": result["file_id"]
                })
                
                print(f"✓ 已转换: {image_path} -> {output_path}")
                
            except Exception as e:
                results.append({
                    "image_path": image_path,
                    "output_path": None,
                    "success": False,
                    "error": str(e)
                })
                print(f"✗ 转换失败: {image_path}, 错误: {str(e)}")
        
        return results


# 使用示例
if __name__ == "__main__":
    # 初始化工具类
    converter = KimiTableToHTML(api_key="your_api_key_here")
    
    # 单个图片转换
    result = converter.table_image_to_html("table_image.jpg")
    converter.save_html(result["html_code"], "output.html")
    print("HTML 代码已生成并保存到 output.html")
    
    # 批量转换
    # images = ["table1.jpg", "table2.jpg", "table3.jpg"]
    # results = converter.batch_convert(images, "output_htmls")
    # print(f"批量转换完成，成功: {sum(r['success'] for r in results)}/{len(results)}")
