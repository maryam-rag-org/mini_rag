from abc import ABC, abstractmethod

class LLMInterface(ABC):

    @abstractmethod    # make sure this methode do set_generation_model
    def set_generation_model(self, model_id: str):
        pass

    @abstractmethod    # make sure this methode do set_generation_model
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass

    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list=[],
                            max_output_tokens: int = None,
                            temperature: float = None ):
        pass

    @abstractmethod
    def embed_text(self, text: str, document_type: str = None):
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass


