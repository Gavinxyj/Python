from multiprocessing import Pool

def fun(x):
	print('sfsdsfd')
	return x * x

for i in range(10):
    Process(target=producer, args=(q,)).start() 
'''
with Pool(processes=5) as pool:
	pool.map(fun, [1,2,3,4,5,6,7,8])

#print(ret.get(timeout=1))
print('the end')

'''