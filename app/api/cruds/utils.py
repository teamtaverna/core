from django.contrib.auth.models import User

from graphql_relay.node.node import from_global_id


def get_errors(e):
    # transform django errors to redux errors
    # django: {"key1": [value1], {"key2": [value2]}}
    # redux: ["key1", "value1", "key2", "value2"]
    fields = e.message_dict.keys()
    messages = ['; '.join(m) for m in e.message_dict.values()]
    errors = [i for pair in zip(fields, messages) for i in pair]
    return errors


def get_user(relayId, otherwise=None):
    try:
        return User.objects.get(pk=from_global_id(relayId)[1])
    except:
        return otherwise


def get_object(object_name, relayId, otherwise=None):
    try:
        return object_name.objects.get(pk=from_global_id(relayId)[1])
    except:
        return otherwise


def load_object(instance, args):
    for key, value in args.items():
        if getattr(instance, key) and key != "id":
            setattr(instance, key, value)
    return instance
