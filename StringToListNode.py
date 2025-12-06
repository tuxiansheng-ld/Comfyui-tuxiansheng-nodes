from comfy_api.latest import io


class StringToListNode(io.ComfyNode):
    """
    A node that splits a string by a delimiter and returns a list of strings
    
    Class methods
    -------------
    define_schema (io.Schema):
        Defines the node metadata, input and output parameters
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        """
            Return a schema which contains all information about the node.
            Some types: "Model", "Vae", "Clip", "Conditioning", "Latent", "Image", "Int", "String", "Float", "Combo".
            For outputs the "io.Model.Output" should be used, for inputs the "io.Model.Input" can be used.
            The type can be a "Combo" - this will be a list for selection.
        """
        return io.Schema(
            node_id="StringToListNode",
            display_name="String To List",
            category="tuxiansheng/utils",
            inputs=[
                io.String.Input(
                    "input_string",
                    multiline=True,  # Allow multiline input
                    default="",  # Empty default
                ),
                io.String.Input(
                    "delimiter",
                    multiline=False,
                    default=",",  # Default delimiter is comma
                )
            ],
            outputs=[
                io.AnyType.Output(),  # Output as a list of strings
                io.Int.Output(),  # Output the length of the list
            ],
        )

    @classmethod
    def execute(cls, input_string, delimiter) -> io.NodeOutput:
        """
        Split the input string by the delimiter and return the resulting list
        """
        # Handle edge cases
        if not input_string:
            result = []
            return io.NodeOutput(result, len(result))
        
        if not delimiter:
            # If delimiter is empty, return each character as a separate item
            result = list(input_string)
            return io.NodeOutput(result, len(result))
            
        # Split the string by the delimiter, keep original content without stripping
        # to preserve Chinese and other Unicode characters
        result = [item for item in input_string.split(delimiter) if item]
        return io.NodeOutput(result, len(result))