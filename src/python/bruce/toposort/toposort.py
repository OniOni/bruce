import copy
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, overload

from ..task import BaseTask


@dataclass
class Node:
    task: BaseTask
    upstream: List["Node"] = field(default_factory=list)
    children: List["Node"] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Node<task: '{self.task.key}', upstream: {[n.task.key for n in self.upstream]}, children: {[n.task.key for n in self.children]}>"

    def all_downstream(self) -> List["Node"]:
        res: List["Node"] = []
        roots = copy.copy(self.children)

        while roots:
            n = roots.pop()

            if n not in res:
                res.append(n)
                roots += n.children

        return res

    def __hash__(self) -> int:
        return hash(repr(self))

    def all_upstream(self) -> List["Node"]:
        res: List["Node"] = []
        roots = copy.copy(self.upstream)

        while roots:
            n = roots.pop()

            if n not in res:
                res.append(n)
                roots += n.upstream

        return res


def to_nodes(tasks: List[BaseTask]) -> Dict[str, Node]:
    reverse: Dict[str, Node] = {}
    for task in tasks:
        if task.key not in reverse:
            reverse[task.key] = Node(task=task)

        for up in task.upstream:
            if up.key not in reverse:
                reverse[up.key] = Node(task=up)

            reverse[up.key].children.append(reverse[task.key])
            reverse[task.key].upstream.append(reverse[up.key])

    return reverse


def toposort(tasks: List[BaseTask], to_run: List[str]) -> List[Node]:
    node_mapping = to_nodes(tasks)

    input_nodes = [node_mapping[task] for task in to_run]

    nodes: Set[Node] = set()
    for node in input_nodes:
        nodes.update(node.all_upstream())
        nodes.add(node)

    for n in input_nodes:
        n.children = []

    return _toposort(input_nodes, list(nodes))


def _toposort(roots: List[Node], nodes: List[Node]) -> List[Node]:
    res = []
    while roots:
        root = roots.pop()
        res.append(root)

        for n in root.upstream:
            if n in nodes:
                n.children = [
                    d for d in n.children if d.task.key != root.task.key and d in nodes
                ]

                if not n.children:
                    roots.append(n)

    return list(reversed(res))
