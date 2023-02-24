from database import Base, conn_engine
import os

from flask import Flask


app = Flask(__name__)

from views import *

if __name__ == "__main__":
    
    if not os.path.exists("noderoot.db"):
        pass
    Base.metadata.create_all(conn_engine)
    app.run(debug = True)