
# find missing element in a list
def find_missing(lst):
	return sorted(set(range(lst[0], lst[-1])) - set(lst))

def is_power_of_2(n):
    if n == 0:
        return False
    return (n & (n - 1) == 0)