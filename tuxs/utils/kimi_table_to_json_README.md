# KimiTableToJSON - 表格图片数据提取工具

一个智能的工具类，使用 Kimi API 根据 JSON 模板从图片表格中提取结构化数据。

## 核心功能

- ✅ 根据 JSON 模板从图片提取表格数据
- ✅ 支持自定义 JSON 数据结构
- ✅ 支持从模板文件读取
- ✅ 自动解析 Kimi 返回的 JSON 数据
- ✅ 批量提取多张图片
- ✅ 保存提取结果为 JSON 文件

## 工作原理

```
图片 + JSON模板 → Kimi API → 结构化JSON数据
```

1. 提供一张表格图片
2. 提供 JSON 数据模板（定义数据结构）
3. Kimi 分析图片并按照模板提取数据
4. 返回结构化的 JSON 数据

## 快速开始

### 1. 安装依赖

已包含在 `requirements.txt` 中：
```bash
pip install requests python-dotenv
```

### 2. 配置 API Key

在 `.env` 文件中配置：
```env
KIMI_API_KEY=your_api_key_here
```

### 3. 基本使用

```python
from utils.kimi_table_to_json import KimiTableToJSON

# 初始化工具类
extractor = KimiTableToJSON()

# 定义 JSON 模板
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

# 提取数据
result = extractor.extract_table_data(
    image_path="table_image.jpg",
    json_template=template
)

# 获取提取的数据
if result["json_data"]:
    print(result["json_data"])
    # 保存到文件
    extractor.save_json(result["json_data"], "output.json")
```

## 使用示例

### 示例 1: 使用字典模板

```python
from utils.kimi_table_to_json import KimiTableToJSON

extractor = KimiTableToJSON()

# 定义模板
template = {
    "data": [
        {
            "size": "",
            "back_length": "",
            "shoulder_width": "",
            "bust": "",
            "hem": "",
            "sleeve_length": ""
        }
    ]
}

# 提取数据
result = extractor.extract_table_data(
    image_path="size_chart.jpg",
    json_template=template,
    temperature=0.1  # 低温度保证准确性
)

# 打印结果
print(json.dumps(result["json_data"], ensure_ascii=False, indent=2))
print(f"Token 使用: {result['usage']}")
```

### 示例 2: 从模板文件读取

```python
# JSON 模板文件: template.json
# {
#   "data": [
#     {
#       "size": "S",
#       "back_length": "42",
#       "shoulder_width": "35"
#     }
#   ]
# }

extractor = KimiTableToJSON()

# 从文件读取模板并提取
result = extractor.extract_from_template_file(
    image_path="table.jpg",
    template_file_path="template.json"
)

if result["json_data"]:
    # 保存结果
    extractor.save_json(result["json_data"], "extracted_data.json")
    print("数据提取成功！")
```

### 示例 3: 批量提取

```python
extractor = KimiTableToJSON()

# 模板
template = {
    "data": [{"size": "", "length": "", "width": ""}]
}

# 批量提取
image_list = ["table1.jpg", "table2.jpg", "table3.jpg"]
results = extractor.batch_extract(
    image_paths=image_list,
    json_template=template,
    output_dir="extracted_data"
)

# 统计结果
success_count = sum(1 for r in results if r["success"])
print(f"成功提取: {success_count}/{len(results)}")
```

### 示例 4: 自定义提示词

```python
extractor = KimiTableToJSON()

template = {"data": [{"name": "", "value": ""}]}

custom_prompt = """
请提取图片中的表格数据，要求：
1. 准确识别每一行的名称和数值
2. 如果数值包含单位，保留单位
3. 按照从上到下的顺序提取

按照以下 JSON 格式返回：
{template}
"""

result = extractor.extract_table_data(
    image_path="data_table.jpg",
    json_template=template,
    custom_prompt=custom_prompt,
    temperature=0.05  # 更低的温度
)
```

## API 文档

### KimiTableToJSON 类

#### 初始化

```python
extractor = KimiTableToJSON(api_key: Optional[str] = None)
```

**参数：**
- `api_key`: Kimi API 密钥（可选）。如果不提供，从环境变量 `KIMI_API_KEY` 读取

#### 主要方法

##### 1. `extract_table_data()` - 提取表格数据

```python
result = extractor.extract_table_data(
    image_path: str,                           # 图片路径（必填）
    json_template: Union[str, Dict, list],     # JSON 模板（必填）
    custom_prompt: Optional[str] = None,       # 自定义提示词
    temperature: float = 0.1,                  # 温度参数 (0-1)
    max_tokens: int = 4000                     # 最大token数
)
```

**参数：**
- `image_path`: 图片文件路径
- `json_template`: JSON 模板，可以是：
  - 字符串：JSON 格式字符串
  - 字典：Python dict 对象
  - 列表：Python list 对象
- `custom_prompt`: 自定义提示词（可选）
- `temperature`: 温度参数，建议 0.05-0.2（低温度保证准确性）
- `max_tokens`: 最大生成 token 数

**返回值：**
```python
{
    "json_data": dict/list,      # 提取的 JSON 数据
    "raw_content": str,          # Kimi 返回的原始文本
    "raw_response": dict,        # 完整的 API 响应
    "image_path": str,           # 图片路径
    "usage": dict                # Token 使用情况
}
```

##### 2. `extract_from_template_file()` - 从模板文件提取

```python
result = extractor.extract_from_template_file(
    image_path: str,              # 图片路径
    template_file_path: str,      # 模板文件路径
    custom_prompt: Optional[str] = None,
    temperature: float = 0.1,
    max_tokens: int = 4000
)
```

**参数：**
- `template_file_path`: JSON 模板文件的路径
- 其他参数同 `extract_table_data()`

##### 3. `batch_extract()` - 批量提取

```python
results = extractor.batch_extract(
    image_paths: list,             # 图片路径列表
    json_template: Union[str, Dict, list],  # JSON 模板
    output_dir: str,               # 输出目录
    custom_prompt: Optional[str] = None
)
```

**返回值：** 结果列表
```python
[
    {
        "image_path": str,
        "output_path": str,
        "success": bool,
        "data": dict/list
    }
]
```

##### 4. `save_json()` - 保存 JSON 数据

```python
extractor.save_json(
    json_data: Union[Dict, list],  # JSON 数据
    output_path: str               # 输出文件路径
)
```

##### 5. `set_model()` - 设置模型

```python
extractor.set_model(model: str)
```

**支持的模型：**
- `moonshot-v1-8k-vision-preview` (默认)
- `moonshot-v1-32k-vision-preview`

## JSON 模板设计

### 基本原则

1. **结构清晰**：模板应该清晰地反映数据结构
2. **字段完整**：包含所有需要提取的字段
3. **示例数据**：提供一条示例数据帮助 Kimi 理解

### 模板示例

#### 尺码表模板
```json
{
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
```

#### 产品参数模板
```json
{
  "product": {
    "name": "产品名称",
    "model": "型号",
    "specifications": [
      {
        "param_name": "参数名",
        "param_value": "参数值"
      }
    ]
  }
}
```

#### 价格表模板
```json
{
  "price_list": [
    {
      "item": "项目名称",
      "unit": "单位",
      "price": "价格",
      "remark": "备注"
    }
  ]
}
```

## 参数调优

### temperature（温度）

**推荐值：** 0.05 - 0.2

- **0.05-0.1**: 极高准确性，适合数据提取（推荐）
- **0.1-0.2**: 平衡准确性和灵活性
- **0.2+**: 不推荐用于数据提取

```python
# 高精度提取
result = extractor.extract_table_data(
    image_path="table.jpg",
    json_template=template,
    temperature=0.05  # 极低温度
)
```

### max_tokens

根据表格复杂度设置：
- 简单表格（5行以内）：1000-2000
- 中等表格（5-20行）：2000-4000
- 复杂表格（20行以上）：4000-8000

## 最佳实践

### 1. 模板设计

✅ **推荐做法：**
```json
{
  "data": [
    {
      "size": "S",           // 提供示例值
      "length": "42"
    }
  ]
}
```

❌ **不推荐：**
```json
{
  "data": [
    {
      "size": "",            // 空字符串不够明确
      "length": ""
    }
  ]
}
```

### 2. 图片质量

- ✅ 使用清晰的图片（推荐 1000px 以上）
- ✅ 确保表格完整可见
- ✅ 避免过度倾斜或变形
- ✅ 充足的光线和对比度

### 3. 错误处理

```python
result = extractor.extract_table_data(image_path, template)

if result["json_data"]:
    # 成功提取
    data = result["json_data"]
    extractor.save_json(data, "output.json")
else:
    # 提取失败
    print("数据提取失败，请检查：")
    print("1. 图片是否清晰")
    print("2. JSON 模板是否正确")
    print("3. Kimi 返回内容:", result["raw_content"][:200])
```

### 4. 结果验证

```python
import json

result = extractor.extract_table_data(image_path, template)

if result["json_data"]:
    data = result["json_data"]
    
    # 验证数据结构
    if "data" in data and isinstance(data["data"], list):
        print(f"✓ 提取了 {len(data['data'])} 条数据")
        
        # 验证必需字段
        required_fields = ["size", "back_length"]
        for item in data["data"]:
            for field in required_fields:
                if field not in item or not item[field]:
                    print(f"⚠️ 缺少字段: {field}")
    else:
        print("✗ 数据结构不符合预期")
```

## 与其他工具类的配合

### 配合 TableRenderer 使用

```python
from utils.kimi_table_to_json import KimiTableToJSON
from utils.TableRenderer import TableRenderer

# 1. 从图片提取数据
extractor = KimiTableToJSON()
result = extractor.extract_from_template_file(
    image_path="table.jpg",
    template_file_path="template.json"
)

# 2. 使用提取的数据填充 HTML
if result["json_data"]:
    renderer = TableRenderer()
    renderer.render_table_from_data(
        html_template_path="template.html",
        data=result["json_data"]["data"],
        output_path="output.html"
    )
```

### 完整工作流

```python
# 步骤1: 图片 → JSON 数据
extractor = KimiTableToJSON()
json_result = extractor.extract_from_template_file(
    image_path="original_table.jpg",
    template_file_path="style1.json"
)

# 步骤2: JSON 数据 → HTML
renderer = TableRenderer()
html_output = renderer.render_table_from_data(
    html_template_path="style1.html",
    data=json_result["json_data"]["data"],
    output_path="rendered_table.html"
)

# 步骤3: HTML → 图片
screenshotter = HTMLScreenshotter()
screenshotter.capture_from_file(
    html_file_path="rendered_table.html",
    output_image="final_table.png",
    width=800,
    height=600
)
```

## 运行测试

```bash
# 运行单元测试
python test/test_kimi_table_to_json.py

# 运行示例代码
python utils/kimi_table_to_json.py
```

## 常见问题

### Q1: 提取的数据不准确？

**解决方案：**
1. 降低 temperature 到 0.05
2. 在自定义 prompt 中强调准确性
3. 确保模板示例数据清晰
4. 检查图片质量

### Q2: JSON 解析失败？

**解决方案：**
1. 查看 `raw_content` 了解 Kimi 返回了什么
2. 调整 prompt，强调返回纯 JSON
3. 增加 max_tokens（可能内容被截断）

### Q3: 批量提取时部分失败？

**解决方案：**
1. 检查失败的图片质量
2. 单独处理失败的图片
3. 适当增加 temperature 提高容错性

## 许可证

本项目遵循项目根目录的许可证。
