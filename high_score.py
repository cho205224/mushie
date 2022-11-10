def get_high_score():
    with open('high_score', 'r') as f:
        hs = f.readline()
        return int(hs)


def write_high_score(score):
    with open('high_score', 'w') as f:
        f.write(score)
        return
