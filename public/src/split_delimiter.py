from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    # This function takes a list of TextNodes and looks for a specific
    # delimiter (like "_" or "**") inside any plain TEXT nodes, splitting
    # them into separate TEXT and formatted nodes.
    new_nodes = []

    for node in old_nodes:
        # If a node is already formatted (e.g. BOLD from a previous pass),
        # we don't touch it — just pass it through unchanged.
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Split the text on the delimiter.
        # Example: "a _b_ c".split("_") -> ['a ', 'b', ' c']
        parts = node.text.split(delimiter)

        # If the delimiter appears an odd number of times, split() will
        # return an EVEN number of parts, meaning one delimiter is unmatched
        # (e.g. "a _b c" -> ['a ', 'b c'] -> only 2 parts, unbalanced).
        if len(parts) % 2 == 0:
            raise ValueError(
                f"Unmatched delimiter {delimiter!r} in text: {node.text!r}"
            )

        # Walk through the split parts. Because delimiters come in pairs,
        # content ALTERNATES between "outside" and "inside" the delimiter:
        #   index 0 -> outside (plain text)
        #   index 1 -> inside (formatted, e.g. italic)
        #   index 2 -> outside (plain text)
        #   ...and so on
        for i, part in enumerate(parts):
            if part == "":
                # Skip empty strings (happens when delimiter is at the
                # very start/end of the text, e.g. "_hello_" -> ['', 'hello', ''])
                continue

            if i % 2 == 0:
                # Even index = text OUTSIDE the delimiter = plain text
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Odd index = text INSIDE the delimiter = formatted text
                new_nodes.append(TextNode(part, text_type))

    return new_nodes
