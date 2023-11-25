"""Import sqlite3 : used to manage our database"""
import sqlite3
from datetime import date
from string import Template
import uuid

connection = sqlite3.connect("db_video_platform.db", check_same_thread=False)

cursor = connection.cursor()

# --------------------------------------------
# --------------Table definition--------------
# --------------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS account (
    uuid_account TEXT,
    name_account varchar(25) NOT NULL,
    mail_account varchar(50) NOT NULL,
    password_account TEXT NOT NULL,
    file_picture TEXT NOT NULL,
    date DATE NOT NULL,
    banner_picture TEXT NOT NULL,
    banned INT NOT NULL,
    admin INT NOT NULL,
    about TEXT)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS videos(
    uuid_video TEXT NOT NULL,
    file_video TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    uuid_sender TEXT NOT NULL,
    views INT NOT NULL,
    likes INT NOT NULL,
    file_minia TEXT NOT NULL,
    date DATE NOT NULL,
    dislike INT NOT NULL,
    visibility INT NOT NULL)"""
               )

cursor.execute("""
CREATE TABLE IF NOT EXISTS follows (
    uuid_follower TEXT NOT NULL,
    uuid_followed TEXT NOT NULL)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS likes (
    uuid_liker TEXT NOT NULL,
    uuid_video TEXT NOT NULL)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS dislikes (
    uuid_disliker TEXT NOT NULL,
    uuid_video TEXT NOT NULL)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS comments (
    uuid_comment TEXT NOT NULL,
    uuid_uploader TEXT NOT NULL,
    uuid_video TEXT NOT NULL,
    content TEXT NOT NULL,
    date DATE NOT NULL)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS errors (
    date DATE NOT NULL,
    error TEXT NOT NULL)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS account_reports (
    uuid_report TEXT NOT NULL,
    date DATE NOT NULL,
    uuid_account TEXT NOT NULL,
    reason TEXT NOT NULL,
    more_infos TEXT)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS handled_account_reports (
    uuid_report TEXT NOT NULL,
    date DATE NOT NULL,
    uuid_account TEXT NOT NULL,
    reason TEXT NOT NULL,
    more_infos TEXT,
    decision TEXT NOT NULL)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS video_reports (
    uuid_report TEXT NOT NULL,
    date DATE NOT NULL,
    uuid_video TEXT NOT NULL,
    reason TEXT NOT NULL,
    more_infos TEXT)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS handled_video_reports (
    uuid_report TEXT NOT NULL,
    date DATE NOT NULL,
    uuid_video TEXT NOT NULL,
    reason TEXT NOT NULL,
    more_infos TEXT,
    decision TEXT NOT NULL)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS banned_videos(
    uuid_video TEXT NOT NULL,
    file_video TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    uuid_sender TEXT NOT NULL,
    views INT NOT NULL,
    likes INT NOT NULL,
    file_minia TEXT NOT NULL,
    date DATE NOT NULL,
    dislike INT NOT NULL)"""
               )

connection.commit()


# ------------------------------------------
# --------------Account System--------------
# ------------------------------------------
def create_account(uuid: str, username: str, mail: str, password: str, file_picture: str):
    '''function for creating and referencing an account in the database.

    Keyword arguments:
    -uuid:str
    -username:str
    -mail:str
    -password:str
    -file-extension:str

    '''
    cursor.execute(f"""
    INSERT INTO account VALUES
    ('{uuid}', '{username}', '{mail}', '{password}', '{file_picture}', '{date.today().strftime("%Y-%m-%d")}', 'default-banner.jpg', 0, 0, 'Hello I am {username} !', 0)
    """)
    print("Success: Account created")
    connection.commit()


def get_account_for_login(mail: str, password: str):
    '''function that lets you search for an account by e-mail and password.
    
    Keyword arguments:
    -mail:str
    -password:str
    '''
    cursor.execute(f"""
    SELECT * FROM account
    WHERE mail_account = '{mail}'
    """)
    account = cursor.fetchone()
    if password == account[3]:
        print(account)
        return account
    return None


def check_if_account_exists(mail: str, username: str = None):
    '''function for verifying the existence of an account based on an e-mail address and a password.

    Keyword arguments:
    -mail:str -- mailgiven by user
    -password:str -- password given by user

    Return : True/False
    '''
    cursor.execute(f"""
    SELECT * FROM account
    WHERE mail_account = '{mail}'""")
    account = cursor.fetchone()
    print(account)
    if account is None:
        cursor.execute(f"""
        SELECT * FROM account
        WHERE name_account = '{username}'""")
        account = cursor.fetchone()
        print(account)
        if account is None:
            return False
    return True


def get_account_with_uuid(uuid: str):
    '''function that lets you search for an account by uuid.

    Keyword arguments:
    -uuid:str -- UUID of the account

    Return : the account found
    '''
    cursor.execute(f"""
    SELECT * FROM account
    WHERE uuid_account = '{uuid}'""")
    account = cursor.fetchone()
    return account


def search_channel_by_name(text: str):
    """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    cursor.execute(f"""
    SELECT * FROM account
    WHERE name_account LIKE '%{text}%'
    """)
    channels = cursor.fetchmany(10)
    return channels

def update_account(uuid:str, name:str, pp_name:str, banner_name:str, about:str):
    if name != '':
        cursor.execute(f"""
            UPDATE account
            SET name_account = '{name}'
            WHERE uuid_account = '{uuid}'""")
        connection.commit()
    if pp_name != '':
        cursor.execute(f"""
            UPDATE account
            SET file_picture = '{pp_name}'
            WHERE uuid_account = '{uuid}'""")
        connection.commit()
    if banner_name != '':
        cursor.execute(f"""
            UPDATE account
            SET banner_picture = '{banner_name}'
            WHERE uuid_account = '{uuid}'""")
        connection.commit()
    if about != '':
        cursor.execute(f"""
            UPDATE account
            SET about = '{about}'
            WHERE uuid_account = '{uuid}'""")
        connection.commit()

def update_darkmode_with_uuid(uuid:str):
    if get_account_with_uuid(uuid)[10]==1:
        cursor.execute(f"""
            UPDATE account
            SET darkmode = 0
            WHERE uuid_account = '{uuid}'""")
        connection.commit()
    else:
        cursor.execute(f"""
            UPDATE account
            SET darkmode = 1
            WHERE uuid_account = '{uuid}'""")
        connection.commit()

def get_number_accounts():
    cursor.execute("""SELECT * FROM account""")
    value = len(cursor.fetchall())
    return value

def ban_account_with_uuid(uuid:str):
    cursor.execute(f"""
            UPDATE account
            SET banned = 1
            WHERE uuid_account = '{uuid}'""")
    connection.commit()

def check_if_banned(uuid:str):
    cursor.execute(f"""
    SELECT * FROM account
    WHERE uuid_account = '{uuid}'""")
    account = cursor.fetchone()
    if account[7]==1:
        return False
    return True

def check_if_admin(uuid:str):
    cursor.execute(f"""
    SELECT * FROM account
    WHERE uuid_account = '{uuid}'""")
    account = cursor.fetchone()
    if account[8]==1:
        return True
    return False

# -----------------------------------------
# --------------Videos System--------------
# -----------------------------------------


def post_video(uuid_video:str, filetype:str, title:str, description:str, uuid_account:str, filetype_minia:str, visibility:int):
    '''function for posting and referencing a video in the database.

    Keyword arguments:
    -UUID_video:str
    -filetype:str
    -title:str
    -description:str
    -UUID_account:str
    -filetype_minia:str

    Return: nothing
    '''
    cursor.execute(f"""
    INSERT INTO videos VALUES
    ('{uuid_video}', '{filetype}', '{title}', '{description}', '{uuid_account}', 0, 0, '{filetype_minia}', '{date.today().strftime("%Y-%m-%d")}', 0, {visibility})
    """)
    connection.commit()


def check_if_video_exists(uuid: str):
    """function that checks if a video is registered in the database
    
    Keyword arguments:
    uuid:str -- uuid of the potential video
    Return: True/False
    """
    if get_video_with_uuid(uuid) is None:
        return False
    else:
        return True
    
def check_video_visibility_with_uuid(uuid:str):
    if check_if_video_exists(uuid):
        video = get_video_with_uuid(uuid)
        if video[10]==2:
            return True
        return False


def get_video_with_uuid(uuid: str):
    """function used to get a specific video
    
    Keyword arguments:
    uuid:str -- uuid of the video
    Return: return_description
    """
    cursor.execute(f"""
    SELECT * FROM videos
    WHERE uuid_video = '{uuid}'""")
    video = cursor.fetchone()
    return video


def get_video_from_user(uuid_user: str, visibility_level:int):
    """function used to get all videos of a user
    
    Keyword arguments:
    uuid_user:str -- uuid of the account
    Return: videos:list
    """
    cursor.execute(f"""
    SELECT * FROM videos
    WHERE uuid_sender = '{uuid_user}' AND visibility <= {visibility_level}""")
    videos = cursor.fetchall()
    return videos[::-1]

def get_random_video():
    """function used to get a random video

    Return: video
    """
    cursor.execute("""
    SELECT * FROM videos
    WHERE visibility = 0
    ORDER BY RANDOM()
    LIMIT 1  
    """)
    video = cursor.fetchone()
    return video


def add_view_to_video(uuid):
    """function that increment the views of a video
    
    Keyword arguments:
    uuid:str -- uuid of the video
    Return: nothing
    """
    cursor.execute(f"""
        UPDATE videos
        SET views = views + 1
        WHERE uuid_video = '{uuid}'""")
    connection.commit()


def search_video_by_name(text: str):
    """function used to search videos by their name
    
    Keyword arguments:
    text:str -- text contained in video title
    Return: videos:list
    """
    cursor.execute(f"""
    SELECT * FROM videos
    WHERE title LIKE '%{text}%'
    """)
    videos = cursor.fetchall()
    return videos


def get_videos_by_date(accounts):
    """function used to get videos from a list of accounts, ordered by dates
    
    Keyword arguments:
    account:list -- accounts where the videos come from
    Return: videos:list
    """
    text = ""
    for i in accounts:
        text = text + f" '{i[0]}' OR"
    text = text[:-3]
    cursor.execute(f"""
    SELECT * FROM videos
    WHERE uuid_sender ={text}
    ORDER BY date DESC""")
    videos = cursor.fetchall()
    return videos

def get_number_videos():
    cursor.execute("""SELECT * FROM videos""")
    value = len(cursor.fetchall())
    return value

def delete_video_with_uuid(uuid:str):
    cursor.execute(f"""
    DELETE FROM videos WHERE uuid_video = '{uuid}'
    """)
    connection.commit()

def ban_video_with_uuid(uuid:str):
    video = get_video_with_uuid(uuid)
    delete_video_with_uuid(video[0])
    cursor.execute(f"""
    INSERT INTO banned_videos VALUES
    ('{video[0]}', '{video[1]}', '{video[2]}', '{video[3]}', '{video[4]}', {video[5]}, {video[6]}, '{video[7]}', '{video[8]}', {video[9]})
    """)
    connection.commit()

    

# ------------------------------------------
# --------------Follows System--------------
# ------------------------------------------


def add_follow(uuid_follower: str, uuid_following: str):
    """function used to add a follow in the database
    
    Keyword arguments:
    uuid_follower:str -- uuid of the new follower
    uuid_folloing:str -- uuid of the account followed
    Return: nothing
    """
    cursor.execute(f"""
    INSERT INTO follows VALUES
    ('{uuid_follower}', '{uuid_following}')""")
    connection.commit()
    if check_if_is_following(uuid_follower, uuid_following):
        print(f"Success follow : {uuid_follower} to {uuid_following}")


def remove_follow(uuid_follower:str, uuid_following:str):
    """function used to remove a follow in the database
    
    Keyword arguments:
    uuid_follower:str -- uuid of the follower
    uuid_folloing:str -- uuid of the account followed
    Return: nothing
    """
    cursor.execute(f"""
    DELETE FROM follows
    WHERE uuid_follower = '{uuid_follower}' AND uuid_followed = '{uuid_following}';
    """)
    connection.commit()


def get_follows_of_user(uuid: str):
    '''Provides a list of a user's subscriptions

    Keyword arguments:
    uuid_follower:str -- uuid of the follower
    Return: list of accounts followed
    '''
    cursor.execute(f"""
    SELECT * FROM follows
    WHERE uuid_follower = '{uuid}'""")
    follow_uuids = cursor.fetchall()
    print(follow_uuids)
    return ([get_account_with_uuid(i[1]) for i in follow_uuids])


def followers_number(uuid: str):
    '''function used to get the number of followers of an account

    Keyword arguments:
    uuid:str -- uuid of the account
    Return: number of followers
    '''
    cursor.execute(f"""
    SELECT COUNT (*) FROM follows
    WHERE uuid_followed = '{uuid}'""")
    account = int(cursor.fetchone()[0])
    return account


def check_if_is_following(uuid_follower: str, uuid_followed: str):
    """function that checks if a user follows another user
    
    Keyword arguments:
    uuid_follower:str -- uuid of the potential follower
    uuid_followed:str -- uuid of the potential followed
    Return: return_description
    """
    if uuid_follower != uuid_followed:
        cursor.execute(f"""
        SELECT * FROM follows
        WHERE uuid_follower = '{uuid_follower}' AND uuid_followed = '{uuid_followed}'""")
        follow_uuids = cursor.fetchone()
        print(follow_uuids)
        if follow_uuids is None:
            return False
        return True

# -------------------------------------------------
# --------------Likes/Dislikes System--------------
# -------------------------------------------------

def add_like(uuid_liker: str, uuid_video: str, dislike:bool = False):
    """function used to add a like in the database
    
    Keyword arguments:
    uuid_liker:str -- uuid of the new liker
    uuid_video:str -- uuid of the video liked
    Return: nothing
    """
    if dislike == False:
        cursor.execute(f"""
        INSERT INTO likes VALUES
        ('{uuid_liker}', '{uuid_video}')""")
        connection.commit()
        cursor.execute(f"""
            UPDATE videos
            SET likes = likes + 1
            WHERE uuid_video = '{uuid_video}'""")
        connection.commit()
    else:
        cursor.execute(f"""
        INSERT INTO dislikes VALUES
        ('{uuid_liker}', '{uuid_video}')""")
        connection.commit()
        cursor.execute(f"""
            UPDATE videos
            SET dislike = dislike + 1
            WHERE uuid_video = '{uuid_video}'""")
        connection.commit()


def remove_like(uuid_liker:str, uuid_video:str, dislike:bool = False):
    """function used to remove a follow in the database
    
    Keyword arguments:
    uuid_liker:str -- uuid of the liker
    uuid_video:str -- uuid of the video liked
    Return: nothing
    """
    if dislike == False:
        cursor.execute(f"""
        DELETE FROM likes
        WHERE uuid_liker = '{uuid_liker}' AND uuid_video = '{uuid_video}';
        """)
        connection.commit()
        cursor.execute(f"""
            UPDATE videos
            SET likes = likes - 1
            WHERE uuid_video = '{uuid_video}'""")
        connection.commit()
    else:
        cursor.execute(f"""
        DELETE FROM dislikes
        WHERE uuid_disliker = '{uuid_liker}' AND uuid_video = '{uuid_video}';
        """)
        connection.commit()
        cursor.execute(f"""
            UPDATE videos
            SET dislike = dislike - 1
            WHERE uuid_video = '{uuid_video}'""")
        connection.commit()

def check_like(uuid_liker:str, uuid_video:str, dislike:bool = False):
    """function that check if a like from a specific user on a specific video already exists
    
    Keyword arguments:
    uuid_liker:str -- uuid of the liker
    uuid_video:str -- uuid of the video liked
    Return: True/False
    """
    if dislike == False:
        cursor.execute(f"""
        SELECT 1 FROM likes
        WHERE uuid_liker = '{uuid_liker}' AND uuid_video = '{uuid_video}';""")
        if cursor.fetchone() is None:
            return False
        return True
    else:
        cursor.execute(f"""
        SELECT 1 FROM dislikes
        WHERE uuid_disliker = '{uuid_liker}' AND uuid_video = '{uuid_video}';""")
        if cursor.fetchone() is None:
            return False
        return True

# -------------------------------------------------
# --------------Comments System--------------------
# -------------------------------------------------

def add_comment(uuid_uploader:str, uuid_video:str, content:str):
    uuid_comment=uuid.uuid4()
    cursor.execute(f"""
        INSERT INTO comments VALUES
        ('{uuid_comment}', '{uuid_uploader}', '{uuid_video}', '{content}', '{date.today().strftime("%Y-%m-%d")}')""")
    connection.commit()
    return uuid_comment

def get_all_comments_of_video_for_videoviewer(uuid_video:str):
    cursor.execute(f"""
        SELECT * FROM comments
        WHERE uuid_video = '{uuid_video}';""")
    comments_infos = cursor.fetchall()
    comments =[]
    for comment in comments_infos:
        account = get_account_with_uuid(comment[1])
        comments.append([account[0], account[1], account[4], comment[3], comment[4]])
    return comments

# -------------------------------------------------
# --------------ERRORS System----------------------
# -------------------------------------------------

def add_error_to_db(text:str):
    cursor.execute(f"""
        INSERT INTO errors VALUES
        ('{date.today().strftime("%Y-%m-%d")}', '{text}')""")
    connection.commit()

# -------------------------------------------------
# --------------REPORT System----------------------
# -------------------------------------------------

def add_new_report_account(uuid_user:str, reason:str, more_infos:str):
    cursor.execute(f"""
        INSERT INTO account_reports VALUES
        ('{uuid.uuid4()}', '{date.today().strftime("%Y-%m-%d")}', '{uuid_user}', '{reason}', '{more_infos}')""")
    connection.commit()

def get_all_reports():
    cursor.execute("""SELECT * FROM account_reports""")
    return cursor.fetchall()

def get_report_with_uuid(uuid:str):
    cursor.execute(f"""
                   SELECT * FROM account_reports
                   WHERE uuid_report = '{uuid}'
                   """)
    return cursor.fetchone()

def remove_report_with_uuid(uuid:str):
    cursor.execute(f"""
                   DELETE FROM account_reports
                   WHERE uuid_report = '{uuid}'
                   """)
    connection.commit()

def transfer_report_to_handled(uuid:str, decision:str):
    report = get_report_with_uuid(uuid)
    cursor.execute(f"""
        INSERT INTO handled_account_reports VALUES
        ('{report[0]}', '{report[1]}', '{report[2]}', '{report[3]}', '{report[4]}', '{decision}')""")
    connection.commit()
    remove_report_with_uuid(uuid)



def add_new_report_video(uuid_video:str, reason:str, more_infos:str):
    cursor.execute(f"""
        INSERT INTO video_reports VALUES
        ('{uuid.uuid4()}', '{date.today().strftime("%Y-%m-%d")}', '{uuid_video}', '{reason}', '{more_infos}')""")
    connection.commit()

def get_all_reports_video():
    cursor.execute("""SELECT * FROM video_reports""")
    return cursor.fetchall()

def get_report_with_uuid_video(uuid:str):
    cursor.execute(f"""
                   SELECT * FROM video_reports
                   WHERE uuid_report = '{uuid}'
                   """)
    return cursor.fetchone()

def remove_report_with_uuid_video(uuid:str):
    cursor.execute(f"""
                   DELETE FROM video_reports
                   WHERE uuid_report = '{uuid}'
                   """)
    connection.commit()

def transfer_report_to_handled_video(uuid:str, decision:str, report):
    cursor.execute(f"""
        INSERT INTO handled_video_reports VALUES
        ('{report[0]}', '{report[1]}', '{report[2]}', '{report[3]}', '{report[4]}', '{decision}')""")
    connection.commit()
    remove_report_with_uuid_video(uuid)

def search_handled_report_account(uuid_account:str):
    cursor.execute(f"""
    SELECT * from handled_account_reports WHERE uuid_account = '{uuid_account}'
    """)
    return cursor.fetchone()

def search_ban_acount(text:str):
    cursor.execute(f"""
    SELECT * FROM account
    WHERE banned = 1 AND (uuid_account LIKE '%{text}%' OR mail_account LIKE '%{text}%' OR name_account LIKE '%{text}%')
    """)
    accounts_found = cursor.fetchall()
    accounts_banned = []
    for account in accounts_found:
        report = search_handled_report_account(account[0])
        accounts_banned.append([account[0],account[1], account[2], report[3], report[2], report[5]])
    return accounts_banned

# -------------------------------------------------
# --------------ADMIN System----------------------
# -------------------------------------------------

def add_new_admin(uuid:str):
    cursor.execute(f"""
        UPDATE account
        SET admin = 1
        WHERE uuid_account == '{uuid}'
    """)
    connection.commit()