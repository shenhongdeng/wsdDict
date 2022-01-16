from flask import Blueprint, make_response, jsonify
from common.response_bean import ResponseBean
from server.home_server import HomeService

AppRedictSearchGetUserIp = Blueprint("AppRedictSearchGetUserIp", __name__)

@AppRedictSearchGetUserIp.route('/home/redictSearchGetUserIp', methods = ["GET"])
def ReturnRedictSearchGetUserIp():
    handler = RedictSearchGetUserIPHandler()
    return handler.get()

class RedictSearchGetUserIPHandler(object):
    homeService = HomeService()

    def get(self):
        # 获取参数
        data = self.homeService.get_redict_use_ip()

        # 组装结果
        result = ResponseBean.set_data(data)
        resp = make_response(jsonify(result))
        return resp
        
    def options(self):
        self.write('{"errorCode":"00","errorMessage","success"}')


