# import from aws powertools needed for logging
from aws_lambda_powertools import Logger, Tracer
# impport from aws powertools needed for batch processing
from aws_lambda_powertools.utilities.batch import BatchProcessor
# import from aws powertools needed for partial failure mechanics
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord
# import from aws powertools needed for event type
from aws_lambda_powertools.utilities.batch import EventType
# import from aws powertools needed for partial batch processing
from aws_lambda_powertools.utilities.batch import process_partial_response

# create a partial failure batch processor for sqs queue
batch_processor = BatchProcessor(event_type=EventType.SQS)

# define Logger and Tracer
tracer = Tracer()
logger = Logger()


# Define a function to receive one record at a time from the batch
# @batch_processor.record_handler
def record_handler(record: SQSRecord):
    print(record.body)
    save_to_dynamodb(record.body)
    if not record.body:
        raise InvalidPayload("Payload does not contain minimum information to be processed.")


# Add an invalid payload exception class
class InvalidPayload(Exception):
    ...
    # Add a custom error message to the exception
    def __str__(self):
        return "Payload does not contain minimum information to be processed."


# Define the handler to kick off processing
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event, context: LambdaContext):
    return process_partial_response(  
        event=event,
        record_handler=record_handler,
        processor=batch_processor,
        context=context,
    )

# Define function send http get request
def send_api_get(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    print(response.status_code)
    r = response.json()
    print(r.get("abilities"))
    # for loop to print first element of r
    abilities_list = []
    for i in r
        ability = r.get("abilities")[0]
        abilities_list += ability
    print abilities_list




