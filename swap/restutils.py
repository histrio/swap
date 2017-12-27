import json as _json

from swap import __version__


def gen_error(obj=None, message='', code=400):
    if not obj:
        obj = {}
    res = {
        '_status': 'ERR',
        '_error': {'code': code, 'message': message}
    }
    res.update(obj)
    return _json.dumps(res), code, {'Content-Type': 'application/json'}


def gen_ok(obj=None, code=200):
    result = {'API': 'Swap', 'version': __version__, 'status': "OK"}
    if obj is not None:
        result.update({'result': obj})
    return _json.dumps(obj), code, {'Content-Type': 'application/json'}


def return_error(e):
    return gen_error(e.obj, e.message, e.code)


class Return(Exception):
    def __init__(self, message='', code=400, obj=None):
        if obj is None:
            self.obj = {}
        else:
            self.obj = obj
        self.code = code
        super(Return, self).__init__(message)
