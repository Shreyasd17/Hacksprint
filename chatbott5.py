import streamlit as st
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline
import torch
import PyPDF2

def get_health_tip():
    return "A healthy diet and regular exercise are important for maintaining good health."

# Load the T5 model and tokenizer
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# Function for generating T5 response
def generate_t5_response(prompt_input):
    with torch.no_grad():
        input_ids = tokenizer.encode(prompt_input, return_tensors="pt")
        output = model.generate(input_ids, max_length=512, num_return_sequences=1, no_repeat_ngram_size=2)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Load data from multiple PDFs
def load_data():
    # Read the preprocessed data from the preprocessing.py file
    with open("preprocessed_data.txt", "r") as file:
        text_data = file.read()
    return text_data


    text_data = ""
    for pdf_file_path in pdf_file_paths:
        pdf_file = open(pdf_file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_data += page.extract_text()

        pdf_file.close()

    return text_data

# Initialize a question-answering pipeline
qa_pipeline = pipeline("question-answering")

# Store T5 generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Clear chat history button
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', key="clear_chat_history_button", on_click=clear_chat_history)

# Process user input
def process_input(user_input):
    global data
    with st.spinner("Thinking..."):
        if "health" in user_input.lower():
            response = get_health_tip()
        elif "psychology" in user_input.lower():
            # Replace this with your logic for psychology-related responses
            response = generate_t5_response(user_input)
        else:
            # Standard response for non-relevant queries
            response = "I don't have enough data to answer that. Let's talk about mental health or psychology."

        st.session_state.messages.append({"role": "user", "content": f"You: {user_input}"})
        st.session_state.messages.append({"role": "assistant", "content": f"Assistant: {response}"})

# User input field
user_input = st.text_input("You:", key="user_input")

# Process input on button click
if st.button("Send", key="send_button"):
    if user_input.strip() != "":
        process_input(user_input)
