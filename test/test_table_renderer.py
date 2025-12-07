"""
TableRenderer 工具类的单元测试
测试表格数据填充功能
"""
import os
import sys
import unittest

# 添加父目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.TableRenderer import TableRenderer


class TestTableRenderer(unittest.TestCase):
    """TableRenderer 工具类测试"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        cls.renderer = TableRenderer()
        cls.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.html_template = os.path.join(cls.project_root, "table_template", "style1.html")
        cls.json_data = os.path.join(cls.project_root, "table_template", "style1.json")
        
        print("\n" + "=" * 70)
        print("开始测试 TableRenderer 工具类")
        print("=" * 70)
    
    def test_01_validate_json(self):
        """测试 JSON 数据验证"""
        print("\n[测试1] 验证 JSON 数据格式")
        
        result = self.renderer.validate_json_data(self.json_data)
        self.assertTrue(result)
        print("✓ JSON 数据格式验证通过")
    
    def test_02_render_from_files(self):
        """测试从文件读取并渲染"""
        print("\n[测试2] 从 HTML 模板和 JSON 数据生成表格")
        
        output_file = os.path.join(self.project_root, "test_output_table.html")
        
        # 渲染表格
        result_html = self.renderer.render_table(
            self.html_template,
            self.json_data,
            output_file
        )
        
        # 验证输出
        self.assertIsNotNone(result_html)
        self.assertTrue(len(result_html) > 0)
        self.assertTrue(os.path.exists(output_file))
        
        print(f"✓ 成功生成表格文件: {output_file}")
        
        # 验证内容
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # 检查是否包含数据
            self.assertIn('S', content)
            self.assertIn('M', content)
            self.assertIn('L', content)
            self.assertIn('42', content)
            self.assertIn('43', content)
            self.assertIn('44', content)
        
        print("✓ 表格数据填充正确")
        
        # 清理测试文件
        if os.path.exists(output_file):
            os.remove(output_file)
            print("✓ 测试文件已清理")
    
    def test_03_render_from_data_dict(self):
        """测试从数据字典渲染"""
        print("\n[测试3] 使用数据字典生成表格")
        
        # 自定义数据
        custom_data = [
            {
                "size": "XL",
                "back_length": "45",
                "shoulder_width": "38",
                "bust": "104",
                "hem": "100",
                "sleeve_length": "66.6"
            },
            {
                "size": "XXL",
                "back_length": "46",
                "shoulder_width": "39",
                "bust": "108",
                "hem": "104",
                "sleeve_length": "67.8"
            }
        ]
        
        output_file = os.path.join(self.project_root, "test_output_custom.html")
        
        # 渲染表格
        result_html = self.renderer.render_table_from_data(
            self.html_template,
            custom_data,
            output_file
        )
        
        # 验证输出
        self.assertIsNotNone(result_html)
        self.assertTrue(os.path.exists(output_file))
        
        print(f"✓ 成功生成自定义表格文件: {output_file}")
        
        # 验证内容
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('XL', content)
            self.assertIn('XXL', content)
            self.assertIn('45', content)
            self.assertIn('46', content)
        
        print("✓ 自定义数据填充正确")
        
        # 清理测试文件
        if os.path.exists(output_file):
            os.remove(output_file)
            print("✓ 测试文件已清理")
    
    def test_04_render_without_output(self):
        """测试不保存文件，只返回 HTML 字符串"""
        print("\n[测试4] 只返回 HTML 字符串（不保存文件）")
        
        # 渲染但不保存
        result_html = self.renderer.render_table(
            self.html_template,
            self.json_data,
            output_path=None
        )
        
        # 验证返回的 HTML
        self.assertIsNotNone(result_html)
        self.assertTrue(len(result_html) > 0)
        self.assertIn('SIZE 尺码信息', result_html)
        self.assertIn('S', result_html)
        self.assertIn('M', result_html)
        self.assertIn('L', result_html)
        
        print("✓ 成功返回 HTML 字符串")
        print(f"  HTML 长度: {len(result_html)} 字符")
    
    def test_05_error_handling(self):
        """测试错误处理"""
        print("\n[测试5] 错误处理测试")
        
        # 测试不存在的文件
        try:
            self.renderer.render_table("nonexistent.html", self.json_data)
            self.fail("应该抛出异常")
        except FileNotFoundError:
            print("✓ 正确处理了不存在的模板文件")
        
        # 测试无效的 JSON 数据
        invalid_json = os.path.join(self.project_root, "test_invalid.json")
        with open(invalid_json, 'w', encoding='utf-8') as f:
            f.write('{"invalid": "data"}')
        
        result = self.renderer.validate_json_data(invalid_json)
        self.assertFalse(result)
        print("✓ 正确检测了无效的 JSON 格式")
        
        # 清理测试文件
        if os.path.exists(invalid_json):
            os.remove(invalid_json)
    
    @classmethod
    def tearDownClass(cls):
        """测试类清理"""
        print("\n" + "=" * 70)
        print("所有测试完成！")
        print("=" * 70)


if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)
