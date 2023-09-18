# BESS-Optimization
1. In the US electricity markets, the BESS must earn revenue by bidding in different market products of the wholesale electricity markets in every hour. The BESS pays for charging energy (MWh) from the market and gets paid for discharging energy (MWh) in the market. The market can support any amount of charging and discharging energy (MWh) needed by the BESS. The net revenue earned by the BESS = total revenue earned from discharging - total cost of charging.
2.	For this problem statement, we consider one market product: Day-Ahead Energy Market (DAM
  2.1.	For DAM – The hourly prices in $/MWh are given. These hourly prices represent the revenue/cost of discharging/charging 1 MWh of energy in the DAM market in one     
         hour. 
  2.2.	Please refer to the file ‘ CES_GridBOOST_Problem_Statement_Data.xlsx’ for getting the price data.
  2.3.	The price data is given for 5 days
3.	The BESS cannot charge and discharge energy in the same hour in any markets.
4.	Each discharged MWh from the BESS results in a degradation cost of $10 to the BESS
5.	Maximum discharge MWh from the BESS is limited to 14,600 MWh.
6.	The BESS parameters are-
  6.1.	Maximum Power the BESS can charge and discharge in an hour – 10MW.
  6.2.	Maximum energy the BESS can store at any hour – 40MWh. The energy stored in the BESS at any hour is also called State of Charge (SoC) of the BESS.
  6.3.	The charging efficiency of the BESS – 90%
  6.4.	The discharging efficiency of the BESS – 100%
  6.5.	At any hour, the BESS should have at least 5% of the Maximum energy stored in the BESS.
7.	The problem must be formulated as a Mixed Integer Linear Programming (MILP) problem and multiplication of decision variables must be avoided.
8.	Expected outputs –
  8.1.	Hourly charging MWh and discharging MWh values for DAM markets.
  8.2.	Hourly State of Charge (MWh) value of the BESS
  8.3.	Hourly revenue from DAM market.
