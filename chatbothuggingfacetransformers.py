import streamlit as st
from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline
import torch
import PyPDF2

def get_health_tip():
    return "A healthy diet and regular exercise are important for maintaining good health."

# Load the GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# App title
st.set_page_config(page_title=" GPT-2 Chatbot")

# Function for generating GPT-2 response
def generate_gpt2_response(prompt_input):
    with torch.no_grad():
        input_ids = tokenizer.encode(prompt_input, return_tensors="pt")
        output = model.generate(input_ids, max_length=512, num_return_sequences=1, no_repeat_ngram_size=2)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Load data from multiple PDFs
def load_data():
    pdf_file_paths = [
        "data/ebooks_academic_geop4e_frontmatter.pdf"
    ]

    text_data = ""
    for pdf_file_path in pdf_file_paths:
        pdf_file = open(pdf_file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_data += page.extract_text()

        pdf_file.close()

    return text_data

# Load the data before using it in the pipeline
data = load_data()

# Initialize a question-answering pipeline
qa_pipeline = pipeline("question-answering")

# Store GPT-2 generated responses
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
        if "health tip" in user_input.lower():
            health_tip = get_health_tip()
            response = health_tip
        else:
            answer = qa_pipeline(question=user_input, context=data)  # Use the loaded text as context
            response = answer["answer"]
    return response

# User prompt and response
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate response if the last message is not from the assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = process_input(prompt)
                st.write(response)
                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)
