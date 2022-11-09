import this
import requests

SUPPORTED_HTTP_METHODS = set([
    "GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"
])




def all_route():
    return {
    "role": "http://127.0.0.1:5000/role",
    "app": "http://127.0.0.1:5000/app",
    "learning_journey": "http://127.0.0.1:5000/learning_journey",
    "positions": "http://127.0.0.1:5000/positions",
    "registration": "http://127.0.0.1:5000/registration",
    "skill_rewarded": "http://127.0.0.1:5000/skill_rewarded",
    "skill_set": "http://127.0.0.1:5000/skill_set",
    "skill": "http://127.0.0.1:5000/skill",
    "staff": "http://127.0.0.1:5000/staff"
}


def invoke_http(url, method='GET', json=None, **kwargs):
    """A simple wrapper for requests methods.
       url: the url of the http service;
       method: the http method;
       data: the JSON input when needed by the http method;
       return: the JSON reply content from the http service if the call succeeds;
            otherwise, return a JSON object with a "code" name-value pair.
    """
    code = 200
    result = {}

    try:
        if method.upper() in SUPPORTED_HTTP_METHODS:
            r = requests.request(method, url, json = json, **kwargs)
        else:
            raise Exception("HTTP method {} unsupported.".format(method))
    except Exception as e:
        code = 500
        result = {"code": code, "message": "invocation of service fails: " + url + ". " + str(e)}
    if code not in range(200,300):
        return result

    ## Check http call result
    if r.status_code != requests.codes.ok:
        code = r.status_code
    try:
        result = r.json() if len(r.content)>0 else ""
    except Exception as e:
        code = 500
        result = {"code": code, "message": "Invalid JSON output from service: " + url + ". " + str(e)}

    return result

