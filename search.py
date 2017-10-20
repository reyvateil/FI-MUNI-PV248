import sqlite3

def get_composers_and_scores_by_name(name):
    conn = sqlite3.connect("scorelib.sqlite")
    cur = conn.cursor()
    res = cur.execute("SELECT person.name, score.title as composer_name \
                       FROM person \
                       JOIN score_author ON score_author.composer = person.id \
                       JOIN score ON score.id = score_author.score \
                       WHERE person.name LIKE ?", (name,))
    for item in res:
        print("{} -- {}".format(item[0], item[1]))

if __name__=='__main__':
    get_composers_and_scores_by_name("%Johann%")
