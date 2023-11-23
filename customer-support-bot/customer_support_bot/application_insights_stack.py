
from aws_cdk import (
    Stack,
    aws_resourcegroups as rg,
    aws_applicationinsights as ai,
    )
# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.



from constructs import Construct
class ApplicationInsightsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        group = rg.CfnGroup(self, 'rgroup', name='reinvent-rg',  
        resource_query= rg.CfnGroup.ResourceQueryProperty(
             query=rg.CfnGroup.QueryProperty(
                 resource_type_filters = [
                     "AWS::Lambda::Function",
                     "AWS::DynamoDB::Table",
                     "AWS::SQS::Queue",
                     "AWS::S3::Bucket",
                     "AWS::Events::Rule",
                     "AWS::ApiGateway::RestApi",
                     "AWS::SNS::Topic",
                     "AWS::StepFunctions::Activity",
                     "AWS::StepFunctions::StateMachine",
                     ],
                 tag_filters = [
                     rg.CfnGroup.TagFilterProperty(key='APP', values=['CustomerChatReinvent2023'])
                 ]
             ), 
             type='TAG_FILTERS_1_0'
        ))

        app_insights =  ai.CfnApplication(
            self, 'application_insight',
            resource_group_name = 'reinvent-rg',
        )

        app_insights.add_depends_on(group)

