import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_node: list[TextNode] = []

    for node in old_nodes:
        # if the node is not of type.Text.. then it must be the of the mentioned texttype of TextType enums (i.e. Bold, Italic, Code, etc)
        # Hence just append that node
        if node.text_type != TextType.TEXT:
            new_node.append(node)
            continue

        sections = node.text.split(delimiter)
        split_nodes = []

        # The sentence(text) when it split, the length of sections will always be an odd number. If not, then it is not valid
        if len(sections) % 2 == 0:
            raise ValueError("Invalid use delimiter")

        for i in range(len(sections)):
            # this ensures that even if the wrapped text (in italic or code or bold) occurs in the first word of the sentence, it is handled
            # in python if the delimiter is in the first word then the first item of the list is empty string
            # for eg ```**This** is an apple. is split into list as ["", "This", "is an apple"]
            if sections[i] == "":
                continue

            # The text nodes will always appear at the even number (0,2,4...)
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))

            # The special types will always occur at the odd numbek
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_node.extend(split_nodes)

    return new_node


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes:list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue


        images_list = extract_markdown_images(node.text)

        if len(images_list) == 0:
            new_nodes.append(node)
            continue
        

        node_text = node.text

        for image in images_list:
            splits = node_text.split(f"![{image[0]}]({image[1]})",maxsplit=1)

            if splits[0] == '':
                new_nodes.append(TextNode(text=image[0], text_type=TextType.IMAGE, url=image[1]))
                node_text = splits[len(splits) - 1]
                continue

            new_nodes.append(TextNode(text=splits[0], text_type=TextType.TEXT))
            new_nodes.append(TextNode(text=image[0], text_type=TextType.IMAGE, url=image[1]))
            
            node_text = splits[len(splits) - 1]

        if node_text != '':
            new_nodes.append(TextNode(text=node_text, text_type=TextType.TEXT))
            

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes:list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        link_list = extract_markdown_links(node.text)

        if len(link_list) == 0:
            new_nodes.append(node)
            continue
        

        node_text = node.text

        for link in link_list:
            splits = node_text.split(f"[{link[0]}]({link[1]})",maxsplit=1)

            if splits[0] == '':
                new_nodes.append(TextNode(text=link[0], text_type=TextType.LINK, url=link[1]))
                node_text = splits[len(splits) - 1]
                continue

            new_nodes.append(TextNode(text=splits[0], text_type=TextType.TEXT))
            new_nodes.append(TextNode(text=link[0], text_type=TextType.LINK, url=link[1]))
            
            node_text = splits[len(splits) - 1]

        if node_text != '':
            new_nodes.append(TextNode(text=node_text, text_type=TextType.TEXT))

    return new_nodes




























    
