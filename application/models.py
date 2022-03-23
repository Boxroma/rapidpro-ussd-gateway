from . import db


class message(db.Model):
    msg_id = db.Column(db.Integer(), primary_key=True)
    tel = db.Column(db.String(20), nullable=False)
    session_id = db.Column(db.String(40), nullable=False)
    received_msg = db.Column(db.String(20), nullable=False)
    response_msg = db.Column(db.String(20))
    received_time = db.Column(db.DateTime(timezone=False), nullable=False)
    response_time = db.Column(db.DateTime(timezone=False))
    received_msg_init = db.Column(db.Boolean(), nullable=False)
    response_continue = db.Column(db.Boolean())
