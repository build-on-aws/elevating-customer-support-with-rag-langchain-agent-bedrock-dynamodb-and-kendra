from constructs import Construct
from aws_cdk import ( aws_iam as iam, Stack, CfnOutput)



class KendraServiceRole(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        stk = Stack.of(self)
        account_id = stk.account
        role_name = stk.stack_name

        self.role = iam.Role(self, "R",assumed_by=iam.ServicePrincipal("kendra.amazonaws.com"))
        
        self.arn = self.role.role_arn
        
        self.role.attach_inline_policy(
            policy = iam.Policy(self, "cw",statements=[
                iam.PolicyStatement(actions=["cloudwatch:PutMetricData"], resources=['*']),
                iam.PolicyStatement(actions=["logs:*"], resources=['*']),
                iam.PolicyStatement(actions=["kendra:BatchPutDocument","kendra:BatchDeleteDocument"], resources=['*']),
                iam.PolicyStatement(actions=["lambda:*"], resources=['*']),
                iam.PolicyStatement(actions=["s3:GetObject"], resources=['*']),
                iam.PolicyStatement(actions=["s3:*"], resources=['*'])
                
            ])
        )

        




        