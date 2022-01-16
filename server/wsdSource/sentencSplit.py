from flask import Blueprint, request, make_response, jsonify
from werkzeug.wrappers import response
from common.response_bean import ResponseBean, CodeConst
import jieba
import json

AppWordSplit = Blueprint("AppWordSplit", __name__)


@AppWordSplit.route("/split", methods=["POST"])
def split():
    handler = WordSplit()
    return handler.post()



class WordSplit(object):
    
    def post(self):
        param = json.loads(request.data)
        sentence = param("sentence")
        if sentence.strip() == "":
            result = ResponseBean.set_status_code(CodeConst.CODE_ERROR_PARAMETER_EMPTY)
            resp = make_response(jsonify(result))
            return resp
        wordList = jieba.lcut(sentence)
        resp = make_response(jsonify(wordList))
        return resp



