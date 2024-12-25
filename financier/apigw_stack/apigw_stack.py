from aws_cdk import Stack
from aws_cdk import aws_apigateway as _apigw
from config.config import APP_NAME, STAGE
from config.gw_paths import ROOT as ROOT_PATH
from constructs import Construct
from functions_stack.functions_stack import FunctionsStack


class APIGatewayStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        functions_stack: FunctionsStack,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.__create_root_api(functions_stack=functions_stack)

        self.STAGE_DEPLOYMENT = _apigw.Deployment(
            self,
            f"{self.__get_apigw_prefix("deployment")}",
            stage_name=STAGE,
            retain_deployments=True,
            api=self.ROOT_API,
        )

    def __get_apigw_prefix(self, name: str) -> str:
        return f"{APP_NAME}-{STAGE}-{name}"

    def __create_root_api(self, functions_stack: FunctionsStack):
        self.ROOT_API = _apigw.LambdaRestApi(
            self,
            f"{APP_NAME}-{STAGE}-api-root",
            rest_api_name=f"{APP_NAME}-{STAGE}-api-{ROOT_PATH}",
            handler=functions_stack.FAST_API_FUNCTION,
            deploy=False,
            default_cors_preflight_options=_apigw.CorsOptions(
                allow_origins=_apigw.Cors.ALL_ORIGINS,
                allow_methods=_apigw.Cors.ALL_METHODS,
            ),
            proxy=True,
        )
