# CliTree

[![PyPI version](https://badge.fury.io/py/clitree.svg)](https://badge.fury.io/py/clitree)
[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/jdevera/python-clitree/actions/workflows/ci.yml/badge.svg)](https://github.com/jdevera/python-clitree/actions/workflows/ci.yml)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

`clitree` is a library to draw tree structures like the CLI utility `tree` does.

Install it with:

```bash
pip install clitree
```

Example usage:

```python
>>> from clitree import tree
>>> 
>>> data = {
...     "name": "root",
...     "children": [
...         {"name": "docs", "children": [
...             {"name": "api.md", "children": []},
...             {"name": "guide.md", "children": []}
...         ]},
...         {"name": "src", "children": [
...             {"name": "main.py", "children": []},
...             {"name": "utils", "children": [
...                 {"name": "helpers.py", "children": []},
...                 {"name": "config.py", "children": []}
...             ]}
...         ]},
...         {"name": "tests", "children": []}
...     ]
... }
>>> 
>>> print(tree(data))
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

```

### Parameters

- `name`: How to extract the name of a node. Can be:
  - A string key (uses `node.get(name)` or `getattr(node, name)`)
  - A callable that returns a string
- `children`: How to obtain the children of a node. Can be:
  - A string key (uses `node.get(children)` or `getattr(node, children)`)
  - A callable that returns an iterable of nodes (including generators)
  - Returns `None` or empty iterable for leaf nodes

### Node Structure

When using string keys for `name` and `children`, nodes are typically:
- Dictionaries with a `get` method, or
- Objects with attributes accessible via `getattr`

However, since `name` and `children` can be callables, nodes can be of any type, as the callables are responsible for extracting the required information.

Requirements:
- The name must resolve to a string value
- Children must be iterable or None

### Error Handling

- `ValueError`: Raised when a node's name resolves to None
- `TypeError`: Raised when children are not iterable