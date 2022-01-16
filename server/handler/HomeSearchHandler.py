from flask import Blueprint, request, jsonify, make_response
from server.home_server import HomeService
from common.response_bean import ResponseBean, CodeConst
from dicts.ner import NERDict
from corenlp_client import CoreNLP
import requests
import json

AppHomeSearch = Blueprint("AppHomeSearch", __name__)

@AppHomeSearch.route("/home/searchContent", methods=["POST"])
def homeSearchHandler():
    print(request.data)
    handler = HomeSearchHandler()
    return handler.post()



class HomeSearchHandler(object):
    def __init__(self):
        self.homeService = HomeService()
        self.ner_dict = NERDict
        self.type2route = {'1': 'zh2zh', '2': 'zh2en', '3': 'en2en'}
        self.annotators = {
            "zh": CoreNLP(url="http://202.112.194.61:8085", lang="zh"),
            "en": CoreNLP(url="http://202.112.194.61:8085", lang="en")
        }

    # 对汉字进行预处理
    def preprocess_zh(self, input_word, input_example):
        return input_word, input_example

    # 对英语进行预处理，因为模型中智能对小写的进行处理
    def preprocess_en(self, input_word, input_example):
        input_word = input_word.lower()
        input_example = input_example.lower()
        return input_word, input_example

    # 查看是不是专业的述语，如果是述语的话直接和表中的相互对应不用再去进行生成释义
    def ner(self, input_word, input_example, input_lang):
        anno = self.annotators[input_lang].annotate(input_example)
        ner_list = anno.entities[0]
        ner_type = None
        if len(ner_list):
            for term in ner_list:
                if input_word == term["text"]:
                    ner_type = term["ner"]
        return ner_type

    # 应为生成的汉字的词语中间是有空格的，我们需要把这些空格去掉
    def postprocess_zh(self, definition):
        return definition.replace(' ', '')

    def postprocess_en(self, definition):
        return definition

    # 查看是不是专业的述语，如果是述语的话直接和表中的相互对应不用再去进行生成释义
    def ner(self, input_word, input_example, input_lang):
        anno = self.annotators[input_lang].annotate(input_example)
        ner_list = anno.entities[0]
        ner_type = None
        if len(ner_list):
            for term in ner_list:
                if input_word == term["text"]:
                    ner_type = term["ner"]
        return ner_type

    # 生成释义的模型就在这里，分为中文和英文两个模型
    def get_definition(self, input_word, input_example, route, input_lang):
        if input_lang == "zh":
            input_word, input_example = self.preprocess_zh(
                input_word, input_example)
        elif input_lang == "en":
            input_word, input_example = self.preprocess_en(
                input_word, input_example)
        if input_word not in input_example:
            definition = ""
        else:
            ner_type = self.ner(input_word, input_example, input_lang)
            if ner_type and ner_type in self.ner_dict:
                definition = self.ner_dict[ner_type][input_lang]
            else:
                res = requests.post(f"http://202.112.194.62:10086/{route}",
                                    json={
                                        "word": input_word,
                                        "example": input_example
                                    })
                definition = res.json()[0]
            out_lang = route.split('2')[1]
            if out_lang == 'zh':
                definition = self.postprocess_zh(definition)
            elif out_lang == 'en':
                definition = self.postprocess_en(definition)
        return definition

    # 检索例句，注意这里的例句是进行检索得出来的，不是直接生成的。
    def get_examples(self, input_word, input_lang):
        # 202.112.194.62替换
        # example_api = "http://127.0.0.1:6889/api/ExampleSearch"
        example_api = "http://202.112.194.62:8088/example-search"
        res = requests.post(example_api,
                            data={
                                "word": input_word,
                                "lang": input_lang
                            })
        retrieval = res.json()
        examples = []
        if not retrieval:
            examples.append({"contentQian": "暂无例句"})
        else:
            for item in retrieval:
                sent = item['content']
                source = item.get('source', '书名暂缺')
                word_idx = sent.index(input_word)
                before = sent[:word_idx]
                after = sent[word_idx + len(input_word):]
                sent = sent.replace(input_word, f"<span>{input_word}</span>")
                examples.append({
                    "content": sent,
                    "contentQian": before,
                    "contentZhong": input_word,
                    "ContentHou": after,
                    "source": source
                })
        return examples

    # 对前边调用的一些封装
    def get_result(self, input_word, input_example, route, input_lang):
        definition = self.get_definition(input_word, input_example, route,
                                         input_lang)
        examples = self.get_examples(input_word, input_lang)
        # 错误处理
        if not definition:
            explain_in_db = "暂无解释" if input_lang == "zh" else \
                "There is no explanation for the moment"
        else:
            explain_in_db = f"{input_word} {definition}"
            # explain_in_db存入数据库
        return definition, examples, explain_in_db
        
    # 运行入口
    def post(self):
        # 获取参数
        param = json.loads(request.data)
        print(param)
        # 参数为空 textType  inputExample  inputWord
        if param['inputWord'].strip() == '' or param['inputExample'].strip(
        ) == '' or param['textType'].strip() == '':
            result = ResponseBean.set_status_code(
                CodeConst.CODE_ERROR_PARAMETER_EMPTY)
            return json.dumps(result, ensure_ascii=False)
        input_word = param['inputWord']
        input_example = param['inputExample']
        # zh en
        text_type = param['textType']
        # 映射
        route = self.type2route[text_type]
        input_lang = 'zh' if text_type == '1' or text_type == '2' else 'en'
        definition, examples, explain_in_db = self.get_result(
            input_word, input_example, route, input_lang)
        
        # 获取用户IP
        ip_str = request.getHeaders('X-Forwarded-For')
        # self.homeService.insert_userIp(ip_str, input_word, input_example,
                                    #    explain_in_db, text_type)

        result_data = [{
            "explain": input_word if definition else 'notin',
            "explain2": definition,
            "examples": examples
        }]
        # 对返回的数据进行封装加上状态码
        result = ResponseBean.set_data(result_data)
        # return make_response(jsonify(result, ensure_ascii=False))
        return make_response(jsonify(result))

    # 这个options没有看明白
    # def options(self):
    #     self.write('{"errorCode":"00","errorMessage","success"}')
if __name__ == "__main__":
    app_home_search.run()