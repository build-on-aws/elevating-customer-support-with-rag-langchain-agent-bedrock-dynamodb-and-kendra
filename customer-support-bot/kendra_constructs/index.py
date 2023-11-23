from constructs import Construct

from aws_cdk import ( 
    aws_iam as iam, Stack,
    aws_kendra as kendra
)

from kendra_constructs.roles import KendraServiceRole


class KendraIndex(Construct):
    def __init__(self, scope: Construct, id: str, edition="DEVELOPER_EDITION", **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        stk = Stack.of(self)
        self.role = KendraServiceRole(self, "KSR")


        document_metadata_configurations=[kendra.CfnIndex.DocumentMetadataConfigurationProperty(
        name="s3_document_id",
        type="STRING_VALUE",

        search=kendra.CfnIndex.SearchProperty(
            displayable=True,
            facetable=False,
            searchable=True,
            sortable=False
        )
    )]

        self.index = kendra.CfnIndex(self, "I",
            edition=edition,
            name=stk.stack_name,
            role_arn=self.role.arn,
            document_metadata_configurations=document_metadata_configurations

        )
        self.index_id = self.index.attr_id

