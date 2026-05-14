from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'worldcup2026secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///worldcup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    predictions = db.relationship('Prediction', backref='user', lazy=True)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_team = db.Column(db.String(100), nullable=False)
    away_team = db.Column(db.String(100), nullable=False)
    match_date = db.Column(db.String(50), nullable=False)
    stage = db.Column(db.String(50), nullable=False)
    home_score = db.Column(db.Integer, nullable=True)
    away_score = db.Column(db.Integer, nullable=True)
    predictions = db.relationship('Prediction', backref='match', lazy=True)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    home_score = db.Column(db.Integer, nullable=False)
    away_score = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def seed_matches():
    if Match.query.count() == 0:
        matches = [
            # Group A
            Match(home_team="Mexico", away_team="South Africa", match_date="2026-06-11", stage="Group A"),
            Match(home_team="South Korea", away_team="Czechia", match_date="2026-06-12", stage="Group A"),
            Match(home_team="Mexico", away_team="Czechia", match_date="2026-06-15", stage="Group A"),
            Match(home_team="South Africa", away_team="South Korea", match_date="2026-06-15", stage="Group A"),
            Match(home_team="South Africa", away_team="Czechia", match_date="2026-06-19", stage="Group A"),
            Match(home_team="Mexico", away_team="South Korea", match_date="2026-06-19", stage="Group A"),
            # Group B
            Match(home_team="Canada", away_team="Bosnia-Herzegovina", match_date="2026-06-12", stage="Group B"),
            Match(home_team="Switzerland", away_team="Qatar", match_date="2026-06-12", stage="Group B"),
            Match(home_team="Canada", away_team="Qatar", match_date="2026-06-16", stage="Group B"),
            Match(home_team="Switzerland", away_team="Bosnia-Herzegovina", match_date="2026-06-16", stage="Group B"),
            Match(home_team="Canada", away_team="Switzerland", match_date="2026-06-20", stage="Group B"),
            Match(home_team="Qatar", away_team="Bosnia-Herzegovina", match_date="2026-06-20", stage="Group B"),
            # Group C
            Match(home_team="Argentina", away_team="Albania", match_date="2026-06-12", stage="Group C"),
            Match(home_team="Ukraine", away_team="Chile", match_date="2026-06-13", stage="Group C"),
            Match(home_team="Argentina", away_team="Chile", match_date="2026-06-16", stage="Group C"),
            Match(home_team="Ukraine", away_team="Albania", match_date="2026-06-17", stage="Group C"),
            Match(home_team="Argentina", away_team="Ukraine", match_date="2026-06-20", stage="Group C"),
            Match(home_team="Chile", away_team="Albania", match_date="2026-06-20", stage="Group C"),
            # Group D
            Match(home_team="USA", away_team="Paraguay", match_date="2026-06-12", stage="Group D"),
            Match(home_team="Australia", away_team="Turkiye", match_date="2026-06-13", stage="Group D"),
            Match(home_team="USA", away_team="Australia", match_date="2026-06-17", stage="Group D"),
            Match(home_team="Turkiye", away_team="Paraguay", match_date="2026-06-17", stage="Group D"),
            Match(home_team="USA", away_team="Turkiye", match_date="2026-06-21", stage="Group D"),
            Match(home_team="Paraguay", away_team="Australia", match_date="2026-06-21", stage="Group D"),
            # Group E
            Match(home_team="Spain", away_team="Brazil", match_date="2026-06-13", stage="Group E"),
            Match(home_team="Japan", away_team="Curacao", match_date="2026-06-14", stage="Group E"),
            Match(home_team="Spain", away_team="Curacao", match_date="2026-06-17", stage="Group E"),
            Match(home_team="Japan", away_team="Brazil", match_date="2026-06-18", stage="Group E"),
            Match(home_team="Spain", away_team="Japan", match_date="2026-06-21", stage="Group E"),
            Match(home_team="Brazil", away_team="Curacao", match_date="2026-06-21", stage="Group E"),
            # Group F
            Match(home_team="France", away_team="Algeria", match_date="2026-06-14", stage="Group F"),
            Match(home_team="Belgium", away_team="New Zealand", match_date="2026-06-14", stage="Group F"),
            Match(home_team="France", away_team="New Zealand", match_date="2026-06-18", stage="Group F"),
            Match(home_team="Belgium", away_team="Algeria", match_date="2026-06-18", stage="Group F"),
            Match(home_team="France", away_team="Belgium", match_date="2026-06-22", stage="Group F"),
            Match(home_team="Algeria", away_team="New Zealand", match_date="2026-06-22", stage="Group F"),
            # Group G
            Match(home_team="England", away_team="Croatia", match_date="2026-06-14", stage="Group G"),
            Match(home_team="Senegal", away_team="Sweden", match_date="2026-06-15", stage="Group G"),
            Match(home_team="England", away_team="Sweden", match_date="2026-06-18", stage="Group G"),
            Match(home_team="Senegal", away_team="Croatia", match_date="2026-06-19", stage="Group G"),
            Match(home_team="England", away_team="Senegal", match_date="2026-06-22", stage="Group G"),
            Match(home_team="Croatia", away_team="Sweden", match_date="2026-06-22", stage="Group G"),
            # Group H
            Match(home_team="Portugal", away_team="DR Congo", match_date="2026-06-15", stage="Group H"),
            Match(home_team="Germany", away_team="Iraq", match_date="2026-06-15", stage="Group H"),
            Match(home_team="Portugal", away_team="Iraq", match_date="2026-06-19", stage="Group H"),
            Match(home_team="Germany", away_team="DR Congo", match_date="2026-06-19", stage="Group H"),
            Match(home_team="Portugal", away_team="Germany", match_date="2026-06-23", stage="Group H"),
            Match(home_team="DR Congo", away_team="Iraq", match_date="2026-06-23", stage="Group H"),
        ]
        db.session.add_all(matches)
        db.session.commit()

@app.route('/')
@login_required
def index():
    group = request.args.get('group', 'All')
    groups = ['All', 'Group A', 'Group B', 'Group C', 'Group D', 
              'Group E', 'Group F', 'Group G', 'Group H']
    
    if group == 'All':
        matches = Match.query.order_by(Match.match_date).all()
    else:
        matches = Match.query.filter_by(stage=group).order_by(Match.match_date).all()
    
    user_predictions = {p.match_id: p for p in Prediction.query.filter_by(user_id=current_user.id).all()}
    total_points = sum(p.points for p in user_predictions.values())
    
    return render_template('index.html', 
        matches=matches, 
        predictions=user_predictions, 
        total_points=total_points,
        groups=groups,
        selected_group=group
    )

@app.route('/predict/<int:match_id>', methods=['POST'])
@login_required
def predict(match_id):
    match = Match.query.get_or_404(match_id)
    home = int(request.form.get('home_score', 0))
    away = int(request.form.get('away_score', 0))
    existing = Prediction.query.filter_by(user_id=current_user.id, match_id=match_id).first()
    if existing:
        existing.home_score = home
        existing.away_score = away
    else:
        pred = Prediction(user_id=current_user.id, match_id=match_id, home_score=home, away_score=away)
        db.session.add(pred)
    db.session.commit()
    flash('Prediction saved!', 'success')
    return redirect(url_for('index'))

@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    if request.method == 'POST':
        match_id = int(request.form.get('match_id'))
        home = int(request.form.get('home_score'))
        away = int(request.form.get('away_score'))
        match = Match.query.get(match_id)
        match.home_score = home
        match.away_score = away
        for pred in Prediction.query.filter_by(match_id=match_id).all():
            points = 0
            if pred.home_score == home and pred.away_score == away:
                points = 3
            elif (pred.home_score - pred.away_score) == (home - away):
                points = 1
            elif (pred.home_score > pred.away_score) == (home > away):
                points = 1
            pred.points = points
        db.session.commit()
        flash('Result saved and predictions scored!', 'success')
    matches = Match.query.order_by(Match.match_date).all()
    return render_template('results.html', matches=matches)

@app.route('/leaderboard')
@login_required
def leaderboard():
    users = User.query.all()
    scores = []
    for user in users:
        total = sum(p.points for p in user.predictions)
        scores.append({'username': user.username, 'points': total})
    scores.sort(key=lambda x: x['points'], reverse=True)
    return render_template('leaderboard.html', scores=scores)

@app.route('/rankings')
@login_required
def rankings():
    return render_template('rankings.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return redirect(url_for('register'))
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

with app.app_context():
    db.create_all()
    seed_matches()

if __name__ == '__main__':
    app.run(debug=True)