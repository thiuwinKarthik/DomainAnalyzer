class TextChunker:
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 3000) -> list:
        """Splits text into chunks small enough for LLaMA-3 context window."""
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]