"""A supported downstream target application.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from g2e import db


class TargetApp(db.Model):

    __tablename__ = 'target_app'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    target_app_links = db.relationship("TargetAppLink", backref=db.backref('target_app', order_by=id))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<TargetApp %r>' % self.id