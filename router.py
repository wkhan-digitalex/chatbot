
import google.generativeai as genai
import google.generativeai as genai
from data_archive import AccountManagementAgent, AccountManagementForICAgent
from rags import chat_with_rag
def router(query):
    query = query.lower()
    model = genai.GenerativeModel("gemini-1.5-flash")
    cloud_keywords = ['aws', 'azure', 'gcp', 'google cloud', 'amazon', 'microsoft',]
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
    'cloud asset api',
    'stackdriver',
    'recommender api',
    'cloud shell',
    'bigquery',
    'vpc service controls',
    # Authentication
    'service account json',
    'principals',
    'whitelist',
    # Documentation
    'questionnaire',
    'faq',
    'security',
    # Currency
    'invoice',
    'multiple currencies',
    'exchange rates',
    # Roles
    'billing admin',
    'project admin',
    'cloud asset viewer',
    'monitoring viewer'
]
    contains_cloud = any(cloud in query for cloud in cloud_keywords)
    contains_account_keyword = any(keyword in query for keyword in account_keywords)
    contains_account_keyword_non_target = any(keyword in query for keyword in account_keywords_non_target)
    contains_indirect = 'indirect' in query or 'target' in query
    if contains_cloud and contains_account_keyword:
        if contains_indirect:
            # Create prompt
            prompt = f"""Answer from the context and recheck three times before answering and answer in full detail without missing any steps."

            Context:
            {AccountManagementForICAgent}

            Question: {query}

            Answer: """

            # Get response from Gemini
            response = model.generate_content(prompt)
            return response.text
        elif not contains_indirect:
            prompt = f"""Answer from the context and recheck three times before answering and answer in full detail without missing any steps."

            Context:
            {AccountManagementAgent}

            Question: {query}

            Answer: """

            # Get response from Gemini
            response = model.generate_content(prompt)
            return response.text
    else:
        prompt = f"""Answer from the context and recheck three times before answering and answer in full detail without missing any steps."

        Context:
        {chat_with_rag(str(query))}

        Question: {query}

        Answer: """

        # Get response from Gemini
        response = model.generate_content(prompt)
        return response.text

