import http.client
import json
from time import sleep

def comp(lang, raw_src_code):

    lang_code = -1
    if lang.lower() in ["python", "py"]:
        lang_code = 71
    elif lang.lower() in ["javascript", "js"]:
        lang_code = 63
    else:
        return "err", "language not recognized"
    conn = http.client.HTTPSConnection("judge0.p.rapidapi.com")

    #raw_src_code = input()
    src_code = raw_src_code.replace("\"", "\\\"")
    payload = "{ \"language_id\": " + lang_code + ", \"source_code\": \"" + src_code + "\"}"
    
    headers = {
        'x-rapidapi-host': "judge0.p.rapidapi.com",
        'x-rapidapi-key': "603da35486msh043fd68b633df01p14f6b3jsnc04489362bfa",
        'content-type': "application/json",
        'accept': "application/json"
    }

    conn.request("POST", "/submissions", payload, headers)

    res = conn.getresponse()
    data = res.read()

    #print(data.decode("utf-8"))

    token = eval(data.decode("utf-8"))["token"]

    while True:
        conn.request("GET", f"/submissions/{token}", headers=headers)
        res = conn.getresponse()
        raw_data = res.read().decode("utf-8")
        data = json.loads(raw_data)
        #print(data)
        if data["status"]["id"] in [1, 2]:
            #print("in queue, waiting")
            sleep(0.1)
            continue
        break

    #print(f"stdout: {data['stdout']}\nstderr: {data['stderr']}")
    if data['stderr'] == None:
        return "ok", data['stdout']
    return "err", data['stderr']

