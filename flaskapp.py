"""-------Import OS : used to manage filenames...-------"""
import os

# -------Import UUID : to set unique IDs for accounts and videos-------
import uuid

# -------Import time-------
import time

# -------Import utility to ensure file name compatibility-------
from werkzeug.utils import secure_filename

# -------Import Flask : basis of our web system-------
from flask import Flask, render_template, request, session, redirect, url_for, Response, make_response, jsonify

# -------Import python file "database" : manages video and account databases-------
import database_system as db

# -------Import python file "directory_checker.py".
# Manages the verification of the existence of each file-------
import directory_checker as dc
import image_management as im

app = Flask(__name__)
# -------Setup parameters for image upload-------
UPLOAD_FOLDER = r"static/videos"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'mp4'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# -------Setup of secret key parameter, necessary for login system operation-------
app.secret_key = 'Weuve_Banana'

# -------Directory check-------
dc.check_directories()

# -------Colors for print-------
class Bcolors:
    """Colors for print"""
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

admin_key=uuid.uuid4()


# -------App route INDEX PAGE-------
@app.route('/')
def index():
    """function executed when the user wants to access to the main page of the website
    
    Return: render_template of the "index" page
    """
    return render_template('index.j2',
                           account_connecter=check_session(),
                           user_account=get_own_user_account(),
                           subscriptions=get_subscriptions(),
                           admin_key=admin_key)

@app.route('/load')
def load():
    return make_response(jsonify(load_n_videos(16)), 200)


# -------Sign up systeme-------
@app.route('/signup')
def signup():
    """function executed when the user wants to access to the "sign up" page of the website

    Return: render_template of the "signup" page
    """
    if check_session():
        return index()
    return render_template('signup.j2',
                            account_connecter=check_session(),
                            user_account=get_own_user_account(),)


@app.route('/post-signup', methods=['get', 'post'])
def post_signup():
    """function executed when the user submits the form to signup.
    It adds a new account in the database if all conditions are met.
    """

    # Get informations from form
    mail = request.form['email']
    name = request.form['name']
    password = request.form['password']
    profile_picture_file = request.files['profile_picture']

    # get file extension of
    _, file_type_picture = os.path.splitext(profile_picture_file.filename)
    uuid_account = generate_uuid()
    new_profile_picture_name = secure_filename(uuid_account+file_type_picture)
    profile_picture_file.save(os.path.join(
        "static/profile_pictures", new_profile_picture_name))
    
    if db.check_if_account_exists(mail, name) is False:
        db.create_account(uuid_account, adapt_text(name), mail, adapt_text(password), new_profile_picture_name)
        print(Bcolors.OKGREEN + Bcolors.BOLD + "SUCCESS Sign Up : " +
              Bcolors.ENDC + f"with mail = {mail}")
        return redirect("/")
    return redirect(url_for('signup'))

# -------Login system-------


@app.route('/login')
def login():
    """function executed when the user wants to access to the "login" page of the website

    Return: render_template of the "login" page
    """
    if check_session():
        return index()
    else:
        return render_template('login.j2', user_account=get_own_user_account())


@app.route('/post-login', methods=['get', 'post'])
def post_login():
    """function executed when the user submits the form to login.
    It checks all conditions to login.
    """
    mail = request.form['email']
    password = request.form['password']
    if db.check_if_account_exists(mail):
        account = db.get_account_for_login(mail, password)
        if account is not None:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            print(Bcolors.OKGREEN + Bcolors.BOLD + "SUCCESS LOGIN : " +
                  Bcolors.ENDC + session['username'])
            return redirect('/')
        print(Bcolors.WARNING + Bcolors.BOLD +
                "WARNING : Account not found " + Bcolors.ENDC + f"with mail = {mail}")
        return redirect(url_for('login'))
    print(Bcolors.WARNING + Bcolors.BOLD +
            "WARNING : Account not found " + Bcolors.ENDC + f"with mail = {mail}")
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    """function executed when the user wants to logout.
    It clears the session.
    """
    session.clear()
    return redirect('/')

# -------Update Account system-------
@app.route('/update-account', methods=['get', 'post'])
def post_account_update():

    name = request.form['name']
    profile_picture_file = request.files['profile_picture']
    banner_picture_file = request.files['banner_picture']
    about_text = request.form['about_text']
    account = db.get_account_with_uuid(session['id'])

    if check_session():
        if profile_picture_file.filename != "":
            os.remove(f"static/profile_pictures/{account[4]}")
            _, file_type_picture = os.path.splitext(profile_picture_file.filename)
            uuid_account = session['id']
            new_profile_picture_name = secure_filename(uuid_account+file_type_picture)
            profile_picture_file.save(os.path.join(
            "static/profile_pictures", new_profile_picture_name))
        else:
            new_profile_picture_name=''
        
        if banner_picture_file.filename != "":
            if account[6] != "default-banner.jpg":
                os.remove(f"static/banners/{account[6]}")
            _, file_type_picture = os.path.splitext(banner_picture_file.filename)
            uuid_account = session['id']
            new_banner_picture_name = secure_filename(uuid_account+file_type_picture)
            banner_picture_file.save(os.path.join(
            "static/banners", new_banner_picture_name))
        else:
            new_banner_picture_name=''
        
        db.update_account(session['id'], adapt_text(name), new_profile_picture_name, new_banner_picture_name, adapt_text(about_text))
    return(redirect('/account-settings'))



# -------Subscriptions page-------


@app.route('/subscriptions')
def subscriptions():
    """function executed when the user wants to access to the "subscriptions" page of the website

    Return: render_template of the "subscriptions" page
    """
    if check_session():
        subs = db.get_follows_of_user(str(session['id']))
        if subs != []:
            videos = db.get_videos_by_date(subs)
            videos_users = []
            for video in videos:
                if video is not None:
                    videos_users.append(db.get_account_with_uuid(video[4]))
        else:
            videos=[]
            videos_users=[]
        return render_template("subscriptions.j2",
                                account_connecter=check_session(),
                                user_account=get_own_user_account(),
                                subscriptions=subs,
                                videos=videos,
                                videos_users=videos_users,
                                admin_key=admin_key,)
    return redirect(url_for('login'))


# -------Video Post systeme-------
@app.route('/upload')
def upload():
    """function executed when the user wants to access to the "upload" page of the website

    Return: render_template of the "upload" page
    """
    if check_session():
        global admin_key
        return render_template('upload_video.j2',
                               account_connecter=check_session(),
                               user_account=get_own_user_account(),
                                subscriptions=get_subscriptions(),
                                admin_key=admin_key)
    return redirect(url_for('login'))


@app.route('/post-video', methods=['get', 'post'])
def video_post():
    """function executed when the user submits the form to post a video.
    It adds the new video to the database.
    """
    if check_session():
        # get all elements of form
        file = request.files['file']
        _, file_extension_video = os.path.splitext(file.filename)
        minia = request.files['minia']
        _, file_extension_minia = os.path.splitext(minia.filename)
        title = request.form['title']
        description = request.form['description']
        visibility = int(request.form['visibility'])
        # UUID system
        generated_uuid = generate_uuid()
        user_uuid = session['id']
        # Saving video
        filename_video = secure_filename(generated_uuid+file_extension_video)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_video))
        filename_video = secure_filename(
            generated_uuid+file_extension_video)
        # Saving miniature
        filename_minia = secure_filename(generated_uuid+file_extension_minia)
        minia.save(os.path.join("static/miniatures", filename_minia))
        im.image_cropping("static/miniatures", generated_uuid, file_extension_minia)
        db.post_video(generated_uuid,
                      filename_video,
                      adapt_text(title),
                      adapt_text(description),
                      user_uuid,
                      (f"{generated_uuid}_crop{file_extension_minia}"),
                      visibility)
        return redirect(f'/video/{generated_uuid}')
    return redirect('/')

# -------Follow Post systeme-------


@app.route('/post-follow', methods=['get', 'post'])
def follow_post():
    """function executed when the user submits the form to follow a user.
    It adds the new follow in the database.
    """
    if check_session():
        uuid_following = request.form['follow_button']
        if session['id'] != uuid_following:
            db.add_follow(session['id'], uuid_following)
        return channel(uuid_following)
    return redirect(url_for('login'))


@app.route('/post-unfollow', methods=['get', 'post'])
def unfollow_post():
    """function executed when the user submits the form to unfollow a user.
    It removes the follow in the database.
    """
    if check_session():
        uuid_following = request.form['unfollow_button']
        if session['id'] != uuid_following:
            db.remove_follow(session['id'], uuid_following)
        return channel(uuid_following)

# -------Follow Post systeme-------

@app.route('/post-like', methods=['POST',])
def like_post():
    """function executed when the user submits the form to like a video.
    It adds/removes the new like in the database.
    """
    if check_session():
        uuid_video=request.referrer.rsplit('/', 1)[-1]
        if db.check_like(session['id'], uuid_video) is False:
            db.add_like(session['id'], uuid_video)
            if db.check_like(session['id'], uuid_video, True)==True:
                db.remove_like(session['id'], uuid_video, True)
            return "True"
        else:
            db.remove_like(session['id'], uuid_video)
            return "True"
    return "False"

@app.route('/post-dislike', methods=['POST',])
def dislike_post():
    """function executed when the user submits the form to like a video.
    It adds/removes the new like in the database.
    """
    if check_session():
        uuid_video=request.referrer.rsplit('/', 1)[-1]
        if db.check_like(session['id'], uuid_video, True) is False:
            db.add_like(session['id'], uuid_video, True)
            if db.check_like(session['id'], uuid_video, False)==True:
                db.remove_like(session['id'], uuid_video, False)
            return "True"
        else:
            db.remove_like(session['id'], uuid_video, True)
            return "True"
    return "False"

# -------Comments Post systeme-------
@app.route('/post-comment', methods=['POST',])
def comment_post():
    if check_session():
        content = adapt_text(request.form['content'])
        db.add_comment(session['id'], request.referrer.rsplit('/', 1)[-1], content)
        comments = db.get_all_comments_of_video_for_videoviewer(request.referrer.rsplit('/', 1)[-1])
    return render_template('comments_list.j2', comments= comments[::-1])

# -------Search video systeme-------
@app.route('/post_search', methods=['get',])
def post_search():
    """function executed when the user submits the form to make a search."""
    search_text = adapt_text(request.args['search_text'])
    if search_text != "":
        print(Bcolors.OKGREEN + Bcolors.BOLD + "Searching : " +
              Bcolors.ENDC + "argument = " + search_text)
        channels = db.search_channel_by_name(search_text)
        videos = db.search_video_by_name(search_text)
        videos_users = []
        for i in videos:
            videos_users.append(db.get_account_with_uuid(i[4]))
        return render_template('search_result.j2',
                               account_connecter=check_session(),
                               user_account=get_own_user_account(),
                               videos_loaded=videos,
                               channels_loaded=channels,
                                subscriptions=get_subscriptions(),
                                admin_key=admin_key,
                                videos_users=videos_users)
    return redirect('/')

# -------Access to Video systeme-------

@app.route('/video/<page_name>')
def videoview(page_name):
    """function executed when the user wants to access to a video of the website

    Return: render_template of the "videoview" page
    """
    if db.check_if_video_exists(page_name):   
        video = db.get_video_with_uuid(page_name)
        if db.check_video_visibility_with_uuid(page_name):
            if check_session():
                if session['id']!=video[4]:
                    return error_page_returning("You do not have permission to access this video", 401)
            else:
                return error_page_returning("You do not have permission to access this video", 401)
            
        db.add_view_to_video(page_name)

        account_from_video = db.get_account_with_uuid(video[4])
        if check_session():
            is_following = db.check_if_is_following(
                session['id'], account_from_video[0])
            is_liking = db.check_like(session['id'], page_name)
            if is_liking is not True:
                is_disliking = db.check_like(session['id'], page_name, True)
            else:
                is_disliking=False
        else:
            is_following = False
            is_liking = False
            is_disliking=False

        comments = db.get_all_comments_of_video_for_videoviewer(page_name)
        print(Bcolors.OKGREEN + Bcolors.BOLD + "ACCESS TO VIDEO :" + Bcolors.ENDC +
              video[0] + video[1] + " = " + video[2] + f" {video[5]} views. uploaded by {video[4]}")
        return render_template("videoviewer.j2",
                               account_connecter=check_session(),
                               video_infos=video,
                               user_account=get_own_user_account(),
                               account_video=account_from_video,
                               is_following=is_following,
                                subscriptions=get_subscriptions(),
                                is_liking=is_liking,
                                is_disliking=is_disliking,
                                url=request.url,
                                comments=comments[::-1],
                                admin_key=admin_key,
                                follow_number=db.followers_number(account_from_video[0]))
    print(print(Bcolors.FAIL+Bcolors.BOLD+"ERROR : video not found : "+Bcolors.ENDC+page_name))
    return error_page_returning("Video not found", 404)

# -------Access to Channel system-------


@app.route('/channel/<page_name>')
def channel(page_name):
    """function executed when the user wants to access to a channel of the website

    Return: render_template of the "channel" page
    """
    account = db.get_account_with_uuid(page_name)
    if account is not None:
        if check_session():
            if session['id']==account[0]:
                videos_from_channel = db.get_video_from_user(page_name,2)
            else:
                videos_from_channel = db.get_video_from_user(page_name,0)
            is_following = db.check_if_is_following(session['id'], account[0])
        else:
            videos_from_channel = db.get_video_from_user(page_name,0)
            is_following = False
        return render_template("channel.j2",
                               account_connecter=check_session(),
                               user_account=get_own_user_account(),
                               uuid=page_name,
                               account_channel=account,
                               videos=videos_from_channel,
                               is_following=is_following,
                               follow_number=db.followers_number(account[0]),
                                subscriptions=get_subscriptions(),
                                admin_key=admin_key)
    return error_page_returning("Channel not found", 404)

# -------Access to Account settings system-------


@app.route('/account-settings')
def account_settings():
    """function executed when the user wants to access to the "account-settings" page of the website

    Return: render_template of the "account-settings" page
    """
    return render_template('account_settings.j2',
                           account_connecter=check_session(),
                           user_account=get_own_user_account(),
                           subscriptions=get_subscriptions(),
                           admin_key=admin_key)

# -------Informations page-------


@app.route('/informations')
def get_informations():
    """function executed when the user wants to access to the "informations" page of the website

    Return: render_template of the "informations" page
    """
    return render_template("informations.j2",
                           account_connecter=check_session(),
                           user_account=get_own_user_account(),
                           subscriptions=get_subscriptions(),
                           admin_key=admin_key)

# -------CGU page-------


@app.route('/cgu')
def get_cgu():
    """function executed when the user wants to access to the "cgu" page of the website

    Return: render_template of the "cgu" page
    """
    return render_template("cgu.j2",
                           account_connecter=check_session(),
                           user_account=get_own_user_account(),
                           subscriptions=get_subscriptions(),
                           admin_key=admin_key)

# -------Other unknown pages page-------


@app.route('/<page_name>')
def unknown():
    """function executed when the user wants to access to an unknown page of the website

    Return: render_template of the "error" page
    """
    return error_page_returning("Page not found", 404)

# -------Open Report page-------

@app.route('/report', methods=['POST',])
def post_report_account():
    uuid_channel_reported=request.form['account-report']
    reason_report=request.form['reason-report']
    more_infos=request.form['more-infos-report']
    db.add_new_report_account(uuid_channel_reported, reason_report, more_infos)
    return redirect(f'/channel/{uuid_channel_reported}')

@app.route('/report-video', methods=['POST',])
def post_report_video():
    uuid_video_reported=request.form['video-report']
    reason_report=request.form['reason-report']
    more_infos=request.form['more-infos-report']
    db.add_new_report_video(uuid_video_reported, reason_report, more_infos)
    return redirect(f'/video/{uuid_video_reported}')


# -------ADMIN SYSTEM-------

@app.route(f"/{admin_key}")
def admin():
    if check_session():
        if db.check_if_admin(session['id']) is True:
            n_accounts = db.get_number_accounts()
            n_videos = db.get_number_videos()
            reports = db.get_all_reports()
            videos_reports = db.get_all_reports_video()
            return render_template("admin-panel.j2", n_users=n_accounts, n_videos=n_videos, reports=reports, videos_reports=videos_reports)
    return redirect('/')


@app.route('/post-ban', methods=['post',])
def post_ban():
    uuid = request.form['report_uuid']
    report = db.get_report_with_uuid(uuid)
    db.ban_account_with_uuid(report[2])
    db.transfer_report_to_handled(uuid, "BAN")
    return("banned")

@app.route('/post-nothing', methods=['post',])
def post_nothing():
    uuid = request.form['report_uuid']
    db.transfer_report_to_handled(uuid, "NOTHING")
    return("nothing")

@app.route('/post-ban-video', methods=['post',])
def post_ban_video():
    uuid = request.form['report_uuid']
    report = db.get_report_with_uuid_video(uuid)
    db.transfer_report_to_handled_video(uuid, "BAN", report)
    db.ban_video_with_uuid(report[2])
    return("banned")

@app.route('/post-nothing-video', methods=['post',])
def post_nothing_video():
    uuid = request.form['report_uuid']
    report = db.get_report_with_uuid_video(uuid)
    db.transfer_report_to_handled_video(uuid, "BAN", report)
    return("nothing")

@app.route('/post-search-admin', methods=['post',])
def post_search_admin():
    if check_session():
        if db.check_if_admin(session['id']) is True:
            search_txt = adapt_text(request.form['search_value'])
            accounts_found = db.search_ban_acount(search_txt)
            return render_template("admin-search.j2", banned_accounts=accounts_found)
    return redirect('/')

    

# -------Check if session exists, used for the navbar to know if the user is connected-------


def check_session():
    '''
    Checks if session exists, used for the navbar to know if the user is connected.
    '''
    if session.get('loggedin'):
        if db.check_if_banned(session['id']):
            return session['loggedin']
        else:
            session.clear()
            return None
    else:
        return None
    
def adapt_text(text:str):
    new_text=""
    for letter in text:
        if letter=="'":
            new_text = new_text + r"''"
        else:
            new_text=new_text + letter
    return new_text

# -------Function that returns a list of N videos-------


def load_n_videos(n_videos: int):
    '''
    Returns a list of N videos.
    Requires the following information:
    -n:int
    '''
    videos_shown = []
    for _ in range(n_videos):
        video = db.get_random_video()
        user =(db.get_account_with_uuid(video[4]))
        videos_shown.append([video[0], video[2], video[5], video[7], video[8], user[1], user[4]])
    return videos_shown

# -------returns  the name of profile_picture file of the user-------


def get_own_user_account():
    '''
    returns the name of profile_picture file of the user, if the user is connected
    '''
    if check_session() is not None:
        uuid_account = session['id']
        account_found = db.get_account_with_uuid(uuid_account)
        return account_found
    return None


def generate_uuid():
    '''
    Generates a random UUID v4
    '''
    return str(uuid.uuid4())


def error_page_returning(message: str, errornumber: int = 0):
    '''
    Provides an error to the user
    Requires the following information:
    -message:str
    '''
    return render_template("error.j2",
                           account_connecter=check_session(),
                           message=f"Error {errornumber}: {message}",
                           user_account=get_own_user_account(),
                           subscriptions=get_subscriptions())

def get_subscriptions():
    """function used to get subscriptions of user

    Return: List subscriptions
    """
    if check_session():
        return db.get_follows_of_user(str(session['id']))
    return []


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
