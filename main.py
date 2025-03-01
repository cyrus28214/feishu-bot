from config import Config
import lark_oapi as lark
import json

def main():
    config = Config.load()
    client = lark.Client.builder()\
        .app_id(config.lark.app_id)\
        .app_secret(config.lark.app_secret)\
        .build()
    
    request: lark.im.v1.CreateMessageRequest = lark.im.v1.CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .request_body(lark.im.v1.CreateMessageRequestBody.builder()
            .receive_id("ou_7d8a6e6df7621556ce0d21922b676706ccs")
            .msg_type("text")
            .content("{\"text\":\"test content\"}")
            .build()) \
        .build()

    response: lark.im.v1.CreateMessageResponse = client.im.v1.message.create(request)

    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

if __name__ == "__main__":
    main()
