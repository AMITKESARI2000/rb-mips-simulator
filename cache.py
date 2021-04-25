cache1_size = 8
cache2_size = 16
block1_size = 4
block2_size = 4
# latency1 = 10
# latency2 = 20

stalls1 = 8
stalls2 = 16
stalls3 = 128  # for memory penalty

assoc1 = 1
assoc2 = 2

RAM = []

cache1 = int(cache1_size / (block1_size * assoc1))

# no_of_blocks_in_cache1 = cache1_size/block1_size
# no_of_sets = no_of_blocks_in_cache1/assoc1

cache2 = int(cache2_size / (block2_size * assoc2))

global counter
counter = 0


class CacheHit:
    global cache1
    global cache2

    cache1 = []
    cache2 = []

    for _ in range(cache1_size):
        cache1.append([[-1, -1, -1]] * assoc1)
        # indices -> tag, data, counter(for LRU)

    for _ in range(cache2_size):
        cache1.append([[-1, -1, -1]] * assoc2)
        # indices -> tag, data, counter(for LRU)

    # Cache 1. Checking if the data is present or not
    def cache_hit_1(self, adrs):
        global cachehit1
        cachehit1 = False
        for i in range(cache1):
            for j in range(assoc1):
                if adrs == cache1[i][j][0]:
                    cachehit1 = True
                    cache1[i][j][2] = counter
                    counter += 1
                    return cache1[i][j][1], stalls1

        if not cachehit1:
            self.cache_hit_2(adrs)
            self.insert_cache1(adrs)

    # Cache 2. Checking if the data is present or not if it is not present in Cache 1
    def cache_hit_2(self, adrs):
        global cachehit2
        cachehit2 = False
        for i in range(cache2):
            for j in range(assoc2):
                if adrs == cache2[i][j][0]:
                    cachehit2 = True
                    cache2[i][j][2] += counter
                    counter += 1
                    return cache2[i][j][1], stalls1 + stalls2

        if not cachehit2:
            self.memory_operation(adrs)
            self.insert_cache2(adrs)

    # Checking in memory if the data is not present in both the Caches
    def memory_operation(self, adrs):
        return RAM[adrs], stalls1 + stalls2 + stalls3

    # Inserting Data in Cache1 if not present
    def insert_cache1(self, adrs):
        cache1inserted = False
        for i in range(cache1):
            for j in range(assoc1):
                if cache1[i][j][0] == -1:
                    cache1[i][j] = [adrs, RAM[adrs], counter]
                    counter += 1
                    cache1inserted = True
        if not cache1inserted:
            self.replace_in_cache1(adrs)

    # Inserting Data in Cache2 if not present
    def insert_cache2(self, adrs):
        cache2inserted = False
        for i in range(cache2):
            for j in range(assoc2):
                if cache2[i][j][0] == -1:
                    cache2[i][j] = [adrs, RAM[adrs], counter]
                    counter += 1
                    cache2inserted = True
        if not cache2inserted:
            self.replace_in_cache2(adrs)

    # If Cache1 is full, then replacing the existing data with new one acc to LRU policy
    def replace_in_cache1(self, adrs):
        ilru = 0
        jlru = 0
        for i in range(cache1):
            for j in range(assoc1):
                if cache1[i][j][3] < cache1[ilru][jlru][3]:
                    ilru = i
                    jlru = j
        cache1[ilru][jlru] = [adrs, RAM[adrs], counter]

    # If Cache2 is full, then replacing the existing data with new one acc to LRU policy
    def replace_in_cache2(self, adrs):
        ilru = 0
        jlru = 0
        for i in range(cache2):
            for j in range(assoc2):
                if cache2[i][j][3] < cache2[ilru][jlru][3]:
                    ilru = i
                    jlru = j
        cache2[ilru][jlru] = [adrs, RAM[adrs], counter]


CacheOP = CacheHit()
