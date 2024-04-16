"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "akina123"

connect_db(app)

@app.route("/")
def root():
    """render homepage."""

    return render_template("index.html")

@app.route('/api/cupcakes')
def get_cupcakes():
    """returns all cupcakes."""
    cupcakes = Cupcake.query.all()
    result = [cupcake.to_dict() for cupcake in cupcakes]
    return jsonify(cupcakes=result)


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """returns specific cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """creates new cupcake based on data entered by user"""
    data = request.json
    new_cupcake = Cupcake(
        flavor=data.get('flavor'),
        size=data.get('size'),
        rating=data.get('rating'),
        image=data.get('image', "https://tinyurl.com/demo-cupcake")
    )
    db.session.add(new_cupcake)
    db.session.commit()
    return jsonify(cupcake=new_cupcake.to_dict()), 201

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """updates cupcake data based on data entered by user"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json
    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """deletes cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")

if __name__ == "__main__":
    app.run(debug=True)