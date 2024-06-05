#############################################################
# FILE: hangman.py
# WRITER: Amir Rosengarten, amir.rosen15, 207942285
# EXERCISE: intro2cs2 ex4 2022
# DESCRIPTION: A program that runs the game 'hangman'
#############################################################


from hangman_helper import *

"""defining global variables"""

MESSAGE_ERROR = 'the input is incorrect'
MESSAGE_ALREADY_SELECTED = 'the letter is already selected'
MESSAGE_GOOD_LETTER = 'good choice'
MESSAGE_WRONG_LETTER = 'wrong guess'
MESSAGE_LOST = 'you lost. the word was '
MESSAGE_WINNER = 'great job! you won'
MESSAGE_TO_USER = 'number of games: {}. your score is {}. do you want to' \
                  ' play again?'


def update_word_pattern(word, pattern, letter):

    """
    the function accepts as parameters the word, the current pattern and
     a letter, and returns an updated pattern containing the same letter.
    :param word: a word
    :param pattern: a pattern
    :param letter: a letter
    :return: update pattern
    """

    if letter not in word:
        return pattern
    lst_word = list(word)
    lst_pattern = list(pattern)
    for i in range(len(lst_word)):
        if lst_word[i] == letter:
            lst_pattern[i] = letter
        pattern = ''.join(lst_pattern)
    return str(pattern)


def letter(value, wrong_lst, pattern_of_word, the_chosen_word, score):

    """
    the function is called in case the player has entered a letter.
    :param value: a letter
    :param wrong_lst: a list of the bad guesses
    :param pattern_of_word: the pattern
    :param the_chosen_word: the word selected by the program
    :param score: the number of points of the player
    :return: the function returns to the user a corresponding message,
     the updated pattern of the word, and the updated number of points
    """

    # check the correctness of the letter#
    if len(value) > 1 or not (value.encode().isalpha()) or value.isupper():
        msg = MESSAGE_ERROR
    elif value in wrong_lst or value in pattern_of_word:
        msg = MESSAGE_ALREADY_SELECTED
    # performs the required actions, and updates the player's number of
    # points accordingly
    elif value in the_chosen_word:
        score -= 1
        # call to function 'pattern_of_word'
        pattern_of_word = update_word_pattern(the_chosen_word,
                                              pattern_of_word,
                                              value)
        n = the_chosen_word.count(value)
        score += (n * (n + 1)) // 2
        msg = MESSAGE_GOOD_LETTER
    else:
        score -= 1
        wrong_lst.append(value)
        if score != 0:
            msg = MESSAGE_WRONG_LETTER
        else:
            msg = MESSAGE_LOST + the_chosen_word
    return msg, pattern_of_word, score


def word(value, the_chosen_word, pattern_of_word, score):

    """
    the function is called in case the player has entered a word
    :param value: a word
    :param the_chosen_word: the word selected by the program
    :param pattern_of_word: the pattern
    :param score: the number of points of the player
    :return: the function returns to the user a corresponding message,
     the updated pattern of the word, and the updated number of points
    """

    if value != the_chosen_word:
        score -= 1
        if score != 0:
            msg = MESSAGE_WRONG_LETTER
        else:
            msg = MESSAGE_LOST + the_chosen_word
    else:
        score -= 1
        count = 0
        for i in pattern_of_word:
            if i == '_':
                count += 1
        score += (count * (count + 1)) // 2
        pattern_of_word = the_chosen_word
        msg = MESSAGE_WINNER
    return msg, pattern_of_word, score


def filter_words_list(words, pattern, wrong_guess_lst):

    """
    the function receives as input a list of words, pattern and list of
     incorrect guesses.
    :param words: list of words
    :param pattern: the pattern
    :param wrong_guess_lst: a list of the bad guesses
    :return: the function returns a new list that contains only the words
     in the input list that can match the previous format and guesses
    """

    filter_lst = []
    for word_1 in words:
        if len(word_1) != len(pattern):
            continue
        is_okey = True
        for i in range(len(pattern)):
            if pattern[i] != '_' and pattern[i] != word_1[i]:
                is_okey = False
            elif pattern[i] == '_' and word_1[i] in pattern:
                is_okey = False
            elif word_1[i] in wrong_guess_lst:
                is_okey = False
        if is_okey:
            filter_lst.append(word_1)
    return filter_lst


def shorter_lst(filter_word_lst, len_lst):

    """
    the function gets a filtered list of words, and the length of the list
    :param filter_word_lst: filtered word list
    :param len_lst: the length of the list
    :return: the function checks if the length of the list of filtered
     words is greater than the set variable value, and if so, then it
      takes from it a sub-list according to the requirements
    """

    min_lst = []
    len_of_hint = HINT_LENGTH
    if len(filter_word_lst) < len_of_hint:
        return filter_word_lst
    else:
        for i in range(0, len_of_hint):
            min_lst.append(filter_word_lst[(i*len_lst)//len_of_hint])
    return min_lst


def hint(score, words_list, pattern_of_word, wrong_lst, the_chosen_word):

    """
    the function is called in case the player asks for a hint. it receives
     the appropriate parameters, and performs actions to check what hint
      to give the player, if he can get a hint.
    :param score: the number of points of the player
    :param words_list: a list of words
    :param pattern_of_word: the pattern
    :param wrong_lst: a list of the bad guesses
    :param the_chosen_word: the word selected by the program
    :return: the function returns a message accordingly, and the number
     of points of the player.
    """

    score -= 1
    # Call to function filter_words_list#
    filter_lst = filter_words_list(words_list, pattern_of_word, wrong_lst)
    # Call the function shorten_lst#
    min_lst = shorter_lst(filter_lst, len(filter_lst))
    msg = ''
    if score != 0:
        show_suggestions(min_lst)
    else:
        show_suggestions(min_lst)
        msg = MESSAGE_LOST + the_chosen_word
    return score, msg


def run_single_game(words_list, score):

    """
    the function gets a list of words, and the number of points of the
     player. the function runs the game, and performs actions according
      to the player's choices.
    :param words_list: list of words
    :param score: the number of points of the player
    :return: the function returns at the end of the game the updated
     number of points of the player
    """

    # the lottery word
    the_chosen_word = get_random_word(words_list)
    # create the pattern of the word
    pattern_of_word = '_' * len(the_chosen_word)
    wrong_lst = []
    msg = ''
    # call the function display_state
    display_state(pattern='_' * len(the_chosen_word),
                  wrong_guess_lst=wrong_lst, points=score,
                  msg='let\'s play hangman')
    # the game will continue as long as the player's number of points is
    # not reset, or the player has not yet guessed the whole word
    while 0 < score and pattern_of_word != the_chosen_word:
        # call the function get_input
        kind_of_type, value = get_input()
        # in case the player guessed a letter
        if kind_of_type == LETTER:
            msg, pattern_of_word, score = letter(value, wrong_lst,
                                                 pattern_of_word,
                                                 the_chosen_word, score)
            # in case the player guessed a word
        elif kind_of_type == WORD:
            msg, pattern_of_word, score = word(value, the_chosen_word,
                                               pattern_of_word, score)
            # in case the player asks for a hint
        elif kind_of_type == HINT:
            score, msg = hint(score, words_list, pattern_of_word,
                              wrong_lst, the_chosen_word)
        display_state(pattern_of_word, wrong_lst, score, msg)
    return score


def main():

    """
    the function does not accept or return values and performs a series of
     operations
    """

    # upload a word file to a list
    lst_of_words = load_words()
    game_count = 0
    points = POINTS_INITIAL
    while True:
        points = run_single_game(lst_of_words, points)
        game_count += 1
        if points > 0:
            msg_to_user = MESSAGE_TO_USER.format(game_count, points)
            if not play_again(msg_to_user):
                break
        else:
            msg_to_user = MESSAGE_TO_USER.format(game_count, points)
            if play_again(msg_to_user):
                game_count = 0
                points = POINTS_INITIAL
            else:
                break


if __name__ == '__main__':
    main()
