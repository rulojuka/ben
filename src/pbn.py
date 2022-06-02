import datetime

import deck52

from collections import deque
from typing import NamedTuple


class Deal(NamedTuple):
    dealer: str
    vulnerable: str
    hands: str

def random_pbn_generator(n_boards=32):
    dealer = list('NESW')
    vuln = deque(['None', 'NS', 'EW', 'Both'])

    def print_deal(board_number, dlr, vul, deal):
        print('[Event "?"]')
        print('[Site "?"]')
        print(f'[Date "{datetime.datetime.now().date().isoformat()}"]')
        print(f'[Board "{board_number}"]')
        print('[West "?"]')
        print('[North "?"]')
        print('[East "?"]')
        print('[South "?"]')
        print('[Scoring "IMP"]')
        print(f'[Dealer "{dlr}"]')
        print(f'[Vulnerable "{vul}"]')
        print(f'[Deal "{deal}"]')
        print('[Declarer "?"]')
        print('[Result "?"]\n')

    def vuln_swap(vul):
        if vul == 'NS':
            return 'EW'
        if vul == 'EW':
            return 'NS'
        return vul

    for i in range(n_boards):
        deal_str = deck52.random_deal()
        
        if i % 4 == 0 and i > 0:
            vuln.append(vuln.popleft())
    
        print_deal(i + 1, dealer[i % 4], vuln[i % 4], f'N:{deal_str}')
        print_deal(i + 1, dealer[(i + 1) % 4], vuln_swap(vuln[i % 4]), f'E:{deal_str}')
        

def load(fin):
    dealer, vulnerable = None, None

    for line in fin:
        if line.startswith('[Dealer'):
            dealer = extract_value(line)
        elif line.startswith('[Vulnerable'):
            vuln_str = extract_value(line)
            vulnerable = {'NS': 'N-S', 'EW': 'E-W', 'All': 'Both'}.get(vuln_str, vuln_str)
        elif line.startswith('[Deal'):
            hands_pbn = extract_value(line)
            [seat, hands] = hands_pbn.split(':')
            hands_nesw = [''] * 4
            first_i = 'NESW'.index(seat)
            for hand_i, hand in enumerate(hands.split()):
                hands_nesw[(first_i + hand_i) % 4] = hand
            
            yield Deal(dealer, vulnerable, ' '.join(hands_nesw))
        else:
            continue

def extract_value(s: str) -> str:
    return s[s.index('"') + 1 : s.rindex('"')]


if __name__ == '__main__':
    random_pbn_generator(32)
