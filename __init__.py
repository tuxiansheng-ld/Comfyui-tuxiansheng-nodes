import os
from typing_extensions import override

from comfy_api.latest import ComfyExtension, io
from dotenv import load_dotenv

# 导入自定义节点包
from . import nodes

# 加载环境变量
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(env_path)


class TuXsExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        """返回需要注册到 ComfyUI 的节点类列表"""
        # 从 nodes 包中收集所有节点类
        node_classes: list[type[io.ComfyNode]] = []
        for node_class in nodes.NODE_CLASS_MAPPINGS.values():
            node_classes.append(node_class)
        return node_classes


async def comfy_entrypoint() -> ComfyExtension:  # ComfyUI calls this to load your extension and its nodes.
    return TuXsExtension()