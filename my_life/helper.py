from random import (
    choice,
    random
)
from hashlib import sha512
import json
import django
from django.utils import timezone
from django.http import HttpResponse

def new_salt():
    source = [chr(x) for x in range(32, 127)]
    salt = u''.join(choice(source) for x in range(0, 32))
    return salt


def new_psw(salt, password):
    password = str(sha512(u'{0}{1}'.format(password, salt).encode('utf-8', 'ignore')).hexdigest())
    return password


def error_handler(error_status, message):
    data = {
            'status': 'ERROR',
            'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
            'code': error_status,
            'message': message
    }
    response = HttpResponse(
        json.dumps(data),
        content_type='application/json',
        status=error_status
    )
    return response


def check_valid_limit_and_offset(limit, offset):
    if not limit and offset:
        return 0, 0
    if limit:
        try:
            int(limit)
        except ValueError as ex:
            print(ex)
    if offset:
        try:
            int(offset)
        except ValueError as ex:
            print(ex)
    return int(limit), int(offset)


def tag_grouping(content, post=False):
    tags = ['<p>', '<br>', '<img>', '<video>', '<link>']
    temp_post = content
    temp_post = temp_post.split('<')
    temp_post = [p for p in temp_post if p != '']
    res = []
    for i in temp_post:
        if post:
            if i[0] == 'p':
                res.append({'tag': 'p', 'content': i[len(tags[0]) - 1:]})
            elif i[0] == 'b':
                res.append({'tag': 'b', 'content': i[len(tags[1]) - 1:]})
            elif i[0] == 'i':
                res.append({'tag': 'i', 'content': i[len(tags[2]) - 1:]})
            elif i[0] == 'v':
                res.append({'tag': 'v', 'content': i[len(tags[3]) - 1:]})
            elif i[0] == 'l':
                res.append({'tag': 'l', 'content': i[len(tags[4]) - 1:]})
        else:
            if i[0] == 'p':
                res.append({'tag': 'p', 'content': i[len(tags[0]) - 1:]})
    return res
