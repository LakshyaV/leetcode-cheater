from langchain.retrievers import CohereRagRetriever
from langchain_community.chat_models import ChatCohere
from langchain_core.documents import Document

# Load the cohere chat model
cohere_chat_model = ChatCohere(cohere_api_key="AVd0OJeorpIMftjg4eGuT6AIJL75C8nezswvwVRU")
# Create the cohere rag retriever using the chat model with the web search connector
rag = CohereRagRetriever(llm=cohere_chat_model, connectors=[{"id": "web-search"}])
docs = rag.get_relevant_documents("Who founded Cohere?")
# Print the documents
for doc in docs[:-1]:
    print(doc.metadata)
    print("\n\n" + doc.page_content)
    print("\n\n" + "-" * 30 + "\n\n")
# Print the final generation 
answer = docs[-1].page_content
print(answer)
# Print the final citations 
citations = docs[-1].metadata['citations']
print(citations)