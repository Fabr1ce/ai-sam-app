from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.batch import (
    BatchProcessor,
    EventType,
    process_partial_response,
)
from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord
from aws_lambda_powertools.utilities.typing import LambdaContext
import requests

# Step 1. Creates a partial failure batch processor for SQS queues. See partial failure mechanics for details
processor = BatchProcessor(event_type=EventType.SQS)  
tracer = Tracer()
logger = Logger()


# Step 1.1 Define an invalid payload exception
class InvalidPayload(Exception):
    ...

# Step 2. Defines a function to receive one record at a time from the batch
@tracer.capture_method
def record_handler(record: SQSRecord):
    payload: str = record.body  # if json string data, otherwise record.body for str
    print("The pokemon's name is ", payload)
    logger.info(payload)
    send_api_get(payload)
    if not payload:
        raise InvalidPayload("Payload does not contain minimum information to be processed.")  


# Step 3. Kicks off processing
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event, context: LambdaContext):
    return process_partial_response(  
        event=event,
        record_handler=record_handler,
        processor=processor,
        context=context,
    )

@tracer.capture_method
def send_api_get(name):
     url = f"https://pokeapi.co/api/v2/pokemon/{name}"
     response = requests.get(url)
     if response.status_code != 200:
        logger.error(f"Request status is {response.status_code}: Failed", response.content)
        raise Exception(f"Request status is {response.status_code}: Failed")
     else:  # if status code is 200, then proceed to get the pokemon type and abilities
    
        print("Request status is", response.status_code, ":Successful")
        r = response.json()
        print(f"{name}'s Type is ", r.get("types")[0].get(    "type").get("name"))
        abilities = []
        for i in r.get("abilities"):
            ability = i.get("ability").get("name")
            abilities += [ability]
        print (f"{name}'s abilities are:",  abilities)