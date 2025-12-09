# TableRenderer - 表格数据渲染工具

一个简单易用的工具类，用于根据 JSON 数据填充 HTML 表格模板，实现数据与模板分离。

## 核心功能

- ✅ 从 JSON 文件读取数据填充 HTML 表格
- ✅ 支持直接使用数据字典填充
- ✅ 保持 HTML 模板的标题和表头固定不变
- ✅ 只修改表格数据部分
- ✅ 自动验证 JSON 数据格式
- ✅ 支持输出到文件或返回 HTML 字符串

## 快速开始

### 1. 安装依赖

```bash
pip install beautifulsoup4
```

### 2. 准备文件

#### HTML 模板文件 (style1.html)
标题、表头、样式保持固定：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>尺码信息表</title>
    <style>
        /* 样式定义 */
    </style>
</head>
<body>
    <table>
        <thead>
            <tr><th colspan="6">SIZE 尺码信息</th></tr>
            <!-- 注意事项等固定内容 -->
        </thead>
        <tbody>
            <tr>
                <td rowspan="2">开衫尺码</td>
                <td>后中长</td>
                <td>肩宽</td>
                <td>胸围</td>
                <td>摆围</td>
                <td>袖长</td>
            </tr>
            <!-- 数据行会被替换 -->
        </tbody>
    </table>
</body>
</html>
```

#### JSON 数据文件 (style1.json)
只包含可变的数据：

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
    },
    {
      "size": "M",
      "back_length": "43",
      "shoulder_width": "36",
      "bust": "96",
      "hem": "92",
      "sleeve_length": "64.2"
    }
  ]
}
```

### 3. 基本使用

```python
from utils.TableRenderer import TableRenderer

# 初始化渲染器
renderer = TableRenderer()

# 渲染表格
renderer.render_table(
    html_template_path="table_template/style1.html",
    json_data_path="table_template/style1.json",
    output_path="output.html"
)
```

## 使用示例

### 示例 1: 从文件生成表格

```python
from utils.TableRenderer import TableRenderer

renderer = TableRenderer()

# 验证 JSON 数据格式
if renderer.validate_json_data("data.json"):
    # 渲染并保存
    html_content = renderer.render_table(
        html_template_path="template.html",
        json_data_path="data.json",
        output_path="result.html"
    )
    print("表格生成成功！")
```

### 示例 2: 使用数据字典（不需要 JSON 文件）

```python
from utils.TableRenderer import TableRenderer

renderer = TableRenderer()

# 自定义数据
data = [
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

# 渲染表格
renderer.render_table_from_data(
    html_template_path="template.html",
    data=data,
    output_path="custom_table.html"
)
```

### 示例 3: 只返回 HTML 字符串（不保存文件）

```python
from utils.TableRenderer import TableRenderer

renderer = TableRenderer()

# 不指定 output_path，只返回 HTML 字符串
html_string = renderer.render_table(
    html_template_path="template.html",
    json_data_path="data.json",
    output_path=None  # 不保存文件
)

# 可以进一步处理 HTML 字符串
print(html_string)
```

### 示例 4: 结合其他工具使用

```python
from utils.TableRenderer import TableRenderer
from utils.HTMLScreenshotter import HTMLScreenshotter

# 1. 渲染表格
renderer = TableRenderer()
html_content = renderer.render_table(
    "template.html",
    "data.json",
    "table.html"
)

# 2. 将表格截图为图片
screenshotter = HTMLScreenshotter()
screenshotter.capture_from_file(
    "table.html",
    "table_image.png",
    width=800,
    height=600
)

print("表格已渲染并截图！")
```

## API 文档

### TableRenderer 类

#### 初始化

```python
renderer = TableRenderer()
```

#### 主要方法

##### 1. `render_table()` - 从文件渲染表格

```python
html_string = renderer.render_table(
    html_template_path: str,  # HTML 模板文件路径
    json_data_path: str,      # JSON 数据文件路径
    output_path: str = None   # 输出文件路径（可选）
) -> str                      # 返回填充后的 HTML 字符串
```

**参数：**
- `html_template_path`: HTML 模板文件的路径
- `json_data_path`: JSON 数据文件的路径
- `output_path`: 输出文件路径（可选）。如果提供，会保存到文件；如果不提供，只返回字符串

**返回：**
- 填充后的 HTML 字符串

##### 2. `render_table_from_data()` - 从数据字典渲染

```python
html_string = renderer.render_table_from_data(
    html_template_path: str,     # HTML 模板文件路径
    data: List[Dict[str, str]],  # 数据列表
    output_path: str = None      # 输出文件路径（可选）
) -> str                         # 返回填充后的 HTML 字符串
```

**参数：**
- `html_template_path`: HTML 模板文件的路径
- `data`: 数据列表，每个元素是一个字典，包含表格行的数据
- `output_path`: 输出文件路径（可选）

**返回：**
- 填充后的 HTML 字符串

##### 3. `validate_json_data()` - 验证 JSON 数据

```python
is_valid = renderer.validate_json_data(
    json_data_path: str  # JSON 数据文件路径
) -> bool                # 是否验证通过
```

**参数：**
- `json_data_path`: JSON 数据文件的路径

**返回：**
- `True`: 数据格式正确
- `False`: 数据格式错误

## JSON 数据格式规范

### 必需字段

JSON 文件必须包含 `data` 数组，数组中的每个对象代表一行数据：

```json
{
  "data": [
    {
      "size": "尺码",              // 必需
      "back_length": "后中长",      // 必需
      "shoulder_width": "肩宽",    // 必需
      "bust": "胸围",              // 必需
      "hem": "摆围",               // 必需
      "sleeve_length": "袖长"      // 必需
    }
  ]
}
```

### 字段说明

| 字段名 | 说明 | 类型 | 必需 |
|--------|------|------|------|
| `size` | 尺码（S/M/L/XL等） | string | 是 |
| `back_length` | 后中长（单位：CM） | string | 是 |
| `shoulder_width` | 肩宽（单位：CM） | string | 是 |
| `bust` | 胸围（单位：CM） | string | 是 |
| `hem` | 摆围（单位：CM） | string | 是 |
| `sleeve_length` | 袖长（单位：CM） | string | 是 |

### 示例数据

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
}
```

## HTML 模板要求

### 必需结构

HTML 模板必须包含以下结构：

```html
<table>
    <thead>
        <!-- 标题和注意事项（固定） -->
    </thead>
    <tbody>
        <tr>
            <!-- 表头行（固定） -->
            <td rowspan="2">开衫尺码</td>
            <td>后中长</td>
            <td>肩宽</td>
            <td>胸围</td>
            <td>摆围</td>
            <td>袖长</td>
        </tr>
        <!-- 数据行会被自动替换 -->
    </tbody>
</table>
```

### 重要说明

1. **`<tbody>` 必须存在**：工具会在 `<tbody>` 中填充数据
2. **第一行是表头**：`<tbody>` 的第一行会被保留作为表头
3. **数据行会被替换**：第二行开始的所有数据行会被 JSON 数据替换
4. **样式会保留**：CSS 样式和其他固定内容不会被修改

## 错误处理

### 常见错误及解决方案

#### 1. JSON 格式错误

```python
if not renderer.validate_json_data("data.json"):
    print("JSON 数据格式不正确，请检查")
```

#### 2. 文件不存在

```python
try:
    renderer.render_table("template.html", "data.json", "output.html")
except FileNotFoundError as e:
    print(f"文件不存在: {e}")
```

#### 3. HTML 结构不符合要求

```python
try:
    renderer.render_table("template.html", "data.json")
except ValueError as e:
    print(f"HTML 模板结构错误: {e}")
```

## 最佳实践

1. **模板与数据分离**
   - HTML 模板只包含结构和样式
   - JSON 只包含可变数据
   - 便于维护和更新

2. **数据验证**
   - 使用 `validate_json_data()` 验证数据格式
   - 确保所有必需字段都存在

3. **灵活使用**
   - 需要保存文件时提供 `output_path`
   - 只需要 HTML 字符串时不提供 `output_path`

4. **与其他工具结合**
   - 可以与 `HTMLScreenshotter` 结合生成图片
   - 可以与 `KimiClient` 结合处理数据

## 运行测试

```bash
# 运行单元测试
python test/test_table_renderer.py

# 运行示例代码
python utils/table_renderer.py
```

## 许可证

本项目遵循项目根目录的许可证。
