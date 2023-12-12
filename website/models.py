from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func, desc


class Wildshape(db.Model):
    class_id = db.Column(db.Integer, db.ForeignKey('classtype.id'))
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    req_lvl = db.Column(db.Integer)
    dmg_type = db.Column(db.String(150))
    dmg_stat = db.Column(db.Integer)
    hit_dice = db.Column(db.String(150))
    temp_ac = db.Column(db.Integer)
    temp_hp = db.Column(db.Integer)
    
class Spell(db.Model):
    class_id = db.Column(db.Integer, db.ForeignKey('classtype.id'))
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    spell_lvl = db.Column(db.Integer)
    dmg_type = db.Column(db.String(150))
    dmg_basestat = db.Column(db.Integer)
    dmg_perlvl = db.Column(db.Integer)
    hit_dice = db.Column(db.String(150))
    
class Weapon(db.Model):
    class_id = db.Column(db.Integer, db.ForeignKey('classtype.id'))
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    req_lvl = db.Column(db.Integer)
    dmg_type = db.Column(db.String(150))
    dmg_basestat = db.Column(db.Integer)
    hit_dice = db.Column(db.String(150))
    twohand = db.Column(db.Integer)
    
class Armor(db.Model):
    class_id = db.Column(db.Integer, db.ForeignKey('classtype.id'))
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    ac_stat = db.Column(db.Integer)
    ac_buff = db.Column(db.String(150))
    req = db.Column(db.String(150))
    
class Classtype(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(150))
    skill1 = db.Column(db.String(3))
    skill2 = db.Column(db.String(3))
    main_prof = db.Column(db.String(150))
    base_hp = db.Column(db.Integer)
    hp_per_lvl = db.Column(db.Integer)
    extra_atk = db.Column(db.Integer)
    armor = db.relationship('Armor')
    weapons = db.relationship('Weapon')
    spells = db.relationship('Spell')
    wildshape = db.relationship('Wildshape')
    shield = db.Column(db.Integer)
    
class Player(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(150))
    class_name = db.Column(db.String(150))
    level = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    atk_count = db.Column(db.Integer)
    str_stat = db.Column(db.Integer)
    dex_stat = db.Column(db.Integer)
    con_stat = db.Column(db.Integer)
    int_stat = db.Column(db.Integer)
    wis_stat = db.Column(db.Integer)
    car_stat = db.Column(db.Integer)
    wildshape_name = db.Column(db.String(150))
    armor_name = db.Column(db.String(150))
    ac = db.Column(db.Integer)
    weapon_name = db.Column(db.String(150))
    weapon_dmg = db.Column(db.Integer)
    spell_name = db.Column(db.String(150))
    spell_dmg = db.Column(db.Integer)
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    players = db.relationship('Player')