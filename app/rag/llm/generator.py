import re
import unicodedata

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from app.rag.prompts.rag_prompt import build_rag_prompt


class AnswerGenerator:
    """Genere une reponse a partir du contexte recupere."""

    def __init__(self) -> None:
        model_name = "google/flan-t5-base"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def generate(self, question: str, context: str, max_new_tokens: int = 150) -> str:
        if not question.strip():
            raise ValueError("La question ne peut pas etre vide.")

        if not context.strip():
            return "Je ne dispose pas de contexte suffisant pour repondre."

        prompt = build_rag_prompt(question=question, context=context)
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        )
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False
        )
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        if self._should_fallback(answer):
            return self._build_fallback_answer(question, context)

        return answer

    def summarize(self, context: str, max_new_tokens: int = 180) -> str:
        if not context.strip():
            return "Je ne dispose pas de contenu suffisant pour produire un resume."

        prompt = (
            "Resume le document suivant en francais de maniere claire et concise.\n\n"
            f"Document :\n{context}\n\n"
            "Resume :"
        )
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        )
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False
        )
        summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        if self._should_fallback(summary):
            return self._build_fallback_summary(context)

        return summary

    @staticmethod
    def _should_fallback(answer: str) -> bool:
        cleaned = AnswerGenerator._normalize_text(answer.strip())

        if not cleaned:
            return True

        if len(cleaned.split()) < 6:
            return True

        prompt_leak_patterns = [
            "vous etes un assistant de support client",
            "vous êtes un assistant de support client",
            "tu es un assistant de support client",
            "tu es un assistant de support client pour un site e-commerce",
            "reponds en francais",
            "réponds en français",
            "using only the contexte",
            "if information is not present",
            "dis clairement que tu ne sais pas",
            "contexte ci-dessous",
            "reponse de support",
            "réponse de support",
        ]

        if any(pattern in cleaned for pattern in prompt_leak_patterns):
            return True

        if cleaned.startswith("vous êtes") or cleaned.startswith("vous etes"):
            return True

        if cleaned.startswith("tu es"):
            return True

        if " and " in cleaned or "research" in cleaned:
            return True

        return False


    @staticmethod
    def _build_fallback_answer(question: str, context: str) -> str:
        sentences = AnswerGenerator._extract_meaningful_sentences(context)

        if not sentences:
            return "Je ne dispose pas de contexte suffisant pour repondre."

        ranked_sentences = AnswerGenerator._rank_sentences_for_question(question, sentences)

        if len(ranked_sentences) == 1:
            return f"Selon notre FAQ, {ranked_sentences[0]}"

        selected = ranked_sentences[:3]
        return "Selon notre FAQ, " + " ".join(selected)

    @staticmethod
    def _build_fallback_summary(context: str) -> str:
        sentences = AnswerGenerator._extract_meaningful_sentences(context)

        if not sentences:
            return "Je ne dispose pas de contenu suffisant pour produire un resume."

        selected = sentences[:3]
        return "Resume du document : " + " ".join(selected)

    @staticmethod
    def _extract_meaningful_sentences(context: str) -> list[str]:
        normalized_context = context.replace("\n", " ")
        raw_sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+", normalized_context.strip())
            if sentence.strip()
        ]

        cleaned_sentences = []
        for sentence in raw_sentences:
            # Ignore short section titles such as "Frais de livraison" or "Retours".
            if len(sentence.split()) <= 4 and not re.search(r"[.!?]$", sentence):
                continue

            cleaned_sentences.append(sentence)

        return cleaned_sentences

    @staticmethod
    def _rank_sentences_for_question(question: str, sentences: list[str]) -> list[str]:
        question_keywords = AnswerGenerator._extract_keywords(question)

        if not question_keywords:
            return sentences

        def sentence_score(sentence: str) -> tuple[int, int]:
            normalized_sentence = AnswerGenerator._normalize_text(sentence)
            keyword_hits = sum(1 for keyword in question_keywords if keyword in normalized_sentence)
            informative_bonus = 1 if len(sentence.split()) >= 8 else 0
            return (-keyword_hits, -informative_bonus)

        ranked = sorted(sentences, key=sentence_score)
        return ranked

    @staticmethod
    def _extract_keywords(text: str) -> list[str]:
        normalized = AnswerGenerator._normalize_text(text)
        tokens = re.findall(r"\b\w+\b", normalized)
        stopwords = {
            "qu", "que", "quoi", "qui", "de", "du", "des", "le", "la", "les",
            "un", "une", "est", "et", "a", "au", "aux", "en", "dans", "sur",
            "pour", "par", "comment", "pourquoi", "ce", "cette", "ces", "mon",
            "ma", "mes", "vos", "votre", "je", "tu", "il", "elle", "nous",
            "vous", "ils", "elles", "puis", "avoir", "avec"
        }
        return [token for token in tokens if token not in stopwords and len(token) > 2]

    @staticmethod
    def _normalize_text(text: str) -> str:
        text = text.lower()
        text = unicodedata.normalize("NFKD", text)
        text = "".join(char for char in text if not unicodedata.combining(char))
        return text
