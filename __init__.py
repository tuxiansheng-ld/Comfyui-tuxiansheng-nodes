from typing_extensions import override

from comfy_api.latest import ComfyExtension, io
from dotenv import load_dotenv

# Import our nodes
from .StringToListNode import StringToListNode

load_dotenv(".env")

class TuXsExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            StringToListNode,
        ]


async def comfy_entrypoint() -> ComfyExtension:  # ComfyUI calls this to load your extension and its nodes.
    return TuXsExtension()