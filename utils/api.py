from urllib import request, parse
import json

def APIRequest(base_url, params=None, postdata=None, headers={}, return_json=True):
    url = base_url
    if params:
        url += "?"
        for key, value in params.items():
            url += f"{key}={parse.quote_plus(value)}&"
        url = url[:-1]
    
    if postdata:
        data = parse.urlencode(postdata).encode()
        req =  request.Request(url, data=data, headers=headers) # this will make the method "POST"
    else:
        req =  request.Request(url, headers=headers)
    resp = request.urlopen(req)
        
    if return_json:
        return json.loads(resp.read())
    else:
        return resp.read()