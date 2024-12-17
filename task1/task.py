import typing as tp
import json


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


def get_from_json(object_string: str) -> tp.Dict[str, tp.Any]:
    return json.loads(object_string)


def parse_graph(graph: tp.Dict[str, tp.Dict],  graph_repr: tp.Dict[str, tp.Dict],  parent: tp.Optional[str]=None ) -> None:
    for key, val in graph.items():
        children = []
        if isinstance(val, dict) and val != dict():
            parse_graph(val, graph_repr, key)
            children = list(val.keys())
        graph_repr[key] = [children, parent]


def main(input_string: str) -> None:
    source_graph = get_from_json(input_string)
    graph_repr ={}
    parse_graph(source_graph, graph_repr)
    sorted_repr = {key: val for key, val in sorted(graph_repr.items(), key=lambda x: x[0])}
    print(sorted_repr)


if __name__ == "__main__":
    main(JSON_TEST)