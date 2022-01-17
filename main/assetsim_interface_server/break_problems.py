import math
import copy
from datetime import datetime as dt
from datetime import timedelta

from google.protobuf.json_format import MessageToDict
from tariff_convert import sce_gs2_tariff_convert



def secs_till_midnight(date):
    midnight = dt(year=date.year, month=date.month, day=date.day, hour=23, minute=59, second=59)
    delta_secs = midnight - date
    return delta_secs.total_seconds()

def primary_problem_to_secondary(settings, economics, collections, resources):
    """Returns a dictionary of daily and monthly optimization problems."""
    settings = MessageToDict(settings, preserving_proto_field_name=True)
    economics = MessageToDict(economics, preserving_proto_field_name=True)
    collections_list = []
    resources_list = []

    for c in collections:
        collections_list.append(MessageToDict(c, preserving_proto_field_name=True))
    for r in resources:
        resources_list.append(MessageToDict(r, preserving_proto_field_name=True))

    interval_duration_secs = settings.get('run_horizon', {}).get('run_horizon_fmt_2', {}).get('base_interval_duration')
    number_of_intervals = settings.get('run_horizon', {}).get('run_horizon_fmt_2', {}).get('number_of_intervals')
    if not interval_duration_secs:
        raise ValueError("base_interval_duration missing in the optimization problem settings.")
    elif not interval_duration_secs.endswith('s'):
        raise ValueError("base_interval_duration format is not supported in the optimization problem settings.")
    else:
        interval_duration_secs = int(interval_duration_secs.replace('s',''))
    
    if not number_of_intervals:
        raise ValueError("number_of_intervals missing in the optimization problem settings.")
    else:
        number_of_intervals = int(number_of_intervals)

    start_time = settings.get('run_horizon', {}).get('run_horizon_fmt_2', {}).get('horizon_start_time')
    start_time_dt = dt.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
    end_time_dt = start_time_dt + timedelta(seconds=number_of_intervals*interval_duration_secs)
    dates = []
    monthly_problem_dates = {}
    daily_problem_dates = {}
    secondary_problems = {}
    t = start_time_dt
    while t <= end_time_dt:
        dates.append(t)
        t = t + timedelta(seconds=interval_duration_secs)
    for d in dates:
        if not monthly_problem_dates.get(f'{d.year}.{d.month}'):
            monthly_problem_dates[f'{d.year}.{d.month}'] = []
        monthly_problem_dates[f'{d.year}.{d.month}'].append(d)
    for month, dates in monthly_problem_dates.items():
        daily_problem_dates[month] = daily_problem_dates.get('month') or {}
        for d in dates:
            daily_problem_dates[month][str(d.day)] = daily_problem_dates[month].get(str(d.day)) or []
            daily_problem_dates[month][str(d.day)].append(d)
        for k, v in daily_problem_dates[month].items():
            daily_problem_dates[month][k] = (min(v), max(v))

    for month, monthly_dates in monthly_problem_dates.items():
        daily_problems = []
        monthly_settigs = copy.deepcopy(settings)
        monthly_run_horizon = {
            'run_horizon': {
                'horizon_start_time': min(monthly_dates).strftime("%Y-%m-%dT%H:%M:%SZ"), 
                'base_interval_duration': f'{interval_duration_secs}s', 
                'number_of_intervals': math.floor((max(monthly_dates) - min(monthly_dates))/timedelta(seconds=interval_duration_secs))
            }
        }
        monthly_settigs.update(monthly_run_horizon)
        
        for day, minmax_times in daily_problem_dates[month].items():
            
            daily_settings = copy.deepcopy(settings)
            daily_run_horizon = {
                'run_horizon': {
                    'horizon_start_time': minmax_times[0].strftime("%Y-%m-%dT%H:%M:%SZ"), 
                    'base_interval_duration': f'{interval_duration_secs}s', 
                    'number_of_intervals': math.floor((minmax_times[1]-minmax_times[0]).total_seconds()/interval_duration_secs)
                }
            }

            daily_settings.update(daily_run_horizon)
            daily_problem = {
                'settings': daily_settings,
                'economics': MessageToDict(sce_gs2_tariff_convert.get_economics_proto_for_simulation_period(minmax_times[0], minmax_times[1])),
                'resources': resources_list,
                'collections': collections_list
            }
            daily_problems.append(daily_problem)

        secondary_problems[month] = {
            'monthly_problem': {
                'settings': monthly_settigs,
                'economics': MessageToDict(sce_gs2_tariff_convert.get_economics_proto_for_simulation_period(min(monthly_dates), max(monthly_dates))),
                'resources': resources_list,
                'collections': collections_list,
            },
            'daily_problems': daily_problems
        }

    return secondary_problems
