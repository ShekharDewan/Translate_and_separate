
import os
import glob
import json
from openai import OpenAI
from typing import Dict, Optional

# Easy API key configuration - just replace this value

OPENAI_API_KEY = "your-api-key-here"

class ConversationSeparator:
    def __init__(self, api_key: str):
        """Initialize the separator with OpenAI client."""
        self.client = OpenAI(api_key=api_key)

    def _validate_json_response(self, json_str: str) -> Dict[str, str]:
        """Validate and clean up JSON response from OpenAI."""
        try:
            cleaned_json = json_str.strip('```json\n').strip('```')
            result = json.loads(cleaned_json)
            
            if not isinstance(result.get("business"), str) or not isinstance(result.get("personal"), str):
                raise ValueError("Invalid response format")
                
            return {
                "business": result["business"].strip(),
                "personal": result["personal"].strip()
            }
        except json.JSONDecodeError:
            return {"business": "", "personal": ""}

    def separate_conversations(self, content: str, file_ext: str) -> Dict[str, str]:
        """Send text content to OpenAI and get separated conversations."""
        prompt = f"""Analyze and separate the following text into business and personal conversations.
        Return a JSON object with 'business' and 'personal' keys containing the separated text.
        Do not wrap the JSON in markdown code blocks. Preserve all original formatting.
        File type: {file_ext}

        Text to separate:
        {content}"""

        try:
            print("    Sending to GPT-4o for analysis...")
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Explicitly using gpt-4o as requested
                messages=[
                    {"role": "system", "content": "You are a precise text classifier that separates text into business and personal conversations. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            
            raw_output = response.choices[0].message.content.strip()
            return self._validate_json_response(raw_output)
            
        except Exception as e:
            print(f"    Error during API call: {str(e)}")
            return {"business": "", "personal": content}

    def process_file(self, filepath: str, personal_folder: str, business_folder: str) -> bool:
        """Process a single file and write separated content to respective folders."""
        try:
            base_filename = os.path.basename(filepath)
            print(f"\nProcessing: {base_filename}")
            
            file_ext = os.path.splitext(base_filename)[1]
            filename_without_ext = os.path.splitext(base_filename)[0]

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            separation = self.separate_conversations(content, file_ext)

            for content_type, content_text in separation.items():
                if not content_text:
                    continue

                output_folder = business_folder if content_type == "business" else personal_folder
                output_filename = f"{filename_without_ext}_{content_type}{file_ext}"
                output_path = os.path.join(output_folder, output_filename)

                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content_text)
                print(f"    Created: {output_filename}")
            
            print(f"✓ Completed: {base_filename}")
            return True
        except Exception as e:
            print(f"× Failed to process {base_filename}: {str(e)}")
            return False

def process_conversations(input_folder: str, personal_folder: str, business_folder: str) -> bool:
    """Main function to process conversations."""
    try:
        print("\n=== Starting Conversation Separator ===")
        
        # Create output folders if they don't exist
        for folder in [personal_folder, business_folder]:
            os.makedirs(folder, exist_ok=True)

        # Initialize separator with the API key
        separator = ConversationSeparator(api_key=OPENAI_API_KEY)

        # Process all files in input folder
        files = glob.glob(os.path.join(input_folder, "*.*"))
        if not files:
            print("No files found to process!")
            return False

        print(f"\nFound {len(files)} files to process...")
        
        success = True
        for i, filepath in enumerate(files, 1):
            print(f"\n[{i}/{len(files)}]")
            if not separator.process_file(filepath, personal_folder, business_folder):
                success = False

        print("\n=== Processing Complete ===")
        print(f"Results saved in:\n- {personal_folder}\n- {business_folder}")
        
        return success
    except Exception as e:
        print(f"\nError during processing: {str(e)}")
        return False

if __name__ == '__main__':
    # Example usage - just run this file after setting your API key above
    success = process_conversations(
        input_folder="translated_files",
        personal_folder="personal_conversations",
        business_folder="business_conversations"
    )
    print("\nFinal Status:", "✓ Success" if success else "× Failed")