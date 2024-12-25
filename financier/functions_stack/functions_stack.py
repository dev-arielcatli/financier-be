import os

from aws_cdk import Stack
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_lambda as _lambda
from config.config import APP_NAME, DIR_FUNCTIONS, LAMBDA_FASTAPI, STAGE
from constructs import Construct
from dynamodb_stack.dynamodb_stack import DynamoDBStack


class FunctionsStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        database_stack: DynamoDBStack,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.GLOBAL_ENVIRONMENT = {"STAGE": STAGE, "APP_NAME": APP_NAME}
        self.create_python_layer()
        self.create_fastapi_function(name=LAMBDA_FASTAPI, database_stack=database_stack)

    def get_lambda_prefix(self) -> str:
        return f"{APP_NAME}-{STAGE}-function"

    def create_fastapi_function(self, name: str, database_stack: DynamoDBStack):
        function_id = f"{self.get_lambda_prefix()}-{name}"
        self.FAST_API_FUNCTION = _lambda.Function(
            self,
            function_id,
            function_name=function_id,
            runtime=_lambda.Runtime.PYTHON_3_12,
            layers=[self.python_layer],
            code=_lambda.Code.from_asset(DIR_FUNCTIONS),
            handler=f"{name}.handler",
            role=self.create_function_role(
                "fastapi-dynamodb-role", [database_stack.reader_writer_policy]
            ),
            environment=self.GLOBAL_ENVIRONMENT,
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

    def create_function_role(
        self, name: str, policies: list[_iam.PolicyStatement]
    ) -> _iam.Role:
        default_role_name = self.get_function_role_name(name)
        role = _iam.Role(
            self,
            default_role_name,
            assumed_by=_iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name=default_role_name,
        )
        role.add_to_policy(
            _iam.PolicyStatement(
                actions=[
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                ],
                resources=["*"],
            )
        )
        for policy in policies:
            role.add_to_policy(policy)
        return role

    def get_function_role_name(self, name: str) -> str:
        return f"{self.get_lambda_prefix()}-{name}-role"
