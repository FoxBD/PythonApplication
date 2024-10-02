from app import db

# image fills the whole URL of an image, mimetype unused and is always null
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.Text, nullable=True)
    mimetype = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'mimetype': self.mimetype
        }