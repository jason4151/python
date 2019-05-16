#!/usr/bin/env python3
import requests
import time

# Initial URL
url = 'http://algo.work/interview/a'

# Dictionary Key
key = 'children'

# Rewards List
rewards = []

# Get Reward Function
def get_reward(url):
    try:
        json_data = requests.get(url).json()
        if key in json_data.keys():
            for child_url in json_data['children']:
                get_reward(child_url)
                rewards.append(float((json_data['reward'])))
        else:
            rewards.append(float((json_data['reward'])))
    except:
        print(f'\nERROR: Invalid URL Input: {url}')

# Main
def main():
    if len(rewards) > 0:
        rewards.clear()
    start = time.time()
    print(f'Traversing: {url}')  
    get_reward(url)
    total = str((sum(rewards)))
    print(f'Reward Total: {total}')
    print(f'Duration: {time.time() - start}s')

if __name__ == '__main__':
    main()