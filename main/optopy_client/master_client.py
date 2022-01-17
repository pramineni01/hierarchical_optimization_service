import json
import sys
import os
import logging
import time
import grpc
# sys.path.append(f"{os.path.dirname(__file__)}/../protobuf/generated")

from task_management_tools import (
    create_task, 
    execute_task, 
    read_worker_status, 
    read_json_into_proto, 
    execute_streaming_tasks,
    read_request_dict_to_proto,
    proto_to_dict,
)
from optorun_pb2 import OptoRunResponse
from collections_pb2 import CollectionType

class HOPT_MASTER():

    def __init__(
        self,
        channel,
        primary_request: dict,
        primary_request_id: str,
        secondary_requests: list,
        secondary_request_ids: list,    
    ):
        self.channel = channel 
        self.secondary_ids = secondary_request_ids
        self.primary_id = primary_request_id
        ## TODO: should we infere the "unique" id of the primary and secondary requests from the
        ## name section of the proto? and then assert the unique name?
        self.secondary_requests_results = list()
        self.primary_request_results = None

        self.primary_request = read_request_dict_to_proto(primary_request)
        self.secondary_requests = list()
        for secondary_request in secondary_requests:
            self.secondary_requests.append(
                read_request_dict_to_proto(secondary_request)
            )
        return 

    def send_primary_task(self, relax_primary):
        self.primary_request.settings.run_settings.relax_integers = relax_primary
        task = create_task(self.primary_id, self.primary_request)
        task_result = execute_task(self.channel, task)
        read_worker_status(task_result)
        # TODO: I can remove this later; better yet make it a debug level logging.
        master_result = task_result.worker_result
        # TODO: should I parse the task result and return the response?
        return 

    def send_secondary_tasks(self):
        tasks_list = list()
        for index, request in enumerate(self.secondary_requests):
            # core_request = read_request_dict_to_proto(request)
            task = create_task(self.secondary_ids[index], request)
            tasks_list.append(task)

        task_results_list = execute_streaming_tasks(self.channel, tasks_list)
        for task_result in task_results_list:
            read_worker_status(task_result)
        return 

    def solve_and_return_primary(self):
        task = create_task(self.primary_id, response_type = 0)
        start = time.time()
        task_result = execute_task(self.channel, task)
        end = time.time()
        print("Duration of primary work optimization job: ", end - start)
        read_worker_status(task_result)
        self.primary_request_results = task_result.worker_result
        return 

    def solve_and_return_secondaries(self):
        tasks_list = list()
        for worker_id in self.secondary_ids:
            task = create_task(worker_id, response_type = 0)
            tasks_list.append(task)
        start = time.time()
        task_results_list = execute_streaming_tasks(self.channel, tasks_list)
        end = time.time()
        print("Duration of secondary optimization jobs: ", end - start)
        for task_result in task_results_list:
            read_worker_status(task_result)
            self.secondary_requests_results.append(task_result.worker_result)
        # wrap up responses and deliver
        return  

    def terminate_all(self):
        self._terminate_primary()
        self._terminate_secondaries()
        return 

    def _terminate_primary(self):
        task = create_task(self.primary_id, kill_worker = True)
        task_result = execute_task(self.channel, task)
        read_worker_status(task_result)
        # ADD code to chek task_result
        return
    
    def _terminate_secondaries(self):
        tasks_list = list()
        for worker_id in self.secondary_ids:
            task = create_task(worker_id, kill_worker = True)
            tasks_list.append(task)
        task_results_list = execute_streaming_tasks(self.channel, tasks_list)
        for task_result in task_results_list:
            read_worker_status(task_result)
        # ADD code to check task_results_list
        return

    def _parse_primary_response_boundary_conditions(self):
        # okay so here need to extract boundary condition for secondary 
        # 1 issue is how to map the primary and secondary timelines.
            # 1.1  okay let me think of the case for 1 primary and 1 secondary
                # will need both primary and secondary timelines -> primary/secondary requests
                # will need the primary response, 

        # 2. issue is how to have parsing of boundary condition to be generic.
        #  2.1 I can just make it quick for battery soc; and I need peak threshold (where is it now)
        # 2.2 if i want it to be any boundary parm (like commit for gen, etc); then how would it be?
            # the secondary should know what boundary condition it needs to get
            # should this get embeded in optopy standard request?
                # like instead of initial/final soc, and initial commit, we would have an atribute boundary condition for all assets?
                # or does it come under the general umbrella of prior_commitments.
                #  it is not ideal to have initial soc from commitments.
            # we can just 

        for secondary_request in self.secondary_requests:
            self._set_boundary_soc_conditions_from_primary(secondary_request)
            self._set_existing_peak_from_primary(secondary_request) 
        return
    
    def _set_boundary_soc_conditions_from_primary(self, secondary_request):

        primary_request = self.primary_request
        primary_results = self.primary_request_results

        initial_state_index, final_state_index = self._map_secondary_horizon_indices(primary_request, secondary_request)

        battery_list = [
            resource for resource in secondary_request.resources 
                if resource.HasField("properties_storage")
        ]
        # I could probably also use the resource_type enum

        for battery in battery_list:
            self._map_battery_boundary_soc(battery, primary_results, initial_state_index, final_state_index )

        return

    def _map_secondary_horizon_indices(self, primary_request, secondary_request):

        primary_horizon = primary_request.settings.run_horizon.run_horizon_fmt_3.horizon_uniform_intervals
        secondary_horizon = secondary_request.settings.run_horizon.run_horizon_fmt_3.horizon_uniform_intervals

        # should I use timestamp compare method instead?
        initial_state_index = list(primary_horizon).index(secondary_horizon[0])
        
        final_state_index = list(primary_horizon).index(secondary_horizon[-1])
        

        return initial_state_index, final_state_index
    
    def _map_battery_boundary_soc(self, battery, primary_results, initial_state_index, final_state_index):

        primary_battery = [ 
            resource for resource in primary_results.result.resources
                if resource.name == battery.name
        ][0]

        battery.properties_storage.initial_soc.value = \
            primary_battery.outputs_storage.soc.interval_values_fmt_1.values[initial_state_index].value
        battery.properties_storage.final_soc.value = \
            primary_battery.outputs_storage.soc.interval_values_fmt_1.values[final_state_index].value

        return

    def _set_existing_peak_from_primary(self, secondary_request):
        primary_current_peak = self._get_primary_peak_load()
        # the existing peaks atribute is  defined as a list! what does this bear for us?
        # we could have multiple peaks that are assigned to different workers
        # for now I am considering a single peak load for a month.
        secondary_request.enrollments[0].properties.existing_peaks[0].existing_peak_value.value = primary_current_peak
        return
    
    def _get_primary_peak_load(self):
        # 1. how the peak load is extracted from results?
            # should we look at the site(collections), or loads(resources), or net load, etc?
        # 2. do I have the parsing in service; I should!
        # 3. this is mainly for the case of one site only, what about the case when there are multiple sites?

        site_collections = [ 
            collection  for collection  in self.primary_request_results.result.collections
                if collection.type == CollectionType.COLLECTION_TYPE_SITE
        ]
        assert(len(site_collections) ==1)
        site_results = site_collections[0]

        site_export_vals = [ 
            value.value for value in  site_results.outputs_collection_site.net_export.interval_values_fmt_1.values
        ]
        site_max_import = abs(min(site_export_vals))
        return site_max_import

    def get_final_solution(self):
        secondary_solutions = list()
        for response in self.secondary_requests_results:
            secondary_solutions.append(
                proto_to_dict(response)
            )
        return secondary_solutions

    def get_primary_solution(self):
        return proto_to_dict(self.primary_request_results)


def run_btm_primary_secondary(target, primary_request, secondary_requests, request_id, relax_primary=True):

    primary_request_id = "master_" + request_id 
    secondary_requests_id_list = list()
    for index in range(len(secondary_requests)):
        secondary_requests_id_list.append("minion_" + request_id + "_" + str(index))
    
    with grpc.insecure_channel(target) as channel:
        master = HOPT_MASTER(
            channel=channel,
            primary_request=primary_request,
            primary_request_id=primary_request_id,
            secondary_requests=secondary_requests,
            secondary_request_ids=secondary_requests_id_list,
        )
        print("\n Sending Primary.")
        master.send_primary_task(relax_primary)
        master.solve_and_return_primary()
        master._parse_primary_response_boundary_conditions()
        master.send_secondary_tasks()
        master.solve_and_return_secondaries()
        print("\n Terminating.")
        master.terminate_all()
    return master.get_final_solution(), master.get_primary_solution()