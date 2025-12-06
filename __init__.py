from typing_extensions import override

from comfy_api.latest import ComfyExtension, io

# Import our nodes
from .StringToListNode import StringToListNode


class TuXsExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            StringToListNode,
        ]


async def comfy_entrypoint() -> ComfyExtension:  # ComfyUI calls this to load your extension and its nodes.
    return TuXsExtension()