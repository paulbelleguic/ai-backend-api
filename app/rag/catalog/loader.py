from pathlib import Path

import pandas as pd


class CatalogLoader:
    """Charge le catalogue produits depuis un fichier CSV."""

    def __init__(self, file_path: str = "data/raw/products.csv") -> None:
        self.file_path = Path(file_path)

    def load_products(self) -> pd.DataFrame:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Fichier catalogue introuvable : {self.file_path}")

        df = pd.read_csv(self.file_path)

        if df.empty:
            raise ValueError("Le catalogue produits est vide.")

        return df
