class Score_Tracker:
    def __init__(self, first_service) -> None:
        # here 0 corresponds to user as first serve, 1 corresponds to opponenet serving first time 
        self.first_serve = first_service
        self.prev_score = [0, 0]
        self.current_score = [0, 0]

    def update_score(self, score):
        self.prev_score = self.current_score
        self.current_score = score

