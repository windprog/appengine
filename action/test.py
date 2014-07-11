# coding=utf-8

from engine import url, rest


@url("/abc1", methods="get,put")
@url("/abc2", methods=("post", "head"))
def abc(*args, **kwargs):
    return "abc"


@url("/uid/<uid>")
def uid(request, response, uid):
    print request
    response.set_cookie("a", "b")
    response.set_data(uid)


@url("/rest/<uid>")
def get_uid(start_response, uid):
    return rest(start_response, {"uid": uid})
