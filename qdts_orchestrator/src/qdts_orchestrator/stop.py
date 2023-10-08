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
            "name": "Stopping python processes",
            "shell":"killall -s SIGKILL python",
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



def stop():
    if len(sys.argv) != 2:
        print("Please provide an inventory file as argument")
        exit()
    inventory_file_path = sys.argv[1]
    inv = None
    with open( inventory_file_path) as inv_file:
        inv = yaml.safe_load(inv_file)
    
    ansible_runner.run(playbook = stop_play, inventory=inv)
    

if __name__ == "__main__":
    stop()