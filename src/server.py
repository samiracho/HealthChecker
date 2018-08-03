from bottle import ServerAdapter


class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        """
        This class is needed to extend the default bottle server in order to expose a stop method.
        :param handler:
        """
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        # self.server.server_close() <--- alternative but causes bad fd exception
        self.server.shutdown()