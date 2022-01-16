from flask import Flask
from flask_cors import CORS
from handler.FeedbackByUserIPHandler import AppUpdataExplianByUserIP
from handler.HomeSearchGetUserIPHandler import AppGetUsrIP
from handler.HomeSearchHandler import AppHomeSearch
from handler.InsertExplianFeedbackByUserIPHandler import AppInsertExplianFeedbackByUserIP
from handler.InsertReExplianFeedbackByUserIPHandler import AppInsertReExplianFeedbackByUserIP
from handler.RedictSearchGetUserIPHandler import AppRedictSearchGetUserIp
from handler.RedictSearchHandler import AppRedictSearch
from handler.UpExplianZanByUserIPHandler import AppUpExplianZanByUserIP
from config import config 

app = Flask(__name__)
app.config.from_object(config['development'])
CORS(app, support_credentials = True)
app.register_blueprint(AppUpdataExplianByUserIP)
app.register_blueprint(AppGetUsrIP)
# /home/searchContent
app.register_blueprint(AppHomeSearch)
app.register_blueprint(AppInsertExplianFeedbackByUserIP)
app.register_blueprint(AppInsertReExplianFeedbackByUserIP)
app.register_blueprint(AppRedictSearchGetUserIp)
app.register_blueprint(AppRedictSearch)
app.register_blueprint(AppUpExplianZanByUserIP)

if __name__ == "__main__":
    # print(app.url_map)
    # host = '0.0.0.0'
    host = "127.0.0.1"
    port = 8001
    app.run(debug = True, host=host, port=port)


