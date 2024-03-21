import random
import sys
debug=True
class RouletteTable():
    def __init__(self):
        #Individual chances to allow later changes for fairness.
        EuropeanLayout_numbers=[0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26]
        EuropeanLayout_chances=[0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703,0.02702702702702703]
        Layout="European"
        if Layout=="European":
            #European Layout Based on https://casinoalpha.com/wp-content/uploads/2023/06/1.European-Wheel-Design-1-1024x855.png
            self.RouletteNumbers=EuropeanLayout_numbers
            self.RouletteChances=EuropeanLayout_chances
        self.stake=[]
        self.UserMoney=100
        self.BetType=[]
        self.ResNumber=-1
        self.Bet_TypeList=["Empty",#Resets for extra bug-proof
                      #Inside Bets
                      "Single",#Single Bet
                      "Split",#Two vertically/horizontally adjacent numbers
                      "Street",#Three in a line
                      "Corner",#Corner Bet
                      "Top Line",#Single Zero Variation: 0,1,2,3
                      "Double Street",#Bet on six
                      #Outside Bets
                      "Dozen"#First,Second or Third Dozen (12 numbers)
                      "Column"#First, Second or Third Column (12 numbers)
                      "18"  #1-18 or 19-36
                      "Red"#All Red
                      "Black"#All Black
                      "Even"
                      "Odd"
                      ]
        self.Bet_WinningNumber_List=[]
        self.Bet_PayoutList=[0,35,17,11,8,6,6,2,2,1,1,1,1,1]
        #Source of Payouts: https://www.venetianlasvegas.com/casino/table-games/roulette-basic-rules.html
        
        #AllNumbers_Count=len(EuropeanLayout_chances)
        #print("Ther are "+str(AllNumbers_Count)+" numbers.")
        """#Skript used to generate Chances
        printstring="["+str(1/37)
        for i in range(36):
            printstring+=","+str(1/37)
        print(printstring+"]")
        """
    def Bet_stake(self):
        ChipsList=[1,5,10,25,50,100,200,500]
        if self.UserMoney==0:
            print("You are out of credits. Leave and restart/ask the owner for more.") 
            sys.exit()
        print(" You got "+str(self.UserMoney)+" credits.  How much do you want to bet?\nYou can Bet Chips of 1,5,10,25,50,100,200 or 500.")
        while True:
            stake=(input().lower()).replace("credits","").replace(" ","").replace("c","")
            try:
                stake=int(stake) 
            except:
                print("You didnt insert a number.")
                print("Please enter a valid stake.")
                continue
            if stake not in ChipsList:
                print("You can only bet given chips.")
                print("Please enter a valid stake.")
                continue
            if stake>self.UserMoney:
                print("Thats more than you have! Due to safety reasons, its impossible for us to let you make debts.")
                print("You only got "+str(self.UserMoney)+" credits.")
                print("Please enter a valid stake.")
            else:
                print("There we go! "+str(stake)+" credits are on the line.")
                self.stake.append(stake)
                self.UserMoney-=stake
                break
    


    #Access Dictionary with bet numbers
    def BetAccess(self, BetNumberMade):
        #For understanding view European_Numbered_Final4.pdf
        AccessDict={1: (1, [3]) ,
                    2: (1, [6]),
                    3: (1, [9]),
                    4: (1, [12]),
                    5: (1, [15]),
                    6: (1, [18]),
                    7: (1, [21]),
                    8: (1, [24]),
                    9: (1, [27]),
                    10:(1, [30]) ,
                    11:(1, [33]) ,
                    12:(1, [36]) ,
                    13:(4, [2,3,5,6]),
                    14:(4, [5,6,8,9]),
                    15:(4, [8,9,11,12]),
                    16:(4, [11,12,14,15]),
                    17:(4, [14,15,17,18]),
                    18:(4, [17,18,20,21]),
                    19:(4, [20,21,23,24]),
                    20:(4, [23,24,26,27]),
                    21:(4, [26,27,29,30]),
                    22:(4, [29,30,32,33]),
                    23:(4, [32,33,35,35]),
                    24:(1, [0]) ,
                    25:(1, [2]) ,
                    26:(1, [5]) ,
                    27:(1, [8]) ,
                    28:(1, [11]) ,
                    29:(1, [14]) ,
                    30:(1, [17]) ,
                    31:(1, [20]) ,
                    32:(1, [23]) ,
                    33:(1, [26]) ,
                    34:(1, [29]) ,
                    35:(1, [32]) ,
                    36:(1, [35]) ,
                    37:(4, [1, 2, 4, 5,]) ,
                    38:(4, [4, 5, 7, 8]) ,
                    39:(4, [7, 8, 10, 11]) ,
                    40:(4, [10, 11, 13, 14]) ,
                    41:(4, [13, 14, 16, 17]) ,
                    42:(4, [16, 17, 19, 20]) ,
                    43:(4, [19, 20, 22, 23,]) ,
                    44:(4, [22, 23, 25, 26,]) ,
                    45:(4, [25, 26, 28, 29]) ,
                    46:(4, [28, 29, 31, 32,]) ,
                    47:(4, [31, 32, 34, 35]) ,
                    48:(1, [1]) ,
                    49:(1, [4]) ,
                    50:(1, [7]) ,
                    51:(1, [10]) ,
                    52:(1, [13]) ,
                    53:(1, [16]) ,
                    54:(1, [19]) ,
                    55:(1, [22]) ,
                    56:(1, [25]) ,
                    57:(1, [28]) ,
                    58:(1, [31]) ,
                    59:(1, [34]) ,
                    60:(6, [1, 2, 3, 4, 5, 6, ]) ,
                    61:(6, [4, 5, 6, 7, 8, 9,]) ,
                    62:(6, [7, 8, 9, 10, 11, 12,]) ,
                    63:(6, [13, 14, 15, 16, 17, 18,]) ,
                    64:(6, [16, 17, 18, 19, 20, 21,]) ,
                    65:(6, [19, 20, 21, 22, 23, 24,]) ,
                    66:(6, [25, 26, 27, 28, 29, 30,]) ,
                    67:(6, [28, 29, 30, 31, 32, 33,]) ,
                    68:(6, [31, 32, 33, 34, 35, 36]) ,
                    69:(7, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]) ,
                    70:(7, [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]) ,
                    71:(7, [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]) ,
                    72:(8, [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, ]) ,
                    73:(8, [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35,]) ,
                    74:(8, [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36,]) ,
                    75:(9, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]) ,
                    76:(13, [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]) ,
                    #Top Line Bet war versehentlich doppelt und wurde durch 152 ersetzt
                    152:(5, [0,1,2,3]) ,
                    77:(10, [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34]) ,
                    78:(11, [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35,]),
                    79:(12,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, ] ) ,
                    80:( 9, [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]) ,
                    81:( 2, [0, 3]) ,
                    82:( 2, [3, 6]) ,
                    83:( 2, [6, 9]) ,
                    84:( 2, [9, 12]),
                    84:( 2, [12, 15]) ,
                    85:( 2, [15, 18]) ,
                    86:( 2, [18, 21]) ,
                    87:( 2, [21, 24]) ,
                    88:( 2, [24, 27]) ,
                    89:( 2, [27, 30]) ,
                    90:( 2, [30, 33]) ,
                    91:( 2, [33, 36]) ,
                    92:( 2, [0, 2]) ,
                    93:( 2, [2, 5]) ,
                    94:( 2, [5, 8]) ,
                    95:( 2, [8, 11]) ,
                    96:( 2, [11, 14]) ,
                    97:( 2, [14, 17]) ,
                    98:( 2, [17, 20]) ,
                    99:( 2, [20, 23]) ,
                    100:(2 , [23, 26]) ,
                    101:(2 , [26, 29]) ,
                    102:(2 , [29, 32]) ,
                    103:(2 , [32, 35]) ,
                    104:(2 , [0, 1]) ,
                    105:(2 , [1, 4]) ,
                    106:(2 , [4, 7]) ,
                    107:(2 , [7, 10]) ,
                    108:(2 , [10, 13]) ,
                    109:(2 , [13, 16]) ,
                    110:(2 , [16, 19]) ,
                    111:(2 , [19, 22]) ,
                    112:(2 , [22, 25]) ,
                    113:(2 , [25, 28]) ,
                    114:(2 , [28, 31]) ,
                    115:(2 , [31, 34]) ,
                    116:( 3, [1, 2, 3, ]) ,
                    117:( 3, [4, 5, 6,]) ,
                    118:( 3, [7, 8, 9,]) ,
                    119:( 3, [10, 11, 12,]) ,
                    120:( 3, [13, 14, 15,]) ,
                    121:( 3, [16, 17, 18,]) ,
                    122:( 3, [19, 20, 21,]) ,
                    123:( 3, [22, 23, 24,]) ,
                    124:( 3, [25, 26, 27,]) ,
                    125:( 3, [28, 29, 30,]) ,
                    126:( 3, [31, 32, 33,]) ,
                    127:( 3, [34, 35, 36,]) ,
                    128: (2, [2, 3]),
                    129: (2, [5, 6]),
                    130: (2, [8, 9]),
                    131: (2, [11, 12]),
                    132: (2, [14, 15]),
                    133: (2, [17, 18]),
                    134: (2, [20, 21]),
                    135: (2, [23, 24]),
                    136: (2, [26, 27]),
                    137: (2, [29, 30]),
                    138: (2, [32, 33]),
                    139: (2, [35, 36]),
                    140: (2, [1, 2]),
                    141: (2, [4, 5]),
                    142: (2, [7, 8]),
                    143: (2, [10, 11]),
                    144: (2, [13, 14]),
                    145: (2, [16, 17]),
                    146: (2, [19, 20]),
                    147: (2, [22, 23]),
                    148: (2, [25, 26]),
                    149: (2, [28, 29]),
                    150: (2, [31, 32]),
                    151: (2, [34, 35]),
                    }
        BetSet=AccessDict[BetNumberMade]
        
        self.Bet_WinningNumber_List.append(BetSet[1])
        self.BetType.append(BetSet[0])
        if debug:
            print(self.Bet_WinningNumber_List)
            print(self.BetType)
    
    def TurnTheTable(self):
        self.ResNumber=-1
        self.ResNumber=random.choices(self.RouletteNumbers,self.RouletteChances)

    def DisplayResult(self):
        print("The ball landed on the "+str(self.ResNumber[0])+"!")
    def Bet_payout(self, WinningBet):
        print("Wow! You won!")
        Win=self.stake[WinningBet]*self.Bet_PayoutList[self.BetType[WinningBet]]
        print("You get your stake back plus "+str(Win)+ " credits.")    
        self.UserMoney+=Win
        self.UserMoney+=self.stake[WinningBet]
        self.stake[WinningBet]=0
        self.BetType[WinningBet]=0
        self.Bet_WinningNumber_List[WinningBet]=[]
        self.ResNumber=-1
        
    def Bet_LooseAllMessage(self):
        print("I'm sorry, you lost.")
        sumOfLoose=0
        for loose in self.stake: sumOfLoose+=loose
        print("All your stake of entire "+str(sumOfLoose)+" credits is gone.")
        self.stake=[]
        self.BetType=[]
        self.Bet_WinningNumber_List=[]
        self.ResNumber=-1
        print("There are "+str(self.UserMoney)+" credits on your account.")

    def Bet_PartialLostLeft(self):
        print("You won a bit and lost a bit.")
        sumOfLoose=0
        for loose in self.stake: 
            if loose!=[]: sumOfLoose+=loose
        print("The leftover stakes of "+str(sumOfLoose)+" credits is gone.")
        self.stake=[]
        self.BetType=[]
        self.Bet_WinningNumber_List=[]
        self.ResNumber=-1
        print("There are "+str(self.UserMoney)+" credits on your account.")
        

    def WinOrLoose(self):
        if debug:
            print(self.ResNumber)
            print(self.BetType)
        winCount=0
        for CurrentWinningNumbersIndex in range(len(self.Bet_WinningNumber_List)):
            CurrentWinningNumbers=self.Bet_WinningNumber_List[CurrentWinningNumbersIndex]
            if self.ResNumber[0] in CurrentWinningNumbers:
                self.Bet_payout(CurrentWinningNumbersIndex)
                winCount+=1
            
        if winCount==0:
            self.Bet_LooseAllMessage()
        elif winCount<len(self.Bet_WinningNumber_List)-1:
            self.Bet_PartialLostLeft()
        else:
            self.stake=[]
            self.ResNumber=-1
            self.Bet_WinningNumber_List=[]    
    def Bet_ChooseAndStake_once(self):
        self.Bet_stake()
        while True:
            AccessNum=int(input("Insert number between 1-151. "))
            if (AccessNum > 0 and AccessNum <=151):
                break
            else:
                print("Enter valid number please. For more information, seek the infographic.")
        self.BetAccess(AccessNum)
    def Bet_ChooseAndStake_multiple(self):
        againBool=True
        while True:
            if againBool:
                self.Bet_ChooseAndStake_once()
                againBool=False
            if self.UserMoney<1:
                print("You bet all your money. Let the game begin!")
                break
            else:
                again=input("Do you want to set another chip? (yes/no) \n")
                if again.lower()=="y" or again.lower()=="yes":
                    againBool=True
                elif again.lower()=="n" or again.lower()=="no":
                    break
                else:
                    print("Please answer with yes or no.")
                
                
newTable=RouletteTable()
while True:
    newTable.Bet_ChooseAndStake_multiple()
    newTable.TurnTheTable()
    newTable.DisplayResult()
    newTable.WinOrLoose()

"""
#Skript to generate number rows
printnr=0
printstrList=["",""]
Start=6
Addendum=3
Black=False
for     i in range(1,36):
    
    #printnr+=1
    #if not (i % 2) == 0: #Odd/Even 
    #Algorithm for red/black
    if i<10 and not (i%2) == 0:
        if Black:
            continue
        else:
            printstrList[printnr]+=str(i)+", "
    elif i >10 and i<19 and (i%2)==0:
        if Black:
            continue
        else:
            printstrList[printnr]+=str(i)+", "
    elif i > 18 and i<28 and not (i%2)==0:
        if Black:
            continue
        else:
            printstrList[printnr]+=str(i)+", "
    elif i >28 and (i%2)==0:
        if Black:
            continue
        else:
            printstrList[printnr]+=str(i)+", "
    if Black:
        printstrList[printnr]+=str(i)+", "
    #print(str(i)+": (2, [])")


    if i==Start:
        #printnr+=1
        #printstrList.append("")
        Start+=Addendum
        for secondIterNum in range(i-5,i+1):
            printstrList[printnr]+=str(secondIterNum)+", "
        #print(str(i-3)+", "+str(i))
        #print(str(i)+", "+str(i+3))
for row in printstrList:
    print(row)
#"""
