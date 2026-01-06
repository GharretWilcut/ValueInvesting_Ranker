import yfinance as yf

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.eligible = True
        self.stock = yf.Ticker(ticker)

        self.EV = self.get_enterprise_value()
        self.market_cap = self.get_market_cap()
        self.profit_margin = self.get_profit_margin()
        self.rev_toEV = self.get_revtoevpercent()
        self.net_income = self.get_net_income()
        self.twoyr_growth = self.get_2yr_avg_revGrowth()
        self.return_on_EV = self.get_return_on_EV()

        self.rank_score = self.score()

    
    def get_revtoevpercent(self):
        try:
            ev_to_rev = self.stock.info['enterpriseToRevenue']
            return round((1 / ev_to_rev) * 100, 2)
        except:
            self.eligible = False
            return 0


    def get_return_on_EV(self):
        if self.net_income is None or self.EV is None:
            self.eligible = False
            return 0
        return round((self.net_income / self.EV) * 100, 2)

                
    def get_net_income(self):
        try:
            profit = self.profit_margin * self.stock.info['totalRevenue']  
            return profit
        except KeyError: 
            self.eligible = False
            return 0
            
    
    def get_2yr_avg_revGrowth(self):
        financials = self.stock.financials
        try:
            revenues = financials.loc['Total Revenue']
            return round(((((revenues.iloc[0]/revenues.iloc[2])-1)/2)*100),2)
        except KeyError:
            self.eligible = False
            return 0

            
   #def score(self):
    #    if self.eligible == False:
   #         return -100
   #     else:
  #          return (self.EV()/self.market_cap)*(self.rev_toEV + (0.5*self.twoyr_growth) + (0.75*(self.profit_margin)))

    def score(self):
        if not self.eligible:
            return -100

        value_score = clamp(self.rev_toEV, 0, 20)
        profitability_score = clamp(self.profit_margin, 0, 30)
        efficiency_score = clamp(self.return_on_EV, 0, 25)
        growth_score = clamp(self.twoyr_growth, -10, 30)

        capital_structure_adjustment = self.EV / self.market_cap

        composite = (
            0.35 * value_score +
            0.25 * profitability_score +
            0.25 * efficiency_score +
            0.15 * growth_score
        )

        return round(composite * capital_structure_adjustment, 2)

    def get_enterprise_value(self) -> int:
        try:
            ev = self.stock.info['enterpriseValue']
            return ev
        except KeyError:
            self.eligible = False
            
    def get_profit_margin(self):
        try:
            return (self.stock.info['profitMargins'] * 100)
        except KeyError:
            self.eligible = False
    def get_market_cap(self):
        try:
            market_cap = self.stock.info['marketCap']
            return market_cap
        except KeyError:
            self.eligible = False
def clamp(val, low, high):
    return max(low, min(val, high))
