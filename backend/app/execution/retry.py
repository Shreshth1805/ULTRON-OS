class RetryManager:

    def run(

        self,

        function,

        retries=2

    ):

        last_exception = None

        for _ in range(retries + 1):

            try:

                return function()

            except Exception as e:

                last_exception = e

        raise last_exception


retry_manager = RetryManager()