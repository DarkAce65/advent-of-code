from collections import Counter
from enum import Enum
from functools import cmp_to_key

from utils import get_and_cache_input


class HandRank(Enum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


def is_five_of_a_kind(cards: Counter[str]) -> bool:
    return max(cards.values()) == 5


def is_four_of_a_kind(cards: Counter[str]) -> bool:
    return max(cards.values()) == 4


def is_full_house(cards: Counter[str]) -> bool:
    return max(cards.values()) == 3 and min(cards.values()) == 2


def is_three_of_a_kind(cards: Counter[str]) -> bool:
    return max(cards.values()) == 3


def is_two_pair(cards: Counter[str]) -> bool:
    return (
        max(cards.values()) == 2 and sum(1 for value in cards.values() if value == 2) == 2
    )


def is_one_pair(cards: Counter[str]) -> bool:
    return (
        max(cards.values()) == 2 and sum(1 for value in cards.values() if value == 2) == 1
    )


def get_hand_rank(cards: str) -> HandRank:
    card_counts = Counter(cards)
    if is_five_of_a_kind(card_counts):
        return HandRank.FIVE_OF_A_KIND
    elif is_four_of_a_kind(card_counts):
        return HandRank.FOUR_OF_A_KIND
    elif is_full_house(card_counts):
        return HandRank.FULL_HOUSE
    elif is_three_of_a_kind(card_counts):
        return HandRank.THREE_OF_A_KIND
    elif is_two_pair(card_counts):
        return HandRank.TWO_PAIR
    elif is_one_pair(card_counts):
        return HandRank.ONE_PAIR
    return HandRank.HIGH_CARD


def get_hand_rank_with_jokers(cards: str) -> HandRank:
    card_counts = Counter(cards)
    num_jokers = card_counts["J"]
    del card_counts["J"]

    if num_jokers == 5:
        return HandRank.FIVE_OF_A_KIND

    if is_five_of_a_kind(card_counts):
        return HandRank.FIVE_OF_A_KIND
    elif is_four_of_a_kind(card_counts):
        if num_jokers == 1:
            return HandRank.FIVE_OF_A_KIND
        return HandRank.FOUR_OF_A_KIND
    elif is_full_house(card_counts):
        return HandRank.FULL_HOUSE
    elif is_three_of_a_kind(card_counts):
        if num_jokers == 2:
            return HandRank.FIVE_OF_A_KIND
        elif num_jokers == 1:
            return HandRank.FOUR_OF_A_KIND
        return HandRank.THREE_OF_A_KIND
    elif is_two_pair(card_counts):
        if num_jokers == 1:
            return HandRank.FULL_HOUSE
        return HandRank.TWO_PAIR
    elif is_one_pair(card_counts):
        if num_jokers == 3:
            return HandRank.FIVE_OF_A_KIND
        elif num_jokers == 2:
            return HandRank.FOUR_OF_A_KIND
        elif num_jokers == 1:
            return HandRank.THREE_OF_A_KIND
        return HandRank.ONE_PAIR

    if num_jokers == 4:
        return HandRank.FIVE_OF_A_KIND
    elif num_jokers == 3:
        return HandRank.FOUR_OF_A_KIND
    elif num_jokers == 2:
        return HandRank.THREE_OF_A_KIND
    elif num_jokers == 1:
        return HandRank.ONE_PAIR
    return HandRank.HIGH_CARD


ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
ranks_with_joker = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


def compare_hands(first: str, second: str) -> int:
    first_hand_rank = get_hand_rank(first)
    second_hand_rank = get_hand_rank(second)
    if first_hand_rank != second_hand_rank:
        return first_hand_rank.value - second_hand_rank.value

    for f, s in zip(first, second):
        diff = ranks.index(f) - ranks.index(s)
        if diff != 0:
            return diff

    return 0


def compare_hands_with_jokers(first: str, second: str) -> int:
    first_hand_rank = get_hand_rank_with_jokers(first)
    second_hand_rank = get_hand_rank_with_jokers(second)
    if first_hand_rank != second_hand_rank:
        return first_hand_rank.value - second_hand_rank.value

    for f, s in zip(first, second):
        diff = ranks_with_joker.index(f) - ranks_with_joker.index(s)
        if diff != 0:
            return diff

    return 0


def part_one(problem_input: list[str]) -> int:
    hands: list[tuple[str, int]] = []
    for line in problem_input:
        hand, bet = line.split()
        hands.append((hand, int(bet)))

    key = cmp_to_key(compare_hands)
    ordered_hands = sorted(hands, key=lambda h: key(h[0]))

    return sum(bet * (index + 1) for (index, (_, bet)) in enumerate(ordered_hands))


def part_two(problem_input: list[str]) -> int:
    hands: list[tuple[str, int]] = []
    for line in problem_input:
        hand, bet = line.split()
        hands.append((hand, int(bet)))

    key = cmp_to_key(compare_hands_with_jokers)
    ordered_hands = sorted(hands, key=lambda h: key(h[0]))

    return sum(bet * (index + 1) for (index, (_, bet)) in enumerate(ordered_hands))


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
