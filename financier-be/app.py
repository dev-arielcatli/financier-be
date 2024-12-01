
import aws_cdk as cdk

from config.config import APP_NAME, STAGE

from functions_stack.functions_stack import FunctionsStack

def create_stack_name(name: str) -> str:
    return f"{APP_NAME}-{STAGE}-stack-{name}"

app = cdk.App()

functions_stack = FunctionsStack(app, create_stack_name("functions"))

app.synth()