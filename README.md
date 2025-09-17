# Kubernetes Simulator 

A comprehensive mini-project simulating core Kubernetes features, including node management, pod scheduling, health monitoring, a command-line interface (CLI), and a web-based UI dashboard. Built with Python, Flask, Docker, and a custom API server, this project demonstrates a simplified Kubernetes-like cluster for educational purposes.



## 🎯 Project Overview
The Kubernetes Simulator replicates key Kubernetes functionalities in a lightweight, local environment:
- **Node Management**: Add and track nodes with CPU core allocations
- **Pod Scheduling**: Assign pods to nodes using multiple scheduling algorithms (First-Fit, Best-Fit, Worst-Fit, Round-Robin)
- **Algorithm Selection**: Choose and switch between different scheduling algorithms dynamically
- **Health Monitoring**: Detect node failures (no heartbeats for 30 seconds) and mark nodes as "failed"
- **CLI**: User-friendly commands (`add-node`, `launch-pod`, `set-algorithm`) to interact with the cluster
- **UI Dashboard**: A Flask-based web interface (`http://localhost:5000`) to visualize nodes, pods, algorithms, and their statuses in real-time
- **Docker Integration**: Nodes run as Docker containers for scalability and isolation

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI Client    │    │   API Server    │    │  Web Dashboard  │
│                 │    │                 │    │                 │
│ • add-node      │◄──►│ • Node Manager  │◄──►│ • Real-time UI  │
│ • launch-pod    │    │ • Pod Scheduler │    │ • Status View   │
│ • requests      │    │ • Health Monitor│    │ • Resource View │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│  Docker Nodes   │    │  Docker Compose │
│                 │    │                 │
│ • Container 1   │    │ • API Server    │
│ • Container 2   │    │ • Network Setup │
│ • Container N   │    │ • Port Mapping  │
└─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

### Required Software
- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Python 3.7+** with pip
- **Git** (optional, for cloning)

### System Requirements
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 2GB free space
- **OS**: Windows 10+, macOS 10.14+, or Linux

## 🚀 Quick Start Guide

### Step 1: Clone and Navigate
```bash
# If cloning from repository
git clone <repository-url>
cd 018_020_023_025_KubernetesSimulator-main

# Or if you have the files locally
cd "018_020_023_025_KubernetesSimulator-main"
```

### Step 2: Verify Docker Installation
```bash
docker --version
docker ps
```
**Expected Output**: Docker version information and empty container list

### Step 3: Build Node Docker Image
```bash
docker build -t node-image ./node
```
**What this does**: Creates a Docker image containing the node service
**Expected Output**: Success message with image ID

### Step 4: Start API Server
```bash
docker-compose up -d
```
**What this does**: Starts the API server in background mode
**Expected Output**: Container started successfully

### Step 5: Install CLI Dependencies
```bash
pip install requests
```
**What this does**: Installs required Python library for CLI communication

### Step 6: Test the Simulator
```bash
# Add a node with 4 CPU cores
python client/cli.py add-node 4

# Launch a pod requiring 2 CPU cores
python client/cli.py launch-pod 2
```

### Step 7: Access Web Dashboard
Open your browser and navigate to: `http://localhost:5000`

## 📖 Detailed Command Reference

### 🖥️ Node Management Commands

#### Add a Node
```bash
python client/cli.py add-node <cpu_cores>
```
**Parameters**:
- `<cpu_cores>`: Number of CPU cores (integer, 1-16 recommended)

**Examples**:
```bash
python client/cli.py add-node 4    # Creates node with 4 cores
python client/cli.py add-node 8    # Creates node with 8 cores
python client/cli.py add-node 2    # Creates node with 2 cores
```

**What happens**:
1. CLI sends POST request to `/nodes` API endpoint
2. API server generates unique node ID
3. Docker container starts with node service
4. Node begins sending heartbeats every 5 seconds
5. Node registers with API server

**Expected Output**:
```
Node <node-id> with 4 CPU cores added (container: node-4-<timestamp>)
```

### 🚀 Pod Management Commands

#### Launch a Pod
```bash
python client/cli.py launch-pod <cpu_cores>
```
**Parameters**:
- `<cpu_cores>`: CPU cores required by the pod (integer, 1-16)

**Examples**:
```bash
python client/cli.py launch-pod 2    # Pod needs 2 cores
python client/cli.py launch-pod 1    # Pod needs 1 core
python client/cli.py launch-pod 3    # Pod needs 3 cores
```

**What happens**:
1. CLI sends POST request to `/pods` API endpoint
2. Pod scheduler uses the currently selected algorithm
3. Finds suitable node based on algorithm logic
4. Assigns pod to selected node
5. Updates node's available CPU cores

**Expected Output**:
```
Pod <pod-id> scheduled on node <node-id>
```

**Error Output** (if no suitable node):
```
Failed to launch pod: No suitable node found
```

### 🧠 Algorithm Management Commands

#### Set Scheduling Algorithm
```bash
python client/cli.py set-algorithm <algorithm>
```
**Parameters**:
- `<algorithm>`: One of: `first-fit`, `best-fit`, `worst-fit`, `round-robin`

**Examples**:
Example for Best fit
Befor assigning 
<img width="1899" height="643" alt="Screenshot 2025-09-17 030033" src="https://github.com/user-attachments/assets/529f9b4d-7206-4d9e-b4af-65b4b988223f" />
After Assigning using Best fit
<img width="1904" height="665" alt="Screenshot 2025-09-17 030049" src="https://github.com/user-attachments/assets/1f3a3160-238e-4150-a004-08c7158ffdcd" />


```bash
python client/cli.py set-algorithm best-fit      # Use Best-Fit algorithm
python client/cli.py set-algorithm worst-fit     # Use Worst-Fit algorithm
python client/cli.py set-algorithm round-robin   # Use Round-Robin algorithm
python client/cli.py set-algorithm first-fit     # Use First-Fit algorithm (default)
```

**Expected Output**:
```
Scheduling algorithm set to: best-fit
```

#### Get Current Algorithm
```bash
python client/cli.py get-algorithm
```
**Expected Output**:
```
Current algorithm: best-fit
Available algorithms: first-fit, best-fit, worst-fit, round-robin
```

#### List All Nodes
```bash
python client/cli.py list-nodes
```
**Expected Output**:
```
Current Nodes:
  Node <node-id-1>: 2/4 cores available, Status: healthy
  Node <node-id-2>: 6/8 cores available, Status: healthy
```

### 🔍 Monitoring Commands

#### List All Nodes (API)
```bash
curl http://localhost:5000/nodes
```
**What it returns**: JSON with all node information
```json
{
  "node-id-1": {
    "cpu_cores": 4,
    "available_cores": 2,
    "status": "healthy",
    "pods": ["pod-id-1", "pod-id-2"]
  }
}
```

#### Check API Server Health
```bash
curl http://localhost:5000/
```
**Expected Output**: API server status

## 🌐 Web Dashboard

### Accessing the Dashboard
- **URL**: `http://localhost:5000`
- **Features**:
  - Real-time node status
  - Pod assignments
  - Resource utilization
  - Health monitoring

### Dashboard Sections
1. **Nodes Table**:
   - Node ID
   - Total CPU Cores
   - Available CPU Cores
   - Status (Healthy/Failed)
   - Running Pods

2. **Pods Table**:
   - Pod ID
   - Assigned Node
   - CPU Requirements
   - Status

## 🧠 How It Works

### Node Lifecycle
1. **Creation**: Docker container starts with node service
2. **Registration**: Node registers with API server via POST `/nodes`
3. **Heartbeat**: Sends health signals every 5 seconds to `/heartbeat`
4. **Resource Tracking**: Reports available CPU cores
5. **Failure Detection**: If no heartbeat for 30 seconds → marked as "failed"

### Pod Scheduling Algorithms

The simulator supports four different scheduling algorithms that you can choose from:

#### 1. **First-Fit Algorithm** (Default)
- **Strategy**: Selects the first node that can accommodate the pod
- **Process**:
  1. Iterate through nodes in order
  2. Find first node with `available_cores >= requested_cores`
  3. Assign pod to that node
- **Pros**: Simple, fast execution
- **Cons**: May lead to fragmentation over time
- **Use Case**: General purpose, balanced performance

#### 2. **Best-Fit Algorithm**
- **Strategy**: Selects the node with the smallest available space that can fit the pod
- **Process**:
  1. Find all nodes with `available_cores >= requested_cores`
  2. Select node with minimum `available_cores - requested_cores`
  3. Assign pod to that node
- **Pros**: Minimizes resource waste, better space utilization
- **Cons**: Slower execution, may create many small fragments
- **Use Case**: When you want to maximize resource efficiency

#### 3. **Worst-Fit Algorithm**
- **Strategy**: Selects the node with the largest available space
- **Process**:
  1. Find all nodes with `available_cores >= requested_cores`
  2. Select node with maximum `available_cores`
  3. Assign pod to that node
- **Pros**: Leaves large free spaces for future large pods
- **Cons**: May waste resources, slower execution
- **Use Case**: When you expect large pods and want to keep space available

#### 4. **Round-Robin Algorithm**
- **Strategy**: Distributes pods evenly across nodes in a circular fashion
- **Process**:
  1. Maintain a pointer to the last used node
  2. Find next available node starting from the pointer
  3. Assign pod to that node and update pointer
- **Pros**: Load balancing, prevents single node overload
- **Cons**: May not consider actual resource requirements
- **Use Case**: When you want even distribution of workload

### Algorithm Comparison Example

**Scenario**: 3 nodes with capacities [8, 4, 6] cores, launching pods requiring [2, 3, 1] cores

| Algorithm | Pod 1 (2 cores) | Pod 2 (3 cores) | Pod 3 (1 core) | Result |
|-----------|----------------|----------------|----------------|---------|
| **First-Fit** | Node 1 (8→6) | Node 1 (6→3) | Node 1 (3→2) | Node 1: 2 cores left |
| **Best-Fit** | Node 2 (4→2) | Node 3 (6→3) | Node 2 (2→1) | Balanced distribution |
| **Worst-Fit** | Node 1 (8→6) | Node 1 (6→3) | Node 1 (3→2) | Node 1: 2 cores left |
| **Round-Robin** | Node 1 (8→6) | Node 2 (4→1) | Node 3 (6→5) | Even distribution |

### Health Monitoring
- **Heartbeat Interval**: 5 seconds
- **Failure Threshold**: 30 seconds
- **Recovery**: Manual restart required

## 🔧 Advanced Usage

### Multiple Nodes and Pods
```bash
# Create a cluster with multiple nodes
python client/cli.py add-node 8    # High-capacity node
python client/cli.py add-node 4    # Medium-capacity node
python client/cli.py add-node 2    # Low-capacity node

# Launch various pods
python client/cli.py launch-pod 3  # Heavy workload
python client/cli.py launch-pod 1  # Light workload
python client/cli.py launch-pod 2  # Medium workload
```

### Algorithm Testing and Comparison
```bash
# Test different algorithms with the same workload
python client/cli.py set-algorithm first-fit
python client/cli.py launch-pod 2
python client/cli.py launch-pod 1
python client/cli.py launch-pod 3

# Switch to Best-Fit and test
python client/cli.py set-algorithm best-fit
python client/cli.py launch-pod 2
python client/cli.py launch-pod 1
python client/cli.py launch-pod 3

# Compare results
python client/cli.py list-nodes
curl http://localhost:5000/nodes
```

### Algorithm Performance Testing
```bash
# Create test environment
python client/cli.py add-node 10
python client/cli.py add-node 8
python client/cli.py add-node 6

# Test First-Fit
python client/cli.py set-algorithm first-fit
python client/cli.py launch-pod 3
python client/cli.py launch-pod 2
python client/cli.py launch-pod 4
python client/cli.py launch-pod 1

# Check distribution
python client/cli.py list-nodes

# Test Best-Fit (reset by stopping and restarting)
docker-compose down
docker-compose up -d
python client/cli.py add-node 10
python client/cli.py add-node 8
python client/cli.py add-node 6

python client/cli.py set-algorithm best-fit
python client/cli.py launch-pod 3
python client/cli.py launch-pod 2
python client/cli.py launch-pod 4
python client/cli.py launch-pod 1

# Compare results
python client/cli.py list-nodes
```

### Resource Management
```bash
# Check current cluster state
curl http://localhost:5000/nodes | python -m json.tool

# Monitor resource utilization
# Visit http://localhost:5000 for visual dashboard
```

### Testing Failure Scenarios
```bash
# Stop a node container to simulate failure
docker stop <container-name>

# Check how the system handles the failure
curl http://localhost:5000/nodes
```

## 🛠️ Troubleshooting

### Common Issues

#### Docker Not Running
**Error**: `error during connect: Head "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping"`
**Solution**:
1. Start Docker Desktop
2. Wait for it to fully load
3. Verify with `docker ps`

#### Port Already in Use
**Error**: `Port 5000 is already in use`
**Solution**:
```bash
# Stop existing containers
docker-compose down

# Or change port in docker-compose.yml
```

#### Node Creation Fails
**Error**: `Failed to launch node: <error>`
**Solution**:
1. Check Docker is running: `docker ps`
2. Verify image exists: `docker images | grep node-image`
3. Rebuild image: `docker build -t node-image ./node`

#### Pod Scheduling Fails
**Error**: `No suitable node found`
**Solution**:
1. Check available nodes: `curl http://localhost:5000/nodes`
2. Add more nodes: `python client/cli.py add-node <cores>`
3. Check node capacity vs pod requirements

### Debug Commands
```bash
# Check running containers
docker ps

# Check container logs
docker logs <container-name>

# Check API server logs
docker-compose logs api-server

# Verify network connectivity
curl -v http://localhost:5000/nodes
```

## 🧹 Cleanup Commands

### Stop the Simulator
```bash
# Stop API server
docker-compose down

# Stop all node containers
docker stop $(docker ps -q --filter ancestor=node-image)

# Remove all node containers
docker rm $(docker ps -aq --filter ancestor=node-image)
```

### Complete Cleanup
```bash
# Remove all containers and images
docker-compose down
docker system prune -a

# Remove specific image
docker rmi node-image
```

## 📊 Project Structure

```
018_020_023_025_KubernetesSimulator-main/
├── api_server/                 # API Server Components
│   ├── app.py                 # Main Flask application
│   ├── node_manager.py        # Node management logic
│   ├── pod_scheduler.py       # Pod scheduling algorithm
│   ├── health_monitor.py      # Health monitoring system
│   ├── models.py              # Data models
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # API server container
│   └── templates/
│       └── dashboard.html     # Web dashboard UI
├── node/                      # Node Service Components
│   ├── node_service.py        # Node service implementation
│   ├── requirements.txt       # Node dependencies
│   └── Dockerfile             # Node container
├── client/                    # CLI Client
│   ├── cli.py                 # Command-line interface
│   └── setup.sh               # Setup script
├── docker-compose.yml         # Docker Compose configuration
└── README.md                  # This file
```

## 🎓 Educational Value

### Kubernetes Concepts Demonstrated
1. **Control Plane**: API server managing cluster state
2. **Worker Nodes**: Containerized compute resources
3. **Pod Scheduling**: Multiple algorithms for resource-aware workload placement
4. **Algorithm Selection**: Dynamic switching between scheduling strategies
5. **Health Monitoring**: Node failure detection and handling
6. **Resource Management**: CPU allocation and tracking
7. **Web UI**: Cluster visualization and monitoring
8. **Load Balancing**: Different approaches to workload distribution

### Learning Outcomes
- Understanding of container orchestration
- Hands-on experience with microservices architecture
- API design and implementation
- Docker containerization
- Web application development
- System monitoring and health checks
- **Algorithm Design**: Understanding different scheduling strategies
- **Performance Analysis**: Comparing algorithm efficiency
- **Resource Optimization**: Learning trade-offs between algorithms
- **System Design**: Implementing configurable components

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Include error handling

## 📝 License

This project is created for educational purposes as part of the Cloud Computing course at PES University.

## 🙏 Acknowledgments

- **Kubernetes Community** for inspiration and concepts
- **Docker** for containerization platform
- **Flask** for web framework
- **PES University** for educational support

---

**Happy Learning! 🚀**

For questions or issues, please refer to the troubleshooting section or contact the development team.
