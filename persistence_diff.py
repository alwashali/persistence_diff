import json
import argparse
import logging
from deepdiff import DeepDiff, Delta

logging.basicConfig(level=logging.ERROR)

def read_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            content = content.replace("\\\"", "")
            content = content.replace("\\", "\\\\")
            return json.loads(content).get("autoruns")
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except IOError as e:
        logging.error(f"IOError occurred while reading {file_path}: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error in {file_path}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while reading {file_path}: {e}")
    return None

def diff_persistence(clean_system, infected_system):
    cp_json = read_json_file(clean_system)
    ip_json = read_json_file(infected_system)

    if cp_json is None or ip_json is None:
        logging.error("Failed to read JSON files. Exiting.")
        return None

    diff = Delta(DeepDiff(cp_json, ip_json, ignore_order=True, report_repetition=True))
    return diff.to_dict()

def print_diff(diff):
    if diff is not None:
        persistence_diff = diff.get("iterable_items_added_at_indexes")
        if persistence_diff is not None:
            tasks = persistence_diff.get("root['schedule_tasks']")
            startup = persistence_diff.get("root['startup_folders']")
            registry = persistence_diff.get("root['registry']")

            if tasks:
                print("\nScheduled Tasks")
                for key, obj in tasks.items():
                    print(obj)

            if startup:
                print("\nStartup Locations")
                for key, obj in startup.items():
                    print(obj)

            if registry:
                print("\nRegistry Locations")
                for key, obj in registry.items():
                    print(obj)

def main():
    parser = argparse.ArgumentParser(
        description='Compare infected and clean files.',
        usage='%(prog)s --infected infected.json --clean clean.json'
    )

    parser.add_argument('--infected', required=True, help='Path to infected system file')
    parser.add_argument('--clean', required=True, help='Path to clean system file')
    args = parser.parse_args()

    infected_system = args.infected
    clean_system = args.clean

    diff = diff_persistence(clean_system, infected_system)
    print_diff(diff)

if __name__ == "__main__":
    main()
