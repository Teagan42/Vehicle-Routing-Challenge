from typing import Sequence, TypeVar, cast

TItem = TypeVar("TItem")


def flatten(nested_list: Sequence[TItem | Sequence[TItem]]) -> Sequence[TItem]:
    flattened: Sequence[TItem] = []
    for item in nested_list:
        if isinstance(item, list):
            flattened.extend(flatten(item))
        else:
            flattened.append(cast(TItem, item))
    return flattened
