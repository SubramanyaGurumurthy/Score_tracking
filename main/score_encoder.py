
from glob import glob
from constants.constants import *
from constants.Score_Tracker import *

'''
Author: Subramanya Nanjangud Gurumurthy
email: subramanyagurumurthy96@gmail.com
'''


encode_list = []
consq_wins = ""
consq_loss = ""
step = 0           # 0 none, 1 step win, 2 step loss
event_count = 1
# this variable helps to track what happened previously. 1 consq_win, 2 consq_loss, 3 step_evnt win 4 step event loss
last_event = events.BEGIN
current_service = service.NONE       # 1 users serve, 2 opponent serve

def user_input():
    """ Reads the user inputs and returns numpy array of size 2x2 or returns NULL if no inputs
        
        Parameters
        ----------
        None

        Returns
        -------
        np.array or NULL
    """
    num = []
    
    # reading the user input
    usr_inp = input()
    # counting the number of variables
    numericals = sum(c.isdigit() for c in usr_inp)



    # if user inputs 2 numbers
    if numericals == 2:
        for s in usr_inp:
            if s.isdigit():
                num.append(int(s))
        return num
    
    else:
        return NULL        

def update_step(self, value):
    
    # win
    if value == WIN:
        step = 1

    elif value == LOSS:
        step = 2

    return step 

def update_cosecutive_wins(self):
    if len(consq_wins) == 0:
        consq_wins = CS_WINS[0]
    
    elif len(consq_wins) == 1:
        index = CS_WINS.index(consq_wins)
        if index != 5:
            index += 1
        
        consq_wins = CS_WINS[index]
        
    return consq_wins

def update_consecutive_loss():
    if len(consq_loss) == 0:
        consq_loss = CS_LOSSES[0]
    
    elif len(consq_loss) == 1:
        index = CS_LOSSES.index(consq_loss)
        if index != 5:
            index += 1
        consq_loss = CS_LOSSES[index]
    
    return consq_loss

def reset(value):
    
    # step win and step loss
    if (value == reset_.RESET_STEPLOSS or reset_.STEP_WIN):
        consq_wins = ""
        consq_loss = ""

    # consecutive win 
    elif value == reset_.RESET_CSWIN:
        consq_loss = ""
        step = 0
    
    # consecutive loss
    elif value == reset_.RESET_CSLOSS:
        consq_wins = ""
        step = 0


def update_first_serve(score_):
    encode_list.append(score_.first_serve)


def update_serve():
    global current_service
    if current_service == service.USER_SERVE:
        print("changing service value...", current_service)
        current_service = service.OPPONENT_SERVE

    elif current_service == service.OPPONENT_SERVE:
        print("changing service value...", current_service)
        current_service = service.USER_SERVE

def check_set(score:list):
    if score[0] >=6 or score [1] >= 6:
        if abs(score[0] - score[1]) >=2:
            return COMPLETE
    else:
        return NOT_COMPLETE

def encode(score:list, score_):
    global current_service 
    global event_count
    
    if current_service == service.NONE:
        update_first_serve(score_)
        current_service = score_.first_serve

    if abs((score_.current_score[0] + score_.current_score[1]) - (score[0] + score[1])) != 1:
        print("entered score is not valid...!!!")
        print("re-enter values")
    
    else:

        print("current event: ", event_count)
        print("current serve: ", current_service)

        # if event_count >= 6:
        if check_set(score) == COMPLETE:
            
            return COMPLETE

        else:   
            print("calculating encoding")
            diff1 = score[0] - score_.current_score[0]
            diff2 = score[1] - score_.current_score[1]
            # if the user is serving now 

            print("current service value: ", current_service)
            
            if(current_service == service.USER_SERVE):
                if diff1 > diff2:
                    # user won the point, need to update encoder accordingly
                    if last_event == events.BEGIN:
                        encode_list.append(update_step(WIN))
                        last_event = events.STEP_WIN
                        reset(reset_.RESET_STEPWIN)

                    elif last_event == events.CONSECUTIVE_WIN:
                        encode_list.append(update_cosecutive_wins())
                        last_event = events.CONSECUTIVE_WIN
                        reset(reset_.RESET_CSWIN)
                    
                    #win a game after loosing consecutively 
                    elif last_event == events.CONSECUTIVE_LOSS:
                        encode_list.append(update_step(WIN))
                        last_event = events.STEP_WIN
                        reset(reset_.RESET_STEPWIN)

                    elif last_event == events.STEP_WIN:
                        encode_list.append(update_cosecutive_wins())
                        reset(reset_.RESET_CSWIN)
                        last_event = events.CONSECUTIVE_WIN
                    
                    elif last_event == events.STEP_LOSS:
                        encode_list.append(update_step(WIN))
                        last_event = events.STEP_WIN
                        reset(reset_.RESET_STEPWIN)

                # user lost the points, need to update encoder accordingly
                elif diff1 < diff2:

                    if last_event == events.BEGIN:
                        encode_list.append(update_step(LOSS))
                        last_event = events.STEP_LOSS
                        reset(reset_.RESET_STEPLOSS)

                    elif last_event == events.CONSECUTIVE_WIN:
                        encode_list.append(update_step(LOSS))
                        last_event = events.STEP_LOSS
                        reset(reset_.RESET_STEPLOSS)
                    
                    elif last_event == events.CONSECUTIVE_LOSS:
                        encode_list.append(update_consecutive_loss())
                        reset(reset_.RESET_CSLOSS)

                    elif last_event == events.STEP_WIN:
                        encode_list.append(update_step(LOSS))
                        last_event = events.STEP_LOSS
                        reset(reset_.RESET_STEPLOSS)
                    
                    elif last_event == events.STEP_LOSS:
                        encode_list.append(update_consecutive_loss())
                        last_event = events.CONSECUTIVE_LOSS
                        reset(reset_.RESET_CSLOSS)

                    
            elif current_service == service.OPPONENT_SERVE:
                if diff2 > diff1:
                    # user won the point on opponent serve
                    if last_event == events.BEGIN:
                        encode_list.append(update_step(WIN))
                        last_event = events.STEP_WIN
                        reset(reset_.RESET_STEPWIN)

                    elif last_event == events.CONSECUTIVE_WIN:
                        encode_list.append(update_cosecutive_wins())
                        last_event = events.CONSECUTIVE_WIN
                        reset(reset_.RESET_CSWIN)
                    
                    #win a game after loosing consecutively 
                    elif last_event == events.CONSECUTIVE_LOSS:
                        encode_list.append(update_step(WIN))
                        last_event = events.STEP_WIN
                        reset(reset_.RESET_STEPWIN)

                    elif last_event == events.STEP_WIN:
                        encode_list.append(update_cosecutive_wins())
                        reset(reset_.RESET_CSWIN)
                        last_event = events.CONSECUTIVE_WIN
                    
                    elif last_event == events.STEP_LOSS:
                        encode_list.append(update_step(WIN))
                        last_event = events.STEP_WIN
                        reset(reset_.RESET_STEPWIN)        

                # user has lost a point in opponent serve
                elif diff2 < diff1:
                    
                    if last_event == events.BEGIN:
                        encode_list.append(update_step(LOSS))
                        last_event = events.STEP_LOSS
                        reset(reset_.RESET_STEPLOSS)

                    elif last_event == events.CONSECUTIVE_WIN:
                        encode_list.append(update_step(LOSS))
                        last_event = events.STEP_LOSS
                        reset(reset_.RESET_STEPLOSS)
                    
                    elif last_event == events.CONSECUTIVE_LOSS:
                        encode_list.append(update_consecutive_loss())
                        reset(reset_.RESET_CSLOSS)

                    elif last_event == events.STEP_WIN:
                        encode_list.append(update_step(LOSS))
                        last_event = events.STEP_LOSS
                        reset(reset_.RESET_STEPLOSS)
                    
                    elif last_event == events.STEP_LOSS:
                        encode_list.append(update_consecutive_loss())
                        last_event = events.CONSECUTIVE_LOSS
                        reset(reset_.RESET_CSLOSS)
            

            score_.update_score(score)
            update_serve()
            event_count = event_count + 1
            return NOT_COMPLETE

def main():
    # print("beginning of the set: \n")
    # print("Please enter the score of each game according the server's perspective, i.e., the first score should be entered which corresponds to the serving player at each game \n")
    # print("Let's begin.....!!!!")
    # print("Enter 0 for user's serve, 1 for opponent's serve")
    print("Please enter who is serving:\n")

    serve_value = input()
    if (serve_value == 0):
        serve_value = service.USER_SERVE
    
    elif serve_value == 1:
        serve_value = service.OPPONENT_SERVE

    score_ = Score_Tracker(serve_value)   

    print("current serve: ", current_service)

    while(True):
        print("Enter score: \n")
        score = user_input()

        if encode(score, score_) == NOT_COMPLETE:
            print("updated current score: ", score_.current_score)
            print("encoded list: ", encode_list)
         
        elif encode(score, score_) == COMPLETE:
            print("Set completed...!!\n")
            print("Encoded values are: \n")
            print(encode_list)
            break


# beginning of the program
if __name__ == "__main__":
    main()