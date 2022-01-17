from concurrent.futures import ThreadPoolExecutor
import logging
import grpc
import json
import sys
import os

sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../")
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../proto/generated")

# from protobuf.generated import hierarchical_svc_pb2, hierarchical_svc_pb2_grpc
from hierarchical_svc_pb2_grpc import HierarchicalSvcServicer, add_HierarchicalSvcServicer_to_server
from hierarchical_svc_pb2 import HierarchicalSvcResponse

import break_problems

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

class Hierarchical(HierarchicalSvcServicer):

    def RunHierarchical(self, request, context):
        settings = request.settings
        economics = request.economics
        collections = request.collections
        resources = request.resources
        secondary_problems = break_problems.primary_problem_to_secondary(settings,economics,collections,resources)
        _ = write_dict_to_files(secondary_problems)
        return HierarchicalSvcResponse(
            status="RUNNING",
            token="abc",
            error_message="",
            results_path="s3://bucket/results"
        )

def write_dict_to_files(input):
    """Writes a dict with multiple keys in multiple JSON files."""
    cwd = os.getcwd()
    for key, data in input.items():
        with open(f'assetsim_interface_client/output/{key}.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

def main():
    server = grpc.server(ThreadPoolExecutor(max_workers=400), maximum_concurrent_rpcs=300)
    add_HierarchicalSvcServicer_to_server(Hierarchical(), server)
    port = 5050
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info('Optopy server ready on port %r', port)
    server.wait_for_termination()

if __name__ == "__main__":
    main()
