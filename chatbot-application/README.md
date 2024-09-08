# Chatbot Application

This is a simple chatbot application built using Python and several libraries including Tkinter, FuzzyWuzzy, SpaCy, and pdfplumber. The chatbot can answer questions based on a predefined dataset and can also learn from user feedback.

## Features

- **Natural Language Processing**: Uses SpaCy for basic NLP tasks.
- **Fuzzy Matching**: Uses FuzzyWuzzy for matching user input to predefined questions.
- **PDF Reading**: Uses pdfplumber to extract text from PDF files.
- **User Feedback**: Allows users to provide feedback on the chatbot's responses.
- **Learning Mechanism**: The chatbot can learn from user feedback and improve over time.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/chatbot-application.git
   cd chatbot-application
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Download SpaCy Model**

   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

1. **Run the Application**

   ```bash
   python chatbot.py
   ```

2. **Interact with the Chatbot**

   - Enter your question in the input box and press "Send".
   - Use the "Feedback" button to provide feedback on the chatbot's response.

## Data Files

- **faqs.csv**: A CSV file containing predefined questions and answers.
- **data.txt**: A text file containing keywords for fuzzy matching.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## Acknowledgments

- Thanks to the developers of the libraries used in this project.
- Inspired by various chatbot implementations and tutorials.

### Additional Notes

1. **Replace Placeholders**: Make sure to replace `https://github.com/yourusername/chatbot-application.git` with the actual URL of your repository.

2. **Data Files**: Ensure that the `faqs.csv` and `data.txt` files are included in your repository or provide instructions on how to create them.

By including this `README.md` file, you provide a clear and structured way for others to understand, install, and use your chatbot application.