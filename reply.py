import lark_oapi as lark
import json

def reply_message_to_group(client: lark.Client, message: str, message_id: str):


    request = lark.im.v1.ReplyMessageRequest.builder() \
        .message_id(message_id) \
        .request_body(lark.im.v1.ReplyMessageRequestBody.builder()
            .content(message)
            .msg_type("text")
            .reply_in_thread(True)
            .build()) \
        .build()
    
    response: lark.im.v1.ReplyMessageResponse = client.im.v1.message.reply(request)

    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.reply failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        
    return response.data