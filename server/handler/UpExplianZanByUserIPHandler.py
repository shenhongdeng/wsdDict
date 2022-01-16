from flask import Blueprint, request, make_response, jsonify
import json
from common.response_bean import ResponseBean, CodeConst
from handler.FeedbackByUserIPHandler import UpdataExplianByUserIPHandler
from server.home_server import HomeService


AppUpExplianZanByUserIP = Blueprint("AppUpExplianZanByUserIP", __name__)

@AppUpExplianZanByUserIP.route("/home/upExplianZan", methods = ["POST"])
def UpExplianZanByUserIP():
    handler = UpdataExplianByUserIPHandler()
    return handler.post()


# 对正向词典 提交自己的修改意见 点赞，目前我们只是做了正向的词典，没有做反向的此电脑
class UpExplianZanByUserIPHandler(object):
    homeService = HomeService()

    def post(self):
        # 获取参数
        param = json.loads(request.body.decode('utf-8'))
        print(param)

        # 参数为空 useripStr,explain,praiseStr,steponStr,modifyStr
        if param['explainStr'].strip() == '':
            result = ResponseBean.set_status_code(
                CodeConst.CODE_ERROR_PARAMETER_EMPTY)
            resp = make_response(jsonify(result))
            return resp

        # 获取用户ip
        ipStr = self.request.headers.get('X-Forwarded-For')
        ipStr = '144.52.166.105'

        # if ipStr == None or ipStr == " ":
        #     print("ip是空的")
        # else:
        #     print("ip是", ipStr)
        #     ipStr = ipStr.split(',')[0]

        # 1. 获取解释当前点赞数最大的 一条 数据
        explainData = self.homeService.get_explain_info_by_use_ip(
            ipStr, param['explainStr'])
        print("################")
        print(explainData)
        # 2。更新点赞数

        # data = self.homeService.insert_explain_feedback_by_userIp(ipStr,param['wordStr'],param['sententStr'],param['explainStr'],param['feedbackStr'])
        # 组装结果
        result = ResponseBean.set_data(explainData)
        resp = make_response(jsonify(result))
        return resp

    def options(self):
        self.write('{"errorCode":"00","errorMessage","success"}')

