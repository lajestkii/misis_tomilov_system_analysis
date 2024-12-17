import json
import math
import typing as tp

JSON_TEST = """
    {
        "1": {
            "2": {
                "3": {
                    "5": {},
                    "6": {}
                },
                "4": {
                    "7": {},
                    "8": {}
                }
            }
        }
    }
"""


class GraphNode:
    def __str__(self) -> str:
        return str(f"{self.children}, {self.parent}, {self.relations}")

    def __init__(self, children: tp.List[int], parent: tp.Optional[str]) -> None:
        self.children: tp.List[int] = children
        self.parent: tp.Optional[str] = parent
        self.relations: tp.List[tp.Optional[int]] = [0] * 5


def calc_enthropy(matrix: tp.List[tp.List[int]]) -> float:
    if len(matrix) == 0:
        return 0.0
    hj = [0.0] * len(matrix[0])
    for row in matrix:
        for i, val in enumerate(row):
            if val == 0:
                continue
            p = val / (len(row) - 1)
            hj[i] -= (p * math.log2(p))
    return sum(hj)


def get_from_json(object_string: str) -> tp.Dict[str, tp.Any]:
    return json.loads(object_string)


def graph_parse(graph: tp.Dict[str, tp.Dict],  graph_repr: tp.Dict[str, GraphNode], parent: tp.Optional[str]=None) -> None:
    for key, val in graph.items():
        children = []
        if isinstance(val, dict) and val != dict():
            graph_parse(val, graph_repr, key)
            children = list(val.keys())
        graph_repr[key] = GraphNode(children, parent)
        graph_repr[key].relations[0] = len(children)
        graph_repr[key].relations[1] = 1 if graph_repr[key].parent is not None else 0


def rel_parse(graph_repr: tp.Dict[str, GraphNode]) -> None:
    for key, val in graph_repr.items():
        if graph_repr[key].parent is not None:
            parent = graph_repr[key].parent
            graph_repr[key].relations[4] += len(graph_repr[parent].children) - 1
            if graph_repr[parent].parent is not None:
                graph_repr[key].relations[3] += 1
        for child in val.children:
            graph_child = graph_repr[str(child)]
            graph_repr[key].relations[2] += graph_child.relations[2] + len(graph_child.children)
            graph_child.relations[3] += graph_repr[key].relations[3]


def main(input_string: str) -> None:
    source_graph = get_from_json(input_string)
    graph_repr ={}
    graph_parse(source_graph, graph_repr)
    rel_parse(graph_repr)
    sorted_repr = {key: val for key, val in sorted(graph_repr.items(), key=lambda x: x[0])}
    for key, value in sorted_repr.items():
        print(f"{key}: {value.relations}")
    print(calc_enthropy([val.relations for val in sorted_repr.values()]))


if __name__ == "__main__":
    main(JSON_TEST)