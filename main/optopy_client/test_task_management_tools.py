import os
import sys
import logging
import time
import grpc

from task_management_tools import(
    create_task, 
    execute_task, 
    read_worker_status, 
    read_json_into_proto, 
    execute_streaming_tasks,
)


def test_tasks(target):

    with grpc.insecure_channel(target) as channel:
        test_file1 =  "../json_samples/MAR2021DSIOUTPUT/DSI_output_DAY_AHEAD_1.json"
        core_request1 = read_json_into_proto(test_file1)


        id1 = "minion1"
        # create worker
        task1 = create_task(id1, core_request1)
        task_result1 = execute_task(channel, task1)
        read_worker_status(task_result1)
        # execute optimization 
        task2 = create_task(id1, response_type = 0)
        task_result2 = execute_task(channel, task2)
        read_worker_status(task_result2)
        if task_result2.HasField("worker_result"):
            print('Worker result retrieved')
        else:
            print('No task result retrieved')
        task3 = create_task(id1, response_type = 1)
        task_result3 = execute_task(channel, task3)
        read_worker_status(task_result3)
        if task_result3.HasField("worker_result"):
            print('Worker result retrieved')
        else:
            print('No task result retrieved')
        print("\n Doing a parameter update.")
        string_parameters = {"settings.solver_settings.solver": "glpk"}
        task4 = create_task(id1, response_type = 0, string_parameters= string_parameters, kill_worker=False)
        task_result4 = execute_task(channel, task4)
        read_worker_status(task_result4)
        if task_result4.HasField("worker_result"):
            print('Worker result retrieved')
        else:
            print('No task result retrieved')
        task5 = create_task(id1, response_type = 0, kill_worker=True)
        task_result5 = execute_task(channel, task5)
        read_worker_status(task_result5)
        if task_result5.HasField("worker_result"):
            print('Worker result retrieved')
        else:
            print('No task result retrieved')

        # id2 = "minion2"
        # test_file2 =  "../json_samples/MAR2021DSIOUTPUT/DSI_output_DAY_AHEAD_2.json"
        # core_request2 = read_json_into_proto(test_file2)
        # # create worker
        # task1 = create_task(id2, core_request2)
        # task_result1 = execute_task(channel, task1)
        # read_worker_status(task_result1)
        # # execute optimization 
        # task2 = create_task(id2, response_type = 0)
        # task_result2 = execute_task(channel, task2)
        # read_worker_status(task_result2)
        # if task_result2.HasField("worker_result"):
        #     print('Worker result retrieved')
        # else:
        #     print('No task result retrieved')
        # task3 = create_task(id2, response_type = 1, kill_worker=True)
        # task_result3 = execute_task(channel, task3)
        # read_worker_status(task_result3)
        # if task_result3.HasField("worker_result"):
        #     print('Worker result retrieved')
        # else:
        #     print('No task result retrieved')

        # # task streaming 
        # print("\n Test streaming")
        # print("Create workers")
        # task_11 = create_task(id1, core_request1)
        # task_12 = create_task(id2, core_request2)
        # tasks_list1 = [task_11, task_12]
        # task_results_list1 = execute_streaming_tasks(channel, tasks_list1)
        # for task_result in task_results_list1:
        #     read_worker_status(task_result)
        # print("\n Do optimizations") 
        # task_21 = create_task(id1, response_type = 0)
        # task_22 = create_task(id2, response_type = 0)
        # tasks_list2 = [task_21, task_22]
        # task_results_list2 = execute_streaming_tasks(channel, tasks_list2)
        # print(len(task_results_list2))
        # for task_result in task_results_list2:
        #     read_worker_status(task_result)
        # print("\n Just get values") 
        # task_31 = create_task(id1, response_type = 0)
        # task_32 = create_task(id2, response_type = 0)
        # tasks_list3 = [task_31, task_32]
        # task_results_list3 = execute_streaming_tasks(channel, tasks_list3)
        # print(len(task_results_list3))
        # for task_result in task_results_list3:
        #     read_worker_status(task_result)
        # print("\n Kill workers") 
        # task_41 = create_task(id1, response_type = 1, kill_worker = True)
        # task_42 = create_task(id2, response_type = 1, kill_worker = True)
        # tasks_list4 = [task_41, task_42]
        # task_results_list4 = execute_streaming_tasks(channel, tasks_list4)
        # for task_result in task_results_list4:
        #     read_worker_status(task_result)

    return 


if __name__ == '__main__':

    logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
        )

    # target = production-auto-deploy.optopy-server-482-production.svc.cluster.local:5050
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = '0.0.0.0:5050'

    test_tasks(target)