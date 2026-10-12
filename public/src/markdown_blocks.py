from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
 
 
def block_to_block_type(block):
    lines = block.split("\n")
 
    # Heading: 1-6 '#' characters, a space, then text
    if re.match(r"^#{1,6} \S", block):
        return BlockType.HEADING
 
    # Code: starts with ``` and a newline, ends with ```
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
 
    # Quote: every line starts with '>'
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
 
    # Unordered list: every line starts with '- '
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
 
    # Ordered list: lines start with "1. ", "2. ", "3. ", ...
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
 
    return BlockType.PARAGRAPH
    
    


def markdown_to_blocks(text:str) -> list[str]:
    raw_blocks = text.split("\n\n")
    blocks = []
    
    for block in raw_blocks:
        # Remove leading/trailing spaces and single newlines
        cleaned_block = block.strip()
        
        # Only add the block if it contains actual content
        if cleaned_block != "":
            blocks.append(cleaned_block)
            
    return blocks

