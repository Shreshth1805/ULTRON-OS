from app.learning.learner import learner


class LearnerAgent:

    def learn(

        self,

        project,

        review,

        testing,

        reflection

    ):

        return learner.learn(

            project,

            review,

            testing,

            reflection

        )


learner_agent = LearnerAgent()