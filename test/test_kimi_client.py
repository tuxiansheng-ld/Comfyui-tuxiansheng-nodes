"""
KimiClient 工具类的单元测试
测试通用 Kimi API 调用功能
"""
import os
import sys
import unittest

# 添加父目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from utils.kimi_client import KimiClient


class TestKimiClient(unittest.TestCase):
    """KimiClient 工具类测试"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        # 检查是否设置了 API Key
        api_key = os.getenv("KIMI_API_KEY")
        if not api_key:
            raise ValueError("请在 .env 文件中设置 KIMI_API_KEY")
        
        cls.client = KimiClient()
        print("\n" + "=" * 70)
        print("开始测试 KimiClient 工具类")
        print("=" * 70)
    
    def test_01_init(self):
        """测试初始化"""
        print("\n[测试1] 初始化客户端")
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.client.api_key)
        print(f"✓ 客户端初始化成功，默认模型: {self.client.model}")
    
    def test_02_set_model(self):
        """测试设置模型"""
        print("\n[测试2] 设置模型")
        original_model = self.client.model
        self.client.set_model("moonshot-v1-32k")
        self.assertEqual(self.client.model, "moonshot-v1-32k")
        print(f"✓ 模型切换成功: {original_model} -> {self.client.model}")
        # 恢复默认模型
        self.client.set_model("moonshot-v1-8k")
    
    def test_03_chat_text_only(self):
        """测试纯文本对话"""
        print("\n[测试3] 纯文本对话")
        result = self.client.chat_text_only(
            prompt="请用一句话介绍月之暗面公司",
            system_prompt="你是一个专业的AI助手，回答要简洁",
            temperature=0.3
        )
        
        self.assertIn("content", result)
        self.assertIsInstance(result["content"], str)
        self.assertTrue(len(result["content"]) > 0)
        
        print(f"✓ 文本对话成功")
        print(f"  提示词: '请用一句话介绍月之暗面公司'")
        print(f"  回答: {result['content'][:100]}...")
        print(f"  Token使用: {result['usage']}")
    
    def test_04_chat_with_custom_params(self):
        """测试自定义参数"""
        print("\n[测试4] 自定义参数调用")
        result = self.client.chat(
            prompt="写一首关于AI的七言绝句",
            temperature=0.8,  # 提高创造性
            max_tokens=200
        )
        
        self.assertIn("content", result)
        print(f"✓ 自定义参数调用成功")
        print(f"  生成的诗:\n{result['content']}")
    
    # 注意: 以下测试需要实际的图片文件，默认跳过
    # 如需测试图片功能，请取消注释并提供真实图片路径
    
    # def test_05_analyze_image(self):
    #     """测试单张图片分析"""
    #     print("\n[测试5] 单张图片分析")
    #     image_path = "test_image.jpg"  # 替换为实际图片路径
    #     
    #     if not os.path.exists(image_path):
    #         self.skipTest(f"测试图片不存在: {image_path}")
    #     
    #     result = self.client.analyze_image(
    #         image_path=image_path,
    #         prompt="请描述这张图片的内容",
    #         system_prompt="你是一个专业的图像分析专家"
    #     )
    #     
    #     self.assertIn("content", result)
    #     print(f"✓ 图片分析成功")
    #     print(f"  分析结果: {result['content'][:200]}...")
    
    # def test_06_analyze_images(self):
    #     """测试多张图片分析"""
    #     print("\n[测试6] 多张图片分析")
    #     image_paths = ["image1.jpg", "image2.jpg"]  # 替换为实际图片路径
    #     
    #     for path in image_paths:
    #         if not os.path.exists(path):
    #             self.skipTest(f"测试图片不存在: {path}")
    #     
    #     result = self.client.analyze_images(
    #         image_paths=image_paths,
    #         prompt="请比较这两张图片的异同"
    #     )
    #     
    #     self.assertIn("content", result)
    #     print(f"✓ 多图片分析成功")
    #     print(f"  比较结果: {result['content'][:200]}...")
    
    def test_07_error_handling(self):
        """测试错误处理"""
        print("\n[测试7] 错误处理")
        
        # 测试无效的 API Key
        try:
            invalid_client = KimiClient(api_key="invalid_key")
            invalid_client.chat_text_only("测试")
            self.fail("应该抛出异常")
        except Exception as e:
            print(f"✓ 正确处理了无效API Key: {type(e).__name__}")
    
    @classmethod
    def tearDownClass(cls):
        """测试类清理"""
        print("\n" + "=" * 70)
        print("所有测试完成！")
        print("=" * 70)


if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)
