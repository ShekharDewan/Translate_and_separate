import os
import glob
import json
import openai

# Set debug flag to True to enable detailed output.
DEBUG = True

# Instantiate a client using the new API interface.
from openai import OpenAI

OPENAI_API_KEY = "your-api-key-here"


client = openai.OpenAI(api_key=OPENAI_API_KEY)


# Mapping of file extensions to specific formatting instructions.
FORMAT_INSTRUCTIONS = {
    '.md': "The content is in Markdown format. Preserve all markdown formatting (e.g., headers, lists, bold, italics, code blocks) exactly.",
    '.html': "The content is in HTML format. Preserve all HTML tags and formatting exactly.",
    '.txt': "The content is plain text. Preserve all line breaks and whitespace exactly.",
    '.json': "The content is a JSON document. Preserve its structure and formatting exactly.",
    # Add more extensions as needed.
}

def translate_content(content: str, file_ext: str) -> str:
    """
    Translates the given content to English.
    
    Args:
        content: The text content from the file.
        file_ext: The file extension (e.g., '.md', '.html', '.txt').
        
    Returns:
        The translated text, with formatting preserved as much as possible.
    """
    # Choose formatting instructions based on the file extension.
    instruction = FORMAT_INSTRUCTIONS.get(file_ext.lower(), 
        "The content is plain text. Preserve all formatting (such as line breaks and whitespace) exactly."
    )
    
    # Construct the prompt. Notice we explicitly mention the file type.
    prompt = (
        f"The following text is extracted from a file with extension '{file_ext}'. {instruction}\n\n"
        "Translate all non-English sentences to English. Leave any text that is already in English unchanged. "
        "Preserve all formatting exactly. Output only the final translated content, with no additional commentary.\n\n"
        f"{content}"
    )
    
    if DEBUG:
        print("DEBUG: Prompt being sent:")
        print(prompt)
        print("-" * 40)
    
    try:
        # Use the new client method.
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a translation assistant that converts non-English text into English "
                        "while preserving all formatting as exactly as possible."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        
        if DEBUG:
            # Dump the response as a dictionary (using model_dump) for debugging.
            print("DEBUG: API response:")
            print(json.dumps(response.model_dump(), indent=2))
            print("-" * 40)
        
        # Extract the translation.
        translation = response.choices[0].message.content.strip()
        
        if DEBUG:
            print("DEBUG: Final translation output:")
            print(translation)
            print("-" * 40)
            
        return translation
    except Exception as e:
        print(f"Error during translation: {e}")
        return content

def process_files(input_folder: str, output_folder: str):
    """
    Processes all text-based files in the input folder. The file extension is used to adjust 
    translation instructions. Translated files are saved in the output folder.
    
    Args:
        input_folder: Directory containing source files.
        output_folder: Directory where translated files will be saved.
    """
    if not os.path.exists(input_folder):
        print(f"Input folder '{input_folder}' does not exist.")
        return
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Process any file with an extension (you can modify the glob pattern if needed)
    files = glob.glob(os.path.join(input_folder, "*.*"))
    if not files:
        print(f"No files found in {input_folder}.")
        return
    
    for filepath in files:
        filename = os.path.basename(filepath)
        file_ext = os.path.splitext(filename)[1]
        print(f"Processing file: {filepath} (extension: {file_ext})")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if DEBUG:
                print("DEBUG: Original file content:")
                print(content)
                print("-" * 40)
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            continue
        
        translated_content = translate_content(content, file_ext)
        output_filename = os.path.splitext(filename)[0] + "_translated" + file_ext
        output_path = os.path.join(output_folder, output_filename)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            print(f"Translated file saved as: {output_path}\n")
        except Exception as e:
            print(f"Error writing file {output_path}: {e}")

def test_translation():
    """
    Test function to translate a sample content containing mixed languages.
    """
    sample_content = (
        "Header: Welkom\n\n"
        "Dit is een voorbeeld. This sentence is in English.\n\n"
        "List:\n"
        "- Eerste punt\n"
        "- Second point\n\n"
        "Note: Zorg ervoor dat alle opmaak behouden blijft."
    )
    file_ext = ".txt"
    print("DEBUG: Running test translation with sample content:")
    print(sample_content)
    print("-" * 40)
    translated = translate_content(sample_content, file_ext)
    print("DEBUG: Translated sample content:")
    print(translated)
    print("-" * 40)

def main():
    # Uncomment the next line to run the test translation.
    # test_translation()
    
    # Specify your folder organization:
    # Place source files (of any text-based type) in "input_files"
    # Translated files will be written to "translated_files"
    input_folder = "input_files"
    output_folder = "translated_files"
    process_files(input_folder, output_folder)

if __name__ == '__main__':
    main()
