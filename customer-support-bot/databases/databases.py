from aws_cdk import (
    RemovalPolicy,
    aws_dynamodb as ddb
)
from constructs import Construct


REMOVAL_POLICY = RemovalPolicy.DESTROY

TABLE_CONFIG = dict (removal_policy=REMOVAL_POLICY, billing_mode= ddb.BillingMode.PAY_PER_REQUEST)


class Tables(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.whatsapp_MetaData = ddb.Table(
            self, "whatsapp-MetaData", 
            partition_key=ddb.Attribute(name="messages_id", type=ddb.AttributeType.STRING),
            stream=ddb.StreamViewType.NEW_AND_OLD_IMAGES
        )
                                      
        self.session_tabble = ddb.Table(
            self, "SessionTable", 
            partition_key=ddb.Attribute(name="SessionId", type=ddb.AttributeType.STRING),
            **TABLE_CONFIG)
        
        self.passangerTable = ddb.Table(
            self, "passangerTable", 
            partition_key=ddb.Attribute(name="Passenger_ID", type=ddb.AttributeType.STRING),
            **TABLE_CONFIG)
        
        self.session_active_tabble = ddb.Table(
            self, "Session_active_value_Table", 
            partition_key=ddb.Attribute(name="phone_number", type=ddb.AttributeType.STRING),
            **TABLE_CONFIG)