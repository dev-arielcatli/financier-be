import aws_cdk as cdk
from apigw_stack.apigw_stack import APIGatewayStack
from config.config import APP_NAME, STAGE
from functions_stack.functions_stack import FunctionsStack
from s3_fe_stack.s3_fe_stack import FEWebHostingStack


def create_stack_name(name: str) -> str:
    return f"{APP_NAME}-{STAGE}-stack-{name}"


app = cdk.App()

functions_stack = FunctionsStack(app, create_stack_name("functions"))
apigw_stack = APIGatewayStack(
    app, create_stack_name("apigw"), functions_stack=functions_stack
)
fe_hosting_stack = FEWebHostingStack(app, create_stack_name("application"))

app.synth()
