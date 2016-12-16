import logging
import aiohttp_jinja2
import aiohttp
import random
import string


log = logging.getLogger(__name__)


@aiohttp_jinja2.template('')
def websockets(request):
    resp = aiohttp.web.WebSocketResponse()
    ok, protocol = resp.can_prepare(request)
    if not ok:
        return aiohttp_jinja2.render_template('base.html', request, {})
    yield from resp.prepare(request)
    name = (random.choice(string.ascii_uppercase) +
            ''.join(random.sample(string.ascii_lowercase * 10, 10)))
    request.app['sockets'][name] = resp

    while True:
        msg = yield from resp.receive()
        print("The message was: ", msg.data)
        resp.send_str(msg.data)
        # if msg.type == aiohttp.web.MsgType.text:
        #     for ws in request.app['sockets'].values():
        #         if ws is not resp:
        #             ws.send_str("connected")
        # else:
        #     break

    del request.app['sockets'][name]
    for ws in request.app['sockets'].values():
        ws.send_str("disconnected")
    return resp


def hi(request):
    return aiohttp.web.Response(text='test hi')


def setup(app):
    app.router.add_route('GET', '/', hi)
    app.router.add_route('GET', '/ws', websockets)