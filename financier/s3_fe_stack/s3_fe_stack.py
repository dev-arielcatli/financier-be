from constructs import Construct
from aws_cdk import (
    Stack,
    aws_s3 as _s3,
    CfnOutput
)

from config.config import STAGE, APP_NAME

class FEWebHostingStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.create_s3_stack_for_fe()
        self.output_fe_bucket_url()

    def get_s3_prefix(self, name: str) -> str:
        return f"{APP_NAME}-{STAGE}-s3-{name}"

    def create_s3_stack_for_fe(self):
        s3_name = self.get_s3_prefix("application")
        # TODO: Update this when we have CF distribution
        self.FE_S3_BUCKET = _s3.Bucket(
            self,
            s3_name,
            bucket_name=s3_name,
            block_public_access=_s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False
            ),
            public_read_access=True,
            website_index_document="index.html",
            website_error_document="index.html"
        )
        self.FE_S3_BUCKET_URL = self.FE_S3_BUCKET.bucket_website_url

    def output_fe_bucket_url(self):
        CfnOutput(self, self.get_s3_prefix("fe_bucket"), 
                  value=self.FE_S3_BUCKET_URL, 
                  description="URL of the web application")