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

        if 'data' in content:
            if content['data'].get('__schema'):
                return response
            flattened_content = {}
            index = 0
            for resource in list(content['data'].values()):
                # Use case for retrieval of all records
                key = list(content['data'].keys())[index]
                if (resource and 'edges' in resource
                        and isinstance(resource['edges'], list)
                        and 'node' in resource['edges'][0]):

                    flattened_content[key] = []
                    for item in list(resource.values())[0]:
                        flattened_content[key].append(list(item.values())[0])
                elif isinstance(resource, list):
                    flattened_content[key] = [x for x in resource]
                # Use case for retrieval a record
                elif isinstance(resource, dict):
                    if self.contains_dict_or_None(resource):
                        flattened_content.update(resource)
                    else:
                        flattened_content[key] = resource
                elif resource is None:
                    flattened_content[list(content['data'].keys())[index]] = resource

                index += 1

            if 'errors' in content:
                flattened_content['error'] = content['errors'][0]['message']

            content = flattened_content

        response.content = json.dumps(content)
        return response

    def contains_dict_or_None(self, resource):
        for key, value in resource.items():
            if value is None:
                return True

            return isinstance(value, dict)
