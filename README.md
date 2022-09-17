# Score_tracking

## Aim
The aim of this work is to come up with a concept which can store the [tennis's game](https://en.wikipedia.org/wiki/Tennis_scoring_system#:~:text=%22game%22-,For,-instance%2C%20if%20the) scoring pattern and to print out the encoded message, which can be decoded to get the exact scoring pattern of that particular game. The project helps the player to keep the track of his/her performance throughout, which could be later used to understand player's patterns of Game performance. 

## Requirements
Programming language used: [python 3.9.13](https://www.python.org/downloads/release/python-3913/).
### Libraries: 
- [enum](https://docs.python.org/3/library/enum.html)

## Folder Structure:
    .
    ├── ...
    ├── main  
    |   |── constants
    |   |   |── __init__.py
    |   |   |── contants.py
    |   |   └── Score_Tracker.py
    |   |
    │   └── score_encoder.py 
    └── ...
    
## Algorithms and Logics used:
- The encoder module uses events logic to find the Game's encoding value. The tennis Game which start from [0, 0] has the target to of reaching 6 by either players with the difference of 2. 
- In case if the score does not have difference of 2 i.e., when a player reaches 6 but the opponent's score is 5, the Game extends untill  
