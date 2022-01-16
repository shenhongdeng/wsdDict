from flask import Blueprint, make_response, jsonify, request
import json
from common.response_bean import ResponseBean, CodeConst
from handler.InsertReExplianFeedbackByUserIPHandler import AppInsertReExplianFeedbackByUserIP
from server.home_server import HomeService



AppInsertExplianFeedbackByUserIP = Blueprint('AppInsertExplianFeedbackByUserIP', __name__)

@AppInsertExplianFeedbackByUserIP.route("/home/insertExplianFeedback", methods=["POST"])
def InsertExplianFeedbackByUserIP():
    handler = InsertExplianFeedbackByUserIPHandler()
    return handler.post()

# 对正向词典 解释 提出反馈修改意见，对整个词典提供的一些意见
class InsertExplianFeedbackByUserIPHandler(object):
    homeService = HomeService()

    def post(self):
        # 获取参数
        param = json.loads(request.body.decode('utf-8'))
        print(param)

        # 参数为空 useripStr,explain,praiseStr,steponStr,modifyStr
        if param['wordStr'].strip() == '' or param['sententStr'].strip(
        ) == '' or param['explainStr'].strip(
        ) == '' or param['feedbackStr'].strip() == '':
            result = ResponseBean.set_status_code(
                CodeConst.CODE_ERROR_PARAMETER_EMPTY)
            resp = make_response(jsonify(result))
            return resp

        # 获取用户ip
        ipStr = self.request.headers.get('X-Forwarded-For')
        # ipStr = "127.0.0.1"

        if ipStr == None or ipStr == " ":
            print("ip是空的")
        else:
            print("ip是", ipStr)
            ipStr = ipStr.split(',')[0]
            data = self.homeService.insert_explain_feedback_by_userIp(
                ipStr, param['wordStr'], param['sententStr'],
                param['explainStr'], param['feedbackStr'])
        # 组装结果
        result = ResponseBean.set_data(data)
        resp = make_response(jsonify(result))
        return resp

    def options(self):
        self.write('{"errorCode":"00","errorMessage","success"}')


if __name__ == "__main__":
    AppInsertReExplianFeedbackByUserIP.run()

