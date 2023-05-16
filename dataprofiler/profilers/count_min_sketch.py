#!/usr/bin/env python
"""Count-min Sketching implementation."""
import math
import random
from typing import Any

import mmh3
import numpy as np


class CMS:
    """A count-min sketch data structure."""

    def __init__(self, num_bins: int, num_hashes: int) -> None:
        """
        Create CMS.

        :param num_bins: number of bins per hash function
        :type num_bins: int
        :param num_hashes: number of hashes used in hash_table
        :type num_hashes: int
        """
        random.seed(42)
        self.num_bins = num_bins
        self.num_hashes = num_hashes
        self.hash_table = np.zeros((num_hashes, num_bins))
        self.rs = random.sample(range(1000), self.num_hashes)
        self.num_unique_bins = 0

    def add_cms(self, key: Any) -> None:
        """
        Added byte-object to hash_table.

        :param key: the key that is being hashed into the hash_table.
        :type key: Any
        """
        for t in range(self.num_hashes):
            sd = self.rs[t]
            hash_value = int(mmh3.hash(key, signed=False, seed=sd)) / (2.0**32 - 1)
            key_value = int(math.floor(hash_value * (self.num_bins - 1)))
            if self.hash_table[t, key_value] == 0:
                self.num_unique_bins += 1
            self.hash_table[t, key_value] += 1
            current_estimate = self.hash_table[t, key_value]
            if t == 0:
                best_estimate = current_estimate
            else:
                if current_estimate < best_estimate:
                    best_estimate = current_estimate

    def get_cms_count(self, key: Any) -> int:
        """
        Get the count of key in hash_table.

        :param key: the key that is being looked up
        :type key: Any
        :return: count associated with key
        :rtype: int
        """
        for t in range(self.num_hashes):
            sd = self.rs[t]
            hash_value = int(mmh3.hash(key, signed=False, seed=sd)) / (2.0**32 - 1)
            key_value = int(math.floor(hash_value * (self.num_bins - 1)))
            current_estimate = self.hash_table[t, key_value]
            if t == 0:
                best_estimate = current_estimate
            else:
                if current_estimate < best_estimate:
                    best_estimate = current_estimate
        return int(best_estimate)

    def merge_cms(self, other: Any) -> None:
        """
        Merge one cms hash_table into this.hash_table.

        :param other: the CMS that is being merged.
        :type other: CMS
        """
        self.hash_table = np.add(self.hash_table, other.hash_table)

    def get_top_values(self):
        """
        Return the top-k values in the heap.

        :return: the top-k values in the heap.
        :type: List[Any]
        """
        if self.top_k is not None:
            return self.top_k.top_values()
