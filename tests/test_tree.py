import doctest
import textwrap
from pathlib import Path

import pytest

from clitree import tree


def tree_str(s: str) -> str:
    return textwrap.dedent(s).strip("\n")


def test_basic_tree():
    data = {
        "name": "root",
        "children": [
            {"name": "child 1", "children": []},
            {
                "name": "child 2",
                "children": [
                    {"name": "child 4", "children": []},
                    {"name": "child 5", "children": []},
                ],
            },
            {"name": "child 3", "children": []},
        ],
    }

    expected = tree_str("""
        root
        ├── child 1
        ├── child 2
        │   ├── child 4
        │   └── child 5
        └── child 3
    """)

    result = tree(data)
    assert result == expected


def test_custom_name_and_children():
    data = {
        "label": "root",
        "items": [
            {"label": "child 1", "items": []},
            {
                "label": "child 2",
                "items": [
                    {"label": "child 4", "items": []},
                    {"label": "child 5", "items": []},
                ],
            },
        ],
    }

    expected = tree_str("""
        root
        ├── child 1
        └── child 2
            ├── child 4
            └── child 5
    """)

    result = tree(data, name="label", children="items")
    assert result == expected


def test_callable_name_and_children():
    data = {
        "label": "root",
        "items": [
            {"label": "child 1", "items": []},
        ],
    }

    expected = tree_str("""
        ROOT
        └── CHILD 1
    """)

    result = tree(
        data,
        name=lambda node: node["label"].upper(),
        children=lambda node: node["items"],
    )
    assert result == expected


def test_generator_children():
    def child_gen(node):
        if node["name"] == "root":
            for i in range(5):
                yield {"name": f"child {i}", "children": []}
        else:
            return []

    data = {"name": "root", "children": []}

    expected = tree_str("""
        root
        ├── child 0
        ├── child 1
        ├── child 2
        ├── child 3
        └── child 4
    """)

    result = tree(data, children=child_gen)
    assert result == expected


def test_missing_name():
    data = {"children": []}

    with pytest.raises(ValueError, match="Node name resolved to None"):
        tree(data)


def test_none_children():
    data = {"name": "root", "children": None}

    expected = tree_str("""
        root
    """)

    result = tree(data, children=lambda _: None)
    assert result == expected


def test_non_iterable_children():
    data = {
        "name": "root",
        "children": 25,  # not iterable
    }

    with pytest.raises(TypeError) as excinfo:
        tree(data)
    assert "not iterable" in str(excinfo.value)


def test_readme_example():
    # Test the example in README.md
    readme_path = Path(__file__).parent.parent / "README.md"
    assert readme_path.exists(), "README.md not found"
    result = doctest.testfile(
        str(readme_path),
        module_relative=False,
        optionflags=doctest.NORMALIZE_WHITESPACE,
    )
    assert result.failed == 0, f"README example failed: {result}"


def test_object_with_attributes():
    class Node:
        def __init__(self, name, children=None):
            self.name = name
            self.children = children or []

    data = Node(
        "root",
        [
            Node("docs", [Node("api.md", []), Node("guide.md", [])]),
            Node(
                "src",
                [
                    Node("main.py", []),
                    Node("utils", [Node("helpers.py", []), Node("config.py", [])]),
                ],
            ),
            Node("tests", []),
        ],
    )

    expected = tree_str("""
        root
        ├── docs
        │   ├── api.md
        │   └── guide.md
        ├── src
        │   ├── main.py
        │   └── utils
        │       ├── helpers.py
        │       └── config.py
        └── tests
    """)

    result = tree(data)
    assert result == expected
