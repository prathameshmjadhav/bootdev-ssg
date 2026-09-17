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
