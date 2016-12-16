from aiohttp import web
from manager import ws_manager as _ws_manager
import aiohttp_jinja2, logging, asyncio
import jinja2
from views import setup as setup_routes


async def init(loop):
    app = web.Application(loop=loop)
    app.on_shutdown.append(shutdown)
    app['sockets'] = {}
    app['ws_manager'] = _ws_manager
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('C:/Users/casey/Aiohttp-Server/templates'))

    setup_routes(app)

    return app


async def shutdown(app):
    for ws in app['sockets'].values():
        await ws.close()
    app['sockets'].clear()


def main():
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init(loop))
    web.run_app(app)


if __name__ == '__main__':
    main()
