import streamlit as st
import google.generativeai as genai
st.title(f"🎉 :orange[Marketing campaign] context chatbot app") 
st.subheader("Conversation")

# Capture Gemini API Key
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")
 
# Initialize the Gemini Model
if gemini_api_key:
    try:
        # Configure Gemini with the provided API Key
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"An error occurred while setting up the Gemini model: {e}")
 
# Initialize session state for storing chat history and prompt history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize with an empty list

if "prompt_chain" not in st.session_state:
    st.session_state.prompt_chain = "I am your marketing campaign assistant. What type of campaign are you interested in—digital, social media, or email? Once I know your goals, I can recommend strategies and tools tailored to your needs. Additionally, I can help with content ideas, budget planning, and performance tracking. Let’s get started!"
    #"I am a Grammar Helping Chatbot. Please enter a sentence or paragraph you would like help with. I will analyze your text and provide corrections, along with explanations for each error. Additionally, I can offer grammar tips and resources tailored to your needs."

# Display previous chat history using st.chat_message (if available)
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)
 
# Capture user input and generate bot response
if user_input := st.chat_input("Type your message here..."):
    # Store and display user message
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)
   
    # Append the new question to the prompt chain
    st.session_state.prompt_chain += f"\nCustomer: {user_input}"
   
    # Combine the predefined prompt chain with the current user input
    full_input = st.session_state.prompt_chain
   
    # Use Gemini AI to generate a bot response
    if model:
        try:
            response = model.generate_content(full_input)
            bot_response = response.text
           
            # Append bot response to the chat history and update the prompt chain
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)
           
            # Update the prompt chain with the bot's response
            st.session_state.prompt_chain += f"\nAssistant: {bot_response}"
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
