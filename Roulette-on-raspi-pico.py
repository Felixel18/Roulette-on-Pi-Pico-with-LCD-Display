#Felixel18 on github

#merge of the roulette script and the numberpad.
##needs an rasberry pi pico with lcd display and i2c port with sda on pin 20 and scl on pin 21
#also a joystick on pin 26/27 and the joystick button on pin 14/an extra button on pin 14  
#Watch out: the module random.choice may be named random.choices depending on python version. It can be renamed in rouletteTable.TurnTheTable
#if you use random.choices with special weights you need to access the resNumber as resNumber[0]

from time import sleep_ms
from machine import I2C, Pin, ADC
from machine_i2c_lcd import I2cLcd
import random
import sys

#only debugs certain functions inside the roullette part of the script
debug=False


class NumberField():
    def __init__(self):
        #Initiate I2C
        self.i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=100000)
        #Initiate LCD over I2C
        self.lcd = I2cLcd(self.i2c, 0x27, 4, 20)
        self.Button=Pin(14,Pin.IN, Pin.PULL_UP)
        
        self.joystick_x_pin = ADC(Pin(26)) 
        self.joystick_y_pin = ADC(Pin(27))
        self.Cursory=0
        self.Cursorx=0
        self.NumberPadItems=[["EMPTY",],["0","1","2","3"],["4","5","6","7"],["8","9","Delete","Enter"]]
        self.CurrentNumber=[" "," "," "]
        self.returnBool=False
        self.FirstExtraMarker=19
        self.SecondExtraMarker=19
        self.CurrentBoard=[self.CurrentNumber[0],self.CurrentNumber[1],self.CurrentNumber[2]," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",
                           " "," "," "," "," ", " "," ",self.NumberPadItems[1][0]," ",self.NumberPadItems[1][1], " ",self.NumberPadItems[1][2]," ",self.NumberPadItems[1][3]," "," "," "," "," "," ",
                           " "," "," "," "," ", " "," ",self.NumberPadItems[2][0]," ",self.NumberPadItems[2][1], " ",self.NumberPadItems[2][2]," ",self.NumberPadItems[2][3]," "," "," "," "," "," ",
                           " "," "," "," "," ", " "," ",self.NumberPadItems[3][0]," ",self.NumberPadItems[3][1], " ", "D", " ","E"," "," "," "," "," "," "]
    def rebuildsCurrentBoard(self):
        self.CurrentBoard=[self.CurrentNumber[0],self.CurrentNumber[1],self.CurrentNumber[2]," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",
                           " "," "," "," "," ", " "," ",self.NumberPadItems[1][0]," ",self.NumberPadItems[1][1], " ",self.NumberPadItems[1][2]," ",self.NumberPadItems[1][3]," "," "," "," "," "," ",
                           " "," "," "," "," ", " "," ",self.NumberPadItems[2][0]," ",self.NumberPadItems[2][1], " ",self.NumberPadItems[2][2]," ",self.NumberPadItems[2][3]," "," "," "," "," "," ",
                           " "," "," "," "," ", " "," ",self.NumberPadItems[3][0]," ",self.NumberPadItems[3][1], " ", "D", " ","E"," "," "," "," "," "," "]
        self.CurrentBoard[self.FirstExtraMarker]="|"
        self.CurrentBoard[self.SecondExtraMarker]="|"
    def printBoard(self):
        self.lcd.cursor_x = 0
        self.lcd.cursor_y = 0
        self.rebuildsCurrentBoard()
        for FieldInput in self.CurrentBoard:
            self.lcd.putchar(FieldInput)
    
    def GetExtraMarkers(self):
        if self.Cursory==0:
            self.FirstExtraMarker=19
            self.SecondExtraMarker=19
        elif self.Cursory==3 and self.Cursorx==2:
            self.FirstExtraMarker=70
            self.SecondExtraMarker=72
        elif self.Cursory==3 and self.Cursorx==3:
            self.FirstExtraMarker=72
            self.SecondExtraMarker=74
        else:
            CurrentItem=self.NumberPadItems[self.Cursory][self.Cursorx]
            print(CurrentItem)
            print(self.Cursorx)
            #Copy and rewrite to prevent selector selecting written-down numbers
            CurrentBoardCopy=self.CurrentBoard
            CurrentBoardCopy[0]=" "
            CurrentBoardCopy[1]=" "
            CurrentBoardCopy[2]=" "
            CurrentIndex=CurrentBoardCopy.index(CurrentItem)
            self.FirstExtraMarker=CurrentIndex-1
            self.SecondExtraMarker=CurrentIndex+1
    def start_usage(self):
        #Start screen usage.
        print("Display on")
        self.lcd.display_on()
        print("Background light on")
        self.lcd.backlight_on()
        #Display test Output
        self.lcd.putstr("Initiating display:" + "\n\n" + "Display functioning.")
        sleep_ms(3000)
    def end_usage(self):
        self.lcd.clear()
        self.lcd.putstr("Ended display usage.\nDisplay not functioning.")
        sleep_ms(1000)
        self.lcd.clear()
        sleep_ms(300)
        #End screen usage.
        print("Background light off")
        self.lcd.backlight_off()
        print("Display off")
        self.lcd.display_off()
    def GetLastCurrentNumberPosition(self):
        CurrentNumberLen=len(self.CurrentNumber)
        for CurrentNumIndex in range(CurrentNumberLen):
            CurrentInversedNumIndex=CurrentNumberLen-CurrentNumIndex-1
            if self.CurrentNumber[CurrentInversedNumIndex]!=" ":
                return CurrentInversedNumIndex
        return -1
    def Clicked(self):    
        #Failsafe to prevent crashes
        CurrentItems=self.NumberPadItems[self.Cursory]
        if self.Cursorx>(len(CurrentItems)-1):
            self.Cursorx=len(CurrentItems)-1
        ClickedItem=CurrentItems[self.Cursorx]
        LastBlockedIndex=self.GetLastCurrentNumberPosition()
        if ClickedItem=="EMPTY":
            return
        elif ClickedItem=="Enter":
            self.returnBool=True
            return
        elif ClickedItem=="Delete":
            if LastBlockedIndex==-1:
                return
            else:
                self.CurrentNumber[LastBlockedIndex]=" "
        else:
            if LastBlockedIndex==len(self.CurrentNumber)-1:
                return
            else:
                self.CurrentNumber[LastBlockedIndex+1]=ClickedItem

    #Credit to sage071920 on github for the lcd values
    #Modification to meet cursor expectation
    def handle_joystick_input(self):
        # Read analog values from the joystick
        x_value = self.joystick_x_pin.read_u16()
        y_value = self.joystick_y_pin.read_u16()
        print("x_value: "+str(x_value))
        print("y_value: "+str(y_value))
        
        # Determine joystick direction based on analog values
        # Add hysteresis to joystick input
        if y_value > 61000:
            if not self.Cursory==0:
                self.Cursory-=1
                CurrentListSize=len(self.NumberPadItems[self.Cursory])
                if  CurrentListSize <= self.Cursorx:
                    self.Cursorx=CurrentListSize-1
        elif y_value < 500:
            if not len(self.NumberPadItems)-1==self.Cursory:
                self.Cursory+=1
                CurrentListSize=len(self.NumberPadItems[self.Cursory])
                if  CurrentListSize <= self.Cursorx:
                    self.Cursorx=CurrentListSize-1
        if x_value > 61000:
            if not self.Cursorx==0:
                self.Cursorx-=1
            
        elif x_value < 500:
            if len(self.NumberPadItems[self.Cursory])-1<=self.Cursorx:
                self.Cursorx=len(self.NumberPadItems[self.Cursory])-1
            else:
                self.Cursorx+=1
        self.GetExtraMarkers()
        # Read the button state
        button_state = self.Button.value()
        if button_state==0:
            self.Clicked()
            print("Click")

    def ContinuosRequest(self):
        self.Cursory=0
        self.Cursorx=0
        self.CurrentNumber=[" "," "," "]
        self.returnBool=False
        while True:
            self.handle_joystick_input()
            self.printBoard()
            if self.returnBool:
                break
        CurrentStr=(self.CurrentNumber[0]+self.CurrentNumber[1]+self.CurrentNumber[2]).replace(" ","")
        if CurrentStr=="":
            return "EMPTY"
        else:
            return int(CurrentStr)
        
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
        #self.ResNumber=random.choices(self.RouletteNumbers,self.RouletteChances)
        self.ResNumber=random.choice(self.RouletteNumbers)

class RouletteOnPiPico():
    def __init__(self):
        self.Numpad=NumberField()
        self.rouletteTable=RouletteTable()
    def Bet_stake(self):
        ChipsList=[1,5,10,25,50,100,200,500]
        if self.rouletteTable.UserMoney==0:
            self.Numpad.lcd.clear()
            self.Numpad.lcd.putstr("You are out of credits. Leave and restart/ask the owner for more.")
            sys.exit()
        self.Numpad.lcd.clear()
        self.Numpad.lcd.putstr("You got "+str(self.rouletteTable.UserMoney)+" \ncredits. How much do you want to bet?")
        sleep_ms(2000)
        self.Numpad.lcd.clear()
        self.Numpad.lcd.putstr("You can bet chips of 1,5,10,25,50,100,    200 or 500.")
        sleep_ms(2000)    
        while True:
            #stake=(input().lower()).replace("credits","").replace(" ","").replace("c","")
            stake=self.Numpad.ContinuosRequest()
            try:
                stake=int(stake) 
            except:
                self.Numpad.lcd.clear()        
                self.Numpad.lcd.putstr("You didnt insert a number. \n Please enter a valid stake.")
                sleep_ms(2000)
                continue
            if stake not in ChipsList:
                self.Numpad.lcd.clear()        
                self.Numpad.lcd.putstr("You can only bet given chips. \n Please enter a valid stake.")
                sleep_ms(2000)
                continue
            if stake>self.rouletteTable.UserMoney:
                self.Numpad.lcd.clear()        
                self.Numpad.lcd.putstr("Thats more than you have! \n You only got "+str(self.rouletteTable.UserMoney)+" credits.")
                sleep_ms(2000)
                self.Numpad.lcd.clear()        
                self.Numpad.lcd.putstr("Due to safety       reasons, its        impossible for us to\n let you make debts.")

                sleep_ms(4000)
                self.Numpad.lcd.clear()        
                self.Numpad.lcd.putstr("Please enter a valid stake.")
                sleep_ms(2000)

            else:
                self.Numpad.lcd.clear()
                self.Numpad.lcd.putstr("There we go! "+str(stake)+"      credits are on the \n line.")
                self.rouletteTable.stake.append(stake)
                self.rouletteTable.UserMoney-=stake
                sleep_ms(2000)

                break
    def DisplayResult(self):
        self.Numpad.lcd.clear()        
        #self.Numpad.lcd.putstr("The ball landed on  the "+str(self.rouletteTable.ResNumber[0])+"!")
        self.Numpad.lcd.putstr("The ball landed on  the "+str(self.rouletteTable.ResNumber)+"!")
        sleep_ms(2000)

    def Bet_payout(self, WinningBet):        
        Win=self.rouletteTable.stake[WinningBet]*self.rouletteTable.Bet_PayoutList[self.rouletteTable.BetType[WinningBet]]
        self.Numpad.lcd.clear()        
        self.Numpad.lcd.putstr("Wow!  You won!       You get your stake  back plus "+str(Win)+ "      credits.")
        sleep_ms(4000)    
        self.rouletteTable.UserMoney+=Win
        self.rouletteTable.UserMoney+=self.rouletteTable.stake[WinningBet]
        self.rouletteTable.stake[WinningBet]=0
        self.rouletteTable.BetType[WinningBet]=0
        self.rouletteTable.Bet_WinningNumber_List[WinningBet]=[]
        self.rouletteTable.ResNumber=-1

    def Bet_LooseAllMessage(self):
        self.Numpad.lcd.clear()        
        sumOfLoose=0
        for loose in self.rouletteTable.stake: sumOfLoose+=loose
        self.Numpad.lcd.putstr("I'm sorry, you lost.\nAll your stake of\nentire "+str(sumOfLoose)+"\ncredits is gone.")
        sleep_ms(3000)
        self.rouletteTable.stake=[]
        self.rouletteTable.BetType=[]
        self.rouletteTable.Bet_WinningNumber_List=[]
        self.rouletteTable.ResNumber=-1
        self.Numpad.lcd.clear()
        self.Numpad.lcd.putstr("There are "+str(self.rouletteTable.UserMoney)+"\ncredits on your\naccount.")
        sleep_ms(2000)

    def Bet_PartialLostLeft(self):
        sumOfLoose=0
        for loose in self.rouletteTable.stake: 
            if loose!=[]: sumOfLoose+=loose
        self.Numpad.lcd.clear()
        self.Numpad.lcd.putstr("You won a bit and\nlost a bit.")
        sleep_ms(2000)
        self.Numpad.lcd.clear()
        self.Numpad.lcd.putstr("The leftover stakes\nof "+str(sumOfLoose)+" credits\n is gone.")
        sleep_ms(3000)
        self.rouletteTable.stake=[]
        self.rouletteTable.BetType=[]
        self.rouletteTable.Bet_WinningNumber_List=[]
        self.rouletteTable.ResNumber=-1
        self.Numpad.lcd.clear()
        self.Numpad.lcd.putstr("There are "+str(self.rouletteTable.UserMoney)+" credits\non your account.")
        sleep_ms(2000)

    def WinOrLoose(self):
        winCount=0
        for CurrentWinningNumbersIndex in range(len(self.rouletteTable.Bet_WinningNumber_List)):
            CurrentWinningNumbers=self.rouletteTable.Bet_WinningNumber_List[CurrentWinningNumbersIndex]
            #if self.rouletteTable.ResNumber[0] in CurrentWinningNumbers:
            if self.rouletteTable.ResNumber in CurrentWinningNumbers:
                self.Bet_payout(CurrentWinningNumbersIndex)
                winCount+=1
            
        if winCount==0:
            self.Bet_LooseAllMessage()
        elif winCount<len(self.rouletteTable.Bet_WinningNumber_List)-1:
            self.Bet_PartialLostLeft()
        else:
            self.rouletteTable.stake=[]
            self.rouletteTable.ResNumber=-1
            self.rouletteTable.Bet_WinningNumber_List=[]

    def Bet_ChooseAndStake_once(self):
        self.Bet_stake()
        while True:
            self.Numpad.lcd.clear()
            self.Numpad.lcd.putstr("Insert number \nbetween 1-151.")
            sleep_ms(2000)
            AccessNum=self.Numpad.ContinuosRequest()
            if AccessNum=="EMPTY":
                self.Numpad.lcd.clear()
                self.Numpad.lcd.putstr("Enter valid number\nplease. For more    information, seek the infographic.")
                sleep_ms(4000)
                continue
            if (AccessNum > 0 and AccessNum <=151):
                break
            else:
                self.Numpad.lcd.clear()
                self.Numpad.lcd.putstr("Enter valid number\nplease. For more\ninformation, seek \nthe infographic.")
                sleep_ms(4000)
        self.rouletteTable.BetAccess(AccessNum)
    
    def Bet_ChooseAndStake_multiple(self):
        while True:
            self.Bet_ChooseAndStake_once()
            if self.rouletteTable.UserMoney<1:
                self.Numpad.lcd.clear()
                self.Numpad.lcd.putstr("You bet all your\nmoney. Let the game\nbegin!")
                sleep_ms(2000)
                break
            else:
                self.Numpad.lcd.clear()
                self.Numpad.lcd.putstr("Do you want to set  another chip?       (enter number=yes)  (enter empty=no)")
                sleep_ms(3000)
                again=self.Numpad.ContinuosRequest()
                if again=="EMPTY":
                    break
        
    def PlayAgain(self):
        self.Numpad.lcd.clear()
        self.Numpad.lcd.putstr("Do you want to play another round?      (enter number=yes)  (enter empty=no)")
        sleep_ms(3000)
        again=self.Numpad.ContinuosRequest()
        if again=="EMPTY":
            self.Numpad.lcd.clear()
            self.Numpad.lcd.putstr("You exit the casino.\nYou have "+str(self.rouletteTable.UserMoney)+" credits.\nProgramm ends here.")
            sleep_ms(2500)
            sys.exit()
        else:
            return

    def KeepPlaying(self):
        while True:
            self.Bet_ChooseAndStake_multiple()
            self.rouletteTable.TurnTheTable()
            self.DisplayResult()
            self.WinOrLoose()
            self.PlayAgain()

newTable=RouletteOnPiPico()
newTable.KeepPlaying()