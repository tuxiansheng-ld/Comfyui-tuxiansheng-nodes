# tuxs - 图像生成工具集

一个集成了 Kimi API、表格渲染和 HTML 截图功能的 Python 工具包。

## 功能特性

- **KimiClient**: Kimi API 客户端，支持智能对话和内容生成
- **KimiTableToHTML**: 将表格数据转换为 HTML 格式
- **KimiTableToJSON**: 将表格数据转换为 JSON 格式
- **TableRenderer**: 强大的表格渲染器，支持多种样式
- **HTMLScreenshotter**: HTML 页面截图工具

## 安装

### 从 whl 文件安装

```bash
pip install tuxs-0.1.0-py3-none-any.whl
```

### 从源码安装

```bash
cd tuxs
pip install .
```

### 开发模式安装

```bash
cd tuxs
pip install -e .
```

## 快速开始

### 环境变量配置

创建 `.env` 文件并配置必要的环境变量:

```env
KIMI_API_KEY=your_api_key_here
CHROMEDRIVER_PATH=chromedriver
```

### 基本使用

```python
from tuxs import KimiClient, TableRenderer, HTMLScreenshotter

# 使用 Kimi API
client = KimiClient()
response = client.chat("你好")

# 渲染表格
renderer = TableRenderer()
html = renderer.render(data)

# HTML 截图
screenshotter = HTMLScreenshotter()
image = screenshotter.capture(html_content)
```

## 依赖要求

- Python >= 3.8
- requests >= 2.25.0
- python-dotenv >= 0.19.0
- beautifulsoup4 >= 4.9.0
- selenium >= 4.0.0
- Pillow >= 8.0.0
- numpy >= 1.19.0

## 许可证

MIT License

## 作者

tuxiansheng
