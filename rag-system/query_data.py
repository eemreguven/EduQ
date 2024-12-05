import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

from get_embeddings import get_embeddings_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)

def query_rag(query_text: str):
    # Prepare the DB.
    print("Initializing ChromaDB...")
    embedding_function = get_embeddings_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    print("Searching for similar documents...")
    results = db.similarity_search_with_score(query_text, k=5)

    if not results:
        print("No results found in ChromaDB.")
        return "No relevant context found."

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    print(f"Context retrieved:\n{context_text[:500]}...")  # Print first 500 chars

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(f"Prompt prepared:\n{prompt[:500]}...")  # Print first 500 chars

    # Query the model.
    print("Querying the model...")
    model = OllamaLLM(model="llama3.2:3b")
    response_text = model.invoke(prompt)
    print(f"Model response: {response_text}")

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text

if __name__ == "__main__":
    main()