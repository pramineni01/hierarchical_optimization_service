from services.utils import function_pipe, gql_execute, first_dictionary_item


MUTATION_GQL_S3_UPLOAD = '''
mutation ($data: String!, $path: String!){
    atk_assetsim_gql_s3_upload(
        data: $data,
        path: $path
    ) {
        url
    }
}
'''

QUERY_GQL_GET_S3_FILE = '''
query ($path: String!){
  atk_assetsim_gql_get_s3_file(path: $path) {
    data
  }
}
'''

QUERY_GQL_GET_S3_FILES = '''
query ($paths: [String]){
  atk_assetsim_gql_get_s3_files(paths: $paths) {
    data
    path
  }
}
'''

QUERY_GQL_LIST_S3_FILES = '''
query ($path: String!){
  atk_assetsim_gql_list_s3_files(path: $path) {
    url
  }
}
'''


def s3_upload(data, path):
    result = gql_execute(MUTATION_GQL_S3_UPLOAD,
                         {'data': data, 'path': path})
    return function_pipe(result, [first_dictionary_item])

def s3_get_file(path: str):
    result = gql_execute(QUERY_GQL_GET_S3_FILE, {'path': path})
    return function_pipe(result, [first_dictionary_item])

def s3_get_files(paths: list):
    result = gql_execute(QUERY_GQL_GET_S3_FILES, {'paths': paths})
    return function_pipe(result, [first_dictionary_item])

def s3_list_files(path: str):
    result = gql_execute(QUERY_GQL_LIST_S3_FILES, {"path": path})
    return function_pipe(result, [first_dictionary_item])

def found_file_in_s3(path: str, filename: str):
    result = []
    if s3_list_files(path).get('url'):
        result = [i for i in s3_list_files(path).get(
            'url') if "s3://{}".format(i) == "{}/{}".format(path, filename)]
    return any(result)
