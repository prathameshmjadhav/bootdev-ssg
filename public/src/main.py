from public.src.htmlnode import HTMLNode
from textnode import TextNode, TextType

print("hello world")


def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

    node2 = HTMLNode(
        tag="a", props={"href": "https://www.google.com", "target": "_blank"}
    )

    print(node2)


main()
