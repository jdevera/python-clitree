import os
import subprocess
from pathlib import Path

import pytest


def get_example_files():
    project_root = Path(__file__).parent.parent
    examples_dir = project_root / "examples"
    for py_file in examples_dir.glob("*.py"):
        expected_file = py_file.with_suffix(".expected.txt")
        if expected_file.exists():
            yield pytest.param(py_file, expected_file, id=py_file.stem)


@pytest.mark.parametrize("example_path, expected_output_path", get_example_files())
def test_example_output(example_path, expected_output_path):
    # Run the example script and capture its output
    result = subprocess.run(
        ["python", str(example_path)], capture_output=True, text=True, check=True
    )
    actual_output = result.stdout

    # Read the expected output
    with open(expected_output_path, "r") as f:
        expected_output = f.read()

    # Compare the outputs
    assert actual_output == expected_output, (
        f"Output of {example_path.name} does not match expected output."
    )
