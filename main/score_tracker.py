
from constants.constants import *

'''
Author: Subramanya Nanjangud Gurumurthy
email: subramanyagurumurthy96@gmail.com
'''

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
    
    # if user inputs 2 or 3 numbers
    # elif numericals >= 2 and numericals <4:
    #     if numericals == 2:
    #         for s in usr_inp:
    #             if s.isdigit():
    #                 num.append(int(s))
    #         return np.array([[num[0], 0], [num[1], 0]])

    #     elif numericals == 3:
    #         for s in usr_inp:
    #             if s.isdigit():
    #                 num.append(int(s))
    #         return np.array([[num[0], num[1]], [num[2], 0]])
    
    else:
        return NULL        


class Score_Tracker:
    def __init__(self, first_service) -> None:
        # here 0 corresponds to user as first serve, 1 corresponds to opponenet serving first time 
        self.first_serve = first_service
        self.prev_score = [0, 0]
        self.current_score = [0, 0]

    def update_score(self, score):
        self.prev_score = self.current_score
        self.current_score = score


class Score_Encoder:
    
    def __init__(self, score) -> None:
        self.encode_list = []
        self.consq_wins = ""
        self.consq_loss = ""
        self.step = 0           # 0 none, 1 step win, 2 step loss
        self.score = score
        self.update_first_serve()
        self.event_count = 1
        # this variable helps to track what happened previously. 1 consq_win, 2 consq_loss, 3 step_evnt win 4 step event loss
        self.last_event = events.BEGIN
        self.current_service = service.NONE       # 1 users serve, 2 opponent serve
        print("in score encoder, current service: ", self.current_service)
        

    def update_step(self, value):
        
        # win
        if value == WIN:
            self.step = 1

        elif value == LOSS:
            self.step = 2

        return self.step 
    
    def update_cosecutive_wins(self):
        if len(self.consq_wins) == 0:
            self.consq_wins = CS_WINS[0]
        
        elif len(self.consq_wins) == 1:
            index = CS_WINS.index(self.consq_wins)
            if index != 5:
                index += 1
            
            self.consq_wins = CS_WINS[index]
            
        return self.consq_wins

    def update_consecutive_loss(self):
        if len(self.consq_loss) == 0:
            self.consq_loss = CS_LOSSES[0]
        
        elif len(self.consq_loss) == 1:
            index = CS_LOSSES.index(self.consq_loss)
            if index != 5:
                index += 1
            self.consq_loss = CS_LOSSES[index]
        
        return self.consq_loss
    
    def reset(self, value):
        
        # step win and step loss
        if (value == reset_.RESET_STEPLOSS or reset_.STEP_WIN):
            self.consq_wins = ""
            self.consq_loss = ""

        # consecutive win 
        elif value == reset_.RESET_CSWIN:
            self.consq_loss = ""
            self.step = 0
        
        # consecutive loss
        elif value == reset_.RESET_CSLOSS:
            self.consq_wins = ""
            self.step = 0


    def update_first_serve(self):
        self.encode_list.append(self.score.first_serve)

        # user serving first time
        # if (self.score.first_serve == 0):
        #     self.user_score_id = 0
        #     self.opp_score_id = 1
        #     self.current_service = 1

        # # opponent serving for first time
        # elif (self.score.first_serve == 1):
        #     self.user_score_id = 1
        #     self.opp_score_id = 0
        #     self.current_service = 2


    def update_serve(self):
        if self.current_service == service.USER_SERVE:
            print("changing service value...", self.current_service)
            self.current_service = service.OPPONENT_SERVE

        elif self.current_service == service.OPPONENT_SERVE:
            print("changing service value...", self.current_service)
            self.current_service = service.USER_SERVE

    def check_set(self, score:list):
        if score[0] >=6 or score [1] >= 6:
            if abs(score[0] - score[1]) >=2:
                return COMPLETE
        else:
            return NOT_COMPLETE

    def encode(self, score:list):
        if self.current_service == service.NONE:
            self.current_service = self.score.first_serve

        if abs((self.score.current_score[0] + self.score.current_score[1]) - (score[0] + score[1])) != 1:
            print("entered score is not valid...!!!")
            print("re-enter values")
        
        else:

            print("current event: ", self.event_count)
            print("current serve: ", self.current_service)

            # if self.event_count >= 6:
            if self.check_set(score) == COMPLETE:
                
                return COMPLETE

            else:   
                print("calculating encoding")
                diff1 = score[0] - self.score.current_score[0]
                diff2 = score[1] - self.score.current_score[1]
                # if the user is serving now 

                print("current service value: ", self.current_service)
                
                if(self.current_service == service.USER_SERVE):
                    if diff1 > diff2:
                        # user won the point, need to update encoder accordingly
                        if self.last_event == events.BEGIN:
                            self.encode_list.append(self.update_step(WIN))
                            self.last_event = events.STEP_WIN
                            self.reset(reset_.RESET_STEPWIN)

                        elif self.last_event == events.CONSECUTIVE_WIN:
                            self.encode_list.append(self.update_cosecutive_wins())
                            self.last_event = events.CONSECUTIVE_WIN
                            self.reset(reset_.RESET_CSWIN)
                        
                        #win a game after loosing consecutively 
                        elif self.last_event == events.CONSECUTIVE_LOSS:
                            self.encode_list.append(self.update_step(WIN))
                            self.last_event = events.STEP_WIN
                            self.reset(reset_.RESET_STEPWIN)

                        elif self.last_event == events.STEP_WIN:
                            self.encode_list.append(self.update_cosecutive_wins())
                            self.reset(reset_.RESET_CSWIN)
                            self.last_event = events.CONSECUTIVE_WIN
                        
                        elif self.last_event == events.STEP_LOSS:
                            self.encode_list.append(self.update_step(WIN))
                            self.last_event = events.STEP_WIN
                            self.reset(reset_.RESET_STEPWIN)

                    # user lost the points, need to update encoder accordingly
                    elif diff1 < diff2:

                        if self.last_event == events.BEGIN:
                            self.encode_list.append(self.update_step(LOSS))
                            self.last_event = events.STEP_LOSS
                            self.reset(reset_.RESET_STEPLOSS)

                        elif self.last_event == events.CONSECUTIVE_WIN:
                            self.encode_list.append(self.update_step(LOSS))
                            self.last_event = events.STEP_LOSS
                            self.reset(reset_.RESET_STEPLOSS)
                        
                        elif self.last_event == events.CONSECUTIVE_LOSS:
                            self.encode_list.append(self.update_consecutive_loss())
                            self.reset(reset_.RESET_CSLOSS)

                        elif self.last_event == events.STEP_WIN:
                            self.encode_list.append(self.update_step(LOSS))
                            self.last_event = events.STEP_LOSS
                            self.reset(reset_.RESET_STEPLOSS)
                        
                        elif self.last_event == events.STEP_LOSS:
                            self.encode_list.append(self.update_consecutive_loss())
                            self.last_event = events.CONSECUTIVE_LOSS
                            self.reset(reset_.RESET_CSLOSS)

                        
                elif self.current_service == service.OPPONENT_SERVE:
                    if diff2 > diff1:
                        # user won the point on opponent serve
                        if self.last_event == events.BEGIN:
                            self.encode_list.append(self.update_step(WIN))
                            self.last_event = events.STEP_WIN
                            self.reset(reset_.RESET_STEPWIN)

                        elif self.last_event == events.CONSECUTIVE_WIN:
                            self.encode_list.append(self.update_cosecutive_wins())
                            self.last_event = events.CONSECUTIVE_WIN
                            self.reset(reset_.RESET_CSWIN)
                        
                        #win a game after loosing consecutively 
                        elif self.last_event == events.CONSECUTIVE_LOSS:
                            self.encode_list.append(self.update_step(WIN))
                            self.last_event = events.STEP_WIN
                            self.reset(reset_.RESET_STEPWIN)

                        elif self.last_event == events.STEP_WIN:
                            self.encode_list.append(self.update_cosecutive_wins())
                            self.reset(reset_.RESET_CSWIN)
                            self.last_event = events.CONSECUTIVE_WIN
                        
                        elif self.last_event == events.STEP_LOSS:
                            self.encode_list.append(self.update_step(WIN))
                            self.last_event = events.STEP_WIN
                            self.reset(reset_.RESET_STEPWIN)        

                    # user has lost a point in opponent serve
                    elif diff2 < diff1:
                        
                        if self.last_event == events.BEGIN:
                            self.encode_list.append(self.update_step(LOSS))
                            self.last_event = events.STEP_LOSS
                            self.reset(reset_.RESET_STEPLOSS)

                        elif self.last_event == events.CONSECUTIVE_WIN:
                            self.encode_list.append(self.update_step(LOSS))
                            self.last_event = events.STEP_LOSS
                            self.reset(reset_.RESET_STEPLOSS)
                        
                        elif self.last_event == events.CONSECUTIVE_LOSS:
                            self.encode_list.append(self.update_consecutive_loss())
                            self.reset(reset_.RESET_CSLOSS)

                        elif self.last_event == events.STEP_WIN:
                            self.encode_list.append(self.update_step(LOSS))
                            self.last_event = events.STEP_LOSS
                            self.reset(reset_.RESET_STEPLOSS)
                        
                        elif self.last_event == events.STEP_LOSS:
                            self.encode_list.append(self.update_consecutive_loss())
                            self.last_event = events.CONSECUTIVE_LOSS
                            self.reset(reset_.RESET_CSLOSS)
                

                self.score.update_score(score)
                self.update_serve()
                self.event_count = self.event_count + 1
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
    score_encode = Score_Encoder(score_)

    print("current serve: ", score_encode.current_service)

    while(True):
        print("Enter score: \n")
        score = user_input()

        if score_encode.encode(score) == NOT_COMPLETE:
            print("updated current score: ", score_.current_score)
            print("encoded list: ", score_encode.encode_list)
         
        elif score_encode.encode(score) == COMPLETE:
            print("Set completed...!!\n")
            print("Encoded values are: \n")
            print(score_encode.encode_list)
            break


# beginning of the program
if __name__ == "__main__":
    main()