from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from functools import reduce
import os


AUTHORIZATION = os.getenv('AUTHORIZATION')
HASURA_URL = os.getenv('HASURA_URL')
GQL_CLIENT = None
X_HASURA_ACCESS_KEY = os.getenv('X_HASURA_ACCESS_KEY')


GQL_TRANSPORT = RequestsHTTPTransport(
    url=HASURA_URL,
    use_json=True,
    headers={
        "authorization": AUTHORIZATION,
        'x-hasura-access-key': X_HASURA_ACCESS_KEY
    },
    retries=3
)

GQL_CLIENT = Client(
    transport=GQL_TRANSPORT,
    fetch_schema_from_transport=True,
)


def gql_execute(statement, variable=None):
    return GQL_CLIENT.execute(gql(statement), variable)

def first_dictionary_item(dictionary):
    key = list(dictionary.keys())[0]
    return dictionary.get(key)

def function_pipe(initial_value, function_list):
    return reduce(lambda a, c: c(a), function_list, initial_value)
