import yaml
import sys
import ansible_runner
import json



stop_play = [
    {
    "name": "Stopping",
    "hosts": "all",
    "tasks":[
        {
            "name": "Stop",
            "shell":"killall qdts_node",
            "ignore_errors": True
        },
        {
            "name": "Stopping python processes",
            "shell":"killall python",
            "ignore_errors": True
        },
        {
            "name": "Stopping simulaqron",
            "shell":"{{py_env}}/bin/python {{py_env}}/bin/simulaqron stop",
            "ignore_errors": True
        },
    ]

},    
]



def run():
    if len(sys.argv) != 3:
        print("Please provide a config file and a provisioning file")
        exit()
    config_file_path = sys.argv[1]
    inventory_file_path = sys.argv[2]
    config = None
    inv = None
    with open(config_file_path) as config_file:
        config = yaml.safe_load(config_file)
    with open( inventory_file_path) as inv_file:
        inv = yaml.safe_load(inv_file)
    
    ansible_runner.run(playbook = stop_play, inventory=inv)
    

if __name__ == "__main__":
    run()