
from .LLMEnums import LLMEums
from .providers import QwenProvider, CoHereProvider


class LLMProviderFactory:

    def __init__(self, config: dict):

        self.config = config

    def create(self, provider: str):
        if provider == LLMEums.Qwen.value:
            return QwenProvider(
                api_key= self.config.QWEN_API_KEY,
                base_url=self.config.QWEN_API_URL,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE
            )
        
        elif provider == LLMEums.CoHere.value:
            return CoHereProvider(
                api_key= self.config.COHERE_API_KEY,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE
            )

        return None
        