from flask import request,Flask,render_template, url_for,redirect,request,session
import urllib2,json,util,gamesystem

app=Flask(__name__)
app.secret_key = "JackStevenDinaandBiggsAreAwesomeExceptNotReallyDina1"

@app.route("/",methods=["POST","GET"])
def home():
    if request.method=="GET":
        return render_template("home.html")
    else:
        pending = request.form.keys()[0]
        if "tab" in pending:
            return handleTabs(pending)
@app.route("/game/<name>",methods=["POST","GET"])
def game(name):
    if request.method=="GET":
        if session["user"] == util.getCreator(name):
            return render_template("index.html",players=util.getPlayers(name),creator=True,started=util.gameStarted(name))
        else:
            return render_template("index.html",players=util.getPlayers(name),ceator=False)
    else:
        pending = request.form.keys()[0]
        if "tab" in pending:
            return handleTabs(pending)
        if request.form.has_key("startgame"):
            util.startGame(name)
            return render_template("index.html",players=util.getPlayers(name),creator=True,started=True)
        if request.form.has_key("checkin"):
            if util.gameStarted(session["game"]):
                util.callForForce(session["game"],util.getTarget(session["game"],session["user"]))
            if session["user"] == util.getCreator(name):
                return render_template("index.html",players=util.getPlayers(name),creator=True,started=util.gameStarted(name))
            else:
                return render_template("index.html",players=util.getPlayers(name),ceator=False)
        if request.form.has_key("kill"):
            if not util.tryKill(name,session["user"]):
                return redirect(url_for("home"))
            if session["user"] == util.getCreator(name):
                return render_template("index.html",players=util.getPlayers(name),creator=True,started=util.gameStarted(name))
            else:
                return render_template("index.html",players=util.getPlayers(name),ceator=False)
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="GET":
        return render_template("login.html")	
    else:
        pending = request.form.keys()[0]
        if "tab" in pending:
            return handleTabs(pending)
        else: 
            if request.form.has_key("submitlogin"):
                user = str(request.form["Username"])
                password = str(request.form["Password"])
                validate = util.checkUserPass(user,password)
                if validate == 0:
                    #User doesn't exist
                    return render_template("login.html")
                if validate == True:
                    session['user'] = user
                    return redirect(url_for("home"))
                if validate == False:
                    #Password Incorrect
                    return render_template("login.html")

@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="GET":
        return render_template("signup.html")
    else:
        pending = request.form.keys()[0]
        if "tab" in pending:
            return handleTabs(pending)
        user = str(request.form["user"])
        password = str(request.form["pass1"])
        if request.form.has_key("back"):
            return redirect(url_for("home"))
        if user == "":
            return render_template("signup.html",nouser=True)
        if password == "":
            return render_template("signup.html",nopassword=True)
        elif password != str(request.form["pass2"]):
            return render_template("signup.html",notmatching=True)
        if util.createUser(user,password):
            return redirect(url_for("login"))
        else:
            return render_template("signup.html",taken=True)

@app.route("/creategame",methods=["POST","GET"])
def creategame():
    if request.method == "GET":
        if 'user' not in session:
            return redirect(url_for("login"))
        return render_template("creategame.html")
    else:
        pending = request.form.keys()[0]
        if "tab" in pending:
            return handleTabs(pending)
        if request.form.has_key("back"):
            return redirect(url_for("home"))
        if request.form.has_key("submitgame"):
            name = str(request.form["name"])
            password = str(request.form["pass1"])
            if not util.createGame(session["user"],password,name):
                return render_template("creategame.html",taken=True)
            return redirect(url_for("game",name=name))

@app.route("/joingame",methods=["POST","GET"])
def joingame():
    if request.method == "GET":
        if 'user' not in session:
            return redirect(url_for("login"))
        return render_template("joingame.html",games=util.getGameInfos(session["user"]))
    else:
        pending = request.form.keys()[0]
        if "tab" in pending:
            return handleTabs(pending)
        if request.form.has_key("submitjoin"):
            name = str(request.form["Gamename"])
            password = str(request.form["Password"])
            if util.checkGamePass(name,password):
                util.addPlayer(name,session["user"])
                session["game"] = name 
                return redirect(url_for("game",name=name))
            else:
                return render_template("joingame.html",games=util.getGameInfos(session["user"]))

def handleTabs(pressed):
    if "home" in pressed:
        return redirect(url_for("home"))
    if "login" in pressed:
        return redirect(url_for("login"))
    if "signup" in pressed:
        return redirect(url_for("signup"))
    if "creategame" in pressed:
        return redirect(url_for("creategame"))
    if "joingame" in pressed:
        return redirect(url_for("joingame"))

@app.route("/updatelocation")
def updatelocation():
    xcor = request.args.get('xcor', '-1',type=float)
    ycor = request.args.get('ycor', '-1',type=float)
    util.setLoc(session["game"] ,session["user"], [xcor, ycor])
    if session["user"] == util.getCreator(session["game"]):
        return render_template("index.html",players=util.getPlayers(session["game"]),creator=True,started=util.gameStarted(session["game"]))
    else:
        return render_template("index.html",player=util.getPlayers(session["game"]))

@app.route("/getCurrentUser")
def getCurrentUser():
    return json.dumps(session["user"])

@app.route("/getCurrentGame")
def getCurrentGame():
    return json.dumps(session["game"])

@app.route("/getTarget")
def getTarget():
    target = util.getTarget(session["game"], session["user"])
    return json.dumps(target)

@app.route("/getPursuer")
def getPursuer():
    pursuer = util.getPursuer(session["game"], session["user"])
    return json.dumps(pursuer)

@app.route("/getTargetLocation")
def getTargetLocation():
    location = util.getLoc(session["game"], util.getTarget(session["game"], session["user"]));
    return json.dumps(location)

@app.route("/getPursuerLocation")
def getPursuerLoction():
    location = util.getLoc(session["game"], util.getPursuer(session["game"], session["user"]));
    return json.dumps(location)

@app.route("/alive")
def alive():
    alive = util.isAlive(session["game"],session["user"])
    return json.dumps(alive)

@app.route("/started")
def started():
    return json.dumps(util.gameStarted(session["game"]))

@app.route("/alllocs")
def alllocs():
    alllocs = util.getAllLocs(session["game"])
    return json.dumps(alllocs)

@app.route("/dead")
def dead():
    return redirect(url_for("home"))

@app.route("/pcheckin")
def pcheckin():
    result = util.checkForce(session["game"],session["user"])
    return json.dumps(result)

if __name__=="__main__":
    app.run(host='0.0.0.0', port=7305, debug=False)
