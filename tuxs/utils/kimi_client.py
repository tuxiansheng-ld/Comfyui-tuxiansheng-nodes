"""
通用 Kimi API 调用工具类
支持自定义图片和 prompt 的灵活调用
"""
import os
import base64
import requests
from typing import Optional, Dict, Any, List, Union


class KimiClient:
    """通用的 Kimi API 调用工具类"""
    
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
            model: 模型名称
                - moonshot-v1-8k (支持 8k 上下文)
                - moonshot-v1-32k (支持 32k 上下文)
                - moonshot-v1-128k (支持 128k 上下文)
                - moonshot-v1-8k-vision-preview (支持视觉功能 8k)
                - moonshot-v1-32k-vision-preview (支持视觉功能 32k)
        """
        self.model = model
    
    def encode_image(self, image_path: str) -> str:
        """
        将图片编码为 base64 格式的 data URL
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            base64 编码的 data URL 格式字符串
        """
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # 获取图片扩展名（去掉点号）
        ext = os.path.splitext(image_path)[1][1:].lower()
        # 如果是 jpg，转换为 jpeg
        if ext == 'jpg':
            ext = 'jpeg'
        
        # 编码为 base64 并构建 data URL
        base64_image = base64.b64encode(image_data).decode('utf-8')
        return f"data:image/{ext};base64,{base64_image}"
    
    def normalize_base64_image(self, image_input: str) -> str:
        """
        规范化图片输入为 data URL 格式
        
        Args:
            image_input: 可以是:
                - 已经是 data URL 格式 (data:image/xxx;base64,xxx)
                - 纯 base64 字符串
                
        Returns:
            data URL 格式的字符串
        """
        # 如果已经是 data URL 格式，直接返回
        if image_input.startswith('data:image'):
            return image_input
        
        # 如果是纯 base64 字符串，添加默认的 data URL 前缀
        # 默认使用 png 格式
        return f"data:image/png;base64,{image_input}"
    
    def chat(
        self,
        prompt: str,
        image_paths: Optional[Union[str, List[str]]] = None,
        image_base64_list: Optional[Union[str, List[str]]] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 4000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        通用的 Kimi API 调用方法，支持文本和图片输入
        
        Args:
            prompt: 用户提示词（必填）
            image_paths: 图片路径，可以是单个路径字符串或路径列表（可选）
            image_base64_list: 图片 base64 编码，可以是单个字符串或列表（可选）
            system_prompt: 系统提示词，定义 AI 的角色和行为（可选）
            temperature: 温度参数，控制输出随机性 (0-1)，越低越确定
            max_tokens: 最大生成 token 数
            **kwargs: 其他 API 参数（如 top_p, n 等）
            
        Returns:
            包含完整响应信息的字典:
            {
                "content": str,  # AI 返回的文本内容
                "raw_response": dict,  # 原始 API 响应
                "usage": dict,  # token 使用情况
                "model": str  # 使用的模型
            }
        """
        # 构建消息列表
        messages = []
        
        # 添加系统提示词
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # 构建用户消息内容
        user_content = []
        
        # 处理图片输入（支持文件路径和 base64 两种方式）
        has_images = False
        
        # 处理文件路径方式的图片
        if image_paths:
            has_images = True
            # 统一处理为列表
            if isinstance(image_paths, str):
                image_paths = [image_paths]
            
            # 添加所有图片
            for image_path in image_paths:
                image_url = self.encode_image(image_path)
                user_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                })
        
        # 处理 base64 方式的图片
        if image_base64_list:
            has_images = True
            # 统一处理为列表
            if isinstance(image_base64_list, str):
                image_base64_list = [image_base64_list]
            
            # 添加所有 base64 图片
            for base64_img in image_base64_list:
                image_url = self.normalize_base64_image(base64_img)
                user_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                })
        
        # 如果有图片，检查是否需要使用视觉模型
        if has_images and 'vision' not in self.model:
            # 自动切换到视觉模型
            original_model = self.model
            if '128k' in self.model:
                self.model = "moonshot-v1-128k-vision-preview"
            elif '32k' in self.model:
                self.model = "moonshot-v1-32k-vision-preview"
            else:
                self.model = "moonshot-v1-8k-vision-preview"
            print(f"检测到图片输入，已自动切换模型: {original_model} -> {self.model}")
        
        # 添加文本提示词
        user_content.append({
            "type": "text",
            "text": prompt
        })
        
        # 添加用户消息
        messages.append({
            "role": "user",
            "content": user_content
        })
        
        # 调用 API
        response = self._call_api(messages, temperature, max_tokens, **kwargs)
        
        # 提取内容
        content = self._extract_content(response)
        
        return {
            "content": content,
            "raw_response": response,
            "usage": response.get("usage", {}),
            "model": response.get("model", self.model)
        }
    
    def chat_text_only(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 4000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        纯文本对话（不包含图片）
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            temperature: 温度参数 (0-1)
            max_tokens: 最大生成 token 数
            **kwargs: 其他 API 参数
            
        Returns:
            响应字典
        """
        return self.chat(
            prompt=prompt,
            image_paths=None,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
    
    def analyze_image(
        self,
        image_path: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 4000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        分析单张图片
        
        Args:
            image_path: 图片路径
            prompt: 分析提示词
            system_prompt: 系统提示词（可选）
            temperature: 温度参数 (0-1)
            max_tokens: 最大生成 token 数
            **kwargs: 其他 API 参数
            
        Returns:
            响应字典
        """
        return self.chat(
            prompt=prompt,
            image_paths=image_path,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
    
    def analyze_image_base64(
        self,
        image_base64: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 4000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        分析单张 base64 编码的图片
        
        Args:
            image_base64: 图片的 base64 编码字符串（可以包含或不包含 data:image 前缀）
            prompt: 分析提示词
            system_prompt: 系统提示词（可选）
            temperature: 温度参数 (0-1)
            max_tokens: 最大生成 token 数
            **kwargs: 其他 API 参数
            
        Returns:
            响应字典
        """
        return self.chat(
            prompt=prompt,
            image_base64_list=image_base64,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
    
    def analyze_images(
        self,
        image_paths: List[str],
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 4000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        分析多张图片
        
        Args:
            image_paths: 图片路径列表
            prompt: 分析提示词
            system_prompt: 系统提示词（可选）
            temperature: 温度参数 (0-1)
            max_tokens: 最大生成 token 数
            **kwargs: 其他 API 参数
            
        Returns:
            响应字典
        """
        return self.chat(
            prompt=prompt,
            image_paths=image_paths,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
    
    def analyze_images_base64(
        self,
        image_base64_list: List[str],
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 4000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        分析多张 base64 编码的图片
        
        Args:
            image_base64_list: 图片 base64 编码字符串列表
            prompt: 分析提示词
            system_prompt: 系统提示词（可选）
            temperature: 温度参数 (0-1)
            max_tokens: 最大生成 token 数
            **kwargs: 其他 API 参数
            
        Returns:
            响应字典
        """
        return self.chat(
            prompt=prompt,
            image_base64_list=image_base64_list,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
    
    def _call_api(
        self, 
        messages: List[Dict],
        temperature: float = 0.3,
        max_tokens: int = 4000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        调用 Kimi API（内部方法）
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大 token 数
            **kwargs: 其他 API 参数
            
        Returns:
            API 响应结果
        """
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs  # 支持传入其他参数
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def _extract_content(self, response: Dict[str, Any]) -> str:
        """
        从 API 响应中提取内容（内部方法）
        
        Args:
            response: API 响应结果
            
        Returns:
            提取的文本内容
        """
        if "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["message"]["content"]
        return ""


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
    
    # 初始化客户端
    client = KimiClient()
    
    # 示例1: 纯文本对话
    print("=" * 50)
    print("示例1: 纯文本对话")
    print("=" * 50)
    result = client.chat_text_only(
        prompt="请简单介绍一下月之暗面公司",
        system_prompt="你是一个专业的AI助手，善于提供准确简洁的信息"
    )
    print(f"回答: {result['content']}\n")
    print(f"Token使用: {result['usage']}\n")
    
    # 示例2: 分析单张图片
    # print("=" * 50)
    # print("示例2: 分析单张图片")
    # print("=" * 50)
    # result = client.analyze_image(
    #     image_path="test_image.jpg",
    #     prompt="请详细描述这张图片中的内容",
    #     system_prompt="你是一个专业的图像分析专家"
    # )
    # print(f"分析结果: {result['content']}\n")
    
    # 示例3: 分析多张图片
    # print("=" * 50)
    # print("示例3: 分析多张图片")
    # print("=" * 50)
    # result = client.analyze_images(
    #     image_paths=["image1.jpg", "image2.jpg"],
    #     prompt="请比较这两张图片的异同点"
    # )
    # print(f"比较结果: {result['content']}\n")
    
    # 示例4: 自定义图片+提示词
    # print("=" * 50)
    # print("示例4: 自定义使用")
    # print("=" * 50)
    # result = client.chat(
    #     prompt="请将这个表格转换为HTML代码",
    #     image_paths="table.jpg",
    #     system_prompt="你是一个专业的前端开发专家",
    #     temperature=0.2,
    #     max_tokens=8000
    # )
    # print(f"生成的代码:\n{result['content']}\n")
