import json
import argparse
from deepdiff import DeepDiff, Delta

def diff_persistence(clean_system:str ,infected_system:str ) -> dict:
    try:
        with open(clean_system, "r") as file:
            fc = file.read()
            fc = fc.replace("\\\"","")
            fc = fc.replace("\\","\\\\")
            cp_json = json.loads(fc).get("autoruns")
            # Process data
    except FileNotFoundError:
        print("File not found.")
    except IOError as e:
        print("IOError occurred:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)

    try:
        with open(infected_system, "r") as file:
            fc = file.read()
            fc = fc.replace("\\\"","")
            fc = fc.replace("\\","\\\\")
            ip_json = json.loads(fc).get("autoruns")
 
    except FileNotFoundError:
        print("File not found.")
    except IOError as e:
        print("IOError occurred:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)

    
    diff = Delta(DeepDiff(cp_json, ip_json, ignore_order=True, report_repetition=True))

    return diff.to_dict



parser = argparse.ArgumentParser(
        description='Compare infected and clean files.',
        usage='%(prog)s --infected infected.json --clean clean.json'
    )

parser.add_argument('--infected', required=True, help='Path to infected system file')
parser.add_argument('--clean', required=True, help='Path to clean system file')
args = parser.parse_args()

infected_system = args.infected
clean_system = args.clean

diff = diff_persistence(clean_system,infected_system)
if diff is not None:
    persistence_diff = diff.to_dict().get("iterable_items_added_at_indexes")
    if persistence_diff is not None:
        tasks = persistence_diff.get("root['schedule_tasks']")
        startup= persistence_diff.get("root['startup_folders']")
        registery = persistence_diff.get("root['registry']")

        if tasks is not None: 
            print("\nScheduled Tasks")
            for key, obj in tasks.items():     
                print(obj)

        if startup is not None: 
            print("\nStartup Locations")
            for key, obj in startup.items():     
                print(obj)

        if registery is not None: 
            print("\nRegistry Locations")
            for key, obj in registery.items():     
                print(obj)

