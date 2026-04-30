from app.rag.llm.generator import AnswerGenerator
from app.rag.retrieval.retriever import Retriever


class RAGPipeline:
    """Pipeline support FAQ : retrieval FAISS puis generation de reponse."""

    def __init__(self) -> None:
        self.retriever = Retriever()
        self.generator = AnswerGenerator()

    def ask(self, question: str, k: int = 4) -> dict:
        if not question.strip():
            raise ValueError("La question utilisateur ne peut pas etre vide.")

        retrieved_items = self.retriever.retrieve_with_scores(query=question, k=k)
        documents = [item["document"] for item in retrieved_items]
        context = "\n\n".join(document.page_content for document in documents)
        answer = self.generator.generate(question=question, context=context)

        sources = []
        passages = []
        for item in retrieved_items:
            document = item["document"]
            source = document.metadata.get("source", "data/raw/faq.txt")
            if source not in sources:
                sources.append(source)
            passages.append({
                "content": document.page_content,
                "metadata": document.metadata,
                "score": item["score"],
            })

        return {
            "question": question,
            "answer": answer,
            "sources": sources or ["data/raw/faq.txt"],
            "passages": passages,
            "context": context,
        }
