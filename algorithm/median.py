from utils import *
import random
import time

"""
a median of medians algorithm to speed up kdtree formation
process, the determinstic algorithm takes O(n), while the randomized 
one can take average of O(n), but also can reach O(n^2) at worst case, either
will be better than the naive pre-sorting (O(nlogn)). the idea is partition the 
list to buckets each has 5 elements , which can brute forcely sorted and get the median
of each and the fed to a recursive algorithm with worst case  number of recursion calls
T(0.7*n) 
"""


def partition_to_buckets( array , bucket_size):
    """
    bucket_size: number of elements in each bucket usually (5)
    can be any odd number strictly greater than 3
    """
    return [array[i:i+bucket_size] for i in range(0, len(array) , bucket_size) ]


def median_of_medians_randomized(array, index, axis):

    if len(array)  ==0 :
        return
    buckets = partition_to_buckets(array , 5)
    if len(buckets) >= 2 :
        bucket =  buckets[random.choice(list(range(int(.3*len(buckets)), int(.7*len(buckets)))))]
    else:
        bucket = buckets[-1]
    pivot = bucket[len(bucket)//2]

    lower   = [point  for point in array  if point[0][axis] < pivot[0][axis]]

    k = len(lower)
    if index < k :
        return median_of_medians( lower , index, axis)
    elif index > k :
        higher  = [point  for point in array  if point[0][axis] > pivot[0][axis]]
        return median_of_medians(higher , index-k-1, axis)
    else:
        return pivot



def median_of_medians(array, index, axis):


    buckets = partition_to_buckets(array , 5)
    medians = [sorted(bucket, key= lambda point: point[0][axis])[len(bucket)//2] for bucket in buckets]
    if len(medians) ==1 :
        pivot = medians[0]
    elif len(medians) <= 5 : 
        pivot =  sorted(medians, key= lambda point: point[0][axis])[len(medians)//2]
    elif len(medians) > 5:
        pivot  = median_of_medians(medians , len(medians)//2, axis)

    lower   = [point  for point in array  if point[0][axis] < pivot[0][axis]]

    k = len(lower)
    if index < k :
        return median_of_medians( lower , index, axis)
    elif index > k :
        higher  = [point  for point in array  if point[0][axis] > pivot[0][axis]]
        return median_of_medians(higher , index-k-1, axis)
    else:
        return pivot



if __name__ == "__main__" :
    array = points
    s = time.time()
    x = median_of_medians_randomized( array, len(array)//2 , 0)
    print("randomized   : " , time.time()- s)
    s = time.time() 
    y = median_of_medians2( array, len(array)//2 , 0)
    print("determinstic : " , time.time()- s)
    s = time.time()
    z = sorted(array, key=lambda point:point[0][0])[len(array)//2]
    print("sorted       : " , time.time()- s)
    print(x ==  y == z )

