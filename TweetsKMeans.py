# KMeans Clustering to put the tweets in different cluster.
# Author: Kushagra Dar
# Date: 11/10/2019
import errno
import glob
import random
import re
from typing import List
# Data Preprocessing
# Regular expression for cleaning the initial data
def preprocess(alltweets):
    print(' Doing Preprocessing')
    tweets_all: List[str] = []
    for t in alltweets:
        temp = t.split('|')
        if temp == '\n':
            continue
        print(temp[2])
        tweet = temp[2].lower()
        pre_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        tweets_all.append(pre_tweet)
    print(' Done Preprocessing')
    return tweets_all
#Count Number of Words in a tweet
# def countWords(list_of_words):
#     counts_dict = {}
#     for word in list_of_words:
#         if word in counts_dict:
#             counts_dict[word] = counts_dict[word] + 1
#         else:
#             counts_dict[word] = 1
#     return counts_dict


#Find Intersection between two tweets
# def intersection(tweetdata_one, tweetdata_two):
#     result_intesection = 0
#     for word in tweetdata_one:
#         while tweetdata_one[word] != 0 and word in tweetdata_two:
#             if word in tweetdata_two:
#                 tweetdata_two[word] = tweetdata_two[word] - 1
#                 tweetdata_one[word] = tweetdata_one[word] - 1
#                 if tweetdata_two[word] == 0:
#                     tweetdata_two.pop(word, None)
#                 result_intesection += 1
#     print('Intersection : %s' %result_intesection)
#     return result_intesection


#Find Union between two tweets
# def union(tweetdata_one, tweetdata_two):
#     result_union = 0
#     for word in tweetdata_one:
#         if word in tweetdata_two:
#             result_union = result_union + max(tweetdata_one[word], tweetdata_two[word])
#             tweetdata_two.pop(word, None)
#         else:
#             result_union = result_union + tweetdata_one[word]
#     for word in tweetdata_two:
#         result_union = result_union + tweetdata_two[word]
#     print('Union - %s' %result_union)
#     return result_union




def JaccardDistance(tweetDataOne, tweetDataTwo):
    # print(tweetDataOne)
    # print(tweetDataTwo)
    # tweetDataOne_count = countWords(tweetDataOne)
    # tweetDataTwo_count = countWords(tweetDataTwo)
    # print(dict(tweetDataOne_count))
    # print(dict(tweetDataTwo_count))
    # tweetdata_union = union(dict(tweetDataOne_count), dict(tweetDataTwo_count))
    # tweetdata_intersect = intersection(dict(tweetDataOne_count), dict(tweetDataTwo_count))
    # print(set(tweetDataOne.split(" ")))
    # print(set(tweetDataTwo.split(" ")))
    tweetdata_union = set(tweetDataOne.split(" ")).union(set(tweetDataTwo.split(" ")))
    tweetdata_intersect = set(tweetDataOne.split(" ")).intersection(tweetDataTwo.split(" "))
    return round(1.0 - float(len(tweetdata_intersect)/len(tweetdata_union)),4)


# K-Means Algorithm
# For a given number of iterations:
#     Iterate through items:
#         Find the mean closest to the item
#         Assign item to mean
#         Update mean



def form_clusters(tweets_all, centroids):
    print('Creating clusters')
    clusters = {}
    for i in range(len(centroids)):  # Initialize clusters
        clusters[i] = []

    for tweet_id in range(len(tweets_all)):
        min_distance = 1
        clusterId = 0
        for index in range(len(centroids)):
            jaccardDistance = JaccardDistance(centroids[index], tweets_all[tweet_id])
            # print(jaccardDistance)
            if (jaccardDistance < min_distance):
                min_distance = jaccardDistance
                clusterId = index
        clusters[clusterId].append(tweet_id)
    print('Done with Creating clusters')
    return clusters


def find_new_centroids(cluster, tweets):
    print('find New Clusters')
    min_distance = 1
    min_cluster_id = cluster[0]
    for cluster_tweet_id in range(len(cluster)):
        # print(cluster_tweet_id)
        distance = 0
        for other_cluster_tweetid in range(len(cluster)):
            # print(other_cluster_tweetid)
            distance = distance + JaccardDistance(tweets[cluster_tweet_id], tweets[other_cluster_tweetid])
            # print(distance)
        mean = distance/len(cluster)
        # print(mean)
        if mean < min_distance:
            min_distance = mean
            min_cluster_id = cluster_tweet_id
    print('New Clusters Found')
    return min_cluster_id

def sum_squared_error(clusters, centroids, tweet_data):
    # print(clusters)
    # print(centroids)
    # print(tweet_data)
    print('Calculating Sum Squared Error')
    sse = 0
    for cluster in clusters:
        for tweet in clusters[cluster]:
            sse += JaccardDistance(tweet_data[tweet], tweet_data[centroids[cluster]]) ** 2
            # print(JaccardDistance(tweet_data[tweet], tweet_data[centroids[cluster]]) ** 2)
    print('Calculated Sum Squared Error')
    return sse

def main():
    alltweets = []
    path = 'Health-Tweets/*.txt'
    files = glob.glob(path)
    try:
        with open(files[0],encoding="utf8",errors='ignore') as f:
            for line in f:
                curr=line[:-1]
                curr
                alltweets.append(curr)
    except IOError as exc:
        if exc.errno != errno.EISDIR:  # Do not fail if a directory is found, just ignore it.
            raise  #
    tweets_all = preprocess(alltweets)
    tweets_all = tweets_all
    random.shuffle(tweets_all)
    r_dict  = dict()
    val = int(input("Enter the initial seeds you want: "))
    initial_seed = []
    count=0
    while count<val :
        t_val = random.randint(0,len(tweets_all))
        print(t_val)
        if tweets_all[t_val] in r_dict:
            continue
        else:
            r_dict[tweets_all[t_val]]= tweets_all[t_val]
            initial_seed.append(tweets_all[count])
            count=count+1
    #tweets_10 = tweets_all[:10]
    centroids = initial_seed
    while True:
        print('New Iteration Begin')
        new_centroids = []
        clusters = form_clusters(tweets_all, initial_seed)
        #clusters = form_clusters(tweets_10, initial_seed)
        for cluster in clusters:
            new_centroids.append(find_new_centroids(clusters[cluster], tweets_all))
            #new_centroids.append(find_new_centroids(clusters[cluster], tweets_10))
        if new_centroids == centroids:
            break
        else:
            centroids = new_centroids
        print('Iteration Ends')

    for cluster in clusters:
        print('\n')
        print(str(cluster))
        print('Number of Tweets in Cluster - %s' %len(clusters[cluster]))
        print("\t")
        # for tweet in clusters[cluster]:
        #     #print(tweets_10[tweet], ", ")
        #     print(tweets_all[tweet], ", ")
        # print("\n")

    print("\n\n")
    print("SSE: ")
    #print(str(sum_squared_error(clusters, centroids, tweets_10)))
    print(str(sum_squared_error(clusters, centroids, tweets_all)))

if __name__ == "__main__":
    main()
