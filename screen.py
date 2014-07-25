import gtk.gdk
import base64
import cStringIO
import os
from BaseHTTPServer import BaseHTTPRequestHandler
from pymouse import PyMouse
from urlparse import urlparse

class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            path = os.path.dirname(os.path.abspath(__file__))
            path = path + "/index.html"
            with open(path, 'r') as content_file:
                content = content_file.read()
            ctype = "text/html"
        elif self.path == "/jquery-2.js":
            path = os.path.dirname(os.path.abspath(__file__))
            path = path + "/jquery-2.js"
            with open(path, 'r') as content_file:
                content = content_file.read()
            ctype = "text/javascript"
        else:
            query = urlparse(self.path).query
            content = self.send_cast(query)
            ctype = "text/plain"
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.end_headers()
        self.wfile.write(content)

    def send_cast(self, query):
        w = gtk.gdk.get_default_root_window()
        sz = w.get_size()
        if query is not '':
            x,y,btn = query.split("&")
            m = PyMouse()
            x = int(sz[0] * float(x))
            y = int(sz[1] * float(y))
            m.click(x, y, int(btn))
        print "The size of the window is %d x %d" % sz
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
        pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
        ab = pb.scale_simple(sz[0]/2, sz[1]/2, gtk.gdk.INTERP_NEAREST)
        fH = cStringIO.StringIO()
        ab.save_to_callback(fH.write, "jpeg", {"quality": '100'}) 
        if (ab != None):
            # ab.save("screenshot.jpeg","jpeg", {"quality": '60'})
            return base64.b64encode(fH.getvalue())
        else:
            return ""     