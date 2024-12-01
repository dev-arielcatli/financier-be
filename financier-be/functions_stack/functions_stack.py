from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as _apigw
)

from config.config import APP_NAME, STAGE, DIR_FUNCTIONS, LAMBDA_FASTAPI

class FunctionsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.__create_fastapi_function(LAMBDA_FASTAPI)

    def __get_lambda_prefix(self) -> str:
        return f"{APP_NAME}-{STAGE}-function"

    def __create_fastapi_function(self, name: str):
        function_id = f"{self.__get_lambda_prefix()}-{name}"
        self.FAST_API_FUNCTION = _lambda.Function(
            self, function_id,
            function_name=function_id,
            runtime=_lambda.Runtime.PYTHON_3_12,
            code = _lambda.Code.from_asset(DIR_FUNCTIONS),
            handler = f'{name}.handler'
        )