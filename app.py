#log in or sign up to log in as user
#use admin to access admin/superuser
#admin username: ucc7aside
#      password: ball123


from sqlite3 import IntegrityError
from flask import Flask, render_template, request, make_response, redirect, url_for, session, g
from form import RegisterForm, HomeForm, JoinForm, LoginForm, SignupForm,  UpdateForm, AdminForm
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "new-secret-key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect( url_for("login", next=request.url) )
        return view(**kwargs)
    return wrapped_view

@app.before_request
def load_logged_in_admin():
    g.admin = session.get("admin_id", None)

def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect( url_for("admin", next=request.url) )
        return view(**kwargs)
    return wrapped_view

@app.route("/", methods=["GET","POST"])
def home():
    return render_template("home.html")

@app.route("/ucc_7_a_side_admin", methods=["GET","POST"])
def admin_home():
    return render_template("admin_home.html")

@app.route("/register", methods=["GET","POST"])
@login_required
def register():
    form = RegisterForm()
    message=""
    if form.validate_on_submit():
        team = form.team.data
        captain = form.captain.data
        points = 0
        games = 0
        db = get_db()
        db.execute("""INSERT INTO teams (team, captain, games, points)
                            VALUES (?, ?, ?, ?);""", (team, captain, games, points))
        db.execute("""INSERT INTO players (team, player)
                            VALUES (?, ?);""", (team, captain))
        db.commit()
        message = "Your team has successfully been registered!"
    return render_template("register.html", form=form, message=message)

@app.route("/league_table", methods=["GET","POST"])
def league_table():
    teams=""
    db = get_db()
    teams = db.execute("""SELECT * FROM teams
                        ORDER BY points DESC;""").fetchall()
    return render_template("league_table.html", teams=teams)

@app.route("/all_teams", methods=["GET", "POST"])
@login_required
def all_teams():
    db = get_db()
    teams = db.execute("""SELECT * FROM teams
                        ORDER BY team ASC;""").fetchall()
    return render_template("all_teams.html", teams=teams)

@app.route("/requests", methods=["GET", "POST"])
def requests():
    db = get_db()
    request_table = db.execute("""SELECT * FROM requests;""").fetchall()
    return render_template("requests.html", request_table=request_table)

@app.route("/accept_request/<int:player_id>", methods=["GET", "POST"])
@admin_required
def accept_request(player_id):
    db = get_db()
    id = db.execute("""SELECT * FROM requests
                    WHERE player_id = ?;""", (player_id,)).fetchone()
    db.execute("""INSERT INTO players(team, player)
                    SELECT team, name 
                    FROM requests
                    WHERE player_id = ?""", (id["player_id"],))
    
    print(id["player_id"])
    db.execute("""DELETE FROM requests
                WHERE player_id = ?;""",(id["player_id"],))
    db.commit()
    return redirect(url_for('requests'))

@app.route("/decline_request/<int:player_id>", methods=["GET", "POST"])
@admin_required
def decline_request(player_id):
    db = get_db()
    id = db.execute("""SELECT * FROM requests
                    WHERE player_id = ?;""", (player_id,)).fetchone()
    db.execute("""DELETE FROM requests
                WHERE player_id = ?;""",(id["player_id"],))
    db.commit()
    return redirect(url_for('requests'))


@app.route("/join/<int:team_id>", methods=["GET", "POST"])
@login_required
def join(team_id):
    form = JoinForm()
    message = ""
    requests = ""
    db = get_db()
    join = db.execute("""SELECT * FROM teams
                        WHERE team_id = ?;""", (team_id,)).fetchone()
    print(join)
    if form.validate_on_submit():
        message= "You request have been sent :)"
        db = get_db()
        name = form.name.data
        position = form.position.data
        requests = db.execute("""INSERT INTO requests (name, position, team)
                                        VALUES (?, ?, ?);""", (name, position, join["team"]))
        db.commit()
    return render_template("join.html", form=form, message=message, join=join, requests=requests)

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = SignupForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data
        db = get_db()
        possible_clashing_user = db.execute("""SELECT * FROM users 
                                            WHERE user_id = ?;""", (user_id,)).fetchone()
        if possible_clashing_user is not None:
            form.user_id.errors.append("User id is already taken :(")
        else:
            db.execute("""INSERT INTO users (user_id, password)
                                            VALUES (?, ?);""", (user_id, generate_password_hash(password)))
            db.commit()
            return redirect( url_for("login") )
    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error=""
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        matching_user = db.execute("""SELECT * FROM users 
                                            WHERE user_id = ?;""", (user_id,)).fetchone()                                                     
        if matching_user is None:
            form.user_id.errors.append("Unknown user id")
        elif not check_password_hash(matching_user["password"], password):
            form.password.errors.append("Incorrect Password!")
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                return redirect( url_for("home") )
            return redirect(next_page)
    return render_template("login.html", form=form, error="Both fields must be filled in")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    form = AdminForm()
    error =""
    if form.validate_on_submit():
        admin_id = form.admin_id.data
        admin_password = form.admin_password.data
        db = get_db()
        matching_admin =  db.execute("""SELECT * FROM admin
                                        WHERE admin_id = ?;""", (admin_id,)).fetchone()
        if matching_admin is None:
            form.admin_id.errors.append("Unknown admin id")
        elif not check_password_hash(matching_admin["admin_password"],admin_password):
            form.admin_password.errors.append("Incorrect Password")
        else:
            session.clear()
            session["admin_id"] = admin_id
            next_page = request.args.get("next")
            if not next_page:
                return redirect( url_for("admin_home") )
            return redirect(next_page)
    return render_template("admin.html", form=form, error="Both fields must be filled in")

@app.route("/list_of_teams", methods=["GET", "POST"])
@admin_required
def list_of_teams():
    db = get_db()
    teams = db.execute("""SELECT * FROM teams
                        ORDER BY team ASC;""").fetchall()
    return render_template("list_of_teams.html", teams=teams)

@app.route("/logout")
def logout():
    session.clear()
    return redirect( url_for("home") )

@app.route("/update/<int:team_id>", methods = ["GET", "POST"])
@admin_required
def update(team_id):
    form = UpdateForm()
    updated_team=""
    update= ""
    update_games=""
    error = ""
    messsage = ""
    db = get_db()
    update = db.execute("""SELECT * FROM teams
                        WHERE team_id = ?;""", (team_id,)).fetchone()
    if form.validate_on_submit():
        points = form.points.data
        games = form.games.data
        print(points)
        print(games)
        if points != "":
            db = get_db()
            updated_team = db.execute("""UPDATE teams
                        SET points = ?
                        WHERE team_id = ?;""", (points, update["team_id"])).fetchone()
            db.commit()
            form.points.errors.append("")
        elif games != "":
            db = get_db()
            updated_team = db.execute("""UPDATE teams
                        SET games = ?
                        WHERE team_id = ?;""", (games, update["team_id"])).fetchone()
            db.commit()
            form.games.errors.append("")
        else:
            db=get_db()
            db.execute("""UPDATE teams
                                    SET points = ?
                                    WHERE team_id =;""", (points, update["team_id"])).fetchone()
            db.execute("""UPDATE teams
                        SET games = ?
                        WHERE team_id = ?;""", (games, update["team_id"])).fetchone()
            db.commit()
            print(points)
            print(games)
    return render_template("update.html", form=form, update=update, error="Something went wrong", update_games=update_games, updated_team=updated_team)
    
@app.route("/all_players", methods=["GET", "POST"])
@admin_required
def all_players():
    players=""
    db = get_db()
    players = db.execute("""SELECT * FROM players;""").fetchall()
    return render_template("players.html", players=players)
    
