"""
如果执行失败，请将此文件复制到backend目录再次执行。
"""
import time
import peewee
from model import db
from model._post import POST_STATE
from model.comment import Comment
from model.user import User, USER_GROUP
from model.notif import UserNotifLastInfo


def sql_execute(sql):
    try:
        db.execute_sql(sql)
    except Exception as e:
        print(e)
        print('failed: %s' % sql)
        db.rollback()


def work():
    sql_execute('drop table "wiki_history";')
    sql_execute('drop table "wiki_item";')
    sql_execute('drop table "wiki_article";')
    sql_execute('drop table "statistic24h";')
    sql_execute('drop table "statistic24h_log";')
    sql_execute('ALTER TABLE statistic RENAME TO post_stats;')
    sql_execute('ALTER TABLE post_stats ADD edit_count int DEFAULT 0 NULL;')
    sql_execute('ALTER TABLE post_stats DROP viewed_users;')
    sql_execute('ALTER TABLE post_stats DROP edited_users;')
    sql_execute('ALTER TABLE post_stats DROP commented_users;')
    sql_execute('ALTER TABLE post_stats DROP bookmarked_users;')
    sql_execute('ALTER TABLE post_stats DROP upvoted_users;')
    sql_execute('ALTER TABLE post_stats DROP downvoted_users;')
    sql_execute('ALTER TABLE post_stats DROP thanked_users;')
    sql_execute('ALTER TABLE post_stats ADD last_edit_time bigint DEFAULT NULL NULL;')
    sql_execute('ALTER TABLE post_stats ADD last_edit_user_id BYTEA DEFAULT NULL NULL;')
    sql_execute('CREATE INDEX post_stats_last_edit_time_index ON post_stats (last_edit_time);')


if __name__ == '__main__':
    work()
    print('done')
