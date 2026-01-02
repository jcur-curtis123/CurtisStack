import os
import pandas as pd

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama

from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate


CSV_PATH = os.environ.get("CSV_PATH", "data.csv")
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")
EMBED_MODEL = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")


def load_csv_as_documents(csv_path: str):
    df = pd.read_csv(csv_path)

    docs = []
    for i, row in df.iterrows():
        row_text = " | ".join([f"{col}={row[col]}" for col in df.columns])
        docs.append(
            Document(
                page_content=row_text,
                metadata={"row_index": int(i)},
            )
        )
    return docs


def build_vectorstore(docs):
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    return FAISS.from_documents(docs, embeddings)


def build_prompt():
    return PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are a data analyst.\n"
            "Use ONLY the CSV rows below to answer.\n"
            "If the answer is not supported, say you cannot determine it.\n\n"
            "CSV ROWS:\n{context}\n\n"
            "QUESTION:\n{question}\n\n"
            "Answer with:\n"
            "1) A short summary\n"
            "2) Any computed numbers (if possible)\n"
            "3) The row indices you used\n"
        ),
    )


def answer_question(llm, prompt, retrieved_docs, question):
    context = "\n".join(d.page_content for d in retrieved_docs)
    formatted_prompt = prompt.format(context=context, question=question)
    return formatted_prompt, llm.invoke(formatted_prompt)


def main():
    print(f"Loading CSV: {CSV_PATH}")
    docs = load_csv_as_documents(CSV_PATH)

    print("Building FAISS index...")
    vectorstore = build_vectorstore(docs)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})

    llm = Ollama(model=MODEL_NAME)
    prompt = build_prompt()

    print("\nReady. Ask questions. Type 'exit' to quit.\n")

    while True:
        question = input("Q> ").strip()
        if question.lower() in ("exit", "quit"):
            break

        retrieved_docs = retriever.invoke(question)
        formatted_prompt, answer = answer_question(
            llm, prompt, retrieved_docs, question
        )

        print("\n--- Answer ---")
        print(answer)

        rows = sorted({d.metadata["row_index"] for d in retrieved_docs})
        print("\nRows used:", rows)
        print()


if __name__ == "__main__":
    main()
