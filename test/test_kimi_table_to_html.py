"""
KimiTableToHTML 工具类单元测试
"""
import unittest
import os
import sys
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock, mock_open
from io import BytesIO

# 添加父目录到路径以便导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载 .env 文件中的环境变量
try:
    from dotenv import load_dotenv
    # 加载项目根目录的 .env 文件
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    load_dotenv(env_path)
except ImportError:
    # 如果没有安装 python-dotenv，使用默认的环境变量
    pass

from utils import KimiTableToHTML


class TestKimiTableToHTML(unittest.TestCase):
    """KimiTableToHTML 工具类测试"""
    
    def setUp(self):
        """测试前准备"""
        self.test_api_key = "test_api_key_12345"
        self.test_image_path = "D:\\data\\comfyui-image\\尺码1.png"
        self.test_file_id = "file_test_123456"
        
    def test_init_with_api_key(self):
        """测试使用 API key 初始化"""
        converter = KimiTableToHTML(api_key=self.test_api_key)
        
        self.assertEqual(converter.api_key, self.test_api_key)
        self.assertEqual(converter.base_url, "https://api.moonshot.cn/v1")
        self.assertEqual(converter.model, "moonshot-v1-8k")
        self.assertIn("Authorization", converter.headers)
        self.assertEqual(converter.headers["Authorization"], f"Bearer {self.test_api_key}")
    
    @patch.dict(os.environ, {"KIMI_API_KEY": "env_api_key"})
    def test_init_with_env_variable(self):
        """测试使用环境变量初始化"""
        converter = KimiTableToHTML()
        self.assertEqual(converter.api_key, "env_api_key")
    
    def test_init_without_api_key(self):
        """测试没有 API key 时抛出异常"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                KimiTableToHTML()
            self.assertIn("API key is required", str(context.exception))
    
    def test_set_model(self):
        """测试设置模型"""
        converter = KimiTableToHTML(api_key=self.test_api_key)
        
        converter.set_model("moonshot-v1-32k")
        self.assertEqual(converter.model, "moonshot-v1-32k")
        
        converter.set_model("moonshot-v1-128k")
        self.assertEqual(converter.model, "moonshot-v1-128k")
    
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_image_data")
    def test_encode_image(self, mock_file):
        """测试图片编码"""
        converter = KimiTableToHTML(api_key=self.test_api_key)
        
        result = converter.encode_image(self.test_image_path)
        
        # 验证文件被正确打开
        mock_file.assert_called_once_with(self.test_image_path, "rb")
        
        # 验证返回的是 base64 字符串
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
    
    @patch("requests.post")
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_image_data")
    def test_upload_image_success(self, mock_file, mock_post):
        """测试图片上传成功"""
        converter = KimiTableToHTML(api_key=self.test_api_key)
        
        # 模拟成功响应
        mock_response = Mock()
        mock_response.json.return_value = {"id": self.test_file_id}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        result = converter.upload_image(self.test_image_path)
        
        # 验证返回文件 ID
        self.assertEqual(result, self.test_file_id)
        
        # 验证 API 调用
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertIn("https://api.moonshot.cn/v1/files", call_args[0])
    
    @patch("requests.post")
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_image_data")
    def test_upload_image_failure(self, mock_file, mock_post):
        """测试图片上传失败"""
        converter = KimiTableToHTML(api_key=self.test_api_key)
        
        # 模拟失败响应
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("Upload failed")
        mock_post.return_value = mock_response
        
        with self.assertRaises(Exception):
            converter.upload_image(self.test_image_path)
    
    def test_extract_html_with_html_block(self):
        """测试从响应中提取 HTML 代码（带 html 标记）"""
        converter = KimiTableToHTML(api_key=self.test_api_key)
        
        response = {
            "choices": [{
                "message": {
                    "content": "这是生成的代码：\n```html\n<table><tr><td>测试</td></tr></table>\n```"
                }
            }]
        }
        
        result = converter._extract_html(response)
        self.assertIn("<table>", result)
        self.assertIn("</table>", result)
    
    def test_extract_html_with_generic_block(self):
        """测试从响应中提取 HTML 代码（通用代码块）"""
        converter = KimiTableToHTML(api_key=self.test_api_key)
        
        response = {
            "choices": [{
                "message": {
                    "content": "```\n<div>测试内容</div>\n```"
                }
            }]
        }
        
        result = converter._extract_html(response)
        self.assertIn("<div>", result)
    
    def test_extract_html_without_block(self):
        """测试从响应中提取 HTML 代码（无代码块）"""
        converter = KimiTableToHTML(api_key=self.test_api_key)
        
        html_content = "<p>直接返回的 HTML</p>"
        response = {
            "choices": [{
                "message": {
                    "content": html_content
                }
            }]
        }
        
        result = converter._extract_html(response)
        self.assertEqual(result, html_content)
    
    def test_extract_html_empty_response(self):
        """测试空响应"""
        converter = KimiTableToHTML(api_key=self.test_api_key)
        
        response = {"choices": []}
        result = converter._extract_html(response)
        self.assertEqual(result, "")
    
    @patch("requests.post")
    def test_call_api_success(self, mock_post):
        """测试 API 调用成功"""
        converter = KimiTableToHTML(api_key=self.test_api_key)
        
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{
                "message": {"content": "test response"}
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        messages = [{"role": "user", "content": "test"}]
        result = converter._call_api(messages)
        
        self.assertIn("choices", result)
        mock_post.assert_called_once()
    
    @patch("builtins.open", new_callable=mock_open)
    def test_save_html(self, mock_file):
        """测试保存 HTML 文件"""
        converter = KimiTableToHTML(api_key=self.test_api_key)
        
        html_code = "<html><body>测试</body></html>"
        output_path = "output_test.html"
        
        converter.save_html(html_code, output_path)
        
        # 验证文件被打开写入
        mock_file.assert_called_once_with(output_path, 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with(html_code)
    
    @patch.object(KimiTableToHTML, 'upload_image')
    @patch.object(KimiTableToHTML, '_call_api')
    def test_table_image_to_html_success(self, mock_call_api, mock_upload):
        """测试表格图片转 HTML 成功"""
        converter = KimiTableToHTML(api_key=self.test_api_key)
        
        # 模拟上传返回
        mock_upload.return_value = self.test_file_id
        
        # 模拟 API 响应
        mock_call_api.return_value = {
            "choices": [{
                "message": {
                    "content": "```html\n<table><tr><td>测试表格</td></tr></table>\n```"
                }
            }]
        }
        
        result = converter.table_image_to_html(self.test_image_path)
        
        # 验证返回结果
        self.assertIn("html_code", result)
        self.assertIn("raw_response", result)
        self.assertIn("file_id", result)
        self.assertEqual(result["file_id"], self.test_file_id)
        self.assertIn("<table>", result["html_code"])
        
        # 验证方法被调用
        mock_upload.assert_called_once_with(self.test_image_path)
        mock_call_api.assert_called_once()
    
    @patch.object(KimiTableToHTML, 'upload_image')
    @patch.object(KimiTableToHTML, '_call_api')
    def test_table_image_to_html_with_custom_prompt(self, mock_call_api, mock_upload):
        """测试使用自定义提示词"""
        converter = KimiTableToHTML(api_key=self.test_api_key)
        
        mock_upload.return_value = self.test_file_id
        mock_call_api.return_value = {
            "choices": [{
                "message": {"content": "<table></table>"}
            }]
        }
        
        custom_prompt = "自定义的提示词内容"
        result = converter.table_image_to_html(
            self.test_image_path,
            custom_prompt=custom_prompt
        )
        
        # 验证自定义提示词被使用
        call_args = mock_call_api.call_args[0][0]
        user_message = call_args[1]
        self.assertEqual(user_message["content"][1]["text"], custom_prompt)
    
    @patch.object(KimiTableToHTML, 'table_image_to_html')
    @patch.object(KimiTableToHTML, 'save_html')
    @patch('os.makedirs')
    def test_batch_convert_success(self, mock_makedirs, mock_save, mock_convert):
        """测试批量转换成功"""
        converter = KimiTableToHTML(api_key=self.test_api_key)
        
        # 模拟转换返回
        mock_convert.return_value = {
            "html_code": "<table></table>",
            "file_id": self.test_file_id
        }
        
        image_paths = ["test1.jpg", "test2.jpg", "test3.jpg"]
        output_dir = "output_test"
        
        results = converter.batch_convert(image_paths, output_dir)
        
        # 验证结果
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertTrue(result["success"])
            self.assertIn("image_path", result)
            self.assertIn("output_path", result)
        
        # 验证目录被创建
        mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)
        
        # 验证每个图片都被处理
        self.assertEqual(mock_convert.call_count, 3)
        self.assertEqual(mock_save.call_count, 3)
    
    @patch.object(KimiTableToHTML, 'table_image_to_html')
    @patch.object(KimiTableToHTML, 'save_html')
    @patch('os.makedirs')
    def test_batch_convert_with_errors(self, mock_makedirs, mock_save, mock_convert):
        """测试批量转换时部分失败"""
        converter = KimiTableToHTML(api_key=self.test_api_key)
        
        # 模拟第二个失败
        def side_effect(image_path, custom_prompt=None):
            if "test2" in image_path:
                raise Exception("转换失败")
            return {
                "html_code": "<table></table>",
                "file_id": self.test_file_id
            }
        
        mock_convert.side_effect = side_effect
        
        image_paths = ["test1.jpg", "test2.jpg", "test3.jpg"]
        output_dir = "output_test"
        
        results = converter.batch_convert(image_paths, output_dir)
        
        # 验证结果
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0]["success"])
        self.assertFalse(results[1]["success"])
        self.assertTrue(results[2]["success"])
        self.assertIn("error", results[1])


class TestKimiTableToHTMLIntegration(unittest.TestCase):
    """集成测试（需要真实 API key 和测试图片）"""
    
    def setUp(self):
        """测试前准备"""
        self.api_key = os.getenv("KIMI_API_KEY")
        self.skip_integration = not self.api_key
        
        if self.skip_integration:
            self.skipTest("需要设置 KIMI_API_KEY 环境变量才能运行集成测试")
    
    def test_real_api_call(self):
        """真实 API 调用测试（需要真实图片）"""
        if self.skip_integration:
            return
        
        # 创建测试图片（简单的表格图片）
        test_image_path = "test_real_table.jpg"
        
        # 如果测试图片不存在，跳过此测试
        if not os.path.exists(test_image_path):
            self.skipTest(f"需要提供测试图片：{test_image_path}")
        
        converter = KimiTableToHTML(api_key=self.api_key)
        
        try:
            result = converter.table_image_to_html(test_image_path)
            
            # 验证返回结果
            self.assertIn("html_code", result)
            self.assertIn("file_id", result)
            self.assertTrue(len(result["html_code"]) > 0)
            
            # 保存测试结果
            output_path = "test_output.html"
            converter.save_html(result["html_code"], output_path)
            
            # 验证文件被创建
            self.assertTrue(os.path.exists(output_path))
            
            # 清理测试文件
            if os.path.exists(output_path):
                os.remove(output_path)
                
        except Exception as e:
            self.fail(f"集成测试失败: {str(e)}")


def run_tests():
    """运行测试套件"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加单元测试
    suite.addTests(loader.loadTestsFromTestCase(TestKimiTableToHTML))
    
    # 添加集成测试（如果设置了环境变量）
    if os.getenv("KIMI_API_KEY"):
        suite.addTests(loader.loadTestsFromTestCase(TestKimiTableToHTMLIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 打印测试总结
    print("\n" + "=" * 70)
    print("测试总结")
    print("=" * 70)
    print(f"运行测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(result.skipped)}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
