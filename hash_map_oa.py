# Name: Dominic Fantauzzo
# OSU Email: fantauzd@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap Implementation
# Due Date: March 14, 2024,
# Description: Implementation of a hash map using open addressing and quadratic probing to resolve collisions.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the given key already exists in
        the hash map, its associated value is replaced with the new value. If the given key is
        not in the hash map, a new key/value pair is added. This runs in amortized O(1) time as the number of buckets
        to search is limited to a constant and resize doubles capacity.
        """

        # If load is too high then resize to double current capacity
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # find the bucket that the key is first hashed to
        bucket_index = self._hash_function(key) % self._capacity

        # If the bucket is not empty, continue with quadratic probing until we find an empty bucket or the key.
        # We already probed the original bucket, so we start quadratic probing with a base of 1
        i = 1
        while self._buckets.get_at_index(bucket_index) is not None:

            # If the same key is found, then we update the value
            if self._buckets.get_at_index(bucket_index).key == key:
                self._buckets.get_at_index(bucket_index).value = value
                #If the key is in a tombstone, it is no longer a tombstone and size increases
                if self._buckets.get_at_index(bucket_index).is_tombstone:
                    self._buckets.get_at_index(bucket_index).is_tombstone = False
                    self._size += 1
                return

            # Use quadratic probing to find the next index
            bucket_index = (self._hash_function(key) + i ** 2) % self._capacity
            i += 1

        # Once we probe to an empty index, we insert the value
        self._buckets.set_at_index(bucket_index, HashEntry(key, value))
        self._size = self._size + 1


    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. All active key/value pairs must be
        put into the new table, meaning all non-tombstone hash table links must be rehashed.
        Occur in O(N) time where N is the number of elements as each element is copied over.
        """

        # Ensure that the new capacity is a prime number greater than or equal to the current number of elements
        if new_capacity < self._size:
            return

        # Create a new hash table, this handles ensuring capacity is prime
        new_map = HashMap(new_capacity, self._hash_function)

        # Correct the bug in the _next_prime method for 2 that we are not allowed to change
        if new_capacity == 2:
            new_map._capacity = 2
            new_map._buckets.pop()

        # Hash all the hash entries that are not tombstones into the new hash map
        for bucket in self:
            new_map.put(bucket.key, bucket.value)

        # Update buckets and capacity
        self._buckets = new_map._buckets
        self._capacity = new_map._capacity

    def table_load(self) -> float:
        """
        Returns the current hash table load factor. O(1)
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table. Occurs in O(N) where N
        is the number of elements (size).
        """

        # Iterate over each bucket and count buckets that are empty
        full_buckets = 0
        for bucket in self: # Only iterates over buckets that have values (not tombstones)
                full_buckets += 1

        return self._capacity - full_buckets

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the hash
        map, the method returns None. Occurs in O(1) time as number of buckets to search is limited to a constant
        because load factor is limited to 0.5.
        """

        # find the bucket that the key is first hashed to
        bucket_index = self._hash_function(key) % self._capacity

        # If the bucket is not empty, continue with quadratic probing until we find an empty bucket or the key.
        # We already probed the original bucket, so we start quadratic probing with a base of 1
        i = 1
        while self._buckets.get_at_index(bucket_index) is not None:

            # If the same key is found, then we return the value
            if self._buckets.get_at_index(bucket_index).key == key and \
            self._buckets.get_at_index(bucket_index).is_tombstone == False:     # Ignore tombstones
                return self._buckets.get_at_index(bucket_index).value

            # Use quadratic probing to find the next index
            bucket_index = (self._hash_function(key) + i ** 2) % self._capacity
            i += 1

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False.
        Occurs in O(1) time as number of buckets to search is limited to a constant
        because load factor is limited to 0.5.
        """

        # find the bucket that the key is first hashed to
        bucket_index = self._hash_function(key) % self._capacity

        # If the bucket is not empty, continue with quadratic probing until we find an empty bucket or the key.
        # We already probed the original bucket, so we start quadratic probing with a base of 1
        i = 1
        while self._buckets.get_at_index(bucket_index) is not None:

            # If the same key is found, then we return True
            if self._buckets.get_at_index(bucket_index).key == key and \
            self._buckets.get_at_index(bucket_index).is_tombstone == False:         # Ignore tombstones
                return True

            # Use quadratic probing to find the next index
            bucket_index = (self._hash_function(key) + i ** 2) % self._capacity
            i += 1

        # If we reached an empty bucket then the key is not in the hash table
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing (no exception raised).
        Occurs in O(1) time as number of buckets to search is limited to a constant
        because load factor is limited to 0.5.
        """

        # find the bucket that the key is first hashed to
        bucket_index = self._hash_function(key) % self._capacity

        # If the bucket is not empty, continue with quadratic probing until we find an empty bucket or the key.
        # We already probed the original bucket, so we start quadratic probing with a base of 1.
        i = 1
        while self._buckets.get_at_index(bucket_index) is not None:

            # If the same key is found, then make it a tombstone
            if self._buckets.get_at_index(bucket_index).key == key:
                if not self._buckets.get_at_index(bucket_index).is_tombstone: # If already tombstone, do nothing
                    self._buckets.get_at_index(bucket_index).is_tombstone = True
                    self._size -= 1
                return

            # Use quadratic probing to find the next index
            bucket_index = (self._hash_function(key) + i ** 2) % self._capacity
            i += 1


    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map. The order of the keys in the dynamic array does not matter.
        Runs in O(N) time where N is the number of elements (size).
        """

        tuple_arr = DynamicArray()

        # Iterate over each bucket and add any hash entries to the tuple array
        for bucket in self:
                tuple_arr.append((bucket.key, bucket.value))

        return tuple_arr


    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash table capacity.
        Runs in O(N) time where N is the number of elements (size).
        """

        # Iterate over each bucket and set it to None
        for i in range(self._capacity):
            self._buckets.set_at_index(i, None)

        self._size = 0

    def __iter__(self):
        """
        Enables the hash map to iterate across itself.
        """

        # Initialize a variable to track iterators' progress
        self._index = 0

        return self

    def __next__(self):
        """
        Returns the next item in the hash map, based on the current location of the iterator.
        """

        # Find the next item in the buckets dynamic array that is not None or a tombstone
        try:
            while self._buckets.get_at_index(self._index) is None or \
            self._buckets.get_at_index(self._index).is_tombstone == True:
                self._index = self._index + 1

            value = self._buckets.get_at_index(self._index)

        # If we pass the end of the array an exception is raised and we stop iteration
        except DynamicArrayException:
            raise StopIteration

        # Increment index and return value
        self._index = self._index + 1
        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
