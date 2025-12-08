
"""
ComfyUI 自定义节点包初始化文件
自动导入当前目录下所有节点模块
"""

import os
import importlib
from pathlib import Path

# 获取当前目录
current_dir = Path(__file__).parent

# 存储所有导出的节点映射和类映射
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# 遍历当前目录下的所有Python文件
for file in current_dir.glob("*.py"):
    # 跳过__init__.py文件
    if file.name == "__init__.py":
        continue
    
    # 获取模块名（不含.py扩展名）
    module_name = file.stem
    
    try:
        # 动态导入模块
        module = importlib.import_module(f".{module_name}", package=__name__)
        
        # 如果模块有NODE_CLASS_MAPPINGS，合并到总映射中
        if hasattr(module, "NODE_CLASS_MAPPINGS"):
            NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
        
        # 如果模块有NODE_DISPLAY_NAME_MAPPINGS，合并到总映射中
        if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS"):
            NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
            
    except Exception as e:
        print(f"[ComfyUI-Tuxiansheng] 加载节点模块 {module_name} 失败: {str(e)}")

# 导出节点映射
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
