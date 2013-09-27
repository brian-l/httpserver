import socket
import os
import time
import sys
from setproctitle import setproctitle

SO_REUSEPORT = 15

try:
    port = int(sys.argv[2])
except:
    port = 8000

try:
    root = sys.argv[1]
except:
    print "Usage: <root directory> <port (default 8000)>"
    sys.exit(1)

setproctitle('static-http-server')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, SO_REUSEPORT, 1)
s.bind(('', port))
s.listen(1)

print 'Listening on 127.0.0.1:%d' % port

mimetypes = {
    'css': 'text/css',
    'js': 'application/javascript',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
}

def response(req):
    lines = req.split('\n')
    message = lines[0]
    not_found = 'HTTP/1.0 404 Not Found'
    try:
        method, uri, version = message.split(' ')
    except:
        return not_found

    if method == 'GET':
            version = version[:-1]
            start = time.time()
            try:
                extension = uri.split('.')[-1]
                with open("%s/%s" % (root, uri,), 'r') as resource:
                    contents = resource.read()
                print "%s %s %s %d" % (method, uri, version, (time.time() - start))
            except:
                return '%s 404 Not Found' % version

            response = '%s 200 OK\nContent-Type: %s\n\n%s' % (
                version, mimetypes.get(extension), contents
            )
            return response
    else:
        return not_found

while True:
    conn, addr = s.accept()
    data = conn.recv(1024)
    req = response(data)
    conn.send(req)
    conn.close()
