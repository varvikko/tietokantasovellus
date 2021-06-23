import re
from app import app
from jinja2 import evalcontextfilter, Markup, escape


@app.template_filter()
def split(line):
    parts = re.split('(>>\d+|>.+)', line)
    return list(
        map(
            lambda part: { 'url': re.match('>>\d+', part), 'greentext': re.match('>.+', part), 'content': part },
            parts
        )
    )
