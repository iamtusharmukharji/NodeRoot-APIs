from main import app
from routers import users, devices



app.route("/user/signup/", methods = ["POST"])(users.signup)
app.route("/user/get/", methods = ["GET"])(users.get_user_detail)
app.route("/device/enroll/", methods = ["POST"])(devices.enroll_device)