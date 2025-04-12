import lark_oapi as lark
import json

def forward_message_to_group(client: lark.Client, chat_id: str, message_id: str):

    request = lark.im.v1.ForwardMessageRequest.builder() \
        .message_id(message_id) \
        .receive_id_type("chat_id") \
        .request_body(lark.im.v1.ForwardMessageRequestBody.builder()
            .receive_id(chat_id)
            .build()) \
        .build()
    
    response: lark.im.v1.ForwardMessageResponse = client.im.v1.message.forward(request)

    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.forward failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        
    return response.data