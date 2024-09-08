import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog, filedialog
from fuzzywuzzy import process
import csv
import pdfplumber
import spacy
import string

# Load the SpaCy NLP model
nlp = spacy.load("en_core_web_sm")

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def load_data(filepath):
    data = {}
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = remove_punctuation(row['question'].lower())
            answer = row['answer']
            data[question] = answer
    return data

def save_data(filepath, data):
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['question', 'answer'])
        for question, answer in data.items():
            writer.writerow([question, answer])

def get_response(user_input, data):
    user_input = remove_punctuation(user_input.lower())
    return data.get(user_input, None)

def fuzzy_match(user_input, data):
    questions = list(data.keys())
    match, score = process.extractOne(user_input, questions)
    if score > 80:
        return match, data[match]
    return None, None

def read_csv(filepath):
    data = {}
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = remove_punctuation(row['question'].lower())
            answer = row['answer']
            data[question] = answer
    return data

def read_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def load_keywords(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return [remove_punctuation(line.strip().lower()) for line in file]

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot")
        self.data = load_data("faqs.csv")
        self.keywords = load_keywords("data.txt")

        self.chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
        self.chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.user_input = tk.Entry(self.input_frame)
        self.user_input.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, sticky="e", padx=5, pady=5)

        self.feedback_button = tk.Button(self.input_frame, text="Feedback", command=self.get_feedback)
        self.feedback_button.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        self.input_frame.columnconfigure(0, weight=1)

        self.last_user_input = ""
        self.last_response = ""
        self.feedback_data = {}

    def send_message(self, event=None):
        user_text = self.user_input.get().strip()
        if user_text:
            self.display_message("User: " + user_text, color='red')
            user_text_clean = remove_punctuation(user_text.lower())
            
            response = get_response(user_text_clean, self.data)
            if response:
                self.display_message("Chatbot: " + response, color='black')
            else:
                if len(user_text.split()) <= 2:
                    self.display_message("Chatbot: Please provide more details for a specific answer.", color='black')
                elif "what is the" in user_text_clean:
                    if not any(keyword in user_text_clean for keyword in self.keywords):
                        self.display_message("Chatbot: Please specify the city, place, country, or planet.", color='black')
                    else:
                        matched_prompt, response = fuzzy_match(user_text_clean, self.data)
                        if response:
                            self.display_message(f"Chatbot: (Matched prompt: {matched_prompt})\n{response}", color='black')
                        else:
                            self.display_message("Chatbot: I'm sorry, I don't have an answer for that. Please provide more details.", color='black')
                else:
                    matched_prompt, response = fuzzy_match(user_text_clean, self.data)
                    if response:
                        self.display_message(f"Chatbot: (Matched prompt: {matched_prompt})\n{response}", color='black')
                    else:
                        self.display_message("Chatbot: I'm sorry, I don't have an answer for that. Please provide more details.", color='black')
            
            self.user_input.delete(0, tk.END)
            self.last_user_input = user_text
            self.last_response = response

    def display_message(self, message, color='black'):
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, message + "\n", color)
        self.chat_window.tag_config(color, foreground=color)
        self.chat_window.config(state='disabled')
        self.chat_window.yview(tk.END)

    def get_feedback(self):
        if self.last_user_input and self.last_response:
            feedback = messagebox.askquestion("Feedback", f"Was this response helpful?\n\nUser Input: {self.last_user_input}\nResponse: {self.last_response}")
            if feedback == 'no':
                self.feedback_data[remove_punctuation(self.last_user_input.lower())] = True
                messagebox.showinfo("Feedback", "Thank you for your feedback! I will ask for more details next time.")
            else:
                messagebox.showinfo("Feedback", "Thank you for your feedback!")
        else:
            messagebox.showinfo("Feedback", "No recent message to provide feedback on.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()