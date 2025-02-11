# Translate_and_separate
Translates text from any language to english (leaving english unchanged), then separates personal and business requirements

**Remember: Run the translation program first, then run the conversation separator program.**

---

### **1. Translation Program**

**Purpose:**  
Converts your source files (which might contain non‑English text) into fully translated files while preserving all formatting.

**Setup & Usage:**

1. **API Key:**  
   - Open the translation program file.  
   - At the very top, replace the placeholder value in the line:  
     ```python
     API_KEY = "sk-your-api-key-here"
     ```  
     with your actual OpenAI API key.

2. **Folder Structure:**  
   - Create a folder named **`input_files`** and place your source files (e.g., `.txt`, `.md`, `.html`) there.  
   - The program will save the translated files into a folder named **`translated_files`** (it will create this folder if it doesn’t exist).

3. **Run the Program:**  
   - Execute the script (e.g., run `python translation_program.py`).  
   - The program will display brief status updates (e.g., “Processing file: [filename]…” and “Completed processing file: [filename]…”).

4. **Output:**  
   - Check the **`translated_files`** folder for the translated versions of your files.

---

### **2. Conversation Separator Program**

**Purpose:**  
Takes the translated files and separates their contents into “business” and “personal” conversations, writing the results into two distinct folders.

**Setup & Usage:**

1. **API Key:**  
   - Open the conversation separator program file.  
   - At the top, replace the placeholder API key value in the line:  
     ```python
     OPENAI_API_KEY = "sk-your-real-api-key"
     ```  
     with your actual API key.

2. **Folder Structure:**  
   - Ensure that the **`translated_files`** folder (produced by the translation program) is in the same directory as this script.  
   - The program will create (if needed) two folders: **`personal_conversations`** and **`business_conversations`**.

3. **Run the Program:**  
   - Execute the script (e.g., run `python conversation_separator.py`).  
   - The program prints brief messages for each file processed (e.g., “Processing: [filename]”, “Created: [output_filename]”, “✓ Completed: [filename]”).

4. **Output:**  
   - Files that contain business content are saved in **`business_conversations`**.  
   - Files that contain personal content are saved in **`personal_conversations`**.  
   - For mixed files, two separate files (one for each category) are created with suffixes `_business` and `_personal`.

---

**Summary:**  
1. **First, run the Translation Program** to convert your original files (in `input_files/`) into translated files (in `translated_files/`).  
2. **Then, run the Conversation Separator Program** to split the translated files into business and personal content, with the outputs saved in `business_conversations/` and `personal_conversations/`.
