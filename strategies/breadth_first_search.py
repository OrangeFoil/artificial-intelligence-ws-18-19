import time
from collections import namedtuple
from functools import partial
from queue import Queue

from problems.abstract_problem import AbstractProblem
from strategies.abstract_strategy import AbstractStrategy


class BreadthFirstSearch(AbstractStrategy):
    root = None
    goal_node = None

    def find_solution(self):
        self.start_time = time.monotonic()

        Node = namedtuple('Node', 'parent_node, state, action')
        self.root = Node(
            parent_node=None,
            state=self.problem.create_initial_state(),
            action=""
        )
        fifo_queue = Queue()
        fifo_queue.put(self.root)

        # build and traverse tree
        while True:
            # examine the next node
            this_node = fifo_queue.get()
            # is this node the goal?
            if self.problem.is_goal_state(this_node.state):
                self.goal_node = this_node
                break
            # add new state for each possible action
            for action in self.problem.get_actions():
                child_node = Node(
                    parent_node=this_node,
                    state=partial(action, this_node.state)(),
                    action=action,
                )
                fifo_queue.put(child_node)

        self.stop_time = time.monotonic()

    def print_solution(self):
        super().print_solution()
        path = []
        node = self.goal_node
        while node != self.root:
            path.append(node)
            node = node.parent_node
        path.reverse()

        for node in path:
            print("Action: {:50} State: {}".format(
                str(node.action), str(node.state)))

    def print_resource_usage_report(self):
        print("Time taken: {:.3f} seconds".format(
            self.stop_time - self.start_time))
