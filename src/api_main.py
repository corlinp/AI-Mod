import tornado
from tornado import ioloop, web
from src.text_analysis import analyze_text
from src.utils.ai_utils import root_path

class WebHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(root_path + 'web/index.html')

# Creates an API endpoint. Simply POST the data and it will be analyzed.
class APIHandler(tornado.web.RequestHandler):
    def post(self, idx):
        data = self.request.body.decode('UTF-8')
        if len(data) > 1000:
            self.set_status(400)
            self.write({'error': 'Text too long!'})
            return

        # Analyze and report back
        report = analyze_text(data, cheap=True)
        self.write(report)


def make_app():
    return tornado.web.Application([
        (r"/", WebHandler),
        (r"/([^//]*)", tornado.web.StaticFileHandler, {'path': '../web/'}),
        #(r"/([^//]*)", MainHandler),
        (r"/api(/?)", APIHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
