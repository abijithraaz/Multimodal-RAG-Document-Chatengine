import abc

class DataStoring(abc.ABC):

    @abc.abstractmethod
    def vectordata_storing(self, document_chunks, document_name):
        """
        Storing the embedded chunks
        """

class DBModify(abc.ABC):

    @abc.abstractmethod
    def clear_db(self, document_name, sql_query=''):
        """
        Modifying the vector DB
        """
