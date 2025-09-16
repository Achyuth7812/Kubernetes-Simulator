from models import Pod
import random

class PodScheduler:
    def __init__(self, node_manager):
        self.node_manager = node_manager
        self.algorithm = "first-fit"  # Default algorithm
        self.round_robin_index = 0  # For round-robin algorithm

    def set_algorithm(self, algorithm):
        """Set the scheduling algorithm"""
        valid_algorithms = ["first-fit", "best-fit", "worst-fit", "round-robin"]
        if algorithm.lower() in valid_algorithms:
            self.algorithm = algorithm.lower()
            return True
        return False

    def get_algorithm(self):
        """Get current scheduling algorithm"""
        return self.algorithm

    def schedule_pod(self, cpu_cores):
        """Schedule a pod using the selected algorithm"""
        pod = Pod(cpu_cores)
        nodes = self.node_manager.get_nodes()
        
        # Filter available nodes
        available_nodes = {
            node_id: node for node_id, node in nodes.items() 
            if node.status == "running" and node.available_cores >= cpu_cores
        }
        
        if not available_nodes:
            return None, None
        
        # Select node based on algorithm
        selected_node_id = self._select_node(available_nodes, cpu_cores)
        
        if selected_node_id:
            node = available_nodes[selected_node_id]
            node.available_cores -= cpu_cores
            node.pods.append(pod.id)
            return pod.id, selected_node_id
        
        return None, None

    def _select_node(self, available_nodes, cpu_cores):
        """Select node based on the current algorithm"""
        if self.algorithm == "first-fit":
            return self._first_fit(available_nodes, cpu_cores)
        elif self.algorithm == "best-fit":
            return self._best_fit(available_nodes, cpu_cores)
        elif self.algorithm == "worst-fit":
            return self._worst_fit(available_nodes, cpu_cores)
        elif self.algorithm == "round-robin":
            return self._round_robin(available_nodes, cpu_cores)
        else:
            return self._first_fit(available_nodes, cpu_cores)

    def _first_fit(self, available_nodes, cpu_cores):
        """First-Fit: Select the first node that can accommodate the pod"""
        for node_id in available_nodes:
            return node_id
        return None

    def _best_fit(self, available_nodes, cpu_cores):
        """Best-Fit: Select the node with the smallest available space that can fit the pod"""
        best_node_id = None
        min_waste = float('inf')
        
        for node_id, node in available_nodes.items():
            waste = node.available_cores - cpu_cores
            if waste < min_waste:
                min_waste = waste
                best_node_id = node_id
        
        return best_node_id

    def _worst_fit(self, available_nodes, cpu_cores):
        """Worst-Fit: Select the node with the largest available space"""
        worst_node_id = None
        max_available = -1
        
        for node_id, node in available_nodes.items():
            if node.available_cores > max_available:
                max_available = node.available_cores
                worst_node_id = node_id
        
        return worst_node_id

    def _round_robin(self, available_nodes, cpu_cores):
        """Round-Robin: Select nodes in a circular order"""
        node_ids = list(available_nodes.keys())
        if not node_ids:
            return None
        
        # Start from the last used index
        start_index = self.round_robin_index % len(node_ids)
        
        # Find next available node starting from the index
        for i in range(len(node_ids)):
            current_index = (start_index + i) % len(node_ids)
            node_id = node_ids[current_index]
            self.round_robin_index = (current_index + 1) % len(node_ids)
            return node_id
        
        return None
