
---
trigger: always_on
alwaysApply: true
---

# ComfyUI 自定义节点开发规则

## 开发环境信息

### 系统环境
- **操作系统**: Windows 10
- **Python 环境管理**: Conda
- **当前虚拟环境**: comfyui

### 环境配置
# 激活开发环境
conda activate comfyui

# 查看当前环境
conda info --envs

# 安装依赖
pip install -r requirements.txt

### 项目结构
- **项目根目录**: `d:\ComfyUI\custom_nodes\Comfyui-tuxiansheng-nodes`
- 自定义节点应放置在项目根目录下
- 遵循 ComfyUI 自定义节点开发规范

## 开发规范

### 开发注意事项
1. 确保在 comfyui 虚拟环境中进行开发和测试
2. 所有依赖包应安装在 comfyui 环境中
3. 代码修改后需要重启 ComfyUI 才能生效
4. 建议使用相对路径引用项目内文件

### 版本控制规则
- **禁止频繁提交**: 不要每修改完一次代码就提交 Git
- **提交时机**: 应在完成一个完整功能或重要里程碑后再提交
- **提交内容**: 确保代码经过测试且功能正常后再进行提交
- **提交信息**: 编写清晰、有意义的提交信息

## 测试流程

### 测试前准备
# 1. 激活虚拟环境
conda activate comfyui

# 2. 运行测试脚本
python test_script.py

### 测试要求
- 在提交代码前必须完成基本功能测试
- 确保节点在 ComfyUI 中能够正常加载和运行
- 验证输入输出参数的正确性

## 文档规范

### 文档生成规则
- 仅在明确要求生成文档时才创建说明文档
- 默认情况下不自动生成文档
- 专注于代码实现和功能开发
- 代码注释应简洁明了,重点说明关键逻辑
