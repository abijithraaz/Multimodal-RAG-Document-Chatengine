import abc

class BaseLLM(abc.ABC):
    name = "BaseExtractor (abstract)"

    @abc.abstractmethod
    def llmchat(self, prompt:str, encoded_image=None) -> str:
        """
        Returning the query response.
        """