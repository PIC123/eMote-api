import logging
import os
from datetime import datetime
import json

import azure.functions as func

from azure.data.tables import (TableServiceClient, UpdateMode)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    STORAGE_CONN_STRING = os.environ["STORAGE_CONN_STRING"]

    req_body = req.get_json()

    table_service_client = TableServiceClient.from_connection_string(conn_str=STORAGE_CONN_STRING)
    table_client = table_service_client.get_table_client(table_name="Surveys")

    try:
        entry = table_client.get_entity(row_key=req_body.get("surveyID"), partition_key=req_body.get("userID"))
    except:
        return func.HttpResponse(
            "Entry not found",
            status_code=404
        )
    else:
        return func.HttpResponse(
            json.dumps(entry),
            status_code=200
        )
