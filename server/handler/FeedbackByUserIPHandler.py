# 点赞 踩 修改意见 更新，这个功能没有上，只是实现了提交意见
import json
from flask import request, Blueprint, make_response, jsonify
from common.response_bean import ResponseBean, CodeConst
from server.home_server import HomeService

AppUpdataExplianByUserIP = Blueprint('AppUpdataExplianByUserIP', __name__)



class UpdataExplianByUserIPHandler(object):
    homeService = HomeService()

    def post(self):
        # 获取参数
        param = json.loads(request.data.decode('utf-8'))
        print(param)

        # 参数为空 useripStr,explain,praiseStr,steponStr,modifyStr
        if param['explain'].strip() == '' or param['praiseStr'].strip(
        ) == '' or param['steponStr'].strip(
        ) == '' or param['modifyStr'].strip() == '':
            result = ResponseBean.set_status_code(
                CodeConst.CODE_ERROR_PARAMETER_EMPTY)
            resp = make_response(jsonify(result, ensure_ascii=False))
            return resp

        # 获取用户ip
        ipStr = self.request.headers.get('X-Forwarded-For')
        # ipStr = "127.0.0.1"
        print(ipStr)
        if ipStr == None or ipStr == " ":
            print("ip是空的")
        else:
            print("ip是", ipStr)
            ipStr = ipStr.split(',')[0]
            data = self.homeService.updata_search_info(ipStr, param['explain'],
                                                       param['praiseStr'],
                                                       param['steponStr'],
                                       param['modifyStr'])
        # 组装结果
        result = ResponseBean.set_data(data)
        resp = make_response(jsonify(result, ensure_ascii=False))
        return resp

    def options(self):
        self.write('{"errorCode":"00","errorMessage","success"}')

