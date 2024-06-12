#Librerie

import time
import random
import colorama
from colorama import Fore, Style

#Comandi:

def generate_deck(seeds: list, values: list):

    """
    This function generates a list made of every combination of the items in the argument lists in the given order.
    """
    deck = []
    for seed in seeds:
        for value in values:
            card = {"seed":seed,"value": value}
            deck.append(card) 
    return deck

def find_card_value(card):
    if card['value'] in [10,"K","J","Q"]:
        return 10
    elif card['value'] in ["A"]: 
        return 11 #conversion to 1 in line 47
    else:
        return card['value']

def shuffle_deck(deck):
    for i in range(random.randint(10,15)):
        random.shuffle(deck) #just shuffles the deck 10 to 15 times

def sum_values(hand: list):
    """
    returns hand score
    """
    points=0
    num_aces=0
    for card in hand:
        values=find_card_value(card)
        if values==11:
            num_aces+=1
        points+=values #add every card to points
    for i in range(num_aces):
        if points>21: 
            points-=10 #for every ace remove 10 points if needed
    return points

def color_text(text, color):
    colors = {
        'nero': Fore.BLACK,
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE
    }
    return f"{colors.get(color, Fore.RESET)}{text}{Style.RESET_ALL}" #view colorama

def ask_int(phrase: str, error_phrase="0"):
    """
    returns the value requested from the argument as an integer. If not an integer, reasks for the value with the sentence in the sencond argument or a default sentence.
    """
    is_int=True
    while is_int:
        try:
            num=int(input(phrase))
            is_int=False
        except ValueError:
            if error_phrase=="0":
                print(color_text("Error, please insert an integer!!!", "red"))
            else:
                print(color_text(error_phrase, "red"))
    return num 

def add_info(dict: dict, keys: list, values: list ):
    """
    adds to the dict in the first argument as many keys as the elements in the second argument, then associates to every key a value in the third argument. Note: the second and third argumente must have the ame length.
    """
    if len(keys)==len(values):
        p=0
        for i in keys:
            dict[keys[p]]=values[p]
            p+=1
        return dict
    else: 
        print("Go check your code! keys and values must have the same length.")
        exit()

colorama.init(autoreset=True) #starts colorama

#Deck

deck = random.randint(1,8)*generate_deck([color_text("♥", "red"), color_text("♦", "red"), "♣", "♠"],[2, 3, 4, 5, 6, 7, 8, 9, 10, "K", "J", "Q", "A"]) #4 decks are generated
shuffle_deck(deck)

#Start

print("Welcome to Leo and Giuseppe's BlackJack. ")
nplayers=int(ask_int("How many players? "))

#Info + hands
pplayers = 1 #Needed in sentences
players=[]
names=[]
wealths=[] #names and whealths will be attached to players

for i in range(nplayers):
    name=str(input(f"Insert player {pplayers}'s name: "))
    names.append(name)
    wealth=ask_int(f"Insert player {pplayers}'s whealth: ")
    wealths.append(wealth)
    player = {"name": names[pplayers-1], "wealth": wealths[pplayers-1]} #players are dicts. Further information will be added forward in the code
    players.append(player)
    pplayers+=1

#the part above is only executed before the first game

while True: #this part is repeated as long as there are players
    pplayers=1 #for the sentences
    for player in players:
        bet=ask_int(f"insert {player['name']}'s bet: ")
        while bet<=0 or bet>player['wealth']:
            bet=ask_int(color_text("Invalid bet.", "red"), (f"Please {player['name']}, insert a new one: ")) #bet must be positive and lower than wealth

        
        player_hand=[] #creazione della hand
        card1=random.choice(deck)
        deck.remove(card1)
        card2=random.choice(deck)
        deck.remove(card2)
        player_hand.append(card1)
        player_hand.append(card2)
        bust=False #da inserire nel player
        score=sum_values(player_hand)
        blackjack=False #da inserire nel player
        infolist_keys=['hand', 'bet', 'score', 'bust', 'blackjack']
        infolist_values=[player_hand, bet, score, bust, blackjack]
        add_info(player, infolist_keys, infolist_values) #take a look at line 80
        pplayers+=1

        #the part above creates the player's hand, calculates the score adds information about every player
    
    print("Dealer deals the cards...")

    time.sleep(2)

    for player in players:
        player_hand=player["hand"] #needed to update the cards for every player
        player['score']=sum_values(player_hand) #needed to update the score for every player
        cards_print=" ".join([f"{card['value']} {card['seed']}" for card in player_hand]) #player's cards separated by spaces
        if player['score']==21:
            player['blackjack']=True #sets blackjack to True if the score is 21
        print(f"{player['name']}'s bet is {player['bet']}, while his cards are {cards_print}. Score: {player['score']}")

    #dealer creation

    time.sleep(2)

    dealerhand=[]
    dealer_score=sum_values(dealerhand)
    dealerbust=False
    carddealer1=random.choice(deck)
    deck.remove(carddealer1)
    carddealer2 = random.choice(deck)
    deck.remove(carddealer2)
    dealerhand.append(carddealer1)
    dealerhand.append(carddealer2)
    dealer={"hand": dealerhand, "bust": dealerbust, "score": dealer_score}
    print(f"Dealer's first card is {carddealer1['value']} {carddealer1['seed']}")

    #Game

    for player in players:
        player_hand=list(player['hand']) #needed to update cards
        if player['blackjack']==True:
            print(f"Congrats {player['name']}, you made BlackJack! Press enter ")
            input()
        else:
            while player['score']<=21: #until player is busted
                cardyesno=str(input(f"{player['name']}, do  you hit? y/n: ")) #sort of a boolean
                while True: #double cycle required for correct reiteration
                    if cardyesno=="y":
                        cardplus=random.choice(deck)
                        deck.remove(cardplus)
                        player_hand.append(cardplus)
                        cards_print=" ".join([f"{card['value']} {card['seed']}" for card in player_hand])
                        player['score']=sum_values(player_hand)
                        print(f"{player['name']}'s new card is {cardplus['value']} {cardplus['seed']}, his hand {cards_print} and his score {player['score']}")
                        print("\n")
                        break
                        # adds a card to the hand and asks if score is less than 21 again
                    elif cardyesno=="n":
                        cards_print=" ".join([f"{card['value']} {card['seed']}" for card in player_hand])
                        player['score']=sum_values(player_hand)
                        print(f"{player['name']} stands. Cards: {cards_print}, score: {player['score']}")
                        print("\n")
                        break
                        # prints hand and ends the cycle
                    else:
                        cardyesno=str(input(f"{player['name']}, only answer \"y\" o \"n\"! "))
                        print("\n")
                if cardyesno=="n":
                    break
            else:
                player['bust']=True
                print(f"{player['name']}, you busted!")
                print("\n")
                #if player busts cycle ends

    #dealer game

    print("dealers turn!")

    time.sleep(1)
    
    dealer['score']=sum_values(dealerhand)
    cardsdealer_print=" ".join([f"{card['value']} {card['seed']}" for card in dealerhand]) #view line 149
    if any(player['bust']==False for player in players): #if at least a player didn't bust
        print(f"Cruopier reveals his cards: {cardsdealer_print}. Score: {dealer['score']}")
        while dealer['score']<17: #dealer has 2 rules: score<17: hit, score>=17: stand
            carddealerplus=random.choice(deck)
            deck.remove(carddealerplus)
            dealerhand.append(carddealerplus)
            dealer['score']=sum_values(dealerhand) #add a card to dealer
        if len(dealerhand)>2: #if dealer hit
            dealer['score']=sum_values(dealerhand)
            cardsdealer_print=" ".join([f"{card['value']} {card['seed']}" for card in dealerhand])
            print("Il dealer pesca...", end=" ")
            time.sleep(1)
            for card in dealerhand[2:len(dealerhand)+1]:
                print(" ".join([f"{card['value']} {card['seed']}"]))
                time.sleep(0.8)
            #shows the dealer hitting in a way that seems a tomfoolery to make but I spent hours making it so appreciate (it isn't even how I wanted it)
            print(f"dealer's hand is now {cardsdealer_print}. Score: {dealer['score']}") #shows dealer's hand
            if dealer['score']>21:
                dealer["bust"]=True
                print("Dealer busted. Everyone still in game wins") #if dealer busts everyone that hasn't busted wins
    else:
        print("Every player busted. All bets lost.") #se tutti hanno sballato

    time.sleep(1)

    #Money🤑🤑

    if dealer['bust']==False:
        for player in players:
            if player['bust']==False:
                if player['blackjack']==False:
                    if player['score']>dealer['score']:
                        player['wealth']+=player['bet']
                        print(f"{player['name']}, ", color_text("you won! ", "green"), f"You get {player['bet']}$. Your wealth is now {player['wealth']}$")
                    else:
                        player['wealth']-=player['bet']
                        print(f"{player['name']}, ", color_text("you lost. ", "red"), f"You pay {player['bet']}$. Your wealth is now {player['wealth']}$")
                else:
                    player['wealth']+=player['bet']*1.5
                    print(f"{player['name']}, ", color_text("you won with BlackJack! ", "green"), f"You get {player['bet']*1.5}$. Your wealth is now {player['wealth']}$")
            else:
                player['wealth']-=player['bet']
                print(f"{player['name']}, ", color_text("you lost. ", "red"), f"You pay {player['bet']}$. Your wealth is now {player['wealth']}$")
    else:
        for player in players:
            if player['bust']==False and player['blackjack']==True:
                player['wealth']+=player['bet']*1.5
                print(f"{player['name']}, ", color_text("you won with BlackJack! ", "green"), f"You get {player['bet']*1.5}$. Your wealth is now {player['wealth']}$")
            elif player['bust']==False and player['blackjack']==False:
                player['wealth']+=player['bet']
                print(f"{player['name']}, ", color_text("you won! ", "green"), f"You get {player['bet']}$. Your wealth is now {player['wealth']}$")
            elif player['bust']==True:
                player['wealth']-=player['bet']
                print(f"{player['name']}, ", color_text("you lost. ", "red"), f"You pay {player['bet']}$. Your wealth is now {player['wealth']}$")
    #if you don't understand go read BlackJack's rules

    #reset 

    for player in players:
        del player['hand']
        player['bust']=False
        player['blackjack']=False

    #debt expulsion

    removed_players=[player for player in players if player['wealth']<=0]
    for player in removed_players:
        players.remove(player)
        nplayers-=1
        print(f"{player['name']} has no other money and his ass is getting expelled. Your kids won't eat this evening, and it's YOUR FAULT, you gambling addict.")
    #expels those gambling addicts that finish their money

    #exits

    exited_players=[]
    for player in players:
        Continue=str(input(f"{player['name']}, do you stay in? y/n: "))
        while True:
            if Continue=="n":
                exited_players.append(player)
                print(f"{player['name']} exits. Definitely not a wise choice, because 99% of gamblers quit exactly before winning.")
                break
            elif Continue=="y":
                None
                break
            else:
                Continue=str(input(f"{player['name']}, only answer \"y\" o \"n\"! ")) #the cycle is just like the one for the cards
    for player in exited_players:
        players.remove(player)
        nplayers-=1
    #who exits is a lil slow, look at what line 304 says

    #nuovi

    pplayers=1
    numnewplayers=ask_int("How many new players? ")
    nplayers+=numnewplayers
    newplayers=[]
    newnames=[]
    newwealths=[]
    for i in range(numnewplayers):
        newname=str(input(f"Insert new player{pplayers}'s name: "))
        newnames.append(newname)
        newwealth=ask_int(f"Insert new player{pplayers}'s wealth: ")
        newwealths.append(newwealth)
        newplayer={'name': newnames[pplayers-1], 'wealth': newwealths[pplayers-1]}
        newplayers.append(newplayer)
    players+=newplayers
    #welcomes with open arms who wants to spend his fortune

    if nplayers==0:
        print("No players remaining. Game ended")
        break
    #if everyone quits the game closes

input()

"""
Code by Bacuz
"""





