from datetime import datetime
import logging
import os
import uuid

from azure.data.tables import TableServiceClient

from twilio.rest import Client

import azure.functions as func

## Read users list to get list of phone numbers
## for each user, generate survey id and create entry in survey table
## send link to user
def main(mytimer: func.TimerRequest) -> None:
    STORAGE_CONN_STRING = os.environ["STORAGE_CONN_STRING"]
    TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    TWILIO_PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']
    SURVEY_BASE_URL = os.environ['SURVEY_BASE_URL']

    logging.info(STORAGE_CONN_STRING)
    logging.info(TWILIO_ACCOUNT_SID)
    logging.info(TWILIO_AUTH_TOKEN)
    logging.info(TWILIO_PHONE_NUMBER)
    logging.info(SURVEY_BASE_URL)

    table_service_client = TableServiceClient.from_connection_string(conn_str=STORAGE_CONN_STRING)
    survey_table_client = table_service_client.get_table_client(table_name="Surveys")
    user_table_client = table_service_client.get_table_client(table_name="Users")
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    users_item_pages = user_table_client.list_entities()

    for user in users_item_pages:
        survey_data = {
            "PartitionKey": user.get("RowKey"),
            "RowKey": str(uuid.uuid4()),
            "HaveImagesBeenGenerated": False,
            "Response": '',
            "Img": '',
            "SurveyState": 1,
            "Timestamp": datetime.now()
        }
        entity = survey_table_client.create_entity(entity=survey_data)
        message = twilio_client.messages.create(
                                            body=f"Good evening. This is your daily reflection reminder from eMote. Please use this link to fill out your self reflection survey: {SURVEY_BASE_URL}/?sID={survey_data.get('RowKey')}&uID={survey_data.get('PartitionKey')}",
                                            from_=TWILIO_PHONE_NUMBER,
                                            to=user.get("phone")
                                        )

    logging.info('Python timer trigger function ran at %s', datetime.now())
