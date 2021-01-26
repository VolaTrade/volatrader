from BackTest.Result import Result 
from typing import List

class DarwinsDict():

    def __init__(self):
        self.dict = {}


    def insert(self, r: Result) -> None:
        assert isinstance(r, Result)

        if r.key in self.dict:
            if self.dict[r.key].score < r.score:
                self.dict[r.key] = r

            elif self.dict[r.key].score == r.score:
                if self.dict[r.key].strat_score_beta > r.strat_score_beta: #beta tie break 
                    self.dict[r.key] = r

        else:
            self.dict[r.key] = r



    def getResults(self) -> List[Result]:
        
        return list(self.dict.values()) 

    def toString(self) -> str:

        temp_dict = {}
        for key in self.dict.keys():
            temp_dict[key] = self.dict[key].toString()

        return str(temp_dict)

        
