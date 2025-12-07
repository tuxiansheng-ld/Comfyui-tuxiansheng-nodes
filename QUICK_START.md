# 快速入门指南

## 📦 环境要求

- **Conda 环境**: comfyui
- **Python**: 3.7+
- **依赖包**: requests

## 🚀 快速开始

### 1️⃣ 激活 Conda 环境

在运行任何脚本之前，先激活 comfyui conda 环境：

```bash
# Windows PowerShell 或 CMD
conda activate comfyui
```

### 2️⃣ 安装依赖

```bash
pip install requests
```

### 3️⃣ 配置 API Key

设置 Kimi API Key 环境变量：

**方法 A: 临时设置（当前会话有效）**
```powershell
# PowerShell
$env:KIMI_API_KEY="your_api_key_here"

# CMD
set KIMI_API_KEY=your_api_key_here
```

**方法 B: 使用 .env 文件（推荐）**

在项目根目录创建 `.env` 文件：
```
KIMI_API_KEY=your_api_key_here
```

### 4️⃣ 运行测试

**方法 1: 使用批处理脚本（推荐）**
```bash
# 双击运行或在命令行执行
run_test.bat
```

这个脚本会：
- ✅ 自动激活 comfyui 环境
- ✅ 检查环境配置
- ✅ 运行所有单元测试
- ✅ 显示测试结果

**方法 2: 手动运行**
```bash
# 先激活环境
conda activate comfyui

# 运行测试
python test/test_kimi_table_to_html.py
```

## 💡 使用示例

### 基础示例

```python
from utils import KimiTableToHTML

# 初始化（会自动从环境变量读取 API key）
converter = KimiTableToHTML()

# 转换表格图片为 HTML
result = converter.table_image_to_html("your_table_image.jpg")

# 保存结果
converter.save_html(result["html_code"], "output.html")

print("✅ 转换完成！")
```

### 批量转换示例

```python
from utils import KimiTableToHTML

converter = KimiTableToHTML()

# 准备图片列表
images = [
    "table1.jpg",
    "table2.jpg",
    "table3.jpg"
]

# 批量转换
results = converter.batch_convert(
    image_paths=images,
    output_dir="output_htmls"
)

# 查看结果
for r in results:
    if r['success']:
        print(f"✅ {r['image_path']} -> {r['output_path']}")
    else:
        print(f"❌ {r['image_path']} 失败: {r['error']}")
```

## 🔧 在 ComfyUI 节点中使用

如果要在 ComfyUI 自定义节点中使用此工具：

```python
import os
import sys

# 添加路径（如果需要）
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from utils import KimiTableToHTML

class TableToHTMLNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "convert"
    CATEGORY = "utils"
    
    def convert(self, image, api_key):
        # 初始化转换器
        converter = KimiTableToHTML(api_key=api_key)
        
        # 处理图片并转换
        # ... 你的转换逻辑 ...
        
        return (html_code,)
```

## 📁 项目结构

```
Comfyui-tuxiansheng-nodes/
├── utils/                      # 工具类目录
│   ├── __init__.py
│   ├── kimi_table_to_html.py  # Kimi API 工具类
│   └── README.md              # 工具使用文档
├── test/                       # 测试目录
│   ├── __init__.py
│   ├── test_kimi_table_to_html.py  # 单元测试
│   ├── run_tests.py           # 测试运行脚本
│   └── README.md              # 测试说明文档
├── run_test.bat               # Windows 测试批处理脚本
├── QUICK_START.md             # 本文档
└── .env                       # 环境变量配置（需自行创建）
```

## ⚙️ 环境变量说明

| 变量名 | 说明 | 是否必需 | 默认值 |
|--------|------|----------|--------|
| `KIMI_API_KEY` | Kimi API 密钥 | 是 | 无 |
| `CONDA_DEFAULT_ENV` | Conda 环境名称 | 否（自动检测） | - |

## 🐛 常见问题

### Q1: 提示 "无法激活 comfyui 环境"
**A**: 确保：
1. 已安装 Anaconda/Miniconda
2. 已创建 comfyui 环境：`conda create -n comfyui python=3.10`
3. 环境路径在系统 PATH 中

### Q2: 提示 "API key is required"
**A**: 需要设置 KIMI_API_KEY 环境变量或在代码中传入 API key

### Q3: 测试失败
**A**: 
1. 检查是否在 comfyui 环境中：`conda activate comfyui`
2. 检查是否安装了 requests：`pip install requests`
3. 查看具体错误信息进行排查

### Q4: 导入模块失败
**A**: 确保在项目根目录运行脚本，或正确设置 PYTHONPATH

## 📞 获取帮助

- 查看工具文档：`utils/README.md`
- 查看测试文档：`test/README.md`
- 提交 Issue 或 PR

## 🎯 下一步

1. ✅ 激活 comfyui 环境
2. ✅ 安装依赖包
3. ✅ 配置 API Key
4. ✅ 运行测试验证
5. 🚀 开始使用工具类

祝使用愉快！🎉
