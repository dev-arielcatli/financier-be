from aws_cdk import Stack
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_iam as _iam
from config.config import APP_NAME, STAGE
from constructs import Construct


class DynamoDBStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.create_table()
        self.create_db_policies()

    def get_lambda_prefix(self) -> str:
        return f"{APP_NAME}-{STAGE}-table"

    def create_table(self):
        name = f"{self.get_lambda_prefix()}-main"
        self.FINANCIER_TABLE = dynamodb.TableV2(
            self,
            name,
            table_name=name,
            partition_key=dynamodb.Attribute(
                name="user_id", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="category", type=dynamodb.AttributeType.STRING
            ),
        )

    def create_db_policies(self):
        self.reader_writer_policy = _iam.PolicyStatement(
            actions=[
                "dynamodb:BatchGetItem",
                "dynamodb:DescribeGlobalTable",
                "dynamodb:DescribeGlobalTableSettings",
                "dynamodb:DescribeLimits",
                "dynamodb:DescribeReservedCapacity",
                "dynamodb:DescribeReservedCapacityOfferings",
                "dynamodb:DescribeStream",
                "dynamodb:DescribeTable",
                "dynamodb:DescribeTimeToLive",
                "dynamodb:GetItem",
                "dynamodb:GetRecords",
                "dynamodb:GetShardIterator",
                "dynamodb:Query",
                "dynamodb:DescribeStream",
                "dynamodb:PutItem",
                "dynamodb:DeleteItem",
                "dynamodb:BatchWriteItem",
                "dynamodb:UpdateItem",
                "dynamodb:ListStreams",
            ],
            resources=[self.FINANCIER_TABLE.table_arn],
        )
