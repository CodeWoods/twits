#!/usr/bin/env python3
import csv, os, time, tweepy
'''
prerequisites:
- Python 3.x distribution
- Twitter API Keys and Tokens
- Tweepy ( https://github.com/tweepy/tweepy )
- TWITTER_HANDLES.txt

@link:
https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-friends-ids
'''

consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_secret = os.environ['TWITTER_ACESS_SECRET']
twitter_users_file = open('TWITTER_HANDLES.txt', 'r').read().splitlines()
twitter_users_list = [l for l in twitter_users_file if l.strip()]
twitter_users_list = [l for l in twitter_users_list if not l.startswith('#')]
max_users = 5000   # 5000 is the maximum allowed count
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api  = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def write_tsv_file(rows, outfile):
    t_writer = csv.writer(outfile, delimiter='\t')
    t_writer.writerows(rows)

def retrieve_following_list(twitter_user):
    try:
        t__user_ids = api.friends_ids(screen_name=twitter_user, count=max_users)
        t_nicknames = []
        for start in range(0, min(max_users, len(t__user_ids)), 100):
            end = start + 100
            subquery = api.lookup_users(t__user_ids[start:end])
            namelist = [user.screen_name for user in subquery]
            t_nicknames.extend(namelist)

        with open('{}_twitter_following_list.txt'.format(twitter_user), 'w') as outfile:
            rows = zip(t_nicknames, t__user_ids)
            write_tsv_file(rows, outfile)
            #t_writer = csv.writer(f, delimiter='\t')
            #t_writer.writerows(rows)
            
        if len(t_nicknames) >= 4990:
            print('\x1b[1;44m[!] 5000 is the maximum allowed count.\x1b[0m')
        print('[\033[32m+\033[0m] {}: following {} users'.format(twitter_user, len(t__user_ids)))

    except tweepy.TweepError as err:
        print('\x1b[1;41m[x] {} -> {}\x1b[0m'.format(twitter_user, err.reason))

def main():
    start_time = time.time()
    for i, user in enumerate(twitter_users_list):
        retrieve_following_list(twitter_users_list[i])
        i+=1
    print('Done! {0:.3f}s'.format(time.time() - start_time))
if __name__ == '__main__':
    main()