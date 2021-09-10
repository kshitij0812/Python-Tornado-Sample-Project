import argparse
import handlers
import logging
import traceback

import tornado.ioloop

import handlers
import settings

# Configuring logging to show timestamps
logging.basicConfig( format='[%(asctime)s] p%(thread)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG )


async def init():
    config = await settings.get_config()    # Get config
    return config


class Application(tornado.web.Application):
    def __init__(self, config, port):
        routes = [
            # Routes for webpages
            (r"/", handlers.common.Homepage),
            (r"/book_list", handlers.common.BookList),
            (r"/activity_history", handlers.common.ActivityHistory),

            # Routes for APIs
            (r"/api/v1/add_book", handlers.api.AddBook),
            (r"/api/v1/book_list", handlers.api.BookList),
            (r"/api/v1/manage_book", handlers.api.ManageBook),
        ]

        tornado.web.Application.__init__(self, handlers=routes, **config)
        self.listen(port, address='0.0.0.0')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8003)
    args = parser.parse_args()

    config = tornado.ioloop.IOLoop.current().run_sync(init)

    application = Application(config, args.port)

    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        pass
    except Exception:
        traceback.print_exc()
    finally:
        tornado.ioloop.IOLoop.current().stop()
