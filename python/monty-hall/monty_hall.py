import random


class MontyHall:

    def __init__(self):
        pass

    def is_won(self, action='stay'):
        doors = [1, 2, 3]

        hit = random.choice(doors)
        choice = random.choice(doors)

        if action == 'stay':
            return choice == hit

        # delete one unchosen "miss" door
        delete = random.choice(list(set(doors) - set([choice, hit])))

        # move: check if the unchosen remaining door is "hit"?
        return list(set(doors) - set([choice, delete]))[0] == hit

    def simulate(self, n=10000):
        n_win_stay = sum([self.is_won('stay') for i in range(n)])
        p_win_stay = n_win_stay / n

        return p_win_stay, 1 - p_win_stay


if __name__ == '__main__':
    p_win_stay, p_win_move = MontyHall().simulate(10000)
    print(p_win_stay, p_win_move)
