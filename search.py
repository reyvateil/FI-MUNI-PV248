import sqlite3, json, pprint
from collections import defaultdict

def get_composers_and_scores_by_name(name):
    conn = sqlite3.connect("scorelib.sqlite")
    cur = conn.cursor()
    res = cur.execute("SELECT person.name, score.title as composer_name \
                       FROM person \
                       JOIN score_author ON score_author.composer = person.id \
                       JOIN score ON score.id = score_author.score \
                       WHERE person.name LIKE ?", (name,))

    data = defaultdict(list)
    for item in res:
        data[item[0]].append(item[1])

    print(json.dumps(data, ensure_ascii=False))


if __name__=='__main__':
    get_composers_and_scores_by_name("%Johann%")
