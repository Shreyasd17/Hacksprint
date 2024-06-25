import os
from pdfplumber.pdf import Pdf
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Define the extract_data_from_pdfs function
def extract_data_from_pdfs(file_path, pdf_files):
    text_data = []
    for file in pdf_files:
        with open(os.path.join(file_path, file), "rb") as pdf_file:
            pdf = Pdf(pdf_file)
            for page in pdf.pages:
                text_data.append(page.extract_text())
    return " ".join(text_data)

# List of PDF files to process
pdf_files = ["C:\\Users\\Dell\\Desktop\\chatbot\\data\\ebooks_academic_geop4e_frontmatter.pdf", "C:\\Users\\Dell\\Desktop\\chatbot\\data\\Gale-Encyclopedia-of-Psychology-2nd-ed.-2001.pdf","C:\\Users\\user\\Documents\\GitHub\\AlienAlgorithms_HackSpirit\\data\\textbook medical.pdf"]

# Extract text data from specified PDFs and preprocess it
file_path = "data"
text_data = extract_data_from_pdfs(file_path, pdf_files)

# Convert text to lowercase, remove stopwords, punctuation, and special characters, and tokenize it
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

words = word_tokenize(text_data.lower())
words = [word for word in words if word.isalnum()]
words = [word for word in words if word not in stop_words]
words = [stemmer.stem(word) for word in words]

# Save the preprocessed text data in a text file
with open("preprocessed_text_data.txt", "w") as file:
    file.write(" ".join(words))