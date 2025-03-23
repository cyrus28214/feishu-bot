import lark_oapi as lark
import json

def send_message_to_group(client: lark.Client, chat_id: str, message: str):
    '''
    将一条消息发送给一个群聊，目前仅支持纯文本。
    
    TODO: 计划未来支持富文本

    Args:
        client: 飞书客户端
        chat_id: 群聊ID，
        message: 消息内容

    See Also:
        - [飞书开放平台-发送消息](https://open.feishu.cn/document/server-docs/im-v1/message/create?appId=cli_a74823d243e5d01c)
        - [飞书开放平台-如何获得`chat_id`](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/chat-id-description)
    '''

    content = json.dumps({"text": message})

    request: lark.im.v1.CreateMessageRequest = lark.im.v1.CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .request_body(lark.im.v1.CreateMessageRequestBody.builder()
            .receive_id(chat_id)
            .msg_type("text")
            .content(content)
            .build()) \
        .build()
    
    response: lark.im.v1.CreateMessageResponse = client.im.v1.message.create(request)

    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        
    return response.data