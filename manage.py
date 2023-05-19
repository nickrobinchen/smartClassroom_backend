import os

from app import create_app,db
from app.models import Manager
#from flask_script import Manager, Shell,Server
#from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS, cross_origin

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

cors = CORS(app)
# manager = Manager(app)
# migrate = Migrate(app, db)
#
# # print('xxxxxxxxxxxxxxxx',os.path.abspath('.'))


def make_shell_context():
    return dict(app=app, db=db, User=Manager)


# manager.add_command("shell", Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)
# manager.add_command('runserver',Server(host="0.0.0.0",port=5000,use_debugger=True))

if __name__ == '__main__':
    app.run(host='0.0.0.0')