import sys
import os
import json
import grpc

sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../proto/generated")

from master_client import run_btm_primary_secondary

# source_dir = "./sample_inputs/dsi_example"
source_dir = "./sample_inputs/btm_example"
TEST_DICT = {}
# primary_file = "DSI_output_DAY_AHEAD_tendays.json"
# primary_file = "DSI_output_DAY_AHEAD_3.json"
primary_file = "btm_example_load_battery_demand_charge.json"

TEST_DICT["primary"] = os.path.join(source_dir, primary_file)
TEST_DICT["secondary"] = {}
# source_dir = "./sample_inputs/dsi_example/MAR2021DSIOUTPUT/"
source_dir = "./sample_inputs/btm_example/secondaries"
for day in range(1, 4):
    # filename = "DSI_output_DAY_AHEAD_" + str(day) + ".json"
    filename = "btm_example_load_battery_demand_charge_" + str(day) + ".json"

    key = "DAY" + str(day)
    TEST_DICT["secondary"][key] = os.path.join(source_dir, filename)


def main(target):
    with open(TEST_DICT["primary"]) as file:
        primary_request_input_dict = json.load(file)
    
    secondary_requests_file_paths = TEST_DICT["secondary"]
    secondary_requests_list = list()
    for key in secondary_requests_file_paths:
        with open(secondary_requests_file_paths[key]) as file:
            secondary_requests_list.append(json.load(file))
    
    secondary_solution_list, primary_solution = run_btm_primary_secondary(
        target= target,
        primary_request=primary_request_input_dict,
        secondary_requests=secondary_requests_list,
        request_id="test_btm_model",
        relax_primary=False,
        )
    
    for index, solution  in enumerate(secondary_solution_list):
        name = list(secondary_requests_file_paths.keys())[index]
        with open(f"{name}.json", "w") as file:
            json.dump(solution, file, indent=4)
    
    with open("primary_solution.json", "w") as file:
        json.dump(primary_solution, file, indent=4)

    return
    

if __name__ == '__main__':

    # logging.basicConfig(
    #         level=logging.INFO,
    #         format='%(asctime)s - %(levelname)s - %(message)s',
    #     )

    # target = production-auto-deploy.optopy-server-482-production.svc.cluster.local:5050
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = '0.0.0.0:5050'

    main(target)

    
   
    

    
    










