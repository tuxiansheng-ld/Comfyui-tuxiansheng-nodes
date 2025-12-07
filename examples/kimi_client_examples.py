"""
KimiClient 使用示例集合
演示各种常见使用场景
"""
import os
import sys

# 添加父目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from utils.kimi_client import KimiClient


def example_1_simple_chat():
    """示例1: 简单的文本对话"""
    print("\n" + "="*70)
    print("示例1: 简单的文本对话")
    print("="*70)
    
    client = KimiClient()
    
    result = client.chat_text_only(
        prompt="请用一句话解释什么是机器学习",
        system_prompt="你是一个专业的AI教育者，善于用简单的语言解释复杂概念"
    )
    
    print(f"问题: 请用一句话解释什么是机器学习")
    print(f"回答: {result['content']}")
    print(f"Token使用: {result['usage']}")


def example_2_creative_writing():
    """示例2: 创意写作（高温度）"""
    print("\n" + "="*70)
    print("示例2: 创意写作（高温度）")
    print("="*70)
    
    client = KimiClient()
    
    result = client.chat(
        prompt="写一首关于代码之美的现代诗",
        system_prompt="你是一个富有诗意的程序员诗人",
        temperature=0.9,  # 高温度提高创造性
        max_tokens=500
    )
    
    print(f"生成的诗:")
    print(result['content'])
    print(f"\nToken使用: {result['usage']}")


def example_3_data_extraction():
    """示例3: 数据提取（低温度）"""
    print("\n" + "="*70)
    print("示例3: 数据提取（低温度）")
    print("="*70)
    
    client = KimiClient()
    
    text = """
    联系人：张三
    电话：13800138000
    邮箱：zhangsan@example.com
    地址：北京市朝阳区某某街道123号
    """
    
    result = client.chat(
        prompt=f"请从以下文本中提取联系信息，以JSON格式返回：\n{text}",
        system_prompt="你是一个专业的数据提取助手",
        temperature=0.1,  # 低温度保证准确性
    )
    
    print(f"原始文本:\n{text}")
    print(f"\n提取结果:")
    print(result['content'])


def example_4_code_generation():
    """示例4: 代码生成"""
    print("\n" + "="*70)
    print("示例4: 代码生成")
    print("="*70)
    
    client = KimiClient()
    
    result = client.chat(
        prompt="请写一个Python函数，实现二分查找算法",
        system_prompt="你是一个专业的Python开发专家，代码要清晰、有注释",
        temperature=0.2,
        max_tokens=1000
    )
    
    print(f"生成的代码:")
    print(result['content'])


def example_5_model_switching():
    """示例5: 模型切换"""
    print("\n" + "="*70)
    print("示例5: 模型切换")
    print("="*70)
    
    client = KimiClient()
    
    # 使用默认 8k 模型
    print(f"当前模型: {client.model}")
    
    # 切换到 32k 模型处理长文本
    client.set_model("moonshot-v1-32k")
    print(f"切换后模型: {client.model}")
    
    result = client.chat_text_only(
        prompt="请写一篇1000字的文章，主题是人工智能的未来发展",
        max_tokens=5000
    )
    
    print(f"\n文章长度: {len(result['content'])} 字符")
    print(f"Token使用: {result['usage']}")


def example_6_analyze_image():
    """示例6: 分析图片（需要实际图片）"""
    print("\n" + "="*70)
    print("示例6: 分析图片")
    print("="*70)
    
    # 注意: 此示例需要实际的图片文件
    image_path = "test_image.jpg"
    
    if not os.path.exists(image_path):
        print(f"⚠️  图片不存在: {image_path}")
        print("请提供实际图片路径后再运行此示例")
        return
    
    client = KimiClient()
    
    result = client.analyze_image(
        image_path=image_path,
        prompt="请详细描述这张图片的内容，包括场景、物体、颜色等",
        system_prompt="你是一个专业的图像分析专家"
    )
    
    print(f"图片路径: {image_path}")
    print(f"分析结果:\n{result['content']}")
    print(f"使用模型: {result['model']}")


def example_7_table_to_html():
    """示例7: 表格图片转HTML（需要实际图片）"""
    print("\n" + "="*70)
    print("示例7: 表格图片转HTML")
    print("="*70)
    
    # 注意: 此示例需要实际的表格图片
    table_image = "table.jpg"
    
    if not os.path.exists(table_image):
        print(f"⚠️  表格图片不存在: {table_image}")
        print("请提供实际表格图片路径后再运行此示例")
        return
    
    client = KimiClient()
    
    result = client.chat(
        prompt="""请将这个表格转换为HTML代码，要求：
        1. 准确识别表格结构
        2. 保留所有单元格内容
        3. 添加美观的CSS样式
        4. 代码规范易读""",
        image_paths=table_image,
        system_prompt="你是一个专业的前端开发专家",
        temperature=0.2,
        max_tokens=8000
    )
    
    # 保存 HTML 文件
    output_path = "output_table.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result['content'])
    
    print(f"表格图片: {table_image}")
    print(f"HTML已保存到: {output_path}")
    print(f"Token使用: {result['usage']}")


def example_8_compare_images():
    """示例8: 比较多张图片（需要实际图片）"""
    print("\n" + "="*70)
    print("示例8: 比较多张图片")
    print("="*70)
    
    # 注意: 此示例需要实际的图片文件
    image_paths = ["design_v1.png", "design_v2.png"]
    
    for path in image_paths:
        if not os.path.exists(path):
            print(f"⚠️  图片不存在: {path}")
            print("请提供实际图片路径后再运行此示例")
            return
    
    client = KimiClient()
    
    result = client.analyze_images(
        image_paths=image_paths,
        prompt="请比较这两个设计方案的优缺点，并给出改进建议",
        system_prompt="你是一个专业的UI/UX设计专家"
    )
    
    print(f"比较的图片: {', '.join(image_paths)}")
    print(f"比较结果:\n{result['content']}")


def main():
    """运行所有示例"""
    print("\n")
    print("*" * 70)
    print("  KimiClient 使用示例集合")
    print("*" * 70)
    
    try:
        # 运行不需要图片的示例
        example_1_simple_chat()
        example_2_creative_writing()
        example_3_data_extraction()
        example_4_code_generation()
        example_5_model_switching()
        
        # 需要图片的示例（默认跳过）
        # 取消下面的注释并提供实际图片路径后运行
        # example_6_analyze_image()
        # example_7_table_to_html()
        # example_8_compare_images()
        
        print("\n" + "="*70)
        print("✓ 所有示例运行完成！")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
