"""
tuxs - 图像生成工具集

包含以下主要功能模块:
- KimiClient: Kimi API 客户端
- KimiTableToHTML: 表格转 HTML
- KimiTableToJSON: 表格转 JSON
- TableRenderer: 表格渲染器
- HTMLScreenshotter: HTML 截图工具
"""

__version__ = "0.1.0"

from .utils import (
    KimiClient,
    KimiTableToHTML,
    KimiTableToJSON,
    TableRenderer,
    HTMLScreenshotter
)

__all__ = [
    'KimiClient',
    'KimiTableToHTML',
    'KimiTableToJSON',
    'TableRenderer',
    'HTMLScreenshotter',
]
