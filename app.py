import streamlit as st
from datetime import datetime
from langchain_community.llms import Ollama

page_style = '''
<style>
  [data-testid="stAppViewContainer"] {
    background-image: url("https://mcdn.wallpapersafari.com/medium/42/71/yoD8KJ.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    opacity: 0.9;
    background-attachment: fixed;
  }
  [data-testid="stAppViewContainer"]::before {
    content: "";
    display: block;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(255, 255, 255, 0.1);
  }
  [data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.1); 
    font-weight: bold;
  }
  [data-testid="stExpander"]{
    background-color: rgba(214, 234, 248,0.9); 
    color: black;
    font-weight: bold;
    border-radius: 10px;
  }
  .chat-bubble {
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
    max-width: 75%;
  }
  .chat-bubble.user {
    background-color:rgb(46,134,193);
    margin-left: auto;
    color: black;
  }
  .chat-bubble.bot {
    background-color: #85C1E9;
    color: black;
  }
  .chat-bubble .timestamp {
    font-size: 0.8em;
    color: black;
  }
  .input-container {
    margin-top: 20px;
    display: flex;
  }
  .input-container input {
    flex: 1;
    padding: 10px;
    border-radius: 5px 0 0 5px;
    border: 1px solid #ccc;
    font-size: 1.1em;
  }
  .input-container button {
    padding: 10px;
    border-radius: 0 5px 5px 0;
    border: 1px solid #ccc;
    background-color: #007bff;
    color: white;
    font-size: 1.1em;
  }
</style>
'''

st.markdown(page_style, unsafe_allow_html=True)

st.title("Finance Help Chatbot")
with st.expander("Instructions", expanded=True):
    st.markdown("""
        Welcome to the Financial Advisor app! 
        - Query Submission: Please enter your query using the left sidebar.
        - Follow-up Questions: After receiving a response from the chatbot, feel free to ask additional related questions using the chat panel on the right.
        - Enhanced Results: For optimal results, please provide specific details in your queries.
    """, unsafe_allow_html=True)

llm = Ollama(model="phi:latest", base_url="http://ollama-container:11434", verbose=True)

initial_prompt='''You are a highly knowledgeable financial advisor specializing in Indian finance. You have a deep understanding of various financial domains, including personal finance, investments, taxation, real estate, and retirement planning. You are well-versed in Indian financial regulations and policies. Your goal is to provide accurate, insightful, and personalized financial advice to users based on their specific questions and needs.'''

def sendPrompt(prompt):
    global llm
    response = llm.invoke(prompt)
    return response

if 'history' not in st.session_state:
    st.session_state.history = []
    response = sendPrompt(initial_prompt)
    st.session_state.history.append({'role': 'bot', 'content': response, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

st.sidebar.header("Ask your finance-related question:")
st.sidebar.write("Type your question below and click 'Enter'.")
initial_query = st.sidebar.text_input("Your question:", key="initial_query", placeholder="Enter your finance-related question here...")

if initial_query and 'initial_query_processed' not in st.session_state:
    response = sendPrompt(initial_query)
    st.session_state.history.append({'role': 'user', 'content': initial_query, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    st.session_state.history.append({'role': 'bot', 'content': response, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    st.session_state.initial_query_processed = True

with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.history:
        if message['role'] == 'user':
            st.markdown(f'<div class="chat-bubble user"><strong>You:</strong> {message["content"]}<div class="timestamp">{message["timestamp"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble bot"><strong>Bot:</strong> {message["content"]}<div class="timestamp">{message["timestamp"]}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    with st.form(key='chat_form', clear_on_submit=True):
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        user_input = st.text_input("", key="user_input", placeholder="Type your message here...")
        submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            response = sendPrompt(user_input)
            st.session_state.history.append({'role': 'user', 'content': user_input, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            st.session_state.history.append({'role': 'bot', 'content': response, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            st.experimental_rerun()

st.write('<script>window.scrollTo(0,document.body.scrollHeight);</script>', unsafe_allow_html=True)