import streamlit as st
from views.chatbot_functions.response import response_generator
import time

# Clear chat button
if st.button("Nova Conversa"):
    st.session_state.messages = []
    # Refresh the page to clear the chat history
    st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Display welcome message
    st.session_state.messages.append({"role": "assistant", "content": "Oi! Eu sou o Lucas, seu OKR expert. Vamos criar uma nova OKR?"})


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    # Define the avatar based on the role
    avatar = "assets/okr_expert.png" if message["role"] == "assistant" else ":material/person:"
    
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Como posso te ajudar hoje?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user", avatar=":material/person:"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar="assets/okr_expert.png"):
        response = response_generator(prompt,st.session_state.messages)  # Get the assistant's response
        # Stream the response word by word
        response_container = st.empty()
        complete_string = ""
        for word in response.split():
            complete_string += word + " "
            response_container.markdown(complete_string + " ", unsafe_allow_html=True)
            time.sleep(0.07)
        response_container.markdown(response, unsafe_allow_html=True)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

