from typing_extensions import override

from comfy_api.latest import ComfyExtension, io



class TuXsExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            Example,
        ]


async def comfy_entrypoint() -> ExampleExtension:  # ComfyUI calls this to load your extension and its nodes.
    return TuXsExtension()
