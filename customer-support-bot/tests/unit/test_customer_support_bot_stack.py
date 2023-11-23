import aws_cdk as core
import aws_cdk.assertions as assertions

from customer_support_bot.customer_support_bot_stack import CustomerSupportBotStack

# example tests. To run these tests, uncomment this file along with the example
# resource in customer_support_bot/customer_support_bot_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CustomerSupportBotStack(app, "customer-support-bot")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
