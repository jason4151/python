#!/usr/bin/env python3
import requests

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
        print('\nERROR: Invalid URL Input: ' + url)

# Main
def main():
    print('Traversing: ' + url)  
    get_reward(url)
    total = str((sum(rewards)))
    print('Reward Total: ' + total)

if __name__ == '__main__':
    main()