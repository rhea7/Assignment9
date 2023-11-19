from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barky.db'
db = SQLAlchemy(app)

# Separate the read model from the write model (CQRS)
class Bookmark(db.Model):
    __tablename__ = 'bookmark'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200))

# Unit of Work
class UnitOfWork:
    # Using scoped_session for thread-local session
    session_factory = scoped_session(sessionmaker(bind=db.engine))

    @contextmanager
    def start(self):
        session = self.session_factory()
        try:
            yield
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

# DI Bootstrapping
class Container:
    def __init__(self):
        self.uow = UnitOfWork()
        self.message_bus = MessageBus()
        self.configure()

    def configure(self):
        # Setting up the message bus with command handlers and event handlers
        # This would include handlers like AddBookmarkCommandHandler, etc.
        pass

# Command Handler example
class CommandHandler:
    def handle(self, command):
        raise NotImplementedError

# Message Bus
class MessageBus:
    def __init__(self):
        self.command_handlers = {}
        self.event_handlers = {}

    def register_command_handler(self, command_type, handler):
        self.command_handlers[command_type] = handler

    def handle(self, command):
        handler = self.command_handlers[type(command)]
        handler.handle(command)

# Application services would be refactored to use the command pattern
# Commands
class AddBookmarkCommand:
    def __init__(self, title, url, description):
        self.title = title
        self.url = url
        self.description = description

# Command Handlers
class AddBookmarkCommandHandler(CommandHandler):
    def __init__(self, uow):
        self.uow = uow

    def handle(self, command):
        with self.uow.start():
            bookmark = Bookmark(title=command.title, url=command.url, description=command.description)
            db.session.add(bookmark)
            # No need to call commit as it will be handled by the Unit of Work context manager

# Flask routes would use the message bus to handle incoming commands
@app.route('/bookmarks', methods=['POST'])
def add_bookmark():
    data = request.json
    command = AddBookmarkCommand(data['title'], data['url'], data['description'])
    # Assuming container is a global or app context variable
    container.message_bus.handle(command)
    return jsonify({}), 201

# More Flask routes for different CRUD operations

# Initializing the DI container
container = Container()

if __name__ == '__main__':
    app.run(debug=True)
