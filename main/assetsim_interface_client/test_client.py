import json
import logging
from google.protobuf import message
from google.protobuf.json_format import ParseDict, MessageToDict
import grpc
import os
import sys

sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../")
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../proto/generated")

from hierarchical_svc_pb2_grpc import HierarchicalSvcStub
from hierarchical_svc_pb2 import HierarchicalSvcRequest, HierarchicalSvcResponse
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def create_stub(channel):
    stub = HierarchicalSvcStub(channel)
    return stub


def read_json_into_proto(file_name):
    logging.info(f"Parsing '{file_name}' into a gRPC protobuf message.")
    with open(file_name) as file:
        optorun_input_dict = json.load(file)
    return ParseDict(
        js_dict = optorun_input_dict,
        message= HierarchicalSvcRequest(),
        ignore_unknown_fields=False
    )


def run_optopy(channel):
    stub = create_stub(channel)
    input_message = read_json_into_proto('assetsim_interface_client/input/battery.json')
    response = stub.RunHierarchical(HierarchicalSvcRequest(
        settings=input_message.settings,
        resources=input_message.resources,
        collections=input_message.collections,
        economics=input_message.economics
        ))
    print(f"Response status: {HierarchicalSvcResponse.RunStatus.Name(response.status)}")
    print(f"Response token: {response.token}")
    print(f"Response error_message: {response.error_message}")
    print(f"Response results_path: {response.results_path}")
    return

if __name__ == '__main__':

    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = '0.0.0.0:5050'

    with grpc.insecure_channel(target) as channel:
        run_optopy(channel)
