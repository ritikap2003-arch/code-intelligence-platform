from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    model_name='openai/gpt-oss-20b'
)

def analyze_code(query, context_chunks):
    code_context = ''
    for chunk in context_chunks:
        code_context += 'File: ' + chunk['filename'] + chr(10)
        code_context += '---' + chr(10)
        code_context += chunk.get('chunk', '') + chr(10)
        code_context += chr(10)

    system = 'You are an expert code analyst. You will be given actual code. Answer questions based ONLY on the code provided. Always reference specific function names and line details from the code.'

    user = 'Here is the actual code:' + chr(10) + chr(10) + code_context + chr(10) + 'Question: ' + query + chr(10) + chr(10) + 'Answer based on the code above only.'

    messages = [
        SystemMessage(content=system),
        HumanMessage(content=user)
    ]
    response = llm.invoke(messages)
    return response.content