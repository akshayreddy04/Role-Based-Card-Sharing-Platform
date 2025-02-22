from app import db


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    img_url = db.Column(db.String(200), nullable=True)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "description": self.description,
            "gender": self.gender,
            "imgUrl": self.img_url,
        }


class usersdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }


class UserCardAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey(
        'usersdata.id'), nullable=False)  # Owner of the card
    card_id = db.Column(db.Integer, db.ForeignKey(
        'friend.id'), nullable=False)  # Card being shared
    shared_with_id = db.Column(db.Integer, db.ForeignKey(
        'usersdata.id'), nullable=False)  # User who has access

    # Relationships
    owner = db.relationship("usersdata", foreign_keys=[owner_id])
    card = db.relationship("Friend", foreign_keys=[card_id])
    shared_with = db.relationship("usersdata", foreign_keys=[shared_with_id])

    # Unique constraint: Prevent duplicate access entries
    __table_args__ = (db.UniqueConstraint(
        'card_id', 'shared_with_id', name='unique_card_user'),)

    def to_json(self):
        return {
            "id": self.id,
            "owner_id": self.owner_id,  # Owner ID
            "owner_email": self.owner.email if self.owner else None,  # Owner Email
            "card_id": self.card_id,  # Card ID
            "shared_with_id": self.shared_with_id,  # Shared User ID
            # Shared User Email
            "shared_with_email": self.shared_with.email if self.shared_with else None
        }
