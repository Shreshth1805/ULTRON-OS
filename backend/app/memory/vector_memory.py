class VectorMemory:

    def __init__(self):

        self.documents = []

    def add_document(self, text):

        self.documents.append(text)

    def search(self, query):

        results = []

        for doc in self.documents:

            if query.lower() in doc.lower():

                results.append(doc)

        return results


vector_memory = VectorMemory()