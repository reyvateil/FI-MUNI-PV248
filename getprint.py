import sqlite3
import argparse

def get_composers_by_print(print_id):
    conn = sqlite3.connect("scorelib.sqlite")
    cur = conn.cursor()
    res = cur.execute("SELECT print.id as print_id, person.name as composer_name \
                       FROM print \
                       JOIN edition ON print.edition = edition.id \
                       JOIN score ON edition.score = score.id \
                       JOIN score_author ON score.id = score_author.score \
                       JOIN person ON person.id = score_author.composer \
                       WHERE print.id = ?;", (print_id, ))

    for item in res:
        print("Print no. {} was composed by: {}".format(item[0], item[1]))

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("print_id", help="display all composers for given print ID")
    args = parser.parse_args()
    get_composers_by_print(args.print_id)
