import lark_oapi as lark
import json

def get_message_from_group(client: lark.Client, chat_id: str):

    request: lark.im.v1.ListMessageRequest = lark.im.v1.ListMessageRequest.builder() \
        .container_id_type("chat") \
        .container_id(chat_id) \
        .sort_type("ByCreateTimeDesc") \
        .page_size(10) \
        .build()
    
    response: lark.im.v1.ListMessageResponse = client.im.v1.message.list(request)

    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        
    return response.data