# Name: Dominic Fantauzzo
# OSU Email: fantauzd@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap Implementation
# Due Date: March 14, 2024,
# Description: Implementation of a hash map using chaining to resolve collisions.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        not in the hash map, a new key/value pair is added. Runs in amortized O(1) as the number of elements
        in each bucket is limited to a constant and resizing doubles capacity.
        """

        # If load is too high then resize to double current capacity
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # find the bucket that the key is hashed to
        hash_bucket = self._buckets.get_at_index(self._hash_function(key) % self._capacity)

        # Search each node in the bucket
        for node in hash_bucket:
            # If the key is found, update the value
            if node.key == key:
                node.value = value
                return

        # If the key is not found, add it
        hash_bucket.insert(key, value)
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. All existing key/value pairs must
        be put into the new table, meaning the hash table links must be rehashed. Occurs in O(n)
        where n is the number of elements in the original hash table.
        """

        # Ensure that the new capacity is a prime number greater than or equal to 1
        if new_capacity < 1:
            return

        # Create a new hash table, this handles ensuring capacity is prime
        new_map = HashMap(new_capacity, self._hash_function)

        # Correct the bug in the _next_prime method for 2 that we are not allowed to change
        if new_capacity == 2:
            new_map._capacity = 2
            new_map._buckets.pop()

        # Copy each element from the old hash table to the new hash table
        list_pointer = 0
        # Copy all elements from each bucket until the new hash table is the same size as the old hash table
        while new_map._size < self._size:
            for node in self._buckets.get_at_index(list_pointer):
                new_map.put(node.key, node.value)
            list_pointer += 1

        # Update buckets and capacity
        self._buckets = new_map._buckets
        self._capacity = new_map._capacity

    def harder_resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. All existing key/value pairs must
        be put into the new table, meaning the hash table links must be rehashed. Occurs in O(n)
        where n is the number of elements in the original hash table.
        """

        # Ensure that the new capacity is a prime number greater than or equal to 1
        if new_capacity < 1:
            return
        if new_capacity != 2:
            new_capacity = self._next_prime(new_capacity)
        # Initialize new buckets
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())
        # Copy each element from the old hash table to the new hash table
        list_pointer = 0
        counter = 0
        # Copy all elements from each bucket until the new hash table is the same size as the old hash table
        while counter < self._size:
            for node in self._buckets.get_at_index(list_pointer):
                # find the bucket that the key is hashed to with the new capacity and insert it
                hash_bucket = new_buckets.get_at_index(self._hash_function(node.key) % new_capacity)
                hash_bucket.insert(node.key, node.value)
                counter += 1
            list_pointer += 1
        # Update buckets and capacity
        self._buckets = new_buckets
        self._capacity = new_capacity

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table. Occurs in O(n) where n
        is the capacity (number of buckets).
        """

        empty_buckets = 0
        # Checks the length of each bucket and iterates the counter when a bucket is empty
        for i in range(self._buckets.length()):
            if self._buckets.get_at_index(i).length() == 0:
                empty_buckets += 1

        return empty_buckets

    def get(self, key: str):
        """
        Returns the value associated with the given key. If the key is not in the hash
        map, the method returns None. Runs in O(1) as the number of elements
        in each bucket is limited to a constant.
        """

        # Find the bucket that the key is hashed to
        hash_bucket = self._buckets.get_at_index(self._hash_function(key) % self._capacity)

        # Iterate through bucket to find key
        for node in hash_bucket:
            if node.key == key:
                return node.value

        # Return None if not found
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys. Runs in O(1) as the number of elements
        in each bucket is limited to a constant.
        """

        # Find the bucket that the key is hashed to
        hash_bucket = self._buckets.get_at_index(self._hash_function(key) % self._capacity)

        # Iterate through bucket to find key
        for node in hash_bucket:
            if node.key == key:
                return True

        # Return False if not found
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing (no exception needs to be raised).
        Runs in O(1) as the number of elements in each bucket is limited to a constant.
        """

        # Find the bucket that the key is hashed to
        hash_bucket = self._buckets.get_at_index(self._hash_function(key) % self._capacity)

        # Remove node if it is in the bucket
        remove = hash_bucket.remove(key)

        # If the removal was successful, decrement size
        if remove is True:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map. Runs in O(n) where n is the number of elements in the hash table.
        """

        tuple_arr = DynamicArray()
        list_pointer = 0

        # Copy all elements from each bucket as tuples until the tuple array is the same size as the old hash table
        while tuple_arr.length() < self._size:
            for node in self._buckets.get_at_index(list_pointer):
                tuple_arr.append((node.key, node.value))
            list_pointer += 1

        return tuple_arr

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash
        table capacity. Runs in O(1).
        """

        # set each bucket to an empty linked list
        for i in range(self._capacity):
            self._buckets.set_at_index(i, LinkedList())

        # set the size to 0
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    This function will return a tuple containing, in this order, a dynamic array
    comprising the mode (most occurring) value(s) of the given array, and an
    integer representing the highest frequency of occurrence for the mode value(s).
    Runs in O(N) as the hash table methods run in constant time.
    O(N) occurs when we build and search through the hash table for the greatest frequency.

    :param da: A dynamic array of strings
    :return: A tuple with a dynamic array containing the mode(s) and the mode(s)'s frequency.
    """

    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    # Add each string from the dynamic array to a hash map, with its frequency.
    # If the string is already there, increment its frequency
    for i in range(da.length()):
        val = da.get_at_index(i)
        cur = map.get(val) if map.get(val) else 0
        map.put(val, 1 + cur)

    # Create variables to hold the mode(s) and frequency
    mode = DynamicArray()
    freq = 0

    # Return all the unique keys in an array of tuples like (key, frequency)
    keys_array = map.get_keys_and_values()

    # Iterate through the array of tuples and store the mode(s) and frequency
    for i in range(map.get_size()):
        pair = keys_array.get_at_index(i)
        key, key_freq = pair[0], pair[1]
        # If we find a key with higher frequency, replace the mode
        if key_freq > freq:
            mode = DynamicArray()
            mode.append(key)
            freq = key_freq
        # If we find a key with the same frequency, add it to modes
        elif key_freq == freq:
            mode.append(key)

    # Return the mode(s) and frequency as a tuple
    return (mode, freq)


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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")


    print("lets debug resize(2) ..... again")
    print("--------------------------------")
    p = HashMap(11, hash_function_1)
    p.put('key822', 209)
    p.put('key935', 217)
    p.put('key721', 638)
    p.resize_table(2)