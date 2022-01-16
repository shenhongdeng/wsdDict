from flask import Blueprint, make_response, jsonify
from werkzeug.wrappers import request
from common.response_bean import ResponseBean
from server.home_server import HomeService

AppGetUsrIP = Blueprint("AppGetUsrIP", __name__)


@AppGetUsrIP.route("/home/searchGetUserIp", methods=["GET"])
def homeSearchHandler():
    print(request.data)
    handler = HomeSearchGetUserIPHandler()
    # 以get方法访问的，以get方法返回
    return handler.get()


class HomeSearchGetUserIPHandler(object):
    homeService = HomeService()

    def get(self):
        # 获取参数
        data = self.homeService.get_use_ip()

        # 组装结果，并返回
        result = ResponseBean.set_data(data)
        return make_response(jsonify(result, ensure_ascii=False))
    
    # 这个option有什么用还需要询问师兄
    def options(self):
        self.write('{"errorCode":"00","errorMessage","success"}')
