from app.memory_v2.vector_store import (
    vector_store
)


class MemoryRetriever:

    def search(

        self,

        query,

        k=5

    ):

        docs = vector_store.similarity_search(

            query,

            k=k

        )

        return [

            {

                "text": d.page_content,

                "metadata": d.metadata

            }

            for d in docs

        ]


memory_retriever = MemoryRetriever()