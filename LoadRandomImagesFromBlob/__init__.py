import logging
import json
import random
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    STORAGE_CONN_STRING = os.environ["STORAGE_CONN_STRING"]
    req_body = req.get_json()

    blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONN_STRING)

    container_client = blob_service_client.get_container_client(container="static-images")

    img_url_base = "https://emoteuserdata.blob.core.windows.net/static-images/"

    all_blob_urls = [img_url_base + name for name in container_client.list_blob_names()]

    img_urls = []

    for x in range(4):
        img_urls.append(random.choice(all_blob_urls))

    resp = {
        "urls": img_urls
    }

    logging.info(img_urls)

    return func.HttpResponse(json.dumps(resp), status_code=200)
