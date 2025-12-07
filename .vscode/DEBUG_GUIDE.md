# VS Code 调试配置说明

## 📁 配置文件

- **launch.json** - 调试启动配置
- **settings.json** - 工作区设置

## 🚀 使用方法

### 1. 选择 Python 解释器

按 `Ctrl+Shift+P`，输入 `Python: Select Interpreter`，选择 `comfyui` conda 环境。

### 2. 调试测试用例

#### 方法 1: 使用调试配置（推荐）

1. 按 `F5` 或点击左侧调试图标
2. 从下拉菜单选择调试配置：

| 配置名称 | 说明 | 使用场景 |
|---------|------|---------|
| **Debug: 运行所有测试** | 运行 test_kimi_table_to_html.py 中的所有测试 | 完整测试 |
| **Debug: 运行测试脚本** | 运行 run_tests.py 脚本 | 使用测试框架 |
| **Debug: 当前测试文件** | 使用 unittest 发现并运行测试 | 自动发现测试 |
| **Debug: 单个测试用例** | 运行指定的单个测试用例 | 调试特定测试 |
| **Debug: Pytest 运行所有测试** | 使用 pytest 运行测试 | Pytest 用户 |
| **Debug: Kimi 工具类示例** | 运行工具类示例代码 | 测试工具类 |
| **Debug: 当前 Python 文件** | 运行当前打开的 Python 文件 | 通用调试 |

3. 点击绿色播放按钮或按 `F5` 开始调试

#### 方法 2: 在代码中设置断点

1. 在代码行号左侧点击，设置红色断点
2. 选择调试配置并运行
3. 程序会在断点处暂停

#### 方法 3: 使用测试面板

1. 点击左侧"测试"图标（烧杯图标）
2. VS Code 会自动发现所有测试
3. 点击测试旁边的调试图标进行调试

### 3. 调试单个测试用例

如果要调试特定的测试用例，修改 `Debug: 单个测试用例` 配置中的 args：

```json
"args": [
    "test.test_kimi_table_to_html.TestKimiTableToHTML.test_你要调试的测试方法名"
]
```

例如：
- `test.test_kimi_table_to_html.TestKimiTableToHTML.test_init_with_api_key`
- `test.test_kimi_table_to_html.TestKimiTableToHTML.test_upload_image_success`
- `test.test_kimi_table_to_html.TestKimiTableToHTML.test_batch_convert_success`

## 🔧 调试技巧

### 设置断点
- **普通断点**: 点击行号左侧
- **条件断点**: 右键断点 → "编辑断点" → 设置条件
- **日志断点**: 右键断点 → "编辑断点" → 设置日志消息

### 调试控制
- **F5**: 继续执行
- **F10**: 单步跳过（Step Over）
- **F11**: 单步进入（Step Into）
- **Shift+F11**: 单步跳出（Step Out）
- **Ctrl+Shift+F5**: 重新启动调试
- **Shift+F5**: 停止调试

### 查看变量
- **变量面板**: 左侧调试视图中查看所有变量
- **监视**: 添加表达式到"监视"面板
- **悬停**: 鼠标悬停在变量上查看值
- **调试控制台**: 输入表达式查看值

### 调用堆栈
在"调用堆栈"面板中查看函数调用链，点击可跳转到对应位置。

## 📝 环境变量配置

### 方法 1: 使用 .env 文件（推荐）

项目根目录的 `.env` 文件会被自动加载（需要安装 Python 插件）。

### 方法 2: 在 launch.json 中配置

已在所有配置中包含环境变量：
```json
"env": {
    "PYTHONPATH": "${workspaceFolder}",
    "KIMI_API_KEY": "${env:KIMI_API_KEY}"
}
```

### 方法 3: 系统环境变量

在系统中设置 `KIMI_API_KEY` 环境变量。

## 🧪 测试面板使用

VS Code 的测试面板可以：
- ✅ 自动发现所有测试用例
- ✅ 显示测试层级结构
- ✅ 一键运行/调试单个或多个测试
- ✅ 显示测试结果（通过/失败）
- ✅ 查看测试输出和错误信息

### 启用测试面板

1. 打开设置（`Ctrl+,`）
2. 搜索 `python.testing`
3. 确保 `Python > Testing: Unittest Enabled` 已勾选
4. 点击左侧测试图标，刷新测试列表

## 🎯 常用调试场景

### 场景 1: 调试特定测试失败

1. 在测试面板找到失败的测试
2. 右键 → "调试测试"
3. 在相关代码处设置断点
4. 查看变量值，找出问题

### 场景 2: 调试 Mock 测试

1. 在 mock 对象设置处设置断点
2. 在测试方法开始处设置断点
3. 单步执行，观察 mock 对象行为
4. 在调试控制台输入 `mock_obj.call_count` 等查看调用情况

### 场景 3: 调试 API 调用

1. 在 `_call_api` 方法处设置断点
2. 查看请求参数
3. 单步执行，观察响应处理
4. 检查错误处理逻辑

### 场景 4: 调试批量处理

1. 在 `batch_convert` 循环处设置条件断点
2. 条件: `i == 1` （只在处理第二个文件时暂停）
3. 观察特定文件的处理过程

## ⚙️ 配置说明

### justMyCode: false

允许调试进入第三方库代码（如 requests、unittest 等）。

### console: integratedTerminal

在 VS Code 集成终端中运行，可以看到彩色输出和交互。

### PYTHONPATH

确保 Python 能正确找到项目模块。

## 🔍 故障排查

### 问题 1: 找不到模块

**解决方案**: 
1. 检查 Python 解释器是否选择了 comfyui 环境
2. 检查 PYTHONPATH 是否正确设置
3. 在终端运行 `conda activate comfyui` 后再启动 VS Code

### 问题 2: 断点不生效

**解决方案**:
1. 确保代码已保存
2. 检查是否在正确的文件中设置断点
3. 尝试设置 `"justMyCode": false`

### 问题 3: 环境变量未加载

**解决方案**:
1. 确保 `.env` 文件存在且格式正确
2. 重启 VS Code
3. 在 launch.json 中直接设置环境变量

### 问题 4: 测试面板不显示测试

**解决方案**:
1. 检查 settings.json 中的测试配置
2. 点击测试面板的刷新按钮
3. 检查测试文件命名是否符合 `test_*.py` 格式

## 📚 推荐插件

- **Python** (Microsoft) - 必装
- **Python Test Explorer** - 增强测试体验
- **Better Comments** - 更好的注释高亮
- **GitLens** - Git 增强
- **Error Lens** - 实时显示错误

## 🎓 学习资源

- [VS Code Python 调试文档](https://code.visualstudio.com/docs/python/debugging)
- [VS Code Python 测试文档](https://code.visualstudio.com/docs/python/testing)
- [Python unittest 文档](https://docs.python.org/3/library/unittest.html)

## 💡 最佳实践

1. **经常使用断点**: 不要只依赖 print，多用断点查看运行时状态
2. **善用条件断点**: 在循环中只在特定条件下暂停
3. **查看调用堆栈**: 理解代码执行流程
4. **使用监视表达式**: 持续观察关键变量
5. **保存调试配置**: 为常用调试场景创建专门配置

## 🚀 快速开始

1. 打开 VS Code，确保选择了 comfyui Python 环境
2. 打开测试文件 `test/test_kimi_table_to_html.py`
3. 在某个测试方法中设置断点
4. 按 `F5`，选择 `Debug: 运行所有测试`
5. 开始调试！

祝调试愉快！🎉
