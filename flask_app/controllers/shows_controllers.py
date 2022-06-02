from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user_model import User
from flask_app.models.show_model import Show




# =================================================
#  Dashboard
# =================================================

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("please register or login before going to site")
        return redirect("/")
    user_id = session["user_id"]     
    # Retrieve the user name
    user_data = {
        'id' : user_id
    }
    user = User.get_by_id(user_data)
    # Retrieve the cars
    shows = Show.get_all_shows()

    return render_template("dashboard.html", user = user, user_id = user_id, shows = shows)

#==================================================
#Route from Dashboard to New Show Page
# =================================================



@app.route("/new/show")
def new_show():
    return render_template("new_show.html")


# ===================================================
# Route from New Show Page to Create New Show
# ===================================================


@app.route("/create/show", methods=["post"])
def create_show():
    # 1 validate form info
    if not Show.validate_show(request.form):
        return redirect("/new/show")
    if 'user_id' not in session:
        flash("Please log in to see this page")
        return redirect('/')
    query_data = {
        "title" : request.form["title"],
        "network" : request.form["network"],
        "release_date" : request.form["release_date"],
        "description" : request.form["description"],        
        "user_id" : session["user_id"]
    }
   
    Show.create_new_show(query_data)
    return redirect("/dashboard")


# =========================================
# Route from Dashboard,One_Show to Delete Show
# =========================================


@app.route("/shows/<int:id>/delete")
def delete_show(id):
    if "user_id" not in session:
        flash("please register or login before going to site")
        return redirect("/")
    user_id = session["user_id"]     
    query_data = {
        "id" : id,
        "user_id" : user_id
    }
    Show.delete_show(query_data)
    return redirect("/dashboard")


# ========================================
# Route from Dashboard to Edit Show Page
# ========================================

@app.route("/shows/edit/<int:id>")
def edit_show_page(id):
    if "user_id" not in session:
        flash("please register or login before going to site")
        return redirect("/")
    user_id = session["user_id"]
    query_data = {
        "id" : id,
        "user_id" : user_id
    }
    show = Show.get_show_by_id(query_data)
    return render_template("edit_show.html", show = show)

# ============================================
# Route to sumbit Edit on Edit Page
# =============================================

@app.route("/shows/<int:id>/edit", methods=["post"])
def edit_show(id):
    # 1 validate form info
    show_id = request.form["show_id"]
    if not Show.validate_show(request.form):
        return redirect(f"/shows/edit/{show_id}")
   
    if "user_id" not in session:
        flash("please register or login before going to site")
        return redirect("/")
    user_id = session["user_id"]     
    query_data = {
        "id" : id,
        "user_id" : user_id,
        "title" : request.form["title"],
        "network" : request.form["network"],
        "release_date" : request.form["release_date"],
        "description" : request.form["description"],
    }
    Show.edit_show(query_data)
    return redirect("/dashboard")




# =====================================
# Route to One Show
# =====================================


@app.route("/shows/<int:id>")
def one_show(id):
    if "user_id" not in session:
        flash("please register or login before going to site")
        return redirect("/")
    query_data = {
        "id" : id
    }
    show = Show.get_show_by_id(query_data)
    return render_template("one_show.html", show = show)