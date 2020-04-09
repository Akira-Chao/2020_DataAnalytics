import random


def kruskal_card_game(card_decks, face_card_step):
    card_list = [i for i in range(1,11)] + ["J", "Q", "K"]
    total_cards = card_list * 2 * card_decks
    random.shuffle(total_cards)
    real_total_cards = []
    for i, j in enumerate(total_cards):
        if j == "J" or j == "Q" or j == "K":
            j = face_card_step
        real_total_cards.append(int(j))
    hello_message = "========= Welcome to Ricardo's Kruskal Card Game!!! ========="
    print(hello_message)
    print("Face Cards's Step is: ", face_card_step)
    chosen_string = "cards: \n"
    for i, j in enumerate(total_cards[0:10]):
        chosen_string += str(i+1) + ". " +  str(j) + "\n"
    print(chosen_string)
    print()
    chosen_index = int(input('Please enter the index of the card you want to start with: ')) - 1
    chosen_card = real_total_cards[chosen_index]
    print("=============================================================")
    print("The card chosen by you is: ", total_cards[chosen_index])
    print("The total card deck: ", total_cards)
    while True:
        if chosen_index + chosen_card < len(total_cards):
            chosen_index = chosen_index + chosen_card
            chosen_card = real_total_cards[chosen_index]
            print("Your next card is: ", total_cards[chosen_index])
        else:
            ending_message = "========= Game Ended ========="
            while True:
                if len(ending_message) < len(hello_message):
                    ending_message += "="
                else:
                    break
            print(ending_message)
            print("Your ending card is:", total_cards[chosen_index], "\n\n\n")
            break


if __name__ == '__main__':
    card_decks = 2
    face_card_step = 3
    kruskal_card_game(card_decks, face_card_step)