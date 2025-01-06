import abc
from typing import Dict

class DataRetriever(abc.ABC):

    @abc.abstractmethod
    def retrieve_data(self, embedd_client, query):
        """
        Return the loaded data
        """

