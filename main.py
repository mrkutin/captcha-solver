# from http.server import HTTPServer, BaseHTTPRequestHandler
# from solve_captcha import solve_base64
#
# class StoppableHTTPServer(HTTPServer):
#     def run(self):
#         try:
#             self.serve_forever()
#         except KeyboardInterrupt:
#             pass
#         finally:
#             self.server_close()
#
#
# class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
#     def do_POST(self):
#         if self.path != '/solve':
#             self.send_error(404)
#             return
#
#         authorization_header = self.headers.get('Authorization')
#         if authorization_header != 'Bearer !$8wCCe&T%BSg7IZQ75KXs4I3O1r9Qmc':
#             self.send_error(401)
#             return
#
#         content_length = int(self.headers['Content-Length'])
#         body = self.rfile.read(content_length)
#         solution = solve_base64(body)
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#         self.wfile.write(solution.encode())
#
#
# httpd = StoppableHTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
# print('Web server is listening to port ', 8000)
# httpd.run()

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
