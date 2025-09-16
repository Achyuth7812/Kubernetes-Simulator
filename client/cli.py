import requests
import subprocess
import sys
import time
import uuid

def add_node(api_url, cpu_cores):
    try:
        node_id = str(uuid.uuid4())
        response = requests.post(
            f"{api_url}/nodes",
            json={'cpu_cores': cpu_cores}
        )
        if response.status_code != 201:
            raise Exception(f"Failed to register node: {response.text}")
        api_node_id = response.json()['node_id']
        container_name = f"node-{cpu_cores}-{int(time.time())}"
        subprocess.run([
            "docker", "run", "-d", "--network=host",
            "--name", container_name,
            "-e", f"NODE_ID={api_node_id}",
            "-e", f"CPU_CORES={cpu_cores}",
            "node-image"
        ], check=True)
        print(f"Node {api_node_id} with {4} CPU cores added (container: {container_name})")
    except (subprocess.CalledProcessError, requests.RequestException) as e:
        print(f"Failed to launch node: {e}")

def launch_pod(api_url, cpu_cores):
    try:
        response = requests.post(f"{api_url}/pods", json={'cpu_cores': cpu_cores})
        if response.status_code == 201:
            data = response.json()
            print(f"Pod {data['pod_id']} scheduled on node {data['node_id']}")
        else:
            print(f"Failed to launch pod: {response.json()['error']}")
    except requests.RequestException as e:
        print(f"Error communicating with API server: {e}")

def set_algorithm(api_url, algorithm):
    try:
        response = requests.post(f"{api_url}/algorithm", json={'algorithm': algorithm})
        if response.status_code == 200:
            data = response.json()
            print(f"Scheduling algorithm set to: {data['algorithm']}")
        else:
            print(f"Failed to set algorithm: {response.json()['error']}")
    except requests.RequestException as e:
        print(f"Error communicating with API server: {e}")

def get_algorithm(api_url):
    try:
        response = requests.get(f"{api_url}/algorithm")
        if response.status_code == 200:
            data = response.json()
            print(f"Current algorithm: {data['algorithm']}")
            print(f"Available algorithms: {', '.join(data['available_algorithms'])}")
        else:
            print(f"Failed to get algorithm: {response.json()['error']}")
    except requests.RequestException as e:
        print(f"Error communicating with API server: {e}")

def main():
    api_url = "http://localhost:5000"
    if len(sys.argv) < 2:
        print("Usage: python cli.py <command> [args]")
        print("Commands:")
        print("  add-node <cpu_cores>           - Add a node with specified CPU cores")
        print("  launch-pod <cpu_cores>         - Launch a pod with specified CPU cores")
        print("  set-algorithm <algorithm>      - Set scheduling algorithm")
        print("  get-algorithm                  - Get current scheduling algorithm")
        print("  list-nodes                     - List all nodes")
        print("")
        print("Available algorithms: first-fit, best-fit, worst-fit, round-robin")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add-node" and len(sys.argv) == 3:
        cpu_cores = int(sys.argv[2])
        add_node(api_url, cpu_cores)
    elif command == "launch-pod" and len(sys.argv) == 3:
        cpu_cores = int(sys.argv[2])
        launch_pod(api_url, cpu_cores)
    elif command == "set-algorithm" and len(sys.argv) == 3:
        algorithm = sys.argv[2]
        set_algorithm(api_url, algorithm)
    elif command == "get-algorithm":
        get_algorithm(api_url)
    elif command == "list-nodes":
        try:
            response = requests.get(f"{api_url}/nodes")
            if response.status_code == 200:
                nodes = response.json()
                print("Current Nodes:")
                for node_id, node_data in nodes.items():
                    print(f"  Node {node_id}: {node_data['available_cores']}/{node_data['cpu_cores']} cores available, Status: {node_data['status']}")
            else:
                print(f"Failed to list nodes: {response.json()['error']}")
        except requests.RequestException as e:
            print(f"Error communicating with API server: {e}")
    else:
        print("Invalid command or arguments")
        print("Use 'python cli.py' without arguments to see usage")
        sys.exit(1)

if __name__ == '__main__':
    main()
