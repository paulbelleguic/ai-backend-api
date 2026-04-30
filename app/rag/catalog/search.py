import pandas as pd


class CatalogSearch:
    """Recherche et filtre les produits dans le catalogue."""

    def __init__(self, products_df: pd.DataFrame) -> None:
        if products_df.empty:
            raise ValueError("Le catalogue produits est vide.")

        self.products_df = products_df.copy()

    def filter_products(
        self,
        category: str | None = None,
        gender: str | None = None,
        color: str | None = None,
        size: str | None = None,
        max_price: float | None = None,
        only_in_stock: bool = True,
    ) -> pd.DataFrame:
        df = self.products_df.copy()

        if category:
            df = df[df["category"].str.lower() == category.lower()]

        if gender:
            df = df[df["gender"].str.lower() == gender.lower()]

        if color:
            df = df[df["color"].str.lower() == color.lower()]

        if size:
            df = df[df["size"].astype(str).str.lower() == str(size).lower()]

        if max_price is not None:
            df = df[df["price"] <= max_price]

        if only_in_stock:
            df = df[df["stock"] > 0]

        return df.sort_values(by=["price", "stock"], ascending=[True, False])

    def format_results(self, results_df: pd.DataFrame, max_results: int = 5) -> str:
        if results_df.empty:
            return "Aucun produit correspondant n'a ete trouve."

        lines = []
        top_results = results_df.head(max_results)

        for _, row in top_results.iterrows():
            line = (
                f"- {row['name']} | categorie: {row['category']} | "
                f"couleur: {row['color']} | taille: {row['size']} | "
                f"prix: {row['price']:.2f} EUR | stock: {row['stock']}"
            )
            lines.append(line)

        return "\n".join(lines)
