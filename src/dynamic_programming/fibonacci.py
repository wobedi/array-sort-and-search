from time import perf_counter


def fibonacci_recursive(x: int) -> int:
    """Calculates x'th Fibnoacci number in O(2^N) time, O(2^N) space"""
    # ignoring x<=0
    if x == 1 or x == 2:
        return 1
    return fibonacci_recursive(x-1) + fibonacci_recursive(x-2)


def fibonacci_memoized(x: int, cache: {}) -> int:
    """Calculates x'th Fibnoacci number in O(N) time, O(N) space"""
    # ignoring x<=0
    if x == 1 or x == 2:
        return 1
    if x not in cache:
        cache[x] = (fibonacci_memoized(x-1, cache)
                    + fibonacci_memoized(x-2, cache))
    return cache[x]


def fibonacci_bottom_up(x: int, cache: {}) -> int:
    """Calculates x'th Fibnoacci number in O(N) time, O(N) space"""
    # ignoring x<=0
    if x == 1 or x == 2:
        return 1
    cache[1] = cache[2] = 1
    for i in range(3, x + 1):
        cache[i] = cache[i-1] + cache[i-2]
    return cache[x]


def fibonacci_bottom_up_minified(x: int) -> int:
    """Calculates x'th Fibnoacci number in O(N) time, O(1) space"""
    # ignoring x<=0
    if x == 1 or x == 2:
        return 1
    first, second = 1, 2
    for _ in range(4, x + 1):
        res = first + second
        first = second
        second = res
    return res


if __name__ == '__main__':
    print('#####################')
    print('### FIBONACCI(35) ###')
    print('#####################')
    print('RECURSIVE IMPLEMENTATION:')
    start = perf_counter()
    print(fibonacci_recursive(35))
    stop = perf_counter()
    print(f'Secs: {stop - start}\n')

    print('MEMOIZED IMPLEMENTATION:')
    start = perf_counter()
    print(fibonacci_memoized(35, {}))
    stop = perf_counter()
    print(f'Secs: {stop - start}\n')

    print('BOTTOM-UP IMPLEMENTATION:')
    start = perf_counter()
    print(fibonacci_bottom_up(35, {}))
    stop = perf_counter()
    print(f'Secs: {stop - start}\n')

    print('BOTTOM-UP (MINIFIED) IMPLEMENTATION:')
    start = perf_counter()
    print(fibonacci_bottom_up_minified(35))
    stop = perf_counter()
    print(f'Secs: {stop - start}\n')