import json
import re

def content_def():
    with open(r"course_content\info_2.txt", 'r') as f:
        content = f.read()

    content = content.strip()
    headers = re.findall(r"\d+\.\s*([\w ]+)",content)
    content = re.split(r"\s*\d+\.\s+[\w ]+\s*\:\s*\n\s*",content)

    if len(headers) == len(content):
        pass
    else:
        content = [value for value in content if value != ""]
        
    dic = dict()
    for h, c in zip(headers,content):
        dic[f"{h}"] = c

    return json.dumps(dic)
    