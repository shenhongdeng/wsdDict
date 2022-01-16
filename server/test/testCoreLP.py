from corenlp_client import CoreNLP


example = "存储器芯片的读取和写入的特点"

resp = CoreNLP("http://202.112.194.61:8085", lang="zh")(example)
