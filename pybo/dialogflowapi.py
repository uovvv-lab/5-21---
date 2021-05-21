import os
import dialogflow
from google.api_core.exceptions import InvalidArgument
from google.protobuf.json_format import MessageToJson
import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=''

DIALOGFLOW_PROJECT_ID='newagent-ooad'
DIALOGFLOW_LANGUAGE_COOE='ko'

session_client=dialogflow.SessionsClient()

def chat(text, session_id='me'):
    session=session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)
    text_input=dialogflow.types.TextInput(text=text, language_code=DIALOGFLOW_LANGUAGE_COOE)
    query_input=dialogflow.types.QueryInput(text=text_input)
    try:
        response= session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    print(response)

    return '성공'

chat('안녕', '12345')

