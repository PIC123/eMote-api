import logging
import os
import openai
import json

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    openai.api_key = os.getenv("OPENAI_API_KEY")

    req_body = req.get_json()
    words = req_body.get('words')

    prompt = ", ".join(map(str, words)) + "abstract landscape digital painting"

    resp = openai.Image.create(
        prompt=prompt,
        n=4,
        size="256x256"
    )

    img_urls = [x.get("url") for x in resp.get("data")]

    logging.info(img_urls)

    resp = {
        "urls": img_urls
    }

    return func.HttpResponse(json.dumps(resp))