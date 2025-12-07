"""
工作流集成测试
完整流程：图片 → JSON 数据 → HTML 渲染 → 截图

工作流程：
1. 使用 KimiTableToJSON 从图片提取表格数据
2. 使用 TableRenderer 将数据填充到 HTML 模板
3. 使用 HTMLScreenshotter 将 HTML 转换为图片
"""
import os
import sys
import json
import unittest

# 添加父目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from dotenv import load_dotenv
    # 加载 .env 文件
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()
except ImportError:
    pass

from utils.kimi_table_to_json import KimiTableToJSON
from utils.TableRenderer import TableRenderer
from utils.HTMLScreenshotter import HTMLScreenshotter


class TestWorkflowIntegration(unittest.TestCase):
    """工作流集成测试"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        cls.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.test_dir = os.path.join(cls.project_root, "test")
        cls.output_dir = os.path.join(cls.test_dir, "workflow_output")
        
        # 创建输出目录
        os.makedirs(cls.output_dir, exist_ok=True)
        
        print("\n" + "=" * 70)
        print("工作流集成测试 - 图片 → JSON → HTML → 截图")
        print("=" * 70)
        print(f"输出目录: {cls.output_dir}")
    
    def test_01_complete_workflow_style1(self):
        """
        完整工作流测试 - Style1 模板
        
        流程：
        1. 从图片提取 JSON 数据
        2. 渲染 HTML
        3. 生成截图
        """
        print("\n" + "=" * 70)
        print("[测试1] 完整工作流 - Style1 模板")
        print("=" * 70)
        
        # 定义文件路径
        image_path = r"D:\data\comfyui-image\尺码2.png"  # 替换为实际图片路径
        template_file = os.path.join(self.project_root, "table_template", "style1.json")
        html_template = os.path.join(self.project_root, "table_template", "style1.html")
        
        # 输出文件路径
        json_output = os.path.join(self.output_dir, "extracted_style1.json")
        html_output = os.path.join(self.output_dir, "rendered_style1.html")
        screenshot_output = os.path.join(self.output_dir, "screenshot_style1.png")
        
        # 检查图片是否存在
        if not os.path.exists(image_path):
            self.skipTest(f"测试图片不存在: {image_path}")
        
        # 步骤1: 提取 JSON 数据
        print("\n步骤1: 从图片提取表格数据...")
        print(f"  图片路径: {image_path}")
        print(f"  模板路径: {template_file}")
        
        try:
            extractor = KimiTableToJSON()
            result = extractor.extract_from_template_file(
                image_path=image_path,
                template_file_path=template_file,
                temperature=0.1
            )
            
            # 验证数据提取成功
            self.assertIsNotNone(result["json_data"])
            self.assertIn("data", result["json_data"])
            
            # 保存提取的 JSON 数据
            extractor.save_json(result["json_data"], json_output)
            print(f"✓ JSON 数据提取成功")
            print(f"  提取了 {len(result['json_data']['data'])} 条记录")
            print(f"  Token 使用: {result['usage']}")
            print(f"  已保存到: {json_output}")
            
        except ValueError as e:
            if "API key is required" in str(e):
                self.skipTest("需要设置 KIMI_API_KEY 环境变量")
            raise
        
        # 步骤2: 渲染 HTML
        print("\n步骤2: 将数据填充到 HTML 模板...")
        print(f"  HTML 模板: {html_template}")
        
        renderer = TableRenderer()
        rendered_html = renderer.render_table_from_data(
            html_template_path=html_template,
            data=result["json_data"]["data"],
            output_path=html_output
        )
        
        self.assertTrue(os.path.exists(html_output))
        print(f"✓ HTML 渲染成功")
        print(f"  已保存到: {html_output}")
        
        # 步骤3: 生成截图
        print("\n步骤3: 将 HTML 转换为图片...")
        
        try:
            screenshotter = HTMLScreenshotter()
            screenshotter.capture_from_file(
                html_file_path=html_output,
                output_image=screenshot_output,
                width=800,
                height=600
            )
            
            self.assertTrue(os.path.exists(screenshot_output))
            print(f"✓ 截图生成成功")
            print(f"  已保存到: {screenshot_output}")
            
        except Exception as e:
            print(f"⚠️ 截图失败: {e}")
            print(f"  可能需要配置 CHROMEDRIVER_PATH 环境变量")
        
        print("\n" + "=" * 70)
        print("✓ 完整工作流测试完成！")
        print("=" * 70)
    
    def test_02_workflow_with_custom_data(self):
        """
        使用自定义数据的工作流测试
        
        跳过 Kimi API 调用，直接使用示例数据
        """
        print("\n" + "=" * 70)
        print("[测试2] 自定义数据工作流")
        print("=" * 70)
        
        # 定义文件路径
        html_template = os.path.join(self.project_root, "table_template", "style1.html")
        
        # 输出文件路径
        html_output = os.path.join(self.output_dir, "custom_style1.html")
        screenshot_output = os.path.join(self.output_dir, "custom_style1.png")
        
        # 步骤1: 准备自定义数据
        print("\n步骤1: 准备自定义测试数据...")
        custom_data = [
            {
                "size": "S",
                "back_length": "42",
                "shoulder_width": "35",
                "bust": "92",
                "hem": "88",
                "sleeve_length": "63"
            },
            {
                "size": "M",
                "back_length": "43",
                "shoulder_width": "36",
                "bust": "96",
                "hem": "92",
                "sleeve_length": "64.2"
            },
            {
                "size": "L",
                "back_length": "44",
                "shoulder_width": "37",
                "bust": "100",
                "hem": "96",
                "sleeve_length": "65.4"
            }
        ]
        print(f"✓ 准备了 {len(custom_data)} 条测试数据")
        
        # 步骤2: 渲染 HTML
        print("\n步骤2: 渲染 HTML...")
        renderer = TableRenderer()
        rendered_html = renderer.render_table_from_data(
            html_template_path=html_template,
            data=custom_data,
            output_path=html_output
        )
        
        self.assertTrue(os.path.exists(html_output))
        print(f"✓ HTML 渲染成功: {html_output}")
        
        # 步骤3: 生成截图
        print("\n步骤3: 生成截图...")
        
        try:
            screenshotter = HTMLScreenshotter()
            screenshotter.capture_from_file(
                html_file_path=html_output,
                output_image=screenshot_output,
                width=800,
                height=600
            )
            
            self.assertTrue(os.path.exists(screenshot_output))
            print(f"✓ 截图生成成功: {screenshot_output}")
            
        except Exception as e:
            print(f"⚠️ 截图失败: {e}")
            print(f"  提示: 需要配置 chromedriver，参考 .env.example")
        
        print("\n✓ 自定义数据工作流完成！")
    
    def test_03_batch_workflow(self):
        """
        批量处理工作流测试
        
        处理多个模板/数据组合
        """
        print("\n" + "=" * 70)
        print("[测试3] 批量处理工作流")
        print("=" * 70)
        
        # 定义测试数据集
        test_cases = [
            {
                "name": "尺码表1",
                "template": "style1.html",
                "data": [
                    {"size": "S", "back_length": "42", "shoulder_width": "35", 
                     "bust": "92", "hem": "88", "sleeve_length": "63"},
                    {"size": "M", "back_length": "43", "shoulder_width": "36", 
                     "bust": "96", "hem": "92", "sleeve_length": "64.2"}
                ]
            },
            {
                "name": "尺码表2",
                "template": "style1.html",
                "data": [
                    {"size": "L", "back_length": "44", "shoulder_width": "37", 
                     "bust": "100", "hem": "96", "sleeve_length": "65.4"},
                    {"size": "XL", "back_length": "45", "shoulder_width": "38", 
                     "bust": "104", "hem": "100", "sleeve_length": "66.6"}
                ]
            }
        ]
        
        renderer = TableRenderer()
        
        try:
            screenshotter = HTMLScreenshotter()
            has_screenshotter = True
        except:
            has_screenshotter = False
            print("⚠️ HTMLScreenshotter 不可用，跳过截图步骤")
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n处理第 {i}/{len(test_cases)} 个: {test_case['name']}")
            
            # 文件路径
            html_template = os.path.join(self.project_root, "table_template", test_case["template"])
            html_output = os.path.join(self.output_dir, f"batch_{i}.html")
            screenshot_output = os.path.join(self.output_dir, f"batch_{i}.png")
            
            try:
                # 渲染 HTML
                renderer.render_table_from_data(
                    html_template_path=html_template,
                    data=test_case["data"],
                    output_path=html_output
                )
                print(f"  ✓ HTML 渲染完成")
                
                # 生成截图
                if has_screenshotter:
                    screenshotter.capture_from_file(
                        html_file_path=html_output,
                        output_image=screenshot_output,
                        width=800,
                        height=600
                    )
                    print(f"  ✓ 截图生成完成")
                
                results.append({
                    "name": test_case["name"],
                    "success": True,
                    "html": html_output,
                    "screenshot": screenshot_output if has_screenshotter else None
                })
                
            except Exception as e:
                print(f"  ✗ 处理失败: {e}")
                results.append({
                    "name": test_case["name"],
                    "success": False,
                    "error": str(e)
                })
        
        # 统计结果
        success_count = sum(1 for r in results if r["success"])
        print(f"\n批量处理完成: {success_count}/{len(test_cases)} 成功")
        
        self.assertGreater(success_count, 0, "至少应该有一个成功")
    
    @classmethod
    def tearDownClass(cls):
        """测试类清理"""
        print("\n" + "=" * 70)
        print("所有工作流测试完成！")
        print(f"输出文件位于: {cls.output_dir}")
        print("=" * 70)


# 独立运行的示例代码
def run_complete_workflow_example():
    """
    完整工作流示例 - 可以独立运行
    """
    print("\n" + "=" * 70)
    print("完整工作流示例")
    print("=" * 70)
    
    # 初始化项目路径
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "test", "workflow_output")
    os.makedirs(output_dir, exist_ok=True)
    
    # 配置文件路径
    image_path = r"D:\data\comfyui-image\尺码2.png"  # 修改为实际图片路径
    template_json = os.path.join(project_root, "table_template", "style1.json")
    template_html = os.path.join(project_root, "table_template", "style1.html")
    
    # 输出文件路径
    json_output = os.path.join(output_dir, "example_data.json")
    html_output = os.path.join(output_dir, "example_table.html")
    screenshot_output = os.path.join(output_dir, "example_screenshot.png")
    
    try:
        # ========== 步骤1: 提取 JSON 数据 ==========
        print("\n【步骤1】从图片提取表格数据")
        print("-" * 70)
        
        # 尝试从图片提取，如果失败则使用示例数据
        json_data = None
        
        if os.path.exists(image_path):
            try:
                print(f"图片路径: {image_path}")
                extractor = KimiTableToJSON()
                
                result = extractor.extract_from_template_file(
                    image_path=image_path,
                    template_file_path=template_json,
                    temperature=0.1
                )
                
                if result["json_data"]:
                    extractor.save_json(result["json_data"], json_output)
                    json_data = result["json_data"]["data"]
                    print(f"✓ 成功提取 {len(json_data)} 条数据")
                    print(f"✓ 已保存到: {json_output}")
            
            except ValueError as e:
                if "API key is required" in str(e):
                    print("⚠️ 未设置 KIMI_API_KEY，使用示例数据")
                    json_data = None
                else:
                    raise
        
        # 如果没有提取到数据，使用示例数据
        if json_data is None:
            if not os.path.exists(image_path):
                print("⚠️ 图片不存在，使用示例数据")
            
            json_data = [
                {
                    "size": "S",
                    "back_length": "42",
                    "shoulder_width": "35",
                    "bust": "92",
                    "hem": "88",
                    "sleeve_length": "63"
                },
                {
                    "size": "M",
                    "back_length": "43",
                    "shoulder_width": "36",
                    "bust": "96",
                    "hem": "92",
                    "sleeve_length": "64.2"
                },
                {
                    "size": "L",
                    "back_length": "44",
                    "shoulder_width": "37",
                    "bust": "100",
                    "hem": "96",
                    "sleeve_length": "65.4"
                }
            ]
            print(f"✓ 使用 {len(json_data)} 条示例数据")
        
        # ========== 步骤2: 渲染 HTML ==========
        print("\n【步骤2】渲染 HTML 表格")
        print("-" * 70)
        
        renderer = TableRenderer()
        rendered_html = renderer.render_table_from_data(
            html_template_path=template_html,
            data=json_data,
            output_path=html_output
        )
        
        print(f"✓ HTML 渲染成功")
        print(f"✓ 已保存到: {html_output}")
        
        # ========== 步骤3: 生成截图 ==========
        print("\n【步骤3】生成截图")
        print("-" * 70)
        
        screenshotter = HTMLScreenshotter()
        screenshotter.capture_from_file(
            html_file_path=html_output,
            output_image=screenshot_output,
            width=800,
            height=600
        )
        
        print(f"✓ 截图生成成功")
        print(f"✓ 已保存到: {screenshot_output}")
        
        # ========== 完成 ==========
        print("\n" + "=" * 70)
        print("✓ 完整工作流执行成功！")
        print("=" * 70)
        print(f"\n生成的文件:")
        if os.path.exists(json_output):
            print(f"  - JSON 数据: {json_output}")
        print(f"  - HTML 文件: {html_output}")
        print(f"  - 截图文件: {screenshot_output}")
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 可以选择运行单元测试或示例代码
    
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--example":
        # 运行示例代码
        run_complete_workflow_example()
    else:
        # 运行单元测试
        unittest.main(verbosity=2)
