import simu
from math import *

global CACHE_MISS
CACHE_MISS = 0

cache1_size = 8
cache2_size = 16
block1_size = 4
block2_size = 4
# latency1 = 10
# latency2 = 20

assoc1 = 1
assoc2 = 2

# to be changed later...
stalls1 = 2
stalls2 = 4
stalls3 = 10  # for memory penalty

set1 = int(cache1_size / (block1_size * assoc1))
set2 = int(cache2_size / (block2_size * assoc2))

block1 = int(block1_size / 4)
block2 = int(block2_size / 4)


# no_of_blocks_in_cache1 = cache1_size/block1_size
# no_of_sets = no_of_blocks_in_cache1/assoc1


def update_settings(cache1, cache2, block1, block2, assco1, assco2, stall1, stall2, stall3):
    global cache1_size, cache2_size, block1_size, block2_size, assoc1, assoc2, stalls1, stalls2, stalls3

    cache1_size = int(cache1 or cache1_size)
    cache2_size = int(cache2 or cache2_size)
    block1_size = int(block1 or block1_size)
    block2_size = int(block2 or block2_size)
    assoc1 = int(assco1 or assoc1)
    assoc2 = int(assco2 or assoc2)
    stalls1 = int(stall1 or stalls1)
    stalls2 = int(stall2 or stalls2)
    stalls3 = int(stall3 or stalls3)

    print("Updated", cache1_size, cache2_size, block1_size, block2_size, assoc1, assoc2, stalls1, stalls2, stalls3)
    CacheHit.change_caches()


class CacheHit:
    global cache1, cache2, counter1, counter2

    cache1 = []
    cache2 = []
    counter1 = 0
    counter2 = 0

    for _ in range(set1):
        cachetemp1 = []
        for _ in range(assoc1):
            cachet1 = []
            for _ in range(block1):
                cachet1.append([-1, -1, counter1])
            cachetemp1.append(cachet1)
        cache1.append(cachetemp1)
        # indices -> tag, data, counter(for LRU)

    for _ in range(set2):
        cachetemp2 = []
        for _ in range(assoc2):
            cachet2 = []
            for _ in range(block2):
                cachet2.append([-1, -1, counter2])
            cachetemp2.append(cachet2)
        cache2.append(cachetemp2)
        # indices -> tag, data, counter(for LRU)
    print("=" * 100)
    print(cache1)
    print(cache2)
    print("=" * 100)

    def change_caches():
        global cache1, cache2, set1, set2, block1, block2

        set1 = int(cache1_size / (block1_size * assoc1))
        set2 = int(cache2_size / (block2_size * assoc2))

        block1 = int(block1_size / 4)
        block2 = int(block2_size / 4)

        cache1 = []
        cache2 = []

        for _ in range(set1):
            cache1.append([[[-1, -1, counter1]] * block1] * assoc1)
            # indices -> tag, data, counter(for LRU)

        for _ in range(set2):
            cache2.append([[[-1, -1, counter2]] * block2] * assoc2)
            # indices -> tag, data, counter(for LRU)
        print("=" * 100)
        print(cache1)
        print(cache2)
        print("=" * 100)

    # Cache 1. Checking if the data is present or not
    def cache_hit_1(self, adrs):
        global cachehit1
        cachehit1 = False

        adr = bin(adrs)
        l = len(adr)
        adr = adr[0:2] + '0' * (10 - l) + adr[2:]

        # set_id = adrs % set1
        block_bit = int(log(block1, 2))
        set_bit = int(log(set1, 2))

        if block_bit == 0 and set_bit == 0:
            block_id = 0
            set_id = 0
        elif block_bit == 0:
            block_id = 0
            set_id = int(adr[-set_bit:])
        elif set_bit == 0:
            block_id = int(adr[-block_bit:])
            set_id = 0
        else:
            block_id = int(adr[-block_bit:])
            set_id = int(adr[-set_bit-block_bit:-block_bit])

        for j in range(assoc1):
            if adr[2:] == cache1[set_id][j][block_id][0]:
                cachehit1 = True
                global counter1
                cache1[set_id][j][block_id] = [adr[2:], simu.RAM[adrs], counter1]
                counter1 += 1
                return cache1[set_id][j][block_id][1], stalls1

        if not cachehit1:
            temp1 = self.cache_hit_2(adrs)
            self.insert_cache1(adrs)
            return temp1

    # Cache 2. Checking if the data is present or not if it is not present in Cache 1
    def cache_hit_2(self, adrs):
        global cachehit2
        cachehit2 = False

        adr = bin(adrs)
        l = len(adr)
        adr = adr[0:2] + '0' * (10 - l) + adr[2:]

        # set_id = adrs % set1
        block_bit = int(log(block1, 2))
        set_bit = int(log(set1, 2))

        if block_bit == 0 and set_bit == 0:
            block_id = 0
            set_id = 0
        elif block_bit == 0:
            block_id = 0
            set_id = int(adr[-set_bit:])
        elif set_bit == 0:
            block_id = int(adr[-block_bit:])
            set_id = 0
        else:
            block_id = int(adr[-block_bit:])
            set_id = int(adr[-set_bit - block_bit:-block_bit])

        for j in range(assoc2):
            if adr == cache2[set_id][j][block_id][0]:
                cachehit2 = True
                global counter2
                cache2[set_id][j][block_id] = [adr, simu.RAM[adrs], counter2]
                counter2 += 1
                return cache2[set_id][j][block_id][1], stalls1 + stalls2

        if not cachehit2:
            temp2 = self.memory_operation(adrs)
            self.insert_cache2(adrs)
            return temp2

    # Checking in memory if the data is not present in both the Caches
    def memory_operation(self, adrs):
        print("Cache Miss!")
        global CACHE_MISS
        CACHE_MISS += 1
        return simu.RAM[adrs], stalls1 + stalls2 + stalls3

    # Inserting Data in Cache1 if not present
    def insert_cache1(self, adrs):
        cache1inserted = False

        adr = bin(adrs)
        l = len(adr)
        adr = adr[0:2] + '0' * (10 - l) + adr[2:]
        print(adr)

        # set_id = adrs % set1
        block_bit = int(log(block1, 2))
        set_bit = int(log(set1, 2))

        if block_bit == 0 and set_bit == 0:
            block_id = 0
            set_id = 0
        elif block_bit == 0:
            block_id = 0
            set_id = int(adr[-set_bit:])
        elif set_bit == 0:
            block_id = int(adr[-block_bit:])
            set_id = 0
        else:
            block_id = int(adr[-block_bit:])
            set_id = int(adr[-set_bit - block_bit:-block_bit])

        for j in range(assoc1):
            if cache1[set_id][j][block_id][0] == -1:
                global counter1
                for k in range(block1):
                    cache1[set_id][j][k] = [adr, simu.RAM[adrs+k], counter1]
                    print(cache1)
                # cache1[set_id][j][block_id] = [adr, simu.RAM[adrs], counter1]
                counter1 += 1
                cache1inserted = True
                break

        if not cache1inserted:
            self.replace_in_cache1(adrs)

    # Inserting Data in Cache2 if not present
    def insert_cache2(self, adrs):
        cache2inserted = False

        adr = bin(adrs)
        l = len(adr)
        adr = adr[0:2] + '0' * (10 - l) + adr[2:]
        print(adr)

        # set_id = adrs % set1
        block_bit = int(log(block1, 2))
        set_bit = int(log(set1, 2))

        if block_bit == 0 and set_bit == 0:
            block_id = 0
            set_id = 0
        elif block_bit == 0:
            block_id = 0
            set_id = int(adr[-set_bit:])
        elif set_bit == 0:
            block_id = int(adr[-block_bit:])
            set_id = 0
        else:
            block_id = int(adr[-block_bit:])
            set_id = int(adr[-set_bit - block_bit:-block_bit])

        for j in range(assoc2):
            if cache2[set_id][j][block_id][0] == -1:
                global counter2
                for k in range(block2):
                    cache2[set_id][j][k] = [adr, simu.RAM[adrs+k], counter2]
                    print(cache2)
                # cache2[set_id][j][block_id] = [adr, simu.RAM[adrs], counter2]
                counter2 += 1
                cache2inserted = True
                break
        if not cache2inserted:
            self.replace_in_cache2(adrs)

    # If Cache1 is full, then replacing the existing data with new one acc to LRU policy
    def replace_in_cache1(self, adrs):
        ilru = 0
        jlru = 0

        adr = bin(adrs)
        l = len(adr)
        adr = adr[0:2] + '0' * (10 - l) + adr[2:]
        print(adr)

        # set_id = adrs % set1
        block_bit = int(log(block1, 2))
        set_bit = int(log(set1, 2))

        if block_bit == 0 and set_bit == 0:
            block_id = 0
            set_id = 0
        elif block_bit == 0:
            block_id = 0
            set_id = int(adr[-set_bit:])
        elif set_bit == 0:
            block_id = int(adr[-block_bit:])
            set_id = 0
        else:
            block_id = int(adr[-block_bit:])
            set_id = int(adr[-set_bit - block_bit:-block_bit])

        for j in range(assoc1):
            if cache1[set_id][j][block_id][2] < cache1[ilru][jlru][block_id][2]:
                ilru = set_id
                jlru = j
        global counter1
        for k in range(block1):
            cache1[ilru][jlru][k] = [adr, simu.RAM[adrs + k], counter1].copy()
            print(cache1)
        # cache1[ilru][jlru][block_id] = [adr, simu.RAM[adrs], counter1]
        counter1 += 1

    # If Cache2 is full, then replacing the existing data with new one acc to LRU policy
    def replace_in_cache2(self, adrs):
        ilru = 0
        jlru = 0

        adr = bin(adrs)
        l = len(adr)
        adr = adr[0:2] + '0' * (10 - l) + adr[2:]
        print(adr)

        # set_id = adrs % set1
        block_bit = int(log(block1, 2))
        set_bit = int(log(set1, 2))

        if block_bit == 0 and set_bit == 0:
            block_id = 0
            set_id = 0
        elif block_bit == 0:
            block_id = 0
            set_id = int(adr[-set_bit:])
        elif set_bit == 0:
            block_id = int(adr[-block_bit:])
            set_id = 0
        else:
            block_id = int(adr[-block_bit:])
            set_id = int(adr[-set_bit - block_bit:-block_bit])

        for j in range(assoc2):
            if cache2[set_id][j][block_id][2] < cache2[ilru][jlru][block_id][2]:
                ilru = set_id
                jlru = j
        global counter2
        for k in range(block2):
            cache2[ilru][jlru][k] = [adr, simu.RAM[adrs + k], counter2].copy()
            print(cache2)
        # cache2[ilru][jlru][block_id] = [adr, simu.RAM[adrs], counter2]
        counter2 += 1


CacheOP = CacheHit()
