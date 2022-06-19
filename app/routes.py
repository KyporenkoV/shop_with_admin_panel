from app import pwdApp, render_template, session, redirect, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(pwdApp)


class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer, unique=True, nullable=False)
    processor = db.Column(db.String(30), nullable=False)
    display = db.Column(db.String(30), nullable=False)
    camera = db.Column(db.String(30), nullable=False)
    memory = db.Column(db.String(30), nullable=False)
    os = db.Column(db.String(20), nullable=False)
    img = db.Column(db.String(200), nullable=False)
    reviev = db.Column(db.String(1000), nullable=False)

    simcards = db.Column(db.String(1000), nullable=False)
    batery = db.Column(db.String(1000), nullable=False)
    charger = db.Column(db.String(1000), nullable=False)
    material = db.Column(db.String(1000), nullable=False)
    sizes = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return self.name


# ============== routes ==========================

@pwdApp.route('/', methods=['GET'])
def index():
    goods = Goods.query.all()
    return render_template('index.html', data=goods)


@pwdApp.route('/card/<int:card_id>', methods=['GET'])
def card(card_id):
    goods = Goods.query.get(card_id)
    return render_template('card.html', data=goods)


@pwdApp.route('/add', methods=['GET', 'POST'])
def add_goods():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        processor = request.form['processor']
        display = request.form['display']
        camera = request.form['camera']
        os = request.form['os']
        memory = request.form['memory']
        img = request.form['img']
        simcards = request.form['simcards']
        review = request.form['review']
        batery = request.form['batery']
        charger = request.form['charger']
        material = request.form['material']
        sizes = request.form['sizes']
        goods = Goods(name=name, price=price, processor=processor,
                      display=display, camera=camera, os=os, memory=memory,
                      img=img, simcards=simcards, reviev=review, batery=batery,
                      charger=charger, material=material, sizes=sizes)
        try:
            db.session.add(goods)
            db.session.commit()
            return redirect('/')
        except Exception as error:
            print(f'error with adding goods into DB "Goods": {error}')
    else:
        return render_template('add.html')


@pwdApp.route('/checkout/<int:cid>', methods=['GET', 'POST'])
def checkout(cid):
    cur_goods = Goods.query.get(cid)
    if request.method == 'GET':
        return render_template('checkout.html', data=cur_goods)
    elif request.method == 'POST':

        current_order = dict()

        current_order['firstName'] = request.form['firstName']
        current_order['lastName'] = request.form['lastName']
        current_order['phone'] = request.form['phone']
        current_order['email'] = request.form['email']
        current_order['address'] = request.form['address']
        current_order['cc_name'] = request.form['cc_name']
        current_order['cc_number'] = request.form['cc_number']
        current_order['cc_expiration'] = request.form['cc_expiration']
        current_order['cc_cvv'] = request.form['cc_cvv']

        current_order['goods_name'] = cur_goods.name
        current_order['goods_price'] = cur_goods.price

        session['current_order'] = current_order
        return redirect('/order')
    else:
        print('use incorrect method on checkout page')


@pwdApp.route('/order', methods=['GET'])
def order():
    current_order = session.get('current_order', None)
    return render_template('order.html', current_order=current_order)


# ============== errorhandlers ==========================
@pwdApp.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html'), 404

