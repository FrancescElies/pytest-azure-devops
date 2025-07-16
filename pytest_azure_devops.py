# -*- coding: utf-8 -*-

import os
import pytest
from itertools import zip_longest
from math import ceil


def grouper(items, total_groups: int):
    """
    >>> grouper([1,2,3,4,5,6,7,8], 1)
    [[1, 2, 3, 4, 5, 6, 7, 8]]

    >>> grouper( [1,2,3,4,5,6,7,8], 2 )
    [[1, 2, 3, 4], [5, 6, 7, 8]]

    >>> grouper([1,2,3,4,5,6,7,8], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8]]

    >>> grouper([1,2,3,4,5,6,7,8], 4)
    [[1, 2], [3, 4], [5, 6], [7, 8]]

    >>> grouper([1,2,3,4,5,6,7,8], 5)
    [[1, 2], [3, 4], [5, 6], [7], [8]]

    >>> grouper([1,2,3,4,5,6,7,8], 6)
    [[1, 2], [3, 4], [5], [6], [7], [8]]

    >>> grouper([1,2,3,4,5,6,7,8], 7)
    [[1, 2], [3], [4], [5], [6], [7], [8]]

    >>> grouper([1,2,3,4,5,6,7,8], 8)
    [[1], [2], [3], [4], [5], [6], [7], [8]]
    """
    if total_groups <= 0:
        raise ValueError(f"total_groups should be bigger than zero but got {total_groups}")

    # Calculate the size of each group
    group_size = len(lst) // n + (len(lst) % n != 0)

    # Create the groups
    groups = [lst[i:i + group_size] for i in range(0, len(lst), group_size)]

    return groups
	

@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    if not os.environ.get("TF_BUILD"):
        print(
            "pytest-azure-devops installed but not in azure devops (plugin disabled). "
            "To run plugin either run in tests in CI azure devops "
            "or set environment variables "
            "TF_BUILD, SYSTEM_TOTALJOBSINPHASE and "
            "SYSTEM_JOBPOSITIONINPHASE."
        )
        return

    total_agents = int(os.environ.get("SYSTEM_TOTALJOBSINPHASE", 1))
    agent_index = int(os.environ.get("SYSTEM_JOBPOSITIONINPHASE", 1)) - 1

    agent_tests = grouper(items, total_agents)[agent_index]

    print(
        f"Agent nr. {agent_index + 1} of {total_agents} "
        f"selected {len(agent_tests)} of {len(items)} tests "
        "(other filters might apply afterwards, e.g. pytest marks)"
    )

    items[:] = agent_tests


if __name__ == "__main__":
    import doctest

    print(doctest.testmod(raise_on_error=True))
