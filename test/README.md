# 测试说明文档

## 📝 测试概述

本目录包含 Kimi Table to HTML 工具类的完整测试套件，包括单元测试和集成测试。

## 🧪 测试文件

- **test_kimi_table_to_html.py** - 主测试文件，包含所有测试用例
- **run_tests.py** - 测试运行脚本，提供便捷的测试启动方式
- **__init__.py** - 测试包初始化文件

## 🚀 运行测试

### 方法 1: 直接运行测试文件

```bash
python test/test_kimi_table_to_html.py
```

### 方法 2: 使用测试运行脚本

```bash
# 只运行单元测试（不需要 API key）
python test/run_tests.py

# 包含集成测试（需要设置 KIMI_API_KEY 环境变量）
python test/run_tests.py -i

# 详细输出模式
python test/run_tests.py -v
```

### 方法 3: 使用 unittest 模块

```bash
python -m unittest test.test_kimi_table_to_html
```

### 方法 4: 使用 pytest（如果已安装）

```bash
pytest test/test_kimi_table_to_html.py -v
```

## 📋 测试用例列表

### TestKimiTableToHTML - 单元测试类

#### 初始化测试
- ✅ `test_init_with_api_key` - 测试使用 API key 初始化
- ✅ `test_init_with_env_variable` - 测试使用环境变量初始化
- ✅ `test_init_without_api_key` - 测试没有 API key 时抛出异常
- ✅ `test_set_model` - 测试设置模型版本

#### 图片处理测试
- ✅ `test_encode_image` - 测试图片 base64 编码
- ✅ `test_upload_image_success` - 测试图片上传成功
- ✅ `test_upload_image_failure` - 测试图片上传失败

#### API 调用测试
- ✅ `test_call_api_success` - 测试 API 调用成功
- ✅ `test_extract_html_with_html_block` - 测试提取带 html 标记的代码
- ✅ `test_extract_html_with_generic_block` - 测试提取通用代码块
- ✅ `test_extract_html_without_block` - 测试提取无代码块的 HTML
- ✅ `test_extract_html_empty_response` - 测试空响应处理

#### 文件操作测试
- ✅ `test_save_html` - 测试保存 HTML 文件

#### 核心功能测试
- ✅ `test_table_image_to_html_success` - 测试表格图片转 HTML 成功
- ✅ `test_table_image_to_html_with_custom_prompt` - 测试自定义提示词

#### 批量处理测试
- ✅ `test_batch_convert_success` - 测试批量转换成功
- ✅ `test_batch_convert_with_errors` - 测试批量转换时部分失败

### TestKimiTableToHTMLIntegration - 集成测试类

- ⚠️ `test_real_api_call` - 真实 API 调用测试（需要真实 API key 和测试图片）

## 🔧 配置环境变量

### Windows PowerShell
```powershell
$env:KIMI_API_KEY="your_api_key_here"
```

### Windows CMD
```cmd
set KIMI_API_KEY=your_api_key_here
```

### Linux/Mac
```bash
export KIMI_API_KEY=your_api_key_here
```

## 📊 测试覆盖率

当前测试覆盖了以下功能：

- ✅ 类初始化（API key 验证）
- ✅ 模型设置
- ✅ 图片编码
- ✅ 图片上传
- ✅ API 调用
- ✅ HTML 提取（多种格式）
- ✅ 文件保存
- ✅ 单个转换
- ✅ 批量转换
- ✅ 错误处理

## 🎯 测试特点

1. **Mock 测试** - 使用 unittest.mock 模拟外部依赖，无需真实 API
2. **边界测试** - 测试各种边界情况和异常场景
3. **集成测试** - 提供真实 API 调用测试（可选）
4. **完整覆盖** - 覆盖所有公开方法和主要私有方法
5. **自动化运行** - 支持多种运行方式，便于 CI/CD 集成

## 📖 测试示例输出

```
test_init_with_api_key (TestKimiTableToHTML.test_init_with_api_key)
测试使用 API key 初始化 ... ok

test_encode_image (TestKimiTableToHTML.test_encode_image)
测试图片编码 ... ok

test_table_image_to_html_success (TestKimiTableToHTML.test_table_image_to_html_success)
测试表格图片转 HTML 成功 ... ok

======================================================================
测试总结
======================================================================
运行测试数: 17
成功: 17
失败: 0
错误: 0
跳过: 0
```

## ⚠️ 注意事项

1. **单元测试**不需要真实的 API key，使用 mock 对象模拟
2. **集成测试**需要：
   - 真实的 Kimi API key
   - 有效的测试图片文件
   - 网络连接
3. 如果没有设置 `KIMI_API_KEY` 环境变量，集成测试会被自动跳过
4. 测试文件不会创建任何永久文件，所有 mock 操作都在内存中完成

## 🔍 调试测试

如果某个测试失败，可以：

1. 查看详细的错误信息
2. 单独运行失败的测试：
```bash
python -m unittest test.test_kimi_table_to_html.TestKimiTableToHTML.test_xxx
```
3. 添加调试输出或使用 Python 调试器

## 📝 添加新测试

在添加新功能后，请遵循以下步骤添加测试：

1. 在 `TestKimiTableToHTML` 类中添加新的测试方法
2. 测试方法名必须以 `test_` 开头
3. 使用合适的 mock 对象模拟外部依赖
4. 添加清晰的文档字符串说明测试目的
5. 运行测试确保通过

### 测试模板

```python
def test_new_feature(self):
    \"\"\"测试新功能描述\"\"\"
    converter = KimiTableToHTML(api_key=self.test_api_key)
    
    # 准备测试数据
    # ...
    
    # 执行测试
    result = converter.new_method()
    
    # 验证结果
    self.assertEqual(result, expected_value)
```

## 🤝 贡献

欢迎提交新的测试用例或改进现有测试！
