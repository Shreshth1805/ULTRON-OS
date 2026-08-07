from datetime import datetime

from app.learning.memory import (
    learning_memory
)


class Learner:

    def learn(

        self,

        project,

        review,

        testing,

        reflection

    ):

        learning_memory.save(

            project,

            {

                "timestamp": str(

                    datetime.now()

                ),

                "review": review,

                "testing": testing,

                "reflection": reflection

            }

        )

        return {

            "success": True

        }


learner = Learner()