import sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
class Handler(SimpleHTTPRequestHandler):
 def handle(self):
  try: super().handle()
  except (BrokenPipeError, ConnectionResetError): pass
 def do_GET(self):
  if self.path.split('?')[0]=='/ping.txt':
   self.send_response(204)
   self.send_header('Content-Length','0')
   self.send_header('Cache-Control','no-store, max-age=0')
   self.end_headers()
   return
  super().do_GET()
 def do_HEAD(self):
  if self.path.split('?')[0]=='/ping.txt':
   self.send_response(204)
   self.send_header('Content-Length','0')
   self.send_header('Cache-Control','no-store, max-age=0')
   self.end_headers()
   return
  super().do_HEAD()
 def log_message(self,fmt,*args):
  if '/ping.txt' not in str(args): super().log_message(fmt,*args)
if __name__=='__main__':
 with ThreadingHTTPServer(('127.0.0.1',int(sys.argv[1])),Handler) as server:
  print('Serving local game',flush=True)
  server.serve_forever()
