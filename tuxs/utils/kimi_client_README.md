# KimiClient - 通用 Kimi API 调用工具类

一个灵活、易用的 Kimi API 调用工具类，支持自定义图片和 prompt，可用于各种场景。

## 特性

- ✅ 支持纯文本对话
- ✅ 支持单张图片分析
- ✅ 支持多张图片同时分析
- ✅ 自定义 system prompt 和 user prompt
- ✅ 灵活的参数配置（temperature, max_tokens 等）
- ✅ 自动切换视觉模型
- ✅ 从环境变量读取 API Key
- ✅ 完整的错误处理

## 快速开始

### 1. 安装依赖

```bash
pip install requests python-dotenv
```

### 2. 配置 API Key

在项目根目录的 `.env` 文件中添加：

```env
KIMI_API_KEY=your_api_key_here
```

### 3. 基本使用

```python
from utils.kimi_client import KimiClient

# 初始化客户端
client = KimiClient()

# 纯文本对话
result = client.chat_text_only(
    prompt="请介绍一下人工智能",
    system_prompt="你是一个专业的AI助手"
)
print(result['content'])
```

## 使用示例

### 示例 1: 纯文本对话

```python
from utils.kimi_client import KimiClient

client = KimiClient()

# 简单对话
result = client.chat_text_only(
    prompt="什么是机器学习？",
    temperature=0.7,
    max_tokens=500
)

print(f"回答: {result['content']}")
print(f"Token使用: {result['usage']}")
```

### 示例 2: 分析单张图片

```python
# 分析图片内容
result = client.analyze_image(
    image_path="product.jpg",
    prompt="请详细描述这个产品的特点",
    system_prompt="你是一个专业的产品分析师"
)

print(result['content'])
```

### 示例 3: 分析多张图片

```python
# 比较多张图片
result = client.analyze_images(
    image_paths=["design_v1.png", "design_v2.png"],
    prompt="请比较这两个设计方案的优缺点",
    temperature=0.5
)

print(result['content'])
```

### 示例 4: 图片转换（如表格转 HTML）

```python
# 将表格图片转换为 HTML
result = client.chat(
    prompt="请将这个表格转换为HTML代码，要求样式美观",
    image_paths="table.jpg",
    system_prompt="你是一个专业的前端开发专家",
    temperature=0.2,
    max_tokens=8000
)

# 保存 HTML 代码
with open("output.html", "w", encoding="utf-8") as f:
    f.write(result['content'])
```

### 示例 5: 自定义模型

```python
# 使用 32k 上下文模型
client.set_model("moonshot-v1-32k")

result = client.chat_text_only(
    prompt="请写一篇关于AI发展的长文章",
    max_tokens=10000
)
```

### 示例 6: 复杂场景 - 图片OCR + 处理

```python
# OCR识别图片文字并翻译
result = client.chat(
    prompt="请识别图片中的所有文字，并翻译成英文",
    image_paths="document.jpg",
    system_prompt="你是一个专业的OCR和翻译专家",
    temperature=0.1  # 低温度保证准确性
)

print(result['content'])
```

## API 文档

### KimiClient 类

#### 初始化

```python
client = KimiClient(api_key: Optional[str] = None)
```

**参数:**
- `api_key`: Kimi API 密钥（可选）。如果不提供，将从环境变量 `KIMI_API_KEY` 读取

#### 主要方法

##### 1. `chat()` - 通用对话方法

```python
result = client.chat(
    prompt: str,                              # 用户提示词（必填）
    image_paths: Optional[Union[str, List[str]]] = None,  # 图片路径
    system_prompt: Optional[str] = None,      # 系统提示词
    temperature: float = 0.3,                 # 温度参数 (0-1)
    max_tokens: int = 4000,                   # 最大token数
    **kwargs                                   # 其他API参数
)
```

**返回值:**
```python
{
    "content": str,         # AI返回的文本内容
    "raw_response": dict,   # 原始API响应
    "usage": dict,          # token使用情况
    "model": str            # 使用的模型
}
```

##### 2. `chat_text_only()` - 纯文本对话

```python
result = client.chat_text_only(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 4000,
    **kwargs
)
```

##### 3. `analyze_image()` - 分析单张图片

```python
result = client.analyze_image(
    image_path: str,
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 4000,
    **kwargs
)
```

##### 4. `analyze_images()` - 分析多张图片

```python
result = client.analyze_images(
    image_paths: List[str],
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 4000,
    **kwargs
)
```

##### 5. `set_model()` - 设置模型

```python
client.set_model(model: str)
```

**支持的模型:**
- `moonshot-v1-8k` - 8k 上下文（默认）
- `moonshot-v1-32k` - 32k 上下文
- `moonshot-v1-128k` - 128k 上下文
- `moonshot-v1-8k-vision-preview` - 8k 视觉模型
- `moonshot-v1-32k-vision-preview` - 32k 视觉模型

**注意:** 当传入图片时，会自动切换到对应的视觉模型。

## 参数说明

### temperature（温度）
- 范围: 0-1
- 说明: 控制输出的随机性
- 建议值:
  - `0.1-0.3`: 需要准确、确定性输出（如代码、数据提取）
  - `0.5-0.7`: 平衡创造性和准确性（如解释、分析）
  - `0.8-1.0`: 需要创造性输出（如写作、头脑风暴）

### max_tokens（最大token数）
- 说明: 限制生成内容的最大长度
- 建议值:
  - 简短回答: 500-1000
  - 中等长度: 2000-4000
  - 长文本: 8000+

### system_prompt（系统提示词）
- 说明: 定义 AI 的角色、行为和回答风格
- 示例:
  ```python
  system_prompt="你是一个专业的数据分析师，善于从数据中发现洞察"
  system_prompt="你是一个严谨的代码审查专家，注重代码质量和最佳实践"
  ```

## 错误处理

```python
try:
    result = client.chat_text_only("你好")
    print(result['content'])
except ValueError as e:
    print(f"配置错误: {e}")
except requests.exceptions.RequestException as e:
    print(f"API请求错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
```

## 最佳实践

1. **使用环境变量管理 API Key**
   - 永远不要在代码中硬编码 API Key
   - 使用 `.env` 文件并添加到 `.gitignore`

2. **合理设置 temperature**
   - 需要准确性时使用低温度（0.1-0.3）
   - 需要创造性时使用高温度（0.7-1.0）

3. **图片处理**
   - 支持常见图片格式：JPG, PNG, GIF 等
   - 图片会自动转换为 base64 编码
   - 使用图片时会自动切换到视觉模型

4. **优化 token 使用**
   - 根据需求设置合适的 `max_tokens`
   - 检查返回的 `usage` 信息了解消耗

5. **错误处理**
   - 始终使用 try-except 处理可能的异常
   - 检查 API Key 是否正确配置

## 与其他工具类的关系

- **KimiTableToHTML**: 专门用于表格转 HTML 的工具类（基于特定场景优化）
- **KimiClient**: 通用的 Kimi API 调用工具类（适用于各种场景）

如果你只需要表格转 HTML 功能，推荐使用 `KimiTableToHTML`。  
如果需要更灵活的自定义调用，使用 `KimiClient`。

## 运行测试

```bash
# 确保已配置 .env 文件
python test/test_kimi_client.py
```

## 许可证

本项目遵循项目根目录的许可证。
