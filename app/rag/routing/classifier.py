import unicodedata


class QueryRouter:
    """Route une question utilisateur vers la FAQ support ou le catalogue produits."""

    SUPPORT_KEYWORDS = {
        "livraison",
        "retour",
        "retours",
        "remboursement",
        "rembourse",
        "payer",
        "paiement",
        "commande",
        "suivi",
        "expediee",
        "expedie",
        "annuler",
        "annulation",
        "service client",
        "promo",
        "code promotionnel",
        "defectueux",
        "defectueux",
        "echange",
        "echanger",
        "article solde",
        "delai",
        "delais",
        "frais de livraison",
    }

    PRODUCT_KEYWORDS = {
        "produit",
        "produits",
        "taille",
        "couleur",
        "prix",
        "stock",
        "disponible",
        "disponibilite",
        "acheter",
        "cherche",
        "montre-moi",
        "montre moi",
        "moins de",
        "taille 42",
        "taille 38",
        "taille m",
        "taille l",
        "sneakers",
        "hoodie",
        "jeans",
        "jacket",
        "coat",
        "dress",
        "boots",
        "leggings",
        "polo",
        "sweater",
        "shorts",
        "blouse",
        "blazer",
        "cardigan",
        "t-shirt",
        "shirt",
        "top",
    }

    def route(self, query: str) -> dict:
        if not query.strip():
            raise ValueError("La question utilisateur ne peut pas etre vide.")

        normalized_query = self._normalize_text(query)

        support_score = self._count_matches(normalized_query, self.SUPPORT_KEYWORDS)
        product_score = self._count_matches(normalized_query, self.PRODUCT_KEYWORDS)

        if product_score > support_score:
            route = "catalog"
        else:
            route = "support"

        return {
            "route": route,
            "support_score": support_score,
            "product_score": product_score,
        }

    @staticmethod
    def _count_matches(query: str, keywords: set[str]) -> int:
        return sum(1 for keyword in keywords if keyword in query)

    @staticmethod
    def _normalize_text(text: str) -> str:
        text = text.lower()
        text = unicodedata.normalize("NFKD", text)
        return "".join(char for char in text if not unicodedata.combining(char))
