"""
Utility functions.
"""
import logging
from typing import Any, List, Iterable, Iterator, TypeVar, Generic, Union, Optional
from collections import OrderedDict
from collections.abc import MutableMapping, Set


from .device_type.base import (
    GrowattDeviceRegisters,
    custom_function,
)

K = TypeVar('K')
V = TypeVar('V')
D = TypeVar('D')

__all__ = ('LRUCache', 'get_keys_from_register', 'get_all_keys_from_register', 'keys_sequences', 'split_sequence', 'process_registers')

_LOGGER = logging.getLogger(__name__)


def get_keys_from_register(register: dict[int, GrowattDeviceRegisters]) -> set[int]:
    results = set()
    for key, value in register.items():
        results.add(key)

        if value.length > 1:
            for i in range(value.length):
                results.add(key + i)

    return results


def get_all_keys_from_register(registers: dict[int, GrowattDeviceRegisters], keys: set[int]) -> set[int]:
    """
    Lookup all related keys from the given keys based on the register config.
    returns list a sorted list of all keys.
    """
    result = set()

    for key in keys:
        result.add(key)
        if (register := registers.get(key)) is None:
            continue

        if register.length > 1:
            for i in range(register.length):
                result.add(key + i)

    return result


def keys_sequences(keys: Iterable[int], maximum_length: int) -> Set[tuple[int, int]]:
    """
    Creates the set of sequences based on the given keys.
    returns set containing tuples with start_key and length.
    """
    sorted_keys = sorted(keys)
    indexes = split_sequence(sorted_keys, maximum_length)

    sequence = set()

    start = 0
    indexes.append(len(sorted_keys))
    for end in indexes:
        sequence.add((sorted_keys[start], max(sorted_keys[start:end]) - min(sorted_keys[start:end]) + 1))
        start = end

    _LOGGER.debug("determined key seqences %s", [f"start: {s[0]}, end: {s[0] + s[1]}" for s in sequence])
    return sequence


def split_sequence(keys: list[int], maximum_length: int) -> list[int]:
    """
    Based on the list of keys the seperation will be determined based on the seperation between values and the maximum length of keys.
    returns indexes where to split
    """
    _LOGGER.debug(f"split sequence keys: {keys}")

    # determining number of splits and it's related index values based on a seperation treshold

    diff_key_seperation_index = set()
    seperation_treshold = maximum_length / 4

    key_differences = [j - i for i, j in zip(keys[:-1], keys[1:])]
    sorted_key_differences = sorted(key_differences, reverse=True)

    for key_diff in sorted_key_differences:
        if key_diff < seperation_treshold:
            break
        diff_key_seperation_index.add(key_differences.index(key_diff) + 1)

    _LOGGER.debug(f"split sequence indexes based on key seperation: {diff_key_seperation_index}")

    # determining number of splits and it's related index values based on the maximum length

    cumulative_key_seperation_index = set()
    key_cumulative_diff = [key - keys[0] for key in keys]

    i = 0
    j = 0
    while i < len(key_cumulative_diff):
        if key_cumulative_diff[i] >= maximum_length:
            cumulative_key_seperation_index.add(i + j)
            key_cumulative_diff = [key - keys[i + j] for key in keys[i + j:]]
            j += i
            i = 0
        else:
            i += 1

    _LOGGER.debug(f"split sequence indexes based on maximum length: {cumulative_key_seperation_index}")

    # check if both methodes find equal index seperation values
    common_index = cumulative_key_seperation_index.intersection(diff_key_seperation_index)

    _LOGGER.debug(f"split sequence commom indexes: {common_index}")

    cumulative_key_seperation_index.difference_update(common_index)
    diff_key_seperation_index.difference_update(common_index)

    if len(cumulative_key_seperation_index) == 0 and len(diff_key_seperation_index) == 0:
        return sorted(common_index)

    if len(cumulative_key_seperation_index) > 0:
        # sorting the seperation index fixes the processing from small to higher
        for item in sorted(cumulative_key_seperation_index):
            if len(diff_key_seperation_index) == 0:
                common_index.add(item)
                cumulative_key_seperation_index.remove(item)
                continue

            # Trying to optimize the number split by checking if there is a larger seperation nearby
            closest_value = min(diff_key_seperation_index, key=lambda x: abs(x - item))

            if len(common_index) == 0:
                # checking if closest seperation is not violating the maximum length
                if keys[closest_value - 1] - keys[0] < maximum_length:
                    common_index.add(closest_value)
                    cumulative_key_seperation_index.remove(item)
                    diff_key_seperation_index.remove(closest_value)
                else:
                    common_index.add(item)
                    cumulative_key_seperation_index.remove(item)

            else:
                # As there is already a known seperation we should check if our item is not on the other side in comperision to the closest value
                smaller_common_value = min(list(filter(lambda x: x < item, common_index)), default=None)
                larger_common_value = min(list(filter(lambda x: x > item, common_index)), default=None)

                if (smaller_common_value is not None and closest_value < smaller_common_value) or (larger_common_value is not None and closest_value > larger_common_value):
                    common_index.add(item)
                    cumulative_key_seperation_index.remove(item)
                    continue

                # closest_value falls within the same known sepeation as item
                if smaller_common_value is None:
                    if keys[closest_value - 1] - keys[0] < maximum_length:
                        common_index.add(closest_value)
                        cumulative_key_seperation_index.remove(item)
                        diff_key_seperation_index.remove(closest_value)
                    else:
                        common_index.add(item)
                        cumulative_key_seperation_index.remove(item)
                else:
                    if keys[closest_value - 1] - keys[smaller_common_value]:
                        common_index.add(closest_value)
                        cumulative_key_seperation_index.remove(item)
                        diff_key_seperation_index.remove(closest_value)
                    else:
                        common_index.add(item)
                        cumulative_key_seperation_index.remove(item)

    if len(diff_key_seperation_index) > 0:
        common_index.update(diff_key_seperation_index)

    return sorted(common_index)


def process_registers(
        registers: dict[int, GrowattDeviceRegisters],
        register_values: dict[int, int]
) -> dict[str, Any]:
    """
    Processes the register value corisponding to the given register dict.
    returns a dict of name and value
    """
    result: dict[str, Any] = {}

    for key, value in register_values.items():

        if (register := registers.get(key)) is None:
            continue

        if register.value_type == int:
            result[register.name] = value

        elif register.value_type == float and register.length == 2:
            if (second_value := register_values.get(key + 1, None)) is None:
                continue

            result[register.name] = round(
                float((value << 16) + second_value) / register.scale, 3
            )

        elif register.value_type == float:
            result[register.name] = round(float(value) / register.scale, 3)

        elif register.value_type == str:
            string = ""
            for i in range(key, key + register.length):
                if (item := register_values.get(i)) is not None:
                    string += chr(item >> 8)
                    string += chr(item & 0x00FF)

            result[register.name] = string

        elif register.value_type == bool:
            result[register.name] = bool(value)

        elif register.value_type == custom_function:
            if register.function is None:
                continue

            if register.length == 1:
                result[register.name] = register.function(value)
            else:
                result[register.name] = register.function([
                    register_values.get(i) for i in range(key, key + register.length)
                ])

    return result


class LRUCache(MutableMapping, Generic[K, V]):
    """
    A least-recently used (LRU) cache with a fixed cache size.

    This class acts as a dictionary but has a limited size. If the number of
    entries in the cache exeeds the cache size, the leat-recently accessed
    entry will be discareded.

    This is implemented using an ``OrderedDict``. On every access the accessed
    entry is moved to the front by re-inserting it into the ``OrderedDict``.
    When adding an entry and the cache size is exceeded, the last entry will
    be discareded.
    """

    def __init__(self, capacity=None):
        self.capacity = capacity
        self.cache = OrderedDict()  # type: OrderedDict[K, V]

    @property
    def lru(self) -> List[K]:
        return list(self.cache.keys())

    @property
    def length(self) -> int:
        return len(self.cache)

    def clear(self) -> None:
        self.cache.clear()

    def __len__(self) -> int:
        return self.length

    def __contains__(self, key: object) -> bool:
        return key in self.cache

    def __setitem__(self, key: K, value: V) -> None:
        self.set(key, value)

    def __delitem__(self, key: K) -> None:
        del self.cache[key]

    def __getitem__(self, key) -> V:
        value = self.get(key)
        if value is None:
            raise KeyError(key)

        return value

    def __iter__(self) -> Iterator[K]:
        return iter(self.cache)

    def get(self, key: K, default: D = None) -> Optional[Union[V, D]]:
        value = self.cache.get(key)

        if value is not None:
            # Move the entry to the front by re-inserting it
            del self.cache[key]
            self.cache[key] = value

            return value

        return default

    def set(self, key: K, value: V):
        if self.cache.get(key):
            # Move the entry to the front by re-inserting it
            del self.cache[key]
            self.cache[key] = value
        else:
            self.cache[key] = value

            # Check, if the cache is full and we have to remove old items
            # If the queue is of unlimited size, self.capacity is NaN and
            # x > NaN is always False in Python and the cache won't be cleared.
            if self.capacity is not None and self.length > self.capacity:
                self.cache.popitem(last=False)
