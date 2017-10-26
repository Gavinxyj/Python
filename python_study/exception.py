import copy

temp_list = [0,1,2,[3,4]]
print(id(temp_list))
test_list = temp_list
print(id(test_list))
test_copy_list =copy.copy(temp_list)
print(id(test_copy_list))
test_deep_copy_list = copy.deepcopy(test_list)
print(id(test_deep_copy_list))

temp_list.append(4)
print(id(temp_list))
print(test_list, test_copy_list, test_deep_copy_list)

test_list[3].append('sign')
print(test_list, test_copy_list, test_deep_copy_list)