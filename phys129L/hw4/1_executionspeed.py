"""
TKC!
Execution Speed
Matthew Wong
Phys 129L Hw4 Pb1
2022-02-03
"""

import time


class Timer:
    """A simple timing class."""
    
    def __init__(self):
        # float
        self._start_t = None

    def start(self):
        """Start the timer."""
        self._start_t = time.perf_counter_ns()

    def stop(self):
        """Stop the timer.

        Returns:
            float: The time elapsed.
        """
        return time.perf_counter_ns() - self._start_t
        

def perftest(timer, expr, iterations=1000000):
    """Times how long an expression takes.

    The expression is first compiled to a PyCodeObject and then
    executed.

    Args:
        timer (Timer): The Timer object for timing.
        expr (str): The expression to evaluate.
        iterations (int): The number of iterations to test over.
            Defaults to one million iterations.

    Returns:
        float: The average time elapsed per loop.
    """
    test_obj = compile(expr, "<string>", "exec")
    timer.start()
    for _ in range(iterations):
        exec(test_obj)
    elapsed_t = timer.stop()
    return elapsed_t/iterations


# Test variables are defined here
test_a = float()
test_b = 1.0
test_list = []
test_list_b = [float() for i in range(1000000)]

# Test functions are defined here
def nothing():
    pass

def add(a, b):
    a+b

    
def main():
    """Run performance tests over a number of loops.

    I've elected to write a test function to run all these cases
    instead of writing 8 for loops since I frankly believe it's
    better programming practice.

    The tests are stored in a dictionary with a description of the test.
    Each test contains an expression to be tested, which is then
    passed into perftest() which times the test.
    """
    timer = Timer()

    # Tests are stored in {test: description} format
    tests = {
        "pass": "doing nothing (`pass`)",
        "test_a+test_b": "addition of two float variables",
        "test_a*test_b": "multiplication of two float variables",
        "test_a/test_b": "division of two float variables",
        "test_a//test_b": "integer division of two float variables",
        "test_list.append(test_a)": "appending one number to an empty list",
        "test_list_b.append(test_a)": ("appending one number to a list already"
                                       " containing 1000000 entries"),
        "nothing()": "calling a function that does nothing",
        "add(test_a, test_b)": "calling a function that adds two variables",
    }

    for test, description in tests.items():
        result = perftest(timer, test)
        print(f"Average time for {description}: {result} ns per loop.")

    
if __name__ == "__main__":
    main()
