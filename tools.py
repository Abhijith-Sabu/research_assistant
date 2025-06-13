from smolagents import tool
from datetime import datetime
@tool
def save_to_txt(data: str, filename: str = "research_output.txt")-> str:
    """
    Use this to save final structured research output to a text file. Only use if the user asks to save or store the information
    
    Args:
        data: The research data or content to save to the file
        filename: The name of the file to save to (default: research_output.txt)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
   
    return f"Data successfully saved to {filename}"