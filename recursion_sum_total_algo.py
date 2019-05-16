import Algorithmia
import requests

key = 'children'
rewards = []

class AlgorithmError(Exception):
    # Define error handling class

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value).replace("\\n", "\n")

# Get Reward Function
def get_rewards(url):
    try:
        json_data = requests.get(url).json()
        if key in json_data.keys():
            for child_url in json_data['children']:
                get_rewards(child_url)
                rewards.append(float((json_data['reward'])))
        else:
            rewards.append(float((json_data['reward'])))
    except:
        raise AlgorithmError('Please provide a valid URL')

# API calls will begin at the apply() method, with the request body passed as 'input'
# For more details, see algorithmia.com/developers/algorithm-development/languages
def apply(input):
    # Clear rewards list on subsequent execution (https://blog.algorithmia.com/advanced-algorithm-design/)
    if len(rewards) > 0:
        rewards.clear()
    
    # Execute get_rewards recursive function
    get_rewards(input)
    total = str((sum(rewards)))
    return ('Total Rewards: ' + total)