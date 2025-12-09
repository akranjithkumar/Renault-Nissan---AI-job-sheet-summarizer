import ollama

#Ollama Configuration
LLM_MODEL = 'llama2:7b'

def ollama_summarize_section(full_text, section_type):

    try:
        if section_type == "complaint":
            instruction = "From the text provided, give the summary of the customer complaint in only one line as a phrase with double quotes. Start with 'Concern:'"
        elif section_type == "diagnosis":
            instruction = "From the text provided, give the summary of the diagnosis comment in only one line as a phrase with double quotes. Start with 'Verified concern: '"
        elif section_type == "action":
            instruction = "From the text provided, give the summary of how the problem was solved by the company in one line as a phrase with double quotes. Start with 'Rectified by: '"
        else:
            return "ERROR: Invalid section type."

        full_prompt = f"{full_text}\n\n{instruction}"
        
        response = ollama.generate(
            model=LLM_MODEL, 
            prompt=full_prompt, 
            stream=False
        )
        
        summary = response['response'].strip()
        
        return summary
        
    except ollama.RequestError as e:
        return f"ERROR: Ollama is not running or model '{LLM_MODEL}' not found. Check your server status."
    except Exception as e:
        return f"ERROR: Failed to process LLM request ({e})"