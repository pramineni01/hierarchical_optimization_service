import logging
import json
import sys
import os

sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../../proto/generated/")

from google.protobuf.json_format import ParseDict, MessageToDict

from optorun_pb2 import OptoRunRequest
from optomain_pb2_grpc import OptoRunServiceStub
from tasks_pb2 import (
    Task, 
    TaskResult, 
    WorkerStatus, 
    WorkerGenerator, 
    ParameterUpdate, 
    WorkerRequest, 
    PairUpdate,
)


    

def read_request_dict_to_proto(optorun_input_dict):
    return ParseDict(
        js_dict = optorun_input_dict,
        message= OptoRunRequest(), 
        ignore_unknown_fields=False,
    )

def read_json_into_proto(file_name):
    logging.info(f"Parsing '{file_name}' into a gRPC protobuf message.")
    with open(file_name) as file:
        optorun_input_dict = json.load(file)
    return read_request_dict_to_proto(optorun_input_dict)

def read_jsons_into_proto_msgs(file_list):
    output_list = []
    for file_name in file_list:
        msg = read_json_into_proto(file_name)
        output_list.append(msg)
    return output_list

def proto_to_dict(response):
    return MessageToDict(response, including_default_value_fields=True, preserving_proto_field_name=True)

def write_proto_to_json(response):
    json_obj = proto_to_dict(response)
    with open(f"../data/optrun_client_output_{response.input.settings.name}.json", 'w') as file:
        json.dump(json_obj, file, indent=4)

    logging.info('\tOptoRun Client Wrote Response to File')

def create_stub(channel):
    stub = OptoRunServiceStub(channel)
    return stub

def create_parameter_update(string_parameters = None, parameters = None):
    parameter_update = ParameterUpdate()
    if string_parameters:
        for key  in string_parameters:
            new_pair = parameter_update.parameters.add()
            new_pair.key = key 
            new_pair.str_value =  string_parameters[key]
    if parameters:
        for key  in parameters:
            new_pair = parameter_update.parameters.add()
            new_pair.key = key 
            new_pair.double_value =  parameters[key]
    return parameter_update

        

def create_task(
    worker_id,
    core_request = None, 
    string_parameters = None,  
    parameters= None, 
    response_type = 1, 
    kill_worker = False
):
    task = Task()
    task.worker_id = worker_id
    if core_request:

        # okay so here if we create a task without a request,
        #  it's either to get status/response/or kill a worker, right?
        # probably better to make the task type explicit.
        # for now I am focused on the first part, come back to second part ...
        worker_generator= WorkerGenerator()
        worker_generator.core_request.CopyFrom(core_request)
        task.worker_generator.CopyFrom(worker_generator)
        return  task 
    else:
        
        worker_request = WorkerRequest()
        worker_request.response_type = response_type
        worker_request.kill_worker = kill_worker
        if parameters or string_parameters:
            parameter_update = create_parameter_update(string_parameters, parameters)
            worker_request.parameter_update.CopyFrom(parameter_update)
        task.worker_request.CopyFrom(worker_request)
        return task

def transmit_streaming_tasks(tasks_list):
    index = 1
    for task in tasks_list:
        logging.info(f'OptoRun Client Sent Task{index}')
        index += 1
        yield(task)


def execute_task(channel, task):
    ## so on the client side, we send different tasks to the server with the same rpc.
    ## we probably check what tasks it is on the server side, and go a route accordingly.
    stub = create_stub(channel)
    task_result  = stub.OptoTask(task)
    return task_result

def execute_streaming_tasks(channel, tasks_list):
    stub = create_stub(channel)
    responses = stub.OptoStreamingTask(transmit_streaming_tasks(tasks_list))
    task_results_list = []
    for task_result in responses:
        task_results_list.append(task_result)
    return task_results_list


def read_worker_status(task_result):
    print("Worker id: ", task_result.worker_id)
    worker_status = task_result.worker_status
    print("Worker last job status: ", worker_status.last_job_status)
    print("Jobs attempted by worker: ", worker_status.total_jobs)
    print("Worker is active: ", worker_status.is_active)
    return 


