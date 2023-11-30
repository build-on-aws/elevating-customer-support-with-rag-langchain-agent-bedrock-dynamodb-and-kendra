import sys

from aws_cdk import (
    Duration,
    aws_lambda,
    aws_ssm as ssm,
    Stack,
    aws_iam as iam

)

from constructs import Construct


LAMBDA_TIMEOUT= 900

BASE_LAMBDA_CONFIG = dict (
    timeout=Duration.seconds(LAMBDA_TIMEOUT),       
    memory_size=520,
    tracing= aws_lambda.Tracing.ACTIVE)

COMMON_LAMBDA_CONF = dict (runtime=aws_lambda.Runtime.PYTHON_3_11, **BASE_LAMBDA_CONFIG)

from layers import Layers


class Lambdas(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Lay = Layers(self, 'Lay')

        self.whatsapp_in = aws_lambda.Function(
            self, "WAIn", handler="lambda_function.lambda_handler",
            description ="process WhatsApp incoming messages" ,
            code=aws_lambda.Code.from_asset("./lambdas/code/whatsapp_in"),
            layers= [Lay.bs4_requests, Lay.common],**COMMON_LAMBDA_CONF)
        
        self.whatsapp_out = aws_lambda.Function(
            self, "whatsapp_out", handler="lambda_function.lambda_handler",
            description ="Send WhatsApp message" ,
            code=aws_lambda.Code.from_asset("./lambdas/code/whatsapp_out"),
            layers= [Lay.bs4_requests, Lay.common],**COMMON_LAMBDA_CONF)

        self.audio_job_transcriptor = aws_lambda.Function(
            self, "job_Transcribe", 
            description ="Start Transcribe Job  audio to text WhatsApp incoming messages" ,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset("./lambdas/code/audio_job_transcriptor"),
            layers= [Lay.bs4_requests, Lay.common],**COMMON_LAMBDA_CONF)
        
        self.dynamodb_put_item = aws_lambda.Function(
            self, "DynamoDB_put_item", 
            description ="Put items to csv to DynamoDB" ,
            handler="lambda_function.lambda_handler",
            layers=[Lay.bs4_requests,Lay.common],
            code=aws_lambda.Code.from_asset("./lambdas/code/dynamodb_put_item"),
            **COMMON_LAMBDA_CONF)
        
        self.query_dynamodb_passanger = aws_lambda.Function(
            self, "query_dynamodb_passanger", 
            description ="Query DynamoDB passanger table" ,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset("./lambdas/code/query_dynamodb_passanger"),
            **COMMON_LAMBDA_CONF)
        
        self.langchain_agent_text = aws_lambda.Function(
            self, "langChain_agent_text", 
            description ="Airline Agent with LangChain and Amacon Bedrock" ,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset("./lambdas/code/langchain_agent_text"),
            layers= [Lay.bedrock,Lay.bs4_requests,Lay.common,Lay.langchain],
            architecture=aws_lambda.Architecture.ARM_64,
            **COMMON_LAMBDA_CONF)
        
        self.transcriber_done = aws_lambda.Function(
            self, "transcriber_done", 
            description ="Read the text from transcriber job" ,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset("./lambdas/code/transcriber_done"),
            layers= [Lay.bs4_requests, Lay.common],**COMMON_LAMBDA_CONF)
        
        self.data_source_creator = aws_lambda.Function(
            self,
            "CR_datasource",
            handler="lambda_function.lambda_handler",
            layers=[Lay.bs4_requests],
            code=aws_lambda.Code.from_asset("./lambdas/code/data_source_creator"),
            **COMMON_LAMBDA_CONF
        )

        self.process_stream = aws_lambda.Function(
            self, "process_stream", 
            description ="Read the text from transcriber job" ,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset("./lambdas/code/process_stream"),
            layers= [Lay.bs4_requests, Lay.common],**COMMON_LAMBDA_CONF)

        self.data_source_creator.add_to_role_policy(
            iam.PolicyStatement(actions=["kendra:*"], resources=["*"])
        )

        self.data_source_creator.add_to_role_policy(
            iam.PolicyStatement(actions=["iam:PassRole"], resources=["*"])
        )
