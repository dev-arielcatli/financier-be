import os

from aws_cdk import Stack
from aws_cdk import aws_lambda as _lambda
from config.config import APP_NAME, DIR_FUNCTIONS, LAMBDA_FASTAPI, STAGE
from constructs import Construct


class FunctionsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.create_python_layer()
        self.create_fastapi_function(LAMBDA_FASTAPI)

    def get_lambda_prefix(self) -> str:
        return f"{APP_NAME}-{STAGE}-function"

    def create_fastapi_function(self, name: str):
        function_id = f"{self.get_lambda_prefix()}-{name}"
        self.FAST_API_FUNCTION = _lambda.Function(
            self,
            function_id,
            function_name=function_id,
            runtime=_lambda.Runtime.PYTHON_3_12,
            layers=[self.python_layer],
            code=_lambda.Code.from_asset(DIR_FUNCTIONS),
            handler=f"{name}.handler",
        )

    def create_python_layer(self):
        current_dir = os.path.dirname(__file__)
        layers_dir = os.path.join(current_dir, "layers", "python.zip")
        layer_name = f"{self.get_lambda_prefix()}-layer"
        self.python_layer = _lambda.LayerVersion(
            self,
            layer_name,
            code=_lambda.Code.from_asset(layers_dir),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            layer_version_name=layer_name,
        )
