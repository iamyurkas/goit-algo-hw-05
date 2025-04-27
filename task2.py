def binary_search_upper_bound(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        if arr[mid] < target:
            left = mid + 1
        else:
            upper_bound = arr[mid]
            right = mid - 1

    if upper_bound is None and left < len(arr):
        upper_bound = arr[left]

    return iterations, upper_bound

# testing
arr = [1.1, 2.3, 3.5, 4.8, 5.9, 7.2, 8.4]

print(binary_search_upper_bound(arr, 4.5))  # (3, 4.8)
print(binary_search_upper_bound(arr, 6.0))  # (3, 7.2)
print(binary_search_upper_bound(arr, 8.4))  # (2, 8.4)
print(binary_search_upper_bound(arr, 9.0))  # (3, None)