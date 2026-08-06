from app.core.llm import llm

from app.knowledge.retriever import (

    retriever

)


def ask(

    question

):

    docs = retriever.invoke(

        question

    )

    context = "\n\n".join(

        [

            d.page_content

            for d in docs

        ]

    )

    prompt = f"""

Context

{context}

Question

{question}

Answer using only the context.

"""

    response = llm.invoke(

        prompt

    )

    return {

        "answer": response.content,

        "sources": len(docs)

    }