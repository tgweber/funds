from funds.portfolio import Portfolio


def simple_sim(fund1, fund2):
    p = Portfolio()
    p.add_position(fund1, 1)
    p.add_position(fund2, 1)
    return len(p.shared_assets) / len(p.assets)


def simple_diff(fund1, fund2):
    return 1 - simple_sim(fund1, fund2)
