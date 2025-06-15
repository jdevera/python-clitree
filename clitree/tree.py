from typing import Any, Callable, Iterable, TypeVar

Node = Any
T = TypeVar("T")
NodeValueGetter = Callable[[Node], T]


def _get_value(node: Node, key: str | NodeValueGetter[T]) -> T | None:
    """
    Get the value of a key or attribute from a node.

    Args:
        node: The node to get the value from
        key: The key or attribute to get the value from. Can be a string key or a callable

    Returns:
        The value of the key or attribute
    """
    if callable(key):
        return key(node)
    if hasattr(node, "get"):
        return node.get(key)
    return getattr(node, key, None)


def _get_name(node: Node, name: str | NodeValueGetter[str]) -> str:
    result = _get_value(node, name)
    if result is None:
        raise ValueError(f"Node name resolved to None: {node}")
    return str(result)


def _get_children(
    node: Node, children: str | NodeValueGetter[Iterable[Node] | None]
) -> Iterable[Node] | None:
    result = _get_value(node, children)
    if result is None:
        return None
    return result


def _build_tree(
    node: Node,
    name: str | NodeValueGetter[str],
    children: str | NodeValueGetter[Iterable[Node] | None],
    prefix: str = "",
) -> str:
    node_name = _get_name(node, name)
    node_children = _get_children(node, children) or []
    children_list = list(node_children)

    result = [node_name]

    for i, child in enumerate(children_list):
        is_last_child = i == len(children_list) - 1
        connector = "└── " if is_last_child else "├── "
        child_prefix = prefix + ("    " if is_last_child else "│   ")
        result.append(
            prefix + connector + _build_tree(child, name, children, child_prefix)
        )

    return "\n".join(result)


def tree(
    data: Node,
    name: str | NodeValueGetter[str] = "name",
    children: str | NodeValueGetter[Iterable[Node] | None] = "children",
) -> str:
    """
    Generate a tree-like string representation of a hierarchical data structure.

    Args:
        data: The root node of the tree structure
        name: How to extract the name of a node. Can be a string key or a callable
        children: How to extract children of a node. Can be a string key or a callable

    Returns:
        A string representation of the tree structure

    Raises:
        ValueError: If the name resolves to None
        TypeError: If children are not iterable
    """
    return _build_tree(data, name, children)
