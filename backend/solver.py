from backend.utils.globals import *
from backend.utils.utils import options
import math
import time


class Solver(object):

    def __init__(self,game):
        self.dp = {}
        self.game = game
        game.initialize()
        self.solved=False

    def solve(self):
        start_time=time.time()
        self._solve(self.game.to_string())
        end_time=time.time()
        self.solution_stats={'time':end_time-start_time,
                        'subgames':len(self.dp)}
        self.solved=True

    def _solve(self,game_string):
        if len(game_string)<=9:
            self.dp[game_string]=[0,0,0]
        else:
            new_game_strings, new_game_results = options(game_string, self.game.trumps)
            current_objective = -math.inf
            _, turn, type , _= game_string.split('.') 
            for new_game_result,new_game_string in zip(new_game_results,new_game_strings):
                if new_game_string not in self.dp:
                    self._solve(new_game_string)
                new_game_result[0]+=self.dp[new_game_string][0]
                new_game_result[1]+=self.dp[new_game_string][1]
                new_game_result[2]+=self.dp[new_game_string][2]
                maximize_objective = ((turn=='0' and type=='P') or turn!='0' and type=='M')
                minimize_objective = ((turn=='0' and type=='M') or turn!='0' and type=='P')
                if maximize_objective and current_objective<=new_game_result[0]:
                    current_objective = new_game_result[0]
                    self.dp[game_string] = new_game_result
                if minimize_objective and current_objective<=-new_game_result[0]:
                    current_objective = -new_game_result[0]
                    self.dp[game_string] = new_game_result