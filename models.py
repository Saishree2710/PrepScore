from extensions import db
from sqlalchemy.sql import func
from datetime import date


class User(db.Model):
    __tablename__="users"
    user_id=db.Column(
        db.Integer,
        primary_key=True
    )
    name=db.Column(
        db.String(100),
        nullable=False
    )
    email=db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )
    password_hash=db.Column(
        db.String(255),
        nullable=False
    )
    created_at=db.Column(
        db.DateTime,
        server_default=func.now()
    )
class Topic(db.Model):
    
    __tablename__="topics"
    topic_id=db.Column(
        db.Integer,
        primary_key=True
    )    
    topic_name=db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

class Subtopic(db.Model):
     __tablename__="subtopics"
     subtopic_id=db.Column(
         db.Integer,
         primary_key=True
     )
     subtopic_name=db.Column(
         db.String(255),
         unique=True,
         nullable=False
     )
     topic_id=db.Column(
         db.Integer,
         db.ForeignKey("topics.topic_id",ondelete="CASCADE"),
         nullable=False
     )

class PracticeLog(db.Model):
    
    __tablename__="practice_logs"
    practice_id=db.Column(
        db.Integer,
        primary_key=True
    )  
    user_id=db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )
    subtopic_id=db.Column(
        db.Integer,
        db.ForeignKey("subtopics.subtopic_id"),
        nullable=False
    )   
    questions_solved=db.Column(
        db.Integer,
        nullable=False
    )
    practice_date=db.Column(
        db.Date,
        default=date.today,
        nullable=False
    )
    
        