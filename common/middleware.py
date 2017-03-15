import json


class GraphqlResponseFlattenerMiddleware(object):
    """Flatten the Graphql responses in a one-level JSON object."""

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            res = json.loads(response.content.decode())
        except json.JSONDecodeError:
            return response

        if request.method == 'GET':
            # Use case for retrieval of non-exitent record
            if 'data' in res and list(res['data'].values())[0] is None:
                res = None
            # Use case for retrieval of all records
            elif 'data' in res and 'edges' in list(res['data'].values())[0]:
                res = list(list(res['data'].values())[0].values())[0]
                res = [list(item.values())[0] for item in res]
            # Use case for retrieval of a single existing record
            elif 'data' in res and isinstance(list(res['data'].values())[0], dict):
                res = list(res['data'].values())[0]
        elif request.method == 'POST':
            # Use case for creating, deleting and updating a record
            if 'data' in res and isinstance(list(list(res['data'].values())[0].values())[0], dict):
                res = list(list(res['data'].values())[0].values())[0]
            # Use case for deleting and updating a record
            elif 'data' in res and list(list(res['data'].values())[0].values())[0] is None:
                res = None

        response.content = json.dumps(res)

        return response
