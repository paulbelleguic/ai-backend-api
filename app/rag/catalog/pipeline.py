from app.rag.catalog.loader import CatalogLoader
from app.rag.catalog.parser import CatalogQueryParser
from app.rag.catalog.search import CatalogSearch


class CatalogPipeline:
    """Orchestre le chargement, le parsing et la recherche dans le catalogue produits."""

    def __init__(self) -> None:
        loader = CatalogLoader()
        products_df = loader.load_products()
        self.search = CatalogSearch(products_df)
        self.parser = CatalogQueryParser()

    def find_products(
        self,
        category: str | None = None,
        gender: str | None = None,
        color: str | None = None,
        size: str | None = None,
        max_price: float | None = None,
        only_in_stock: bool = True,
    ) -> dict:
        results_df = self.search.filter_products(
            category=category,
            gender=gender,
            color=color,
            size=size,
            max_price=max_price,
            only_in_stock=only_in_stock,
        )

        return {
            "count": len(results_df),
            "results": results_df,
            "formatted_results": self.search.format_results(results_df),
        }

    def search_from_query(self, query: str) -> dict:
        if not query.strip():
            raise ValueError("La requete utilisateur ne peut pas etre vide.")

        filters = self.parser.parse(query)

        results = self.find_products(
            category=filters["category"],
            gender=filters["gender"],
            color=filters["color"],
            size=filters["size"],
            max_price=filters["max_price"],
            only_in_stock=True,
        )

        return {
            "query": query,
            "filters": filters,
            "count": results["count"],
            "results": results["results"],
            "formatted_results": results["formatted_results"],
        }
