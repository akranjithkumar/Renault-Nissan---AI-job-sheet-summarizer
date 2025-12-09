import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import pypdf
import os 

from llm_service import ollama_summarize_section 

BG_PRIMARY = "#1e1e1e"     
BG_SECONDARY = "#2c2c2c"   
ACCENT_BLUE = "#3498db"    
FG_PRIMARY = "#ffffff"     
FONT_FAMILY = "Segoe UI"   


def clear_output_fields():
    complaint_output.delete('1.0', tk.END)
    diagnosis_output.delete('1.0', tk.END)
    action_output.delete('1.0', tk.END)


def process_pdf_and_summarize():
    
    file_path = filedialog.askopenfilename(
        title="Open PDF File", 
        filetypes=[("PDF files", "*.pdf")]
    )
    
    if not file_path:
        return

    clear_output_fields()
    
    status_label.config(text=f"Processing file: {os.path.basename(file_path)}...")
    window.update() 

    try:
        full_text_str = ""
        with open(file_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                     full_text_str += text + "\n"
        
        if not full_text_str.strip():
            messagebox.showerror("Error", "PDF file is empty or text extraction failed.")
            status_label.config(text="Ready.")
            return

        cleaned_text = ' '.join(full_text_str.split()) 
        
        
        # 1 Customer Complaint
        status_label.config(text="Summarizing Complaint (1/3)...")
        window.update()
        complaint_summary = ollama_summarize_section(cleaned_text, "complaint")
        complaint_output.insert(tk.END, complaint_summary)
        
        # 2 Diagnosis Comment
        status_label.config(text="Summarizing Diagnosis (2/3)...")
        window.update()
        diagnosis_summary = ollama_summarize_section(cleaned_text, "diagnosis")
        diagnosis_output.insert(tk.END, diagnosis_summary)

        # 3 Action Taken
        status_label.config(text="Summarizing Action (3/3)...")
        window.update()
        action_summary = ollama_summarize_section(cleaned_text, "action")
        action_output.insert(tk.END, action_summary)
        
        # 4 Final Status
        status_label.config(text="Summarization Complete.")
        
    except Exception as e:
        messagebox.showerror("An Error Occurred", f"Failed during processing: {e}")
        status_label.config(text="Error.")


def create_output_section(parent, title, row):
    label = tk.Label(parent, text=title, bg=BG_PRIMARY, fg=FG_PRIMARY, 
                     font=(FONT_FAMILY, 11, 'bold'), anchor='w')
    label.grid(row=row, column=0, sticky='w', pady=(15, 5))
    
    text_area = scrolledtext.ScrolledText(parent, wrap=tk.WORD, height=4, width=80, 
                                          bg=BG_SECONDARY, fg=FG_PRIMARY, 
                                          insertbackground=FG_PRIMARY, 
                                          bd=0, 
                                          highlightthickness=1, 
                                          highlightbackground=BG_SECONDARY,
                                          highlightcolor=ACCENT_BLUE, 
                                          font=(FONT_FAMILY, 10))
    text_area.grid(row=row+1, column=0, sticky='ew', padx=0, pady=5)
    
    return text_area


# --- Main Window Setup ---

window = tk.Tk()
window.title("Renault Nissan - AI Job Sheet Summarizer")
window.geometry("800x600")
window.configure(bg=BG_PRIMARY)

# Header Frame 
header_frame = tk.Frame(window, bg=ACCENT_BLUE, height=60, relief='flat')
header_frame.pack(fill='x', padx=0, pady=0)

title_label = tk.Label(header_frame, text="Renault Nissan - AI Job Sheet Summarizer", bg=ACCENT_BLUE, fg=BG_PRIMARY, 
                       font=(FONT_FAMILY, 16, 'bold'))
title_label.pack(side=tk.LEFT, padx=20, pady=10)

open_pdf_button = tk.Button(header_frame, text="OPEN PDF", command=process_pdf_and_summarize, 
                            bg=BG_PRIMARY, fg=ACCENT_BLUE, 
                            font=(FONT_FAMILY, 12, 'bold'), 
                            relief=tk.FLAT, bd=0, 
                            padx=15)
open_pdf_button.pack(side=tk.RIGHT, padx=20, pady=10)

# Main Content Frame
main_frame = tk.Frame(window, bg=BG_PRIMARY, padx=20, pady=10)
main_frame.pack(fill='both', expand=True)

# Output Sections
complaint_output = create_output_section(main_frame, "Customer Complaint:", 0)s
diagnosis_output = create_output_section(main_frame, "Diagnosis Comment:", 2)
action_output = create_output_section(main_frame, "Action Taken:", 4)


# Status Bar
status_frame = tk.Frame(window, bg=BG_SECONDARY, height=30)
status_frame.pack(fill='x', side=tk.BOTTOM)

status_label = tk.Label(status_frame, text="Ready. Please ensure Ollama is running.", bg=BG_SECONDARY, fg='gray', 
                        font=(FONT_FAMILY, 9), anchor='w')
status_label.pack(side=tk.LEFT, padx=10, fill='x', expand=True)

main_frame.grid_columnconfigure(0, weight=1)

if __name__ == '__main__':
    window.mainloop()
