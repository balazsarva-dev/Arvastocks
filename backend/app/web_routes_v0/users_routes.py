# from app.settings import login_required
# from app.sign_up_in import (
#     sign_up_user,
#     authenticate_user,
#     delete_user_from_db,
#     registration_accepted_message,
#     update_password,
#     update_email,
# )
# from flask import request, render_template, flash, session, redirect, url_for, g
# from app.forms import RegistrationForm, LoginForm, ChangePasswordForm, UpdateEmailForm
# from app import app


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     form = RegistrationForm()
#     if request.method == "POST":
#         if form.validate_on_submit():
#             username = form.username.data
#             email = form.email.data
#             password = form.password.data
#             signed_up_user = sign_up_user(username, password, email)
#             if signed_up_user:
#                 flash("User registered successfully! ", "success")
#                 registration_accepted_message(username, email)
#                 return redirect(url_for("login"))
#             else:
#                 flash("Failed to register user! ", "error")
#         else:
#             flash("Invalid inputs. Please try again! ", "error")
#     return render_template("register.html", form=form)


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if request.method == "POST":
#         if form.validate_on_submit():
#             username = form.username.data
#             password = form.password.data
#             auth_success = authenticate_user(username, password)
#             if auth_success:
#                 flash("Signed in successfully! ", "success")
#                 return redirect(url_for("home"))
#             else:
#                 flash("Failed to sign in! ", "error")
#         else:
#             flash("Invalid username or password! Please try again. ", "error")
#     return render_template("login.html", form=form)


# @app.route("/logout")
# @login_required
# def logout():
#     session.clear()
#     flash("Signed out successfully! ", "success")
#     return redirect(url_for("home"))


# @app.route("/profile")
# @login_required
# def profile():
#     return render_template("profile.html")


# @app.route("/change_password", methods=["GET", "POST"])
# @login_required
# def change_password():
#     form = ChangePasswordForm()
#     if request.method == "POST":
#         if form.validate_on_submit():
#             old_password = form.old_password.data
#             new_password = form.new_password.data
#             username = g.user["username"]
#             password_updated = update_password(username, old_password, new_password)
#             if password_updated:
#                 flash("Password updated successfully! ", "success")
#                 return redirect(url_for("profile"))
#             else:
#                 flash("Invalid password! ", "error")
#         else:
#             flash("Invalid inputs. Please try again! ", "error")
#     return render_template("change_password.html", new_password_form=form)


# @app.route("/change_email", methods=["GET", "POST"])
# @login_required
# def change_email():
#     form = UpdateEmailForm()
#     if request.method == "POST":
#         if form.validate_on_submit():
#             new_email = form.email.data
#             username = g.user["username"]
#             password = form.password.data
#             email_updated = update_email(username, new_email, password)
#             if email_updated:
#                 flash("Email changed successfully! ", "success")
#                 return redirect(url_for("profile"))
#             else:
#                 flash("Failed to change email! ", "error")
#         else:
#             flash("Invalid inputs. Please try again! ", "error")
#     return render_template("change_email.html", new_email_form=form)


# @app.route("/delete")
# @login_required
# def delete():
#     username = g.user["username"]
#     email = g.user["email"]
#     deleted_user = delete_user_from_db(username, email)
#     return redirect(url_for("home")) if deleted_user else redirect(url_for("profile"))
