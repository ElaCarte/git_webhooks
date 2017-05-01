"""
Classes and functions used in api processing
"""
import hmac
import json
import traceback
from functools import wraps
from hashlib import sha1
import web
import settings


def simple_response_validation(data_dict):
    """
    Simple validation to make sure the github push event has the fields we
    expect

    Should do json schema validation, but there is no schema readily available
    so just make sure the fields we need are there for now

    Make sure to update this when you add field usages!
    """
    try:
        assert 'before' in data_dict
        assert 'after' in data_dict
        assert 'ref' in data_dict
        assert 'repository' in data_dict
        assert 'full_name' in data_dict['repository']
        assert 'head_commit' in data_dict
        assert 'timestamp' in data_dict['head_commit']
        assert 'author' in data_dict['head_commit']
        assert 'pusher' in data_dict
        assert 'name' in data_dict['pusher']
    except AssertionError:
        print "Invalid format data object received or github api " \
              "format changed"
        traceback.print_exc()
        raise web.webapi.BadRequest()


class ForcePushInfoDTO(object):
    """
    Defines force push data that is returned in the force push data lookup
    APIs

    This is usually a subset of info extracted from a github push event
    """

    def __init__(self):

        self.hash_before_force_push = None
        self.hash_after_force_push = None
        self.timestamp_of_after_commit = None
        self.after_commit_author_username = None
        self.pusher_username = None
        self.timestamp_push_event_received = None

    @classmethod
    def from_db_row(cls, row):
        event = row['event']
        created_at = row['created_at']
        event_dict = json.loads(event)
        dto = cls()
        dto.hash_before_force_push = event_dict.get('before')
        dto.hash_after_force_push = event_dict.get('after')
        head_commit = event_dict.get('head_commit', {})
        dto.timestamp_of_after_commit = head_commit.get('timestamp')
        dto.after_commit_author_username = head_commit.get(
            'author').get('username')
        dto.pusher_username = event_dict.get('pusher', {}).get('name')
        dto.timestamp_push_event_received = created_at

        return dto

    def to_dict(self):
        return {
            'hash_before_force_push': self.hash_before_force_push,
            'hash_after_force_push': self.hash_after_force_push,
            'timestamp_of_after_commit': self.timestamp_of_after_commit,
            'after_commit_author_username': self.after_commit_author_username,
            'pusher_username': self.pusher_username,
            'timestamp_push_event_received': self.timestamp_push_event_received
        }


def validate_signature(f):
    """
    Decorator, use only on web.py handler methods for calls from github

    If USE_SECRET_TOKEN is enabled, check if computed sha1 of request data
    matches signature.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if settings.USE_SECRET_TOKEN:
            if not settings.SECRET_TOKEN:
                raise ValueError(
                    'SECRET_TOKEN not set, cannot compute request hash'
                )

            request_data = web.data()
            signature_header = web.ctx.env.get('X-Hub-Signature')
            sha_name, signature = signature_header.split('=')

            if sha_name != 'sha1':
                # github spec says sha1 so if it's not sha1 fail.
                raise web.webapi.BadRequest()

            if not signature:
                raise web.webapi.BadRequest()

            mac = hmac.new(str(settings.SECRET_TOKEN),
                           msg=request_data, digestmod=sha1)
            if not hmac.compare_digest(str(mac.hexdigest()), str(signature)):
                raise web.webapi.Forbidden()

        return f(*args, **kwargs)

    return wrapper
