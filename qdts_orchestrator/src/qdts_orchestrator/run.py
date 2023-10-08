import yaml
import sys
import ansible_runner
import json


start_play = [
    {
    "name": "Execution",
    "hosts": "all",
    "tasks":[
        {
            "name": "Start",
            "shell":{
                "chdir": "~/qkd_workspace/",
                "cmd": "{{py_env}}/bin/python {{py_env}}/bin/qdts_node"
            },
        }
    ]

},    
]

def run():
    if len(sys.argv) != 2:
        print("Please an inventory file as argument")
        exit()
    inventory_file_path = sys.argv[1]
    inv = None

    with open( inventory_file_path) as inv_file:
        inv = yaml.safe_load(inv_file)
    
    ansible_runner.run(playbook = start_play, inventory=inv)
    


if __name__ == "__main__":
    run()