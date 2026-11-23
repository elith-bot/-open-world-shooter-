import sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
class Handler(SimpleHTTPRequestHandler):
 def handle(self):
  try: super().handle()
  except (BrokenPipeError, ConnectionResetError): pass
 def end_headers(self):
  if self.path.split("?")[0]=="/ping.txt": self.send_header("Cache-Control","no-store")
  super().end_headers()
if __name__=="__main__":
 with ThreadingHTTPServer(("127.0.0.1",int(sys.argv[1])),Handler) as server:
  print("Serving local game",flush=True)
  server.serve_forever()
