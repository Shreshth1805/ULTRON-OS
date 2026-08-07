from app.learning.memory import (
    learning_memory
)


class LearningSearch:

    def search(

        self,

        keyword

    ):

        results = []

        for project in learning_memory.list_projects():

            data = learning_memory.load(project)

            if keyword.lower() in str(data).lower():

                results.append(

                    {

                        "project": project,

                        "memory": data

                    }

                )

        return results


learning_search = LearningSearch()