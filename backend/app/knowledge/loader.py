from langchain_community.document_loaders import (

    PyPDFLoader,

    TextLoader

)

from pathlib import Path


class DocumentLoader:

    def load(

        self,

        filename

    ):

        extension = Path(

            filename

        ).suffix.lower()

        if extension == ".pdf":

            loader = PyPDFLoader(

                filename

            )

        else:

            loader = TextLoader(

                filename,

                encoding="utf-8"

            )

        return loader.load()


loader = DocumentLoader()