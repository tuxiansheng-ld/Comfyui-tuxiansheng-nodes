"""
KimiTableToJSON 工具类的单元测试
测试表格数据提取功能
"""
import os
import sys
import json
import unittest

# 添加父目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from utils.kimi_table_to_json import KimiTableToJSON


class TestKimiTableToJSON(unittest.TestCase):
    """KimiTableToJSON 工具类测试"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        # 检查是否设置了 API Key
        api_key = os.getenv("KIMI_API_KEY")
        if not api_key:
            raise ValueError("请在 .env 文件中设置 KIMI_API_KEY")
        
        cls.extractor = KimiTableToJSON()
        cls.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.template_file = os.path.join(cls.project_root, "table_template", "style1.json")
        
        print("\n" + "=" * 70)
        print("开始测试 KimiTableToJSON 工具类")
        print("=" * 70)
    
    def test_01_init(self):
        """测试初始化"""
        print("\n[测试1] 初始化工具类")
        self.assertIsNotNone(self.extractor)
        self.assertIsNotNone(self.extractor.client)
        print("✓ 工具类初始化成功")
    
    def test_02_template_structure(self):
        """测试 JSON 模板结构"""
        print("\n[测试2] 验证 JSON 模板文件")
        
        self.assertTrue(os.path.exists(self.template_file))
        
        with open(self.template_file, 'r', encoding='utf-8') as f:
            template = json.load(f)
        
        # 验证模板结构
        self.assertIn("data", template)
        self.assertIsInstance(template["data"], list)
        
        if len(template["data"]) > 0:
            first_item = template["data"][0]
            required_fields = ["size", "back_length", "shoulder_width", "bust", "hem", "sleeve_length"]
            for field in required_fields:
                self.assertIn(field, first_item)
        
        print("✓ JSON 模板结构验证通过")
        print(f"  模板路径: {self.template_file}")
    
    def test_03_dict_template(self):
        """测试使用字典模板"""
        print("\n[测试3] 使用字典模板")
        
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
        
        # 验证模板可以正确转换为字符串
        template_str = json.dumps(template, ensure_ascii=False, indent=2)
        self.assertIsInstance(template_str, str)
        self.assertIn("data", template_str)
        
        print("✓ 字典模板格式正确")
    
    # 注意: 以下测试需要实际的图片文件，默认跳过
    # 如需测试，请取消注释并提供真实图片路径
    
    # def test_04_extract_from_image(self):
    #     """测试从实际图片提取数据"""
    #     print("\n[测试4] 从图片提取表格数据")
    #     
    #     image_path = "test_table_image.jpg"  # 替换为实际图片路径
    #     
    #     if not os.path.exists(image_path):
    #         self.skipTest(f"测试图片不存在: {image_path}")
    #     
    #     result = self.extractor.extract_from_template_file(
    #         image_path=image_path,
    #         template_file_path=self.template_file,
    #         temperature=0.1
    #     )
    #     
    #     # 验证返回结构
    #     self.assertIn("json_data", result)
    #     self.assertIn("usage", result)
    #     self.assertIn("image_path", result)
    #     
    #     # 验证提取的数据
    #     if result["json_data"]:
    #         self.assertIn("data", result["json_data"])
    #         print("✓ 数据提取成功")
    #         print(f"  提取的数据: {json.dumps(result['json_data'], ensure_ascii=False, indent=2)}")
    #         print(f"  Token使用: {result['usage']}")
    #     else:
    #         print("✗ 数据提取失败（JSON解析错误）")
    
    # def test_05_save_json(self):
    #     """测试保存 JSON 数据"""
    #     print("\n[测试5] 保存 JSON 数据到文件")
    #     
    #     test_data = {
    #         "data": [
    #             {
    #                 "size": "M",
    #                 "back_length": "43",
    #                 "shoulder_width": "36",
    #                 "bust": "96",
    #                 "hem": "92",
    #                 "sleeve_length": "64.2"
    #             }
    #         ]
    #     }
    #     
    #     output_file = os.path.join(self.project_root, "test_output.json")
    #     
    #     # 保存数据
    #     self.extractor.save_json(test_data, output_file)
    #     
    #     # 验证文件存在
    #     self.assertTrue(os.path.exists(output_file))
    #     
    #     # 验证内容正确
    #     with open(output_file, 'r', encoding='utf-8') as f:
    #         loaded_data = json.load(f)
    #     
    #     self.assertEqual(loaded_data, test_data)
    #     print("✓ JSON 数据保存成功")
    #     
    #     # 清理测试文件
    #     if os.path.exists(output_file):
    #         os.remove(output_file)
    #         print("✓ 测试文件已清理")
    
    def test_06_json_extraction(self):
        """测试 JSON 提取方法"""
        print("\n[测试6] JSON 提取方法测试")
        
        # 测试从代码块提取
        content_with_code_block = """
这是一些说明文字
```json
{
  "data": [
    {
      "size": "L",
      "back_length": "44"
    }
  ]
}
```
其他文字
        """
        
        result = self.extractor._extract_json(content_with_code_block)
        self.assertIsNotNone(result)
        self.assertIn("data", result)
        print("✓ 从代码块提取 JSON 成功")
        
        # 测试直接 JSON
        direct_json = '{"data": [{"size": "XL"}]}'
        result2 = self.extractor._extract_json(direct_json)
        self.assertIsNotNone(result2)
        print("✓ 直接提取 JSON 成功")
    
    @classmethod
    def tearDownClass(cls):
        """测试类清理"""
        print("\n" + "=" * 70)
        print("所有测试完成！")
        print("=" * 70)


if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)
