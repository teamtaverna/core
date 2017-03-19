import json


class GraphqlResponseFlattenerMiddleware(object):
    """Flatten the Graphql responses in a one-level JSON object."""

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            content = json.loads(response.content.decode())
        except json.JSONDecodeError:
            return response

        if 'data' in content and request.method == 'GET':
            flattened_content = {}
            index = 0
            for resource in list(content['data'].values()):
                # Use case for retrieval of all records
                if (resource and 'edges' in resource
                        and isinstance(resource['edges'], list)
                        and 'node' in resource['edges'][0]):

                    flattened_content[list(content['data'].keys())[index]] = []
                    for item in list(resource.values())[0]:
                        flattened_content[
                            list(content['data'].keys())[index]
                        ].append(list(item.values())[0])

                # Use case for retrieval a record
                elif resource is None or isinstance(resource, dict):
                    flattened_content[list(content['data'].keys())[index]] = resource

                index += 1
            content = flattened_content
        elif 'data' in content and request.method == 'POST':
            flattened_content = {}
            for resource in list(content['data'].values()):
                if resource:
                    item = list(resource.values())[0]
                    if item is None or isinstance(item, dict):
                        flattened_content[list(resource.keys())[0]] = item
            content = flattened_content

        response.content = json.dumps(content)
        return response
