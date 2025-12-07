# Kimi 表格转 HTML 工具使用说明

## 功能简介

这是一个使用 Kimi (月之暗面) API 将表格图片转换为 HTML 代码的工具类。

## 安装依赖

```bash
pip install requests
```

## 配置 API Key

有两种方式配置 Kimi API Key：

### 方法 1: 环境变量
```bash
# Windows PowerShell
$env:KIMI_API_KEY="your_api_key_here"

# Windows CMD
set KIMI_API_KEY=your_api_key_here

# Linux/Mac
export KIMI_API_KEY=your_api_key_here
```

### 方法 2: 代码中直接传入
```python
from utils import KimiTableToHTML

converter = KimiTableToHTML(api_key="your_api_key_here")
```

## 使用示例

### 基础使用 - 单个图片转换

```python
from utils import KimiTableToHTML

# 初始化工具类
converter = KimiTableToHTML()

# 转换表格图片为 HTML
result = converter.table_image_to_html("table_image.jpg")

# 保存 HTML 文件
converter.save_html(result["html_code"], "output.html")

print("HTML 代码:")
print(result["html_code"])
```

### 自定义提示词

```python
from utils import KimiTableToHTML

converter = KimiTableToHTML()

# 自定义提示词
custom_prompt = """
请分析这张表格图片，生成 HTML 代码，要求：
1. 使用 Bootstrap 5 样式
2. 添加表格边框和斑马纹
3. 标题行使用深色背景
4. 使表格响应式设计
"""

result = converter.table_image_to_html(
    image_path="table.jpg",
    custom_prompt=custom_prompt,
    temperature=0.3,
    max_tokens=4000
)

converter.save_html(result["html_code"], "styled_table.html")
```

### 批量转换

```python
from utils import KimiTableToHTML

converter = KimiTableToHTML()

# 批量转换多张表格图片
image_list = [
    "table1.jpg",
    "table2.png",
    "table3.jpg"
]

results = converter.batch_convert(
    image_paths=image_list,
    output_dir="output_htmls",
    custom_prompt=None  # 使用默认提示词
)

# 查看转换结果
for r in results:
    if r['success']:
        print(f"✓ {r['image_path']} -> {r['output_path']}")
    else:
        print(f"✗ {r['image_path']} 失败: {r['error']}")
```

### 切换模型版本

```python
from utils import KimiTableToHTML

converter = KimiTableToHTML()

# 使用 32k 版本处理更复杂的表格
converter.set_model("moonshot-v1-32k")

result = converter.table_image_to_html("complex_table.jpg")
```

## API 参数说明

### KimiTableToHTML 类

#### `__init__(api_key=None)`
- **api_key**: Kimi API 密钥，可选。不提供时从环境变量读取。

#### `table_image_to_html(image_path, custom_prompt=None, temperature=0.3, max_tokens=4000)`
- **image_path**: 表格图片路径
- **custom_prompt**: 自定义提示词，控制生成的 HTML 样式和要求
- **temperature**: 温度参数 (0-1)，越低结果越确定，越高越有创造性
- **max_tokens**: 最大生成 token 数

返回值：
```python
{
    "html_code": "生成的 HTML 代码",
    "raw_response": "API 原始响应",
    "file_id": "上传的文件 ID"
}
```

#### `batch_convert(image_paths, output_dir, custom_prompt=None)`
- **image_paths**: 图片路径列表
- **output_dir**: 输出目录
- **custom_prompt**: 自定义提示词

#### `save_html(html_code, output_path)`
- **html_code**: HTML 代码字符串
- **output_path**: 保存路径

## 支持的模型

- `moonshot-v1-8k`: 适合简单到中等复杂度的表格
- `moonshot-v1-32k`: 适合复杂表格
- `moonshot-v1-128k`: 适合超大型复杂表格

## 注意事项

1. 确保有稳定的网络连接
2. API Key 需要有足够的余额
3. 支持的图片格式：jpg, jpeg, png 等常见格式
4. 图片大小建议不超过 10MB
5. 生成的 HTML 代码可能需要根据实际需求微调

## 获取 API Key

访问 [Kimi 开放平台](https://platform.moonshot.cn/) 注册并获取 API Key。

## 故障排查

### 问题 1: `ValueError: API key is required`
**解决方案**: 检查是否正确设置了环境变量或在代码中传入了 API key

### 问题 2: 401 Unauthorized
**解决方案**: 检查 API key 是否正确，是否已过期

### 问题 3: 图片上传失败
**解决方案**: 
- 检查图片路径是否正确
- 检查图片格式是否支持
- 检查图片大小是否超限

## 完整示例代码

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import KimiTableToHTML
import os

def main():
    # 设置 API Key (或通过环境变量)
    api_key = os.getenv("KIMI_API_KEY") or "your_api_key_here"
    
    # 初始化转换器
    converter = KimiTableToHTML(api_key=api_key)
    
    # 单个图片转换
    print("正在转换表格图片...")
    result = converter.table_image_to_html(
        image_path="example_table.jpg",
        temperature=0.3,
        max_tokens=4000
    )
    
    # 保存结果
    output_path = "output_table.html"
    converter.save_html(result["html_code"], output_path)
    print(f"✓ HTML 已保存到: {output_path}")
    
    # 打印生成的 HTML 代码
    print("\n生成的 HTML 代码:")
    print("=" * 50)
    print(result["html_code"])
    print("=" * 50)

if __name__ == "__main__":
    main()
```
