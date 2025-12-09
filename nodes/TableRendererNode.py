import os
import sys
from comfy_api.latest import io

# 处理模块导入 - 确保父目录在 sys.path 中
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 直接导入模块，不经过 utils.__init__
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "TableRenderer",
        os.path.join(parent_dir, "utils", "TableRenderer.py")
    )
    table_renderer_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(table_renderer_module)
    TableRenderer = table_renderer_module.TableRenderer
except Exception as e:
    print(f"[TableRendererNode] 导入失败: {e}")
    import traceback
    traceback.print_exc()
    raise


class TableRendererNode(io.ComfyNode):
    """
    表格渲染节点
    根据 JSON 数据填充 HTML 表格模板
    
    Class methods
    -------------
    define_schema (io.Schema):
        定义节点元数据、输入输出参数
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        """
        定义节点架构
        """
        return io.Schema(
            node_id="TableRendererNode",
            display_name="Table Renderer",
            category="tuxiansheng/tables",
            inputs=[
                io.String.Input(
                    "html_template",
                    multiline=True,
                    default="",
                    lazy=True,
                    tooltip="HTML 模板字符串，必须包含 <tbody> 和表头行",
                ),
                io.String.Input(
                    "json_data",
                    multiline=True,
                    default="{}",
                    lazy=True,
                    tooltip="JSON 数据字符串，格式: {\"data\": [{...}]}",
                ),
            ],
            outputs=[
                io.String.Output(display_name="HTML Output"),  # 渲染后的HTML字符串
            ],
        )

    @classmethod
    def check_lazy_status(cls, html_template, json_data):
        """
        控制惰性输入的评估时机
        
        总是需要评估所有输入参数
        """
        return ["html_template", "json_data"]

    @classmethod
    def execute(cls, html_template, json_data) -> io.NodeOutput:
        """
        执行节点逻辑
        
        Parameters:
        -----------
        html_template: str
            HTML 模板字符串
        json_data: str
            JSON 数据字符串
            
        Returns:
        --------
        NodeOutput
            包含渲染后的 HTML 字符串
        """
        try:
            # 验证输入
            if not html_template:
                raise ValueError("HTML 模板字符串不能为空")
            
            if not json_data:
                raise ValueError("JSON 数据字符串不能为空")
            
            # 初始化渲染器
            renderer = TableRenderer()
            
            # 渲染表格
            try:
                filled_html = renderer.render_table_from_strings(
                    html_template=html_template,
                    json_data_str=json_data
                )
                
                print(f"[TableRendererNode] 表格渲染成功")
                return io.NodeOutput(filled_html)
                
            except ValueError as e:
                error_msg = f"HTML 模板格式错误: {str(e)}"
                print(f"[TableRendererNode] {error_msg}")
                return io.NodeOutput(f"<!-- 错误: {error_msg} -->")
            except Exception as e:
                error_msg = f"渲染失败: {str(e)}"
                print(f"[TableRendererNode] {error_msg}")
                return io.NodeOutput(f"<!-- 错误: {error_msg} -->")
        
        except Exception as e:
            error_msg = f"节点执行失败: {str(e)}"
            print(f"[TableRendererNode] {error_msg}")
            return io.NodeOutput(f"<!-- 错误: {error_msg} -->")


# 节点映射配置
NODE_CLASS_MAPPINGS = {
    "TableRendererNode": TableRendererNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TableRendererNode": "Table Renderer"
}
