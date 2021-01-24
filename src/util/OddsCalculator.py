#!/usr/bin/env python
# coding: utf-8

# In[24]:


import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt, atan, isclose


# In[ ]:


class OddsCalculator:
    @classmethod
    def from_american_odds(self, odds):
        american_odds = odds
        decimal_odds = str(100/abs(int(odds))+1) if odds[0] == '-' else str(int(odds)/100+1)
        return [american_odds, decimal_odds]


    @classmethod
    def from_decimal_odds(self, odds):
        american_odds = str(int(100/(float(odds)-1)*-1)) if float(odds) < 2 else '+'+str(int((float(odds)-1)*100))
        decimal_odds = odds
        return [american_odds, decimal_odds]

    @classmethod
    def from_fractional_odds(self, odds):
        odds_nums = odds.split('/')
        decimal_odds = str(int(odds_nums[0])/int(odds_nums[1])+1)
        american_odds = str(self.from_decimal_odds(decimal_odds)[0])
        return [american_odds, decimal_odds]

    @classmethod
    def from_implied_probability(self, odds):
        decimal_odds = 1/float(odds)
        american_odds = self.from_decimal_odds(decimal_odds)[0]

        return [american_odds, decimal_odds]
    
    @classmethod
    def calculate_odds(self, odds):
        if '.' in odds:
            if float(odds) > 1:
                return self.from_decimal_odds(odds)
            else:
                return self.from_implied_probability(odds)
        elif '/' in odds:
            return self.from_fractional_odds(odds)
        elif '-' in odds or '+' in odds:
            return self.from_american_odds(odds)
        else:
            raise Exception('Unsupported Format Exception')
    
    @classmethod
    def implied_probability(self, odds): 
        return float('{0:.4f}'.format(1/float(self.calculate_odds(odds)[1])))
    
    @classmethod
    def parlay(self, odds_list):
        implied_prob = 1
        for odds in odds_list:
            implied_prob *= self.implied_probability(odds)
        return self.calculate_odds(str(implied_prob))[0], implied_prob
    
    @classmethod
    def calculate_return(self, bet, my_bet_odds):
        my_bet_odds_dec = float(self.calculate_odds(my_bet_odds)[1])
        return bet*my_bet_odds_dec-bet

    @classmethod
    def kelly_units(self, my_bet_odds, p, bankroll, multiplier=1):
    	my_bet_odds_dec = float(self.calculate_odds(my_bet_odds)[1])
    	b = my_bet_odds_dec - 1
    	q = 1 - p
    
    	percentage = (b * p - q) / b
    
    	return percentage * bankroll * multiplier

    @staticmethod
    def cent_away(num1, num2):
        return abs(num1-num2) <= .01
    
    @classmethod
    def optimize_hold(self, my_bet, odds_spread, limit=100000):
        my_bet_odds = odds_spread[0]
        opp_bet_odds = odds_spread[1]

        profits = []
        stake = [my_bet]

        for i in range(1,len(odds_spread)):
            opp_bet_odds = odds_spread[i]
            lower_bound = 0
            upper_bound = limit*10

            opp_bet = (upper_bound+lower_bound)/2
            my_return = self.calculate_return(my_bet, my_bet_odds)
            opp_return = self.calculate_return(opp_bet, opp_bet_odds)

            my_win = opp_bet-my_return
            opp_win = my_bet-opp_return
            while not self.cent_away(my_win, opp_win):
                #print(my_win , opp_win, my_bet, opp_bet)
                if opp_win < my_win:
                    upper_bound = opp_bet
                else:
                    lower_bound = opp_bet
                opp_bet = (upper_bound+lower_bound)/2
                opp_return = self.calculate_return(opp_bet, opp_bet_odds)
                my_win = opp_bet-my_return
                opp_win = my_bet-opp_return
                if upper_bound == lower_bound:
                    break
            if i == 1:
                profits.append(my_win)
            else:
                profits.append(opp_bet)
            stake.append(opp_bet)
            #print(sum(profits), sum(stake))
        return (profits, stake)
    
    
    @classmethod
    def calculate_hold(self, odds_spread, push_perc=0.0, limit=100000):
        try:
            profits, stake = self.optimize_hold(limit/10,odds_spread, limit)
            total_stake = sum(stake)
            total_profit = sum(profits)
            hold = (total_profit/total_stake)*(1-push_perc)
            return hold*100
        except:
            return np.nan

    @classmethod
    def actual_probability(self, odds_spread, push_perc=0.0):
        implied_probabilities = []
        for odd in odds_spread:
            implied_probabilities.append(self.implied_probability(odd))
        total = sum(implied_probabilities)
        actual_probabilities = []
        for implied_prob in implied_probabilities:
            actual_probabilities.append(round(implied_prob/total,4))
        assert isclose(sum(actual_probabilities), 1)

        return actual_probabilities

    @staticmethod 
    def haversine(coordinates_a, coordinates_b):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lat1 = coordinates_a[0]
        lon1 = coordinates_a[1]
        lat2 = coordinates_b[0]
        lon2 = coordinates_b[1]

        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371.2 # Radius of earth in kilometers. Use 3959 for miles
        return c * r

