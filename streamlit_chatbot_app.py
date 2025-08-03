# Build a website about Chatbot with python
# cmd - streamlit run streamlit_chatbot_app.py
# cmd - Ctrl+c to stop
# cmd - pip freeze > requirements.txt

import time
import streamlit as st
# from openai import OpenAI
import requests

# Website config
st.set_page_config(
   page_title="JY Chatbot",
   page_icon="🚀",
   layout="centered",
   initial_sidebar_state="expanded",
   menu_items={}
)

# Website title
st.title('This is a website about Ai Chatbot!')

# Time progress bar
bar = st.progress(0)
for i in range(100):
    bar.progress(i + 1, f'In progress... {i+1} %')
    time.sleep(0.05)

bar.progress(100, 'Completed！')



# Function of Chatbot by OpenRouter API
def chat_with_openrouter(api_key, message, model_selected):
    # Define the API endpoint for chat completions
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Set up the headers for the API request, including authorization
    headers = {
        "Authorization": f"Bearer {api_key}",  # Bearer token for authentication
        "Content-Type": "application/json"  # Specify the content type as JSON
    }
    
    # Create the payload with the model and messages
    payload = {
        "model": model_selected,  # The selected model for the chatbot
        "messages": [  # The conversation history
            {"role": "system", "content": "You are a helpful assistant."},  # System message defining the assistant's role
            {"role": "user", "content": message}  # User's input message
        ],
        "stream": False  # Disable streaming responses
    }
    
    # Send a POST request to the OpenRouter API
    response = requests.post(url, headers=headers, json=payload)
    
    # Check if the response was successful (HTTP status code 200)
    if response.status_code == 200:
        # Return the content of the assistant's response
        return response.json()['choices'][0]['message']['content']
    else:
        # Return an error message if the request failed
        return f"Error: {response.status_code}, {response.text}"



# Build a chat agent
# Set OpenAI API key from Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Set a default model
my_model_selected = "google/gemma-3-27b-it:free"

# Display initial chat message
with st.chat_message("assistant"): 
    response = "Hi 👋, I am JY Chatbot 🤖 , feel free to ask me anything!"
    st.write(response)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type something or type 'exit' to end... "):
    # Check for exit command
    if prompt.lower() == "exit":
        st.session_state.messages.append({"role": "user", "content": "You have exited the chat."})
        with st.chat_message("user"):
            st.markdown("You have exited the chat.")
        st.stop()  # Stops the Streamlit app
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            try:
                # Call the chat function and get the response
                response = chat_with_openrouter(api_key, prompt, my_model_selected)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
