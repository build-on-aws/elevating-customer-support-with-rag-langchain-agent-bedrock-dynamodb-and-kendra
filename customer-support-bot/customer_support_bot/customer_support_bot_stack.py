from aws_cdk import (
    # Duration,
    Stack, SecretValue,
    aws_secretsmanager as secretsmanager,
    aws_iam as iam,
    # aws_sqs as sqs,
    aws_dynamodb as ddb,
    RemovalPolicy,
    aws_s3_notifications,
    aws_s3 as s3,
    aws_lambda_event_sources,
    aws_lambda,

)
from constructs import Construct
from lambdas import (Lambdas, DynamodbWithSampleDataStack)
from apis import WebhookApi
from databases import Tables
from s3_cloudfront import S3Deploy
from kendra_constructs import (
    KendraIndex, CRKendraS3Datasource
)

#Amazon DynamoDB Table commun data
REMOVAL_POLICY = RemovalPolicy.DESTROY
TABLE_CONFIG = dict (removal_policy=REMOVAL_POLICY, billing_mode= ddb.BillingMode.PAY_PER_REQUEST)
AudioKeyName = "audio-from-whatsapp"
TextBucketName = "text-to-whatsapp"
model_id = "anthropic.claude-instant-v1"
DISPLAY_PHONE_NUMBER = 'YOU-NUMBER'


class CustomerSupportBotStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

       # The code that defines your stack goes here
        stk = Stack.of(self)
        account_id = stk.account
        region_name = self.region

        #Whatsapp Secrets Values
        secrets = secretsmanager.Secret(self, "Secrets", secret_object_value = {
            'WHATS_TOKEN': SecretValue.unsafe_plain_text('FROM_WHATSAPP'),
            'WHATS_VERIFICATION_TOKEN': SecretValue.unsafe_plain_text('CREATE_ONE'),
            'WHATS_PHONE_ID':SecretValue.unsafe_plain_text('FROM_WHATSAPP'),
            'WHATS_TOKEN': SecretValue.unsafe_plain_text('FROM_WHATSAPP')
           })   
        
        # Create Amazon DynamoDB Tables

        Tbl = Tables(self, 'Tbl')

        table_whatsapp_metadata = Tbl.whatsapp_MetaData
        table_session_tabble = Tbl.session_tabble
        table_passangerTable = Tbl.passangerTable
        table_session_active = Tbl.session_active_tabble

        table_whatsapp_metadata.add_global_secondary_index(index_name = 'jobnameindex', 
                                                            partition_key = ddb.Attribute(name="jobName",type=ddb.AttributeType.STRING), 
                                                            projection_type=ddb.ProjectionType.KEYS_ONLY)

        # Amazon Kendra 
        index = KendraIndex(self, "I")


        #Create Amazon S3 Bucket

        s3_deploy = S3Deploy(self, "airline-demo-", TextBucketName,TextBucketName)
        s3_deploy_qa = S3Deploy(self, "airline-qa-base-", TextBucketName,TextBucketName)

        s3_deploy_qa.deploy("airline-qa-base", "airline-qa-base", "airline-qa-base")

        #Create Amazon Lambda Functions

        Fn  = Lambdas(self,'Fn')

        #Create Amazon API Gateweay

        Api = WebhookApi(self, "API", lambdas=Fn)

        #Data to Amazon Kendra Index
        
        s3_files_es_ds = CRKendraS3Datasource(
            self, "airline-qa-base",
            service_token=Fn.data_source_creator.function_arn,
            index_id= index.index_id,
            role_arn=index.role.arn,
            name = "airline-qa-base-v1",
            description = "airline-qa-base",
            bucket_name=s3_deploy_qa.bucket.bucket_name,
            language_code = 'en',
            inclusion_prefixes=["airline-qa-base/"],
            inclusion_patterns = []
        )
        
        # Amazon Lambda Function dynamodb_put_item to passanger table

        Tbl.passangerTable.grant_full_access(Fn.dynamodb_put_item)
        
        # Load data into table
        DynamodbWithSampleDataStack(
            self, "pasanger-qa-base",
            lambda_function=Fn.dynamodb_put_item,
            table= Tbl.passangerTable,
            file_name = "dataset.csv" 
        )
        
        # Amazon Lambda Function whatsapp_in - Config

        Fn.whatsapp_in.add_environment(key='CONFIG_PARAMETER', value=secrets.secret_arn)
        Fn.whatsapp_in.add_environment(key='whatsapp_MetaData', value=table_whatsapp_metadata.table_name)
        Fn.whatsapp_in.add_environment(key='REFRESH_SECRETS', value='false')
        Fn.whatsapp_in.add_environment(key='DISPLAY_PHONE_NUMBER', value= DISPLAY_PHONE_NUMBER)
        secrets.grant_read(Fn.whatsapp_in)
        Fn.whatsapp_in.add_environment(key='ENV_KEY_NAME', value="messages_id")
        table_whatsapp_metadata.grant_full_access(Fn.whatsapp_in)


        # Amazon Lambda Function process_stream - Config       

        Fn.process_stream.add_environment( key='ENV_LAMBDA_AGENT_TEXT', value=Fn.langchain_agent_text.function_name )
        Fn.process_stream.add_environment( key='JOB_TRANSCRIPTOR_LAMBDA', value=Fn.audio_job_transcriptor.function_name )
        Fn.process_stream.add_environment(key='whatsapp_MetaData', value=Tbl.whatsapp_MetaData.table_name)

        Fn.process_stream.add_event_source(
            aws_lambda_event_sources.DynamoEventSource(table=Tbl.whatsapp_MetaData,
            starting_position=aws_lambda.StartingPosition.TRIM_HORIZON))
        Tbl.whatsapp_MetaData.grant_full_access(Fn.process_stream)

        Fn.langchain_agent_text.grant_invoke(Fn.process_stream)

        # Amazon Lambda Function whatsapp_out - Config

        Fn.whatsapp_out.grant_invoke(Fn.langchain_agent_text)

        # Amazon Lambda Function audio_job_transcriptor - Config

        Fn.audio_job_transcriptor.add_to_role_policy(iam.PolicyStatement( actions=["transcribe:*"], resources=['*']))
        Fn.audio_job_transcriptor.add_environment(key='BucketName', value=s3_deploy.bucket.bucket_name)
        Fn.audio_job_transcriptor.add_environment(key='whatsapp_MetaData', value=Tbl.whatsapp_MetaData.table_name)
        Fn.audio_job_transcriptor.add_environment(key='AudioKeyName', value=AudioKeyName)
        Fn.audio_job_transcriptor.add_environment(key='TextBucketName', value=TextBucketName)

        Fn.audio_job_transcriptor.grant_invoke(Fn.process_stream)

        Fn.audio_job_transcriptor.add_to_role_policy(iam.PolicyStatement( actions=["dynamodb:*"], resources=[f"{Tbl.whatsapp_MetaData.table_arn}",f"{Tbl.whatsapp_MetaData.table_arn}/*"]))
        Fn.audio_job_transcriptor.add_environment(key='ENV_INDEX_NAME', value="jobnameindex")
        Fn.audio_job_transcriptor.add_environment(key='ENV_KEY_NAME', value="messages_id")

        s3_deploy.bucket.grant_read_write(Fn.audio_job_transcriptor) 
        Tbl.whatsapp_MetaData.grant_full_access(Fn.audio_job_transcriptor) 

        # Amazon Lambda Function audio_job_transcriptor done - Config

        
        s3_deploy.bucket.grant_read(Fn.transcriber_done)

        s3_deploy.bucket.add_event_notification(s3.EventType.OBJECT_CREATED,
                                              aws_s3_notifications.LambdaDestination(Fn.transcriber_done),
                                              s3.NotificationKeyFilter(prefix=TextBucketName+"/"))
        
        Fn.transcriber_done.add_to_role_policy(iam.PolicyStatement( actions=["dynamodb:*"], resources=[f"{Tbl.whatsapp_MetaData.table_arn}",f"{Tbl.whatsapp_MetaData.table_arn}/*"]))
        Fn.transcriber_done.add_environment(key='ENV_INDEX_NAME', value="jobnameindex")
        Fn.transcriber_done.add_environment(key='ENV_KEY_NAME', value="messages_id") 
        Fn.transcriber_done.add_environment( key='ENV_LAMBDA_AGENT_TEXT', value=Fn.langchain_agent_text.function_name )       

        Fn.langchain_agent_text.grant_invoke(Fn.transcriber_done)

        Tbl.whatsapp_MetaData.grant_full_access(Fn.transcriber_done)
        Fn.transcriber_done.add_environment(key='whatsapp_MetaData', value=Tbl.whatsapp_MetaData.table_name)

        
        

        """
        s3_deploy.bucket.grant_read_write(Fn.dynamodb_put_item) 

        s3_deploy.bucket.add_event_notification(s3.EventType.OBJECT_CREATED,
                                              aws_s3_notifications.LambdaDestination(Fn.dynamodb_put_item),
                                              s3.NotificationKeyFilter(prefix="airline-dataset/"))
        """
        
        # Amazon Lambda Function query_dynamodb passanger table
        
        Fn.query_dynamodb_passanger.add_environment(key='TABLE_PASSANGER', value=table_passangerTable.table_name)
        Fn.query_dynamodb_passanger.add_environment(key='ENV_KEY_NAME', value="Passenger_ID")
        Tbl.passangerTable.grant_full_access(Fn.query_dynamodb_passanger)

        # Amazon Lambda Function agent Langchain with Amazon Becrock

        Fn.langchain_agent_text.add_environment(key='whatsapp_MetaData', value=table_whatsapp_metadata.table_name)
        Fn.langchain_agent_text.add_environment(key='ENV_INDEX_NAME', value="jobnameindex")
        Fn.langchain_agent_text.add_environment(key='ENV_KEY_NAME', value="messages_id")
        Fn.langchain_agent_text.add_environment(key='TABLE_SESSION_ACTIVE', value=table_session_active.table_name)
        Fn.langchain_agent_text.add_environment(key='KENDRA_INDEX', value= index.index_id)


        table_session_tabble.grant_full_access(Fn.langchain_agent_text) 
        table_whatsapp_metadata.grant_full_access(Fn.langchain_agent_text)
        table_session_active.grant_full_access(Fn.langchain_agent_text)

        Fn.langchain_agent_text.add_to_role_policy(iam.PolicyStatement( actions=["dynamodb:*"], resources=[f"{table_whatsapp_metadata.table_arn}",f"{table_whatsapp_metadata.table_arn}/*"]))

        s3_deploy.bucket.grant_read_write(Fn.langchain_agent_text)
        
        Fn.langchain_agent_text.add_environment( key='ENV_LAMBDA_QUERY_NAME', value=Fn.query_dynamodb_passanger.function_name)
        Fn.langchain_agent_text.add_environment( key='TABLE_SESSION', value=table_session_tabble.table_name)
        Fn.langchain_agent_text.add_environment(key='ENV_MODEL_ID', value=model_id)
        Fn.langchain_agent_text.add_environment( key='WHATSAPP_OUT', value=Fn.whatsapp_out.function_name )

        Fn.langchain_agent_text.add_to_role_policy(iam.PolicyStatement( actions=["bedrock:*"], resources=['*']))

        Fn.query_dynamodb_passanger.grant_invoke(Fn.langchain_agent_text)
        Tbl.passangerTable.grant_full_access(Fn.langchain_agent_text)

        Fn.langchain_agent_text.grant_invoke(Fn.whatsapp_in)

        Fn.langchain_agent_text.add_to_role_policy(iam.PolicyStatement( actions=["kendra:Retrieve"], resources=[f"arn:aws:kendra:{region_name}:{account_id}:index/{index.index_id}"]))
        Fn.langchain_agent_text.add_to_role_policy(iam.PolicyStatement( actions=["kendra:Query"], resources=[f"arn:aws:kendra:{region_name}:{account_id}:index/{index.index_id}"]))

        #s3_deploy.deploy("airline-dataset", "airline-dataset", "airline-dataset")


        #Application insights

