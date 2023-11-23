# Elevating Customer Support With Rag Langchain Agent Bedrock Dynamodb And Kendra 

This assistant app understands multiple languages and aims to provide self-service support through natural conversation or voice messages for common travel issues, [present in this documentation](/customer-support-bot/airline-qa-base). You can check the status of your flights, as well as data related to your trip using your reservation number or passenger identification. 

And the best... ready to deploy using [AWS Cloud Development Kit](https://aws.amazon.com/cdk).

---
![Digrama parte 1](/imagen/diagram.png)

✅ **AWS Level**: Intermediate - 200   

**Prerequisites:**

- [AWS Account](https://aws.amazon.com/resources/create-account/?sc_channel=el&sc_campaign=datamlwave&sc_content=cicdcfnaws&sc_geo=mult&sc_country=mult&sc_outcome=acq) 
-  [Foundational knowledge of Python](https://catalog.us-east-1.prod.workshops.aws/workshops/3d705026-9edc-40e8-b353-bdabb116c89c/) 

💰 **Cost To Complete**: 
- [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [Amazon Lambda Pricing](https://aws.amazon.com/lambda/pricing/)
- [Amazon DynamoDB Pricing](https://aws.amazon.com/dynamodb/pricing/)
- [Amazon Kendra Pricing](https://aws.amazon.com/kendra/pricing/)
- [Amazon ApiGateway](https://aws.amazon.com/api-gateway/pricing/)
- [Amazon Transcribe Pricing](https://aws.amazon.com/transcribe/pricing/)
- [Whatsapp pricing](https://developers.facebook.com/docs/whatsapp/pricing/)

## Step 0: Activate WhatsApp account Facebook Developers

1- [Get Started with the New WhatsApp Business Platform](https://www.youtube.com/watch?v=CEt_KMMv3V8&list=PLX_K_BlBdZKi4GOFmJ9_67og7pMzm2vXH&index=2&t=17s&pp=gAQBiAQB)

2- [How To Generate a Permanent Access Token — WhatsApp API](https://www.youtube.com/watch?v=LmoiCMJJ6S4&list=PLX_K_BlBdZKi4GOFmJ9_67og7pMzm2vXH&index=1&t=158s&pp=gAQBiAQB)

3- [Get started with the Messenger API for Instagram](https://www.youtube.com/watch?v=Pi2KxYeGMXo&list=PLX_K_BlBdZKi4GOFmJ9_67og7pMzm2vXH&index=5&t=376s&pp=gAQBiAQB)

## Step 1: Previous Configuration

✅ **Clone the repo**

```
git clone https://github.com/elizabethfuentes12/aws-qa-agent-with-bedrock-kendra-and-memory.git
```

✅ **Go to**: 

```
cd re-invent-agent
```

✅ **Create The Virtual Environment**: by following the steps in the [README](/re-invent-agent/README.md)

```
python3 -m venv .venv
```

```
source .venv/bin/activate
```
for windows: 

```
.venv\Scripts\activate.bat
```

✅ **Install The Requirements**:

```
pip install -r requirements.txt
```

✅ **Set Values**:

In [customer_support_bot_stack.py](/customer-support-bot/customer_support_bot/customer_support_bot_stack.py) edit this line with the whatsapp Facebook Developer app number: 

`
DISPLAY_PHONE_NUMBER = 'YOU-NUMBER'
`

This agent maintains the history of the conversation, which is stored in the `session_tabble` Amazon DynamoDB table, also have control session management in the `session_active_tabble` Amazon DynamoDB table, and sets the time [here](/customer-support-bot/lambdas/code/langchain_agent_text/lambda_function.py) in this line:


`
if diferencia > 300:  #session time in seg
`

> **Tip:** [Kenton Blacutt](https://github.com/KBB99), an AWS Associate Cloud App Developer, collaborated with Langchain, creating the [Amazon Dynamodb based memory class](https://github.com/langchain-ai/langchain/pull/1058) that allows us to store the history of a langchain agent in an [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html?sc_channel=el&sc_campaign=genaiwave&sc_content=working-with-your-live-data-using-langchain&sc_geo=mult&sc_country=mult&sc_outcome=acq).


## Step 2: Deploy The App With CDK.

Follow steps [here](/customer-support-bot/README.md)

✅ **Synthesize The Cloudformation Template With The Following Command**:

```
cdk synth
```

✅🚀 **The Deployment**:

```
cdk deploy
```

✅ **Review what is deployed in the stack:** 

- Go to the [AWS Cloudformation console](onsole.aws.amazon.com/cloudformation), select the region where you deployed and click on `CustomerSupportBotStack`:

Then go to the resources tab and explore what's deployed:

![Digrama parte 1](/imagen/stack.jpg)

✅ **Wait a few minutes:** 

This stack automatically creates an Amazon Kendra Index with the data source that contains the [Q&A database of the airline "La inventada"](/customer-support-bot/airline-qa-base), you must wait a few minutes for all the data to be synchronized.

![Digrama parte 1](/imagen/Kendra_datasources.jpg)

## Step 3: Activate WhatsApp Messaging In The App

Go to AWS Secrets Manager and edit the WhatsApp settings and replace them with Facebook Developer settings.

![Digrama parte 1](/imagen/secret.png)

## Step 4: Configure Webhook In Facebook Developer Application


![Digrama parte 1](/imagen/webhook.png)

## Let´s try!

✅ **Q&A:** 

You can start asking for customer service information as if it were an airline customer service line.


![Digrama parte 1](/imagen/QA.gif)

✅ **Passenger information:** 

The CDK stack creates the dynamoDB table named `Passenger_ID` with the [sample passenger dataset](/customer-support-bot/airline-dataset) [from Kaggle](https://www.kaggle.com/datasets/iamsouravbanerjee/airline-dataset). Select one and request information regarding it. What if I now change the language and ask the AI in Spanish?

![Digrama parte 1](/imagen/passanger_information.gif)

> The multilanguage function depends on the [LLM you use](https://aws.amazon.com/es/bedrock/).


✅ **Send it voice notes:**  

> [Amazon Transcribe](https://docs.aws.amazon.com/transcribe/latest/dg/lang-id.html) is able to automatically identify the languages spoken in your media without you having to specify a language code.

![Digrama parte 1](/imagen/voice_note.gif)


## 🚀 Keep testing the agent, play with the prompt in this Amazon Lambda function and adjust it to your need.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

