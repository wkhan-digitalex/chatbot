import streamlit as st
import google.generativeai as genai
from data_archive import AccountManagementAgent, AccountManagementForICAgent
from rags import chat_with_rag

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'model' not in st.session_state:
        GEMINI_API_KEY = "AIzaSyCtO7jsR7sT-riZYuCJa69-qdjblR0qez0"
        genai.configure(api_key=GEMINI_API_KEY)
        st.session_state.model = genai.GenerativeModel("gemini-1.5-flash")
        st.session_state.chat = st.session_state.model.start_chat(history=[])

def router(query):
    """Your existing router function"""
    query = query.lower()
    cloud_keywords = ['aws', 'azure', 'gcp', 'google cloud', 'amazon', 'microsoft']
    account_keywords =  [
    # Account Types
    'billing', 'usage', 'member', 'management', 'project', 'subscription',
    'organization', 'tenant',
    # Actions
    'onboard', 'connect', 'setup', 'configure', 'enable', 'create', 'link',
    'add', 'integrate',
    # Authentication
    'login', 'signin', 'signup', 'register', 'credentials', 'permissions',
    'access', 'role', 'iam', 'user',
    # Methods
    'manual', 'automated', 'cli', 'ui', 'console', 'shell', 'automation',
    # Components
    'cur', 'cost explorer', 'tags', 'api', 'service account', 'arn', 
    'bucket', 'dataset', 'export', 'report',
    # Status/Help
    'troubleshoot', 'error', 'help', 'guide', 'steps', 'instructions',
    'how to', 'tutorial', 'documentation',
    # Time-related
    'time', 'duration', 'wait', 'discover', 'process',
    # Roles/Personas  
    'partner', 'target', 'customer', 'admin', 'owner', 'user', 'company',
    # Features
    'cost', 'billing', 'resources', 'monitoring', 'management', 'dashboard',
    'reports', 'analytics'
    ]
    account_keywords_non_target = [
        # ... your existing non-target keywords ...
    ]

    contains_cloud = any(cloud in query for cloud in cloud_keywords)
    contains_account_keyword = any(keyword in query for keyword in account_keywords)
    contains_indirect = 'indirect' in query or 'target' in query

    if contains_cloud and contains_account_keyword:
        if contains_indirect:
            context = AccountManagementForICAgent
        else:
            context = AccountManagementAgent
    else:
        context = chat_with_rag(str(query))

    prompt = f"""Answer from the context and recheck three times before answering and answer in full detail without missing any steps.

    Context:
    {context}

    Question: {query}

    Answer: """

    response = st.session_state.chat.send_message(prompt)
    return response.text

def create_chat_ui():
    """Create the chat UI"""
    st.title("Cloud Support Chatbot")

    # Initialize session state
    initialize_session_state()

    # Chat history display
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = router(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})

def main():
    # Page config
    st.set_page_config(
        page_title="Cloud Support Chatbot",
        page_icon="☁️",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .stChat {
            padding: 20px;
        }
        .stChatMessage {
            padding: 10px;
            border-radius: 15px;
            margin: 5px 0;
        }
        .stChatInput {
            border-radius: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    create_chat_ui()

if __name__ == "__main__":
    main()