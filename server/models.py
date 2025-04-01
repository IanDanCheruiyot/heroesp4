from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    serialize_rules = ('-hero_power.heroes',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    def less_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name

        }

    # Add the relationship
    hero_power = db.relationship('HeroPower', back_populates='heroes', cascade='all, delete')
    powers = association_proxy('hero_power', 'powers', creator=lambda power_obj: HeroPower(power=power_obj))


    def __repr__(self):
        return f'<Hero {self.id}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    # add serialization rules
    serialize_rules = ('-hero_power.power',)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    def less_dict(self):
        return {
            'description': self.description,
            'id': self.id,
            'name': self.name
        }
    # add relationship
    hero_power = db.relationship('HeroPower', back_populates='power', cascade='all, delete')

    heroes = association_proxy('hero_powers', 'heroes', creator=lambda hero_obj:HeroPower(hero=hero_obj))


    # add validation
    @validates('description')
    def validate_description(self, key, description):
        if description and len(description) >= 20:
            return description
        else:
            raise ValueError('Description must be present and at least 20 characters long')


    def __repr__(self):
        return f'<Power {self.id}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    # add serialization rules
    serialize_rules = ('-power.hero_power', '-heroes.hero_power')

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    # add relationships
    heroes_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    powers_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    power = db.relationship('Power', back_populates='hero_power')
    heroes = db.relationship('Hero', back_populates='hero_power')

    def less_dict(self):
        return {
            'strength': self.strength,
            'power_id': self.powers_id,
            'hero_id': self.heroes_id
        }

    # add validation
    @validates('strength')
    def validate_strength(self, key, strength):
        if strength in {'Strong', 'Weak', 'Average'}:
            return strength
        else:
            raise ValueError('Strength should be Strong, Weak, or Average')


    def __repr__(self):
        return f'<HeroPower {self.id}>'