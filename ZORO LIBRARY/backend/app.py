from flask import Flask, request, jsonify, Response
from flask_session import Session
from config import Config
from models import *
from datetime import datetime, timedelta
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies, decode_token
from sqlalchemy import create_engine, func, or_
from sqlalchemy.orm import sessionmaker
import workers, tasks
from flask_mail import Mail
from io import StringIO
import csv
from flask_caching import Cache
from flask_crontab import Crontab

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)
db.init_app(app)
cache = Cache(app)
ma.init_app(app)
bcrypt.init_app(app)
crontab = Crontab(app)
mail = Mail(app)

celery = workers.celery
celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND']
)
celery.Task = workers.ContextTask
app.app_context().push()

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
session = Session()

def CreateAdmin():
    user = User.query.filter_by(email="librarian@gmail.com").first()
    if not user:
        new_user = User(email="librarian@gmail.com", name="librarian", password="admin123", active_books=0, is_flagged=0, last_loggedin=datetime.now())
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
    return "Admin Created"

with app.app_context():
    db.create_all()
    CreateAdmin()


CORS(app, supports_credentials=True)

# Landing Page
@app.route("/")
def home():
    return "Hello World!"

# Updating Active Books
def update_active_books(user_email):
    active_books_count = db.session.query(RequestBook).filter_by(
        user_mail=user_email, is_approved=True, is_returned=False
    ).count()
    
    user = db.session.query(User).filter_by(email=user_email).one()
    user.active_books = active_books_count
    db.session.commit()


# AUTHENTICATION
# Current user
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200


# register
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data["email"]
    name = data["name"]
    password = data["password"]
    active_books = data["active_books"]
    is_flagged = data["is_flagged"]
    last_loggedin = datetime.now()

    if not email or not name or not password:
        return {"error": "All fields are required"}, 400
    
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return {"error": "User already exists"}, 409
    
    new_user = User(email=email, name=name, password=password, active_books=active_books, is_flagged=is_flagged, last_loggedin=last_loggedin)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to create user"}, 500


# login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    if not email or not password:
        return {"error": "All fields are required"}, 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not bcrypt.check_password_hash(user.password, password):
        return {"error": "Invalid email or password"}, 401
    
    user.last_loggedin = datetime.now()
    db.session.commit()

    access_token = create_access_token(identity={
        "email": user.email
    })

    return jsonify({"access_token": access_token, "message": "Login successful"}), 200


# get user details
@app.route('/getuserinfo', methods=['GET'])
@jwt_required()
def getuserinfo():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user["email"]).first()
    user_data = user_schema.dump(user)
    return jsonify(user_data), 200
    
    
# logout
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'message': 'logout successful'})
    unset_jwt_cookies(response)
    return response

# flag user
@app.route('/flag_user', methods=['POST'])
@jwt_required()
def flag_user():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_flagged = True
    db.session.commit()
    return jsonify({"message": "User flagged successfully"}), 200

# unflag user
@app.route('/unflag_user', methods=['POST'])
@jwt_required()
def unflag_user():
    try:
        current_user_identity = get_jwt_identity()
        if not current_user_identity:
            return jsonify({'error': 'User identity not found in token'}), 400

        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({'error': 'Email is required'}), 400

        user = User.query.get(email)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user.is_flagged = False
        db.session.commit()

        return jsonify({'message': 'User unflagged successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# SEARCH
@app.route('/search', methods=['GET'])
@jwt_required()
def search():
    query = request.args.get('q', '')

    sections = Section.query.filter(
        Section.name.ilike(f'%{query}%')
    ).all()

    books = Book.query.filter(
        or_(
            Book.name.ilike(f'%{query}%'),
            Book.author.ilike(f'%{query}%'),
            Book.genre.ilike(f'%{query}%')
        )
    ).all()

    results = {
        'sections': sections_schema.dump(sections),
        'books': books_schema.dump(books)
    }

    return jsonify(results)


# ADMIN STATS
@app.route('/admin_stats', methods=['GET'])
@jwt_required()
def admin_stats():
    try:
        total_users = User.query.count() - 1
        flagged_users = User.query.filter_by(is_flagged=True).count()

        sections = Section.query.all()
        section_stats = []
        for section in sections:
            section_stats.append({
                "section_name": section.name,
                "books_count": len(section.books)
            })

        most_requested = db.session.query(
            RequestBook.book_id, db.func.count(RequestBook.id).label('request_count')
        ).group_by(RequestBook.book_id).order_by(db.desc('request_count')).first()

        most_requested_book = None
        if most_requested:
            book = Book.query.get(most_requested.book_id)
            most_requested_book = {
                "book_name": book.name,
                "author": book.author,
                "request_count": most_requested.request_count
            }

        overdue_date = datetime.now() - timedelta(days=7)
        overdue_requests = RequestBook.query.filter(
            RequestBook.issue_date < overdue_date,
            RequestBook.is_returned.is_(False)
        ).all()

        overdue_users = {}
        for request in overdue_requests:
            if User.query.filter_by(email=request.user_mail, is_flagged=True).first():
                continue

            if request.user_mail not in overdue_users:
                overdue_users[request.user_mail] = {
                    "user_email": request.user_mail,
                    "overdue_requests_count": 0
                }
            overdue_users[request.user_mail]["overdue_requests_count"] += 1

        overdue_users_stats = list(overdue_users.values())

        all_users = User.query.all()
        all_users_stats = []
        for user in all_users:
            all_users_stats.append({
                "user_email": user.email,
                "is_flagged": user.is_flagged
            })

        admin_stats = {
            "user_stats": {
                "total_users": total_users,
                "flagged_users": flagged_users,
                "overdue_users": overdue_users_stats,
                "all_users": all_users_stats
            },
            "books_section_stats": section_stats,
            "most_requested_book": most_requested_book
        }

        return jsonify(admin_stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# SECTIONS 
# read all sections
@app.route("/section", methods=['GET'])
@jwt_required()
def sections():
    sections = Section.query.all()
    sections_data = sections_schema.dump(sections)
    return jsonify(sections_data), 200
    
    
# create
@app.route("/create_section", methods=['POST'])
@jwt_required()
def create_sections():
    data = request.json
    name = data["name"]
    description = data["description"]
    
    if not name or not description:
        return {"error": "All fields are required"}, 400
    
    existing_section = Section.query.filter_by(name=name).first()

    if existing_section:
        return {"error": "Section already exists"}, 409
    
    new_section = Section(name=name, description=description)
    
    try:
        db.session.add(new_section)
        db.session.commit()
        return {"message": "Section created successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to create section"}, 500
    
    
# view section
@app.route('/view_section/<int:id>', methods=['GET'])
@jwt_required()
def view_section(id):
    section = Section.query.get(id)
    if not section:
        return jsonify({"error": "Section not found"}), 404

    books = Book.query.filter_by(section_id=id).all()
    section_data = section_schema.dump(section)
    books_data = books_schema.dump(books)

    response = {
        "section": section_data,
        "books": books_data
    }

    return jsonify(response), 200


# update
@app.route('/update_section/<int:id>', methods=['PUT'])
@jwt_required()
def update_section(id):
    data = request.json
    name = data.get("name")
    description = data.get("description")

    if not name and not description:
        return {"error": "Name or description is required"}, 400

    section = Section.query.filter_by(id=id).first()
    if not section:
        return {"error": "Section not found"}, 404

    existing_section_by_name = Section.query.filter_by(name=name).first()
    if existing_section_by_name and existing_section_by_name.id != section.id:
        return {"error": "Section with this name already exists"}, 409

    section.name = name if name else section.name
    section.description = description if description else section.description

    try:
        db.session.commit()
        return {"message": "Section updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to update section"}, 500
    
    
# delete
@app.route('/delete_section/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_section(id):
    section = Section.query.filter_by(id=id).first()
    try:
        if section:
            books = section.books
            for book in books:
                requests = db.session.query(RequestBook).filter_by(book_id=book.id, is_approved=True, is_returned=False).all()
                for request in requests:
                    update_active_books(request.user_mail)
            db.session.delete(section)
            db.session.commit()
            return {"message": "Section deleted successfully"}, 200
        else:
            return {"error": "Section not found"}, 404
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to delete section"}, 500
    
# BOOKS
# read all books
@app.route("/book", methods=['GET'])
@jwt_required()
def books():
    books = Book.query.all()
    books_data = books_schema.dump(books)
    return jsonify(books_data), 200


# create
@app.route("/create_book", methods=['POST'])
@jwt_required()
def create_books():
    data = request.json
    name = data["name"]
    author = data["author"]
    genre = data["genre"]
    section_id = data["section_id"]
    content = data["content"]
    
    if not name or not author or not genre or not section_id or not content:
        return {"error": "All fields are required"}, 400
    
    existing_book = Book.query.filter_by(name=name).first()

    if existing_book:
        return {"error": "Book already exists"}, 409
    
    new_book = Book(name=name, author=author, genre=genre, section_id=section_id, content=content)
    
    try:
        db.session.add(new_book)
        db.session.commit()
        return {"message": "Book created successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to create book"}, 500
    

# view book
@app.route('/view_book/<int:id>', methods=['GET'])
@jwt_required()
def view_book(id):
    book = Book.query.filter_by(id=id).first()
    if not book:
        return {"error": "Book not found"}, 404
    book_data = book_schema.dump(book)
    return jsonify(book_data), 200


# update
@app.route('/update_book/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    data = request.json
    name = data["name"]
    author = data["author"]
    genre = data["genre"]
    section_id = data["section_id"]
    content = data["content"]

    if not name and not author and not genre and not section_id and not content:
        return {"error": "Some field is required"}, 400

    book = Book.query.filter_by(id=id).first()
    if not book:
        return {"error": "Book not found"}, 404

    existing_book_by_name = Book.query.filter_by(name=name).first()
    if existing_book_by_name and existing_book_by_name.id != book.id:
        return {"error": "Book with this name already exists"}, 409

    book.name = name if name else book.name
    book.author = author if author else book.author
    book.genre = genre if genre else book.name
    book.section_id = section_id if section_id else book.name
    book.content = content if content else book.name

    try:
        db.session.commit()
        return {"message": "Book updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to update book"}, 500


# delete
@app.route('/delete_book/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    book = Book.query.filter_by(id=id).first()
    try:
        if book:
            requests = db.session.query(RequestBook).filter_by(book_id=book.id, is_approved=True, is_returned=False).all()
            db.session.delete(book)
            db.session.commit()
            for request in requests:
                update_active_books(request.user_mail)
            return {"message": "Book deleted successfully"}, 200
        else:
            return {"error": "Book not found"}, 404
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to delete book"}, 500
    
# my books
@app.route('/my_books', methods=['GET'])
@jwt_required()
def get_my_books():
    try:
        current_user_email = get_jwt_identity()['email']
        approved_requests = RequestBook.query.filter_by(user_mail=current_user_email, is_approved=True).all()
        
        result = []
        for request in approved_requests:
            book = Book.query.get(request.book_id)
            result.append(book_schema.dump(book))
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
    
# return book
@app.route('/return_book/<int:id>', methods=['PUT'])
@jwt_required()
def return_book(id):
    try:
        data = request.json
        is_approved = data.get('is_approved', False)
        is_returned = data.get('is_returned', True)

        request_book = RequestBook.query.filter_by(book_id=id, is_approved=True, is_returned=False).first()
        if not request_book:
            return jsonify({'error': 'Request record not found for the book'}), 404

        # Update request_book status
        request_book.is_approved = is_approved
        request_book.is_returned = is_returned
        request_book.return_date = datetime.now()

        # Get the current user email from the JWT token
        current_user = get_jwt_identity()
        if 'email' not in current_user:
            return jsonify({'error': 'Invalid JWT token: Email not found'}), 401

        user_email = current_user['email']
        user = User.query.get(user_email)
        if not user:
            return jsonify({'error': f'User with email {user_email} not found'}), 404

        if user.active_books > 0:
            user.active_books -= 1

        db.session.commit()

        return jsonify({'message': 'Book returned successfully', 'request_book': request_book_schema.dump(request_book)}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    
# REQUESTBOOK
# requesting books
@app.route('/request_book/<int:id>', methods=['POST'])
@jwt_required()
def request_book(id):
    try:
        current_user_identity = get_jwt_identity()
        if not current_user_identity:
            return jsonify({'error': 'User identity not found in token'}), 400

        current_user_email = current_user_identity['email']

        user = User.query.filter_by(email=current_user_email).first()
        if user.is_flagged:
            return jsonify({'error': 'You are flagged and cannot request books.'}), 403

        existing_approved_request = RequestBook.query.filter_by(
            user_mail=current_user_email, book_id=id, is_requested=False, is_approved=True
        ).first()
        if existing_approved_request:
            return jsonify({"error": "Your book request has been approved. Please check My Books."}), 409

        existing_pending_request = RequestBook.query.filter_by(
            user_mail=current_user_email, book_id=id, is_requested=True
        ).first()
        if existing_pending_request:
            return jsonify({'error': 'Book has already been requested'}), 400

        user = User.query.get(current_user_email)
        if user.active_books >= 5:
            return jsonify({"error": "You have reached the maximum limit of active books."}), 400

        new_request = RequestBook(
            user_mail=current_user_email,
            book_id=id,
            is_requested=True
        )

        db.session.add(new_request)
        db.session.commit()

        return jsonify({'message': 'Book requested successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# requests
@app.route('/request', methods=['GET'])
@jwt_required()
def requests():
    try:
        current_user_email = get_jwt_identity()
        current_user_email = current_user_email['email']
        
        if current_user_email == 'librarian@gmail.com':
            requests = RequestBook.query.all()
        else:
            requests = RequestBook.query.filter_by(user_mail=current_user_email).all()

        requests_data = []
        for request in requests:
            request_data = request_book_schema.dump(request)
            book = Book.query.get(request.book_id)
            request_data['book'] = book_schema.dump(book)
            request_data['user_mail'] = request.user_mail
            requests_data.append(request_data)
        
        return jsonify(requests_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# accept request
@app.route('/accept_request/<int:request_id>', methods=['POST'])
@jwt_required()
def accept_request(request_id):
    current_user = get_jwt_identity()

    if current_user["email"] != 'librarian@gmail.com':
        return jsonify({"error": "Only the librarian can accept requests"}), 403

    book_request = RequestBook.query.get(request_id)
    user = User.query.get(book_request.user_mail)
    if user.active_books == 5:
        return jsonify({"error": "User has reached the maximum number of active books"}), 400
    if not book_request:
        return jsonify({"error": "Request not found"}), 404

    book_request.is_requested = False
    book_request.issue_date = datetime.now()
    book_request.is_approved = True
    
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.active_books += 1
    tasks.send_approved_email(book_request.user_mail)
    db.session.commit()
    
    return jsonify({"message": "Book request approved successfully"}), 200


# reject request
@app.route('/reject_request/<int:request_id>', methods=['POST'])
@jwt_required()
def reject_request(request_id):
    current_user = get_jwt_identity()

    if current_user['email'] != 'librarian@gmail.com':
        return jsonify({"error": "Only the librarian can reject requests"}), 403

    book_request = RequestBook.query.get(request_id)
    if not book_request:
        return jsonify({"error": "Request not found"}), 404

    book_request.is_requested = False
    book_request.is_rejected = True
    tasks.send_rejected_email(book_request.user_mail)
    db.session.commit()

    return jsonify({"message": "Book request rejected successfully"}), 200

# FEEDBACK
# submit feedback
@app.route('/feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    user = get_jwt_identity()
    user_email = user['email']
    data = request.get_json()

    book_id = data.get('book_id')
    feedback_text = data.get('feedback')

    if not book_id or not feedback_text:
        return jsonify({'message': 'Book ID and feedback text are required'}), 400

    book = Book.query.get(book_id)

    if not user or not book:
        return jsonify({'message': 'Invalid user or book'}), 404

    feedback = Feedback(user_mail=user_email, book_id=book.id, feedback=feedback_text)
    db.session.add(feedback)
    db.session.commit()

    return jsonify({'message': 'Feedback submitted successfully'}), 201

# view feedbacks
@app.route('/reviews/<int:book_id>', methods=['GET'])
@jwt_required()
def get_reviews(book_id):
    current_user = get_jwt_identity()

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    reviews = Feedback.query.filter_by(book_id=book_id).all()
    if not reviews:
        return jsonify([]), 200

    reviews_list = []
    for review in reviews:
        reviews_list.append({
            'id': review.id,
            'user_mail': review.user_mail,
            'feedback': review.feedback
        })

    return jsonify(reviews_list), 200

# Downloading Report
def generate_csv():
    requests = RequestBook.query.all()
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    
    csv_writer.writerow(['ID', 'User Mail', 'Book ID', 'Issue Date', 'Return Date', 'Status'])
    
    for request in requests:
        if request.is_approved == 1:
            status = 'Approved'
        elif request.is_rejected == 1:
            status = 'Rejected'
        elif request.is_returned == 1:
            status = 'Returned'
        else:
            status = 'Pending'
        csv_writer.writerow([request.id, request.user_mail, request.book_id, request.issue_date, request.return_date, status])
    
    return csv_buffer.getvalue()

@app.route('/download_csv', methods = ['GET'])
def download_csv():
    csv_data = generate_csv()
    return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition':'attachment;filename=requests.csv'})

if __name__ == "__main__":
    app.run(debug=True)
    