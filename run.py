import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from docx import Document

# Load the API key from the environment
from dotenv import load_dotenv
import os
import re
c
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

model = GeminiModel('gemini-2.0-flash', api_key=API_KEY)
agent = Agent(model)

# Define the prompt to clean and structure the text
CLEAN_TEXT_PROMPT = """"
You are a text editor assistant. Your task is to clean, structure, and format the given text.
Ensure proper paragraphing and correct punctuation (., !, ?). Maintain the original meaning. Also ignore anything between [] like [Music] or [Applause].

Input text:
{input_text}

Return only the cleaned text, without extra comments.
"""


async def process_text(input_text: str, output_file: str):
    """Cleans and structures the input text using Pydantic AI"""
    
    # Let's remove the words in brackets, like [Music] or [Applause]
    input_text_cleaned = re.sub(r"\[.*?\]", "", input_text)
    
    # Run the agent with the formatted prompt
    result = await agent.run(CLEAN_TEXT_PROMPT.format(input_text=input_text_cleaned))
    
    # Get the cleaned text
    cleaned_text = result.data

    # Save to .docx
    doc = Document()
    for paragraph in cleaned_text.split("\n\n"):
        doc.add_paragraph(paragraph.strip())
    doc.save(output_file.replace(".txt", ".docx"))

    print(f"Processed text saved to {output_file} and {output_file.replace('.txt', '.docx')}")

# Example: Read input from a file and process it
if __name__ == "__main__":
    # input_file = "data/dataBill_Schuffenhauer.txt"
    # input_file = os.path.join("data", "Bill_Schuffenhauer.txt")
    input_file = os.path.join("data", "Erin_Cafaro.txt")
    # Make the output file name the same as the input file with a different extension
    output_file = input_file.replace(".txt", "_cleaned.txt")

    # Read the raw text
    with open(input_file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Run the text processing pipeline
    asyncio.run(process_text(raw_text, output_file))