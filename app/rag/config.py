from pydantic import BaseModel


class Settings(BaseModel):
    FAQ_PATH: str = "data/raw/faq.txt"
    PRODUCTS_PATH: str = "data/raw/products.csv"
    VECTORSTORE_PATH: str = "data/processed/faiss_index"


settings = Settings()
