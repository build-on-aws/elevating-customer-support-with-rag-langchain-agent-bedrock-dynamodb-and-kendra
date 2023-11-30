'''Custom generic CloudFormation resource example'''

import json
import requests
import boto3
import botocore.exceptions

kendra_client = boto3.client("kendra")


def lambda_handler(event, context):
    '''Handle Lambda event from AWS'''
    # Setup alarm for remaining runtime minus a second
    # signal.alarm((context.get_remaining_time_in_millis() / 1000) - 1)
    try:
       
        print('REQUEST RECEIVED:', event)
        print('REQUEST RECEIVED:', context)
        if event['RequestType'] == 'Create':
            print('CREATE!')
            event['PhysicalResourceId'] = 'NOT_YET'
            create_webcrawler2(event, context)
            # send_response(event, context, "SUCCESS",{"Message": "Resource creation successful!"})
        elif event['RequestType'] == 'Update':
            print('UPDATE!')
            update_webcrawler2(event, context)

        elif event['RequestType'] == 'Delete':
            print('DELETE!')
            delete_webcrawler2(event, context)
           
        else:
            print('FAILED!')
            send_response(event, context, "FAILED",
                          {"Message": "Unexpected event received from CloudFormation"})
    except Exception as error: 
        print('FAILED!', error)
        send_response(event, context, "FAILED", {
            "Message": "Exception during processing"})


def create_webcrawler2 (event, context):
    
    if "ResourceProperties" in event:
        print ("create_datasource")
        props = event['ResourceProperties']
        
        print("props:",props)
        
        kwargs = dict ( 
            Name=props['name'],
            IndexId=props['index_id'],
            Type=props['type'],
            Configuration={"TemplateConfiguration": {"Template":json.loads(props['template'])}},
            Description=props['description'],
            Schedule=props['schedule'],
            RoleArn=props['role_arn'],
            LanguageCode=props['language_code']
        )
        
        print ("kwargs:",kwargs)
        res = kendra_client.create_data_source(**kwargs)
        index_id = props['index_id']
        ds_id = res['Id']
        starting = kendra_client.start_data_source_sync_job(
            Id=ds_id,
            IndexId=index_id
        )
        print ("start sync job:", starting)

        event['PhysicalResourceId'] = f"{index_id}|{ds_id}"
        send_response(event, context, "SUCCESS",{"Message": "Resource creation successful!"})
    else:
        print("no resource properties!")


def delete_webcrawler2 (event, context):
    if 'PhysicalResourceId' in event:
        if event['PhysicalResourceId'] !="NOT_YET":
            index_id, id =  event['PhysicalResourceId'].split("|")
            response = kendra_client.delete_data_source(Id=id,IndexId=index_id)
    send_response(event, context, "SUCCESS", {"Message": "Resource deletion successful!"})


def update_webcrawler2(event, context):
    if "ResourceProperties" in event:
        print ("create_datasource")
        props = event['ResourceProperties']
        index_id, id =  event['PhysicalResourceId'].split("|")

        print("props:",props)
        
        kwargs = dict ( 
            Id = id,
            Name=props['name'],
            IndexId=index_id,
            Configuration={"TemplateConfiguration": {"Template":json.loads(props['template'])}},
            Description=props['description'],
            Schedule=props['schedule'],
            RoleArn=props['role_arn'],
            LanguageCode=props['language_code']
        )
        
        print ("kwargs:",kwargs)
        res = kendra_client.update_data_source(**kwargs)
        print ("response: ",res)
        starting = kendra_client.start_data_source_sync_job(
            Id=id,
            IndexId=index_id
        )
        print ("start sync job:", starting)
        #index_id = props['index_id']
        #event['PhysicalResourceId'] = f"{index_id}|{ds_id}"
        ##ds_id = res['Id']
        # send_response(event, context, "SUCCESS",{"Message": "Resource creation successful!"})
    else:
        print("no resource properties!")
    send_response(event, context, "SUCCESS", {"Message": "Resource update successful!"})

def send_response(event, context, response_status, response_data):
    '''Send a resource manipulation status response to CloudFormation'''
    response_body = json.dumps({
        "Status": response_status,
        "Reason": "See the details in CloudWatch Log Stream: " + context.log_stream_name,
        "PhysicalResourceId": event['PhysicalResourceId'] if 'PhysicalResourceId' in event else "NOPHYID",
        "StackId": event['StackId'],
        "RequestId": event['RequestId'],
        "LogicalResourceId": event['LogicalResourceId'],
        "Data": response_data
    })
    headers = {
    'Content-Type': 'application/json',  
    'Content-Length': str(len(response_body))
    } 


    print('ResponseURL: ', event['ResponseURL'])
    print('ResponseBody:', response_body)

    response = requests.put(event['ResponseURL'], 
                            data=response_body, headers=headers)
    
    print("Status code:", response.status_code)
    print("Status message:", response.text)

    return response


def timeout_handler(_signal, _frame):
    '''Handle SIGALRM'''
    raise Exception('Time exceeded')

# signal.signal(signal.SIGALRM, timeout_handler)

