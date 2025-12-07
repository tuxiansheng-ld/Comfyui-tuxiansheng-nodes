# 工作流集成测试使用说明

完整的数据处理工作流：**图片 → JSON 数据 → HTML 渲染 → 截图**

---

## 📋 功能概述

这个集成测试展示了三个工具类的组合使用：

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐      ┌──────────┐
│  表格图片    │  →  │ JSON 数据    │  →  │  HTML 文件      │  →  │  截图    │
└─────────────┘      └──────────────┘      └─────────────────┘      └──────────┘
     ↓                     ↓                      ↓                     ↓
KimiTableToJSON      数据提取         TableRenderer         HTMLScreenshotter
  (AI 识别)          (结构化)          (模板填充)             (图片生成)
```

---

## 🚀 快速开始

### 方式 1: 运行示例代码（推荐）

```bash
# 使用示例数据运行完整工作流
python test/test_workflow_integration.py --example
```

**特点：**
- ✅ 无需 API key（自动使用示例数据）
- ✅ 无需图片（使用内置数据）
- ✅ 快速验证工作流

### 方式 2: 运行单元测试

```bash
# 运行所有集成测试
python test/test_workflow_integration.py
```

### 方式 3: 使用 VS Code 调试

在 VS Code 中选择以下调试配置：
- **"Debug: 工作流示例"** - 运行示例代码
- **"Debug: 工作流集成测试"** - 运行单元测试

---

## 📂 输出文件

所有生成的文件都保存在 `test/workflow_output/` 目录：

```
test/workflow_output/
├── example_data.json          # 提取的 JSON 数据（如果有）
├── example_table.html         # 渲染的 HTML 文件
├── example_screenshot.png     # 生成的截图
├── custom_style1.html         # 自定义数据测试
├── custom_style1.png
├── batch_1.html               # 批量处理测试
├── batch_1.png
└── ...
```

---

## 🎯 测试用例说明

### 测试 1: 完整工作流 - Style1 模板

```python
def test_01_complete_workflow_style1(self):
    """
    演示完整的三步工作流：
    1. 从图片提取 JSON 数据 (KimiTableToJSON)
    2. 渲染 HTML (TableRenderer)
    3. 生成截图 (HTMLScreenshotter)
    """
```

**流程：**
```
图片文件
  ↓ KimiTableToJSON.extract_from_template_file()
JSON 数据 {"data": [...]}
  ↓ TableRenderer.render_table_from_data()
HTML 文件
  ↓ HTMLScreenshotter.capture_from_file()
PNG 截图
```

**注意：** 需要设置 `KIMI_API_KEY` 环境变量，否则自动使用示例数据

---

### 测试 2: 自定义数据工作流

```python
def test_02_workflow_with_custom_data(self):
    """
    跳过 AI 提取步骤，直接使用自定义数据
    适合已有数据的场景
    """
```

**流程：**
```
自定义 JSON 数据
  ↓ TableRenderer.render_table_from_data()
HTML 文件
  ↓ HTMLScreenshotter.capture_from_file()
PNG 截图
```

---

### 测试 3: 批量处理工作流

```python
def test_03_batch_workflow(self):
    """
    批量处理多组数据
    自动生成多个 HTML 和截图
    """
```

---

## 💻 代码示例

### 示例 1: 完整工作流

```python
from utils.kimi_table_to_json import KimiTableToJSON
from utils.TableRenderer import TableRenderer
from utils.HTMLScreenshotter import HTMLScreenshotter

# 步骤1: 提取 JSON 数据
extractor = KimiTableToJSON()
result = extractor.extract_from_template_file(
    image_path="table_image.jpg",
    template_file_path="table_template/style1.json"
)

# 步骤2: 渲染 HTML
renderer = TableRenderer()
renderer.render_table_from_data(
    html_template_path="table_template/style1.html",
    data=result["json_data"]["data"],
    output_path="output.html"
)

# 步骤3: 生成截图
screenshotter = HTMLScreenshotter()
screenshotter.capture_from_file(
    html_file_path="output.html",
    output_image="output.png",
    width=800,
    height=600
)
```

### 示例 2: 使用自定义数据

```python
from utils.TableRenderer import TableRenderer
from utils.HTMLScreenshotter import HTMLScreenshotter

# 准备数据
data = [
    {
        "size": "M",
        "back_length": "43",
        "shoulder_width": "36",
        "bust": "96",
        "hem": "92",
        "sleeve_length": "64.2"
    }
]

# 渲染 + 截图
renderer = TableRenderer()
renderer.render_table_from_data(
    html_template_path="table_template/style1.html",
    data=data,
    output_path="custom.html"
)

screenshotter = HTMLScreenshotter()
screenshotter.capture_from_file("custom.html", "custom.png", 800, 600)
```

---

## ⚙️ 环境配置

### 必需配置

在 `.env` 文件中配置（如果需要使用 AI 提取功能）：

```env
# Kimi API 密钥（用于图片识别）
KIMI_API_KEY=your_api_key_here

# ChromeDriver 路径（用于截图）
CHROMEDRIVER_PATH=path/to/chromedriver.exe
```

### 可选配置

```env
# 截图默认尺寸
DEFAULT_SCREENSHOT_WIDTH=1920
DEFAULT_SCREENSHOT_HEIGHT=1080
```

---

## 📊 工作流对比

### 完整工作流（包含 AI 提取）

| 步骤 | 工具 | 输入 | 输出 | 时间 |
|------|------|------|------|------|
| 1 | KimiTableToJSON | 图片 + JSON模板 | JSON数据 | ~5-10秒 |
| 2 | TableRenderer | JSON数据 + HTML模板 | HTML文件 | <1秒 |
| 3 | HTMLScreenshotter | HTML文件 | PNG图片 | ~2-3秒 |

**总耗时：** 约 7-14 秒

### 简化工作流（使用已有数据）

| 步骤 | 工具 | 输入 | 输出 | 时间 |
|------|------|------|------|------|
| 1 | TableRenderer | JSON数据 + HTML模板 | HTML文件 | <1秒 |
| 2 | HTMLScreenshotter | HTML文件 | PNG图片 | ~2-3秒 |

**总耗时：** 约 2-4 秒

---

## 🎨 支持的模板

当前支持的表格模板：

### Style1 - 尺码信息表

**文件：**
- 模板：`table_template/style1.html`
- 数据：`table_template/style1.json`

**字段：**
- size (尺码)
- back_length (后中长)
- shoulder_width (肩宽)
- bust (胸围)
- hem (摆围)
- sleeve_length (袖长)

### Style2 - 尺码建议表

**文件：**
- 模板：`table_template/style2.html`
- 数据：`table_template/style2.json`

**字段：**
- size (尺码)
- height_150~175 (各身高建议)
- weight_range (参考体重)

---

## 🔧 常见问题

### Q1: 示例代码运行失败？

**检查项：**
1. 确认已激活 `comfyui` 虚拟环境
2. 确认已安装所有依赖：`pip install -r requirements.txt`
3. 查看错误日志，检查缺少的配置

### Q2: Kimi API 调用失败？

**解决方案：**
- 检查 `.env` 文件中的 `KIMI_API_KEY` 是否正确
- 示例代码会自动降级使用示例数据，无需担心

### Q3: 截图生成失败？

**可能原因：**
- ChromeDriver 未配置
- ChromeDriver 版本与 Chrome 浏览器不匹配

**解决方案：**
```env
# 在 .env 中配置 ChromeDriver 路径
CHROMEDRIVER_PATH=D:/tools/chromedriver.exe
```

### Q4: 如何修改图片路径？

编辑 `test_workflow_integration.py`，修改第 385 行：
```python
image_path = r"D:\data\comfyui-image\尺码2.png"  # 改为你的图片路径
```

---

## 📈 性能优化建议

### 1. 批量处理

使用批量方法提高效率：

```python
# 批量提取
extractor = KimiTableToJSON()
results = extractor.batch_extract(
    image_paths=["img1.jpg", "img2.jpg"],
    json_template=template,
    output_dir="output"
)
```

### 2. 缓存 JSON 数据

提取后保存 JSON，避免重复 API 调用：

```python
# 第一次提取并保存
extractor.save_json(result["json_data"], "cached_data.json")

# 后续直接使用
with open("cached_data.json") as f:
    data = json.load(f)
```

### 3. 复用 Screenshotter 实例

```python
# 复用实例，避免重复启动浏览器
screenshotter = HTMLScreenshotter()
with screenshotter:
    for html_file in html_files:
        screenshotter.capture_from_file(html_file, ...)
```

---

## 📝 扩展开发

### 添加新模板

1. 创建 HTML 模板 `table_template/styleX.html`
2. 创建 JSON 数据模板 `table_template/styleX.json`
3. 在测试中引用新模板

### 自定义工作流

参考 `run_complete_workflow_example()` 函数，编写自己的工作流脚本。

---

## 📚 相关文档

- [KimiTableToJSON 使用文档](../utils/kimi_table_to_json_README.md)
- [TableRenderer 使用文档](../utils/TableRenderer_README.md)
- [KimiClient 使用文档](../utils/kimi_client_README.md)

---

## 🎯 总结

这个集成测试展示了如何将三个工具类组合使用，实现从图片到最终截图的完整数据处理流程。

**核心优势：**
- ✅ 自动化数据提取
- ✅ 模板化 HTML 生成
- ✅ 批量处理支持
- ✅ 灵活的配置选项
- ✅ 完善的错误处理

**适用场景：**
- 📊 电商尺码表生成
- 📋 数据报表自动化
- 🖼️ 批量图片转换
- 📈 数据可视化
