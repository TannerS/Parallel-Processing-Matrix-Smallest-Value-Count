from multiprocessing import Pool
from multiprocessing.sharedctypes import Value, Array
import random
import time
# method to do multiplication of matrix
from multiprocessing.context import Process
# matrix mul function
import sys
def subMatrixSmallestCount(A, itr, block, size, total_smallest, total_count, x):
    # declare local count and smallest value
    smallest = sys.maxsize
    count = 0

    # start a loop to loop size of the block
    for i in range (0, block):
        # temp var
        temp = 0
        # loop range of from 0 to size of column
        for j in range (0, size):
            # A[itr * block + i]
            # e.g. itr = 0, block = 4
            # 0*4 = 0 -> 0 + i -> where i = 0 - (n-1)
            # e.g. itr = 1, block = 4
            # 1 * 4 = 4 -> 4 + i -> where i = 0 - (n-1)
            if(A[itr * block + i][j] < smallest):
                smallest = A[itr * block + i][j]
                count = 1
            elif(A[itr * block + i][j] == smallest):
               count += 1
        # end inner for loop
    # end outter for loop

    #print("Smallest value: ", smallest, " in: ", x)
    #print("Count of that value: ", count, " in: ", x)

    # compare values with current process, and total counted values
    if(smallest < total_smallest.value):
        with total_smallest.get_lock():
            total_smallest.value = smallest
        with total_count.get_lock():
            total_count.value = count
    elif(smallest == total_smallest.value):
        with total_count.get_lock():
            total_count.value += count
# main program
if __name__ == '__main__':
    # get input
    n = int(input("Enter number of nodes: "))
    # empty list of arrays
    matrix = []
    # loop and append an array of ints (i) of random numbers from j to n where it ents n numbers into that array
    for i in range (0, n):
        # append a new array of random n ints into list
        matrix.append(Array('i', [int(random.random() * 10) for j in range(0, n)]))
    # Debug Array
    '''
    print('start matrix')
    for i in range(0,n):
        for j in range (0, n):
            # end="" makes it so it does not print a newline
            print(matrix[i][j], end="")
        print()
    print('end matrix')
    '''
    # declare variables in shared memory
    Smallest = Value('i', n)
    TotalCount = Value('i', 0)
    # get break down of how many rows per process
    size = int(n / 4)
    # take time
    start_time = time.time()
    # create each process
    p0 = Process(target=subMatrixSmallestCount, args=(matrix, 0, size, n, Smallest, TotalCount, 1))
    p1 = Process(target=subMatrixSmallestCount, args=(matrix, 1, size, n, Smallest, TotalCount, 2))
    p2 = Process(target=subMatrixSmallestCount, args=(matrix, 2, size, n, Smallest, TotalCount, 3))
    p3 = Process(target=subMatrixSmallestCount, args=(matrix, 3, size, n, Smallest, TotalCount, 4))
    # start processes
    p0.start()
    p1.start()
    p2.start()
    p3.start()
    # wait for processes to finish
    p0.join()
    p1.join()
    p2.join()
    p3.join()

    print('Smallest value: {}'.format(Smallest.value))
    print('Count of that value: {}'.format(TotalCount.value))
    # print time
    print('Total time: {}s'.format (time.time() - start_time))
















