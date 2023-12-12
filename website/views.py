import dataclasses
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Player, Classtype, Armor, Weapon, Spell, Wildshape
from . import db
from sqlalchemy import func, select
import json

views = Blueprint('views', __name__)

@views.route('/delete-player', methods=['POST'])
def delete_player():
    player = json.loads(request.data) 
    playerId = player['playerId']
    player = Player.query.get(playerId)
    if player:
        if player.user_id == current_user.id:
            db.session.delete(player)
            db.session.commit()
    return jsonify({})

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    return render_template("home.html", user=current_user)

@views.route('/locker', methods=['GET', 'POST'])
@login_required
def locker():
    return render_template("locker.html", user=current_user, players=Player.query.filter_by(user_id=current_user.id))

@views.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    return render_template("create.html", user=current_user)

@views.route("/createdetails/<id>", methods=['GET', 'POST'])
@login_required
def createdetails(id):
    if request.method == 'POST':
        cname = request.form.get('cname')
        clvlstr = request.form.get('clvl')
        clvl = int(clvlstr)
        
        if len(cname) < 3:
            flash('Player name must be at least 3 characters!', category='error')
        elif clvl < 1 or clvl > 20:
            flash('Level must be between 1-20!', category='error')
        else:
            return redirect(url_for('views.character', id=id, lvl=str(clvl), name=cname))
        
    return render_template("createdetails.html", user=current_user, clist=Classtype.query.get(int(id)))

def where_id_and_name(fro, id, name):
    
    if name is None:
        return 0
    elif len(name) == 0:
        return 0
    
    querry = select(fro.name).where(fro.class_id == id).where(fro.name == name)
    rs = db.session.execute(querry)
    if rs.fetchone() is None:
        return 1
    else:
        rs = db.session.execute(querry)
        return 2

@views.route("/character/<id>/<lvl>/<name>", methods=['GET', 'POST'])
@login_required
def character(id, lvl, name):
    if request.method == 'POST':
        wea = request.form.get('wea')
        arm = request.form.get('arm')
        spe = request.form.get('spe')
        wil = request.form.get('wil')
        ski = request.form.get('ski')
        
        cinfo = Classtype.query.get(int(id))
        
        if cinfo.skill2 != "$$$":
            ski = cinfo.skill2
        
        if where_id_and_name(Weapon, id, wea) != 2:
            flash('Weapon name does not exist!', category='error')
        elif where_id_and_name(Armor, id, arm) == 1:
            flash('Armor name does not exist!', category='error')
        elif where_id_and_name(Spell, id, spe) == 1:
            flash('Spell name does not exist!', category='error')
        elif where_id_and_name(Wildshape, id, wil) == 1:
            flash('Wildshape name does not exist!', category='error')
        elif len(ski) != 3:
            flash('Skill must only be the first three characters!', category='error')
        elif ski != "Str" and ski != "Con" and ski != "Dex" and ski != "Cha" and ski != "Wis" and ski != "Int":
            flash('Skill name does not exist!', category='error')       
        else:
            
            str = 10
            dex = 10
            con = 13
            inte = 10
            wis = 10
            cha = 10
            
            if cinfo.skill1 == "Str":
                str = str +5 
                con = con +4
                dex = dex +2
            elif cinfo.skill1 == "Dex":
                dex = dex +5
                inte = inte +3
                cha = cha+3
            elif cinfo.skill1 == "Int":
                inte = inte +5
                wis = wis +4
                cha = cha +2
            elif cinfo.skill1 == "Wis":
                wis = wis +5
                inte = inte +3
                cha = cha +3
            elif cinfo.skill1 == "Cha":
                cha = cha +5
                inte = inte+2
                wis = wis+4
                
            if ski == "Str" or cinfo.skill2 == "Str":
                str = str +5 
                con = con +2
            elif ski == "Dex" or cinfo.skill2 == "Dex":
                dex = dex +5
                inte = inte +2
            elif ski == "Int" or cinfo.skill2 == "Int":
                inte = inte +5
                wis = wis +2
            elif ski == "Wis" or cinfo.skill2 == "Wis":
                wis = wis +5
                inte = inte +2
            elif ski == "Cha" or cinfo.skill2 == "Cha":
                cha = cha +5
                inte = inte+1
                wis = wis+1
            elif ski == "Con":
                con = con+5
                
            weapon = Weapon.query.filter_by(name=wea).first()
            
            new_player = Player(
                user_id=current_user.id,
                player_name=name,
                class_name=cinfo.name,
                level=lvl,
                hp=cinfo.base_hp + (cinfo.hp_per_lvl * int(lvl)) + (con/5 * int(lvl)),
                atk_count=1,
                str_stat = str,
                dex_stat = dex,
                con_stat = con,
                int_stat = inte,
                wis_stat = wis,
                car_stat = cha,
                wildshape_name="$",
                armor_name="$",
                ac=0,
                weapon_name=weapon.name,
                weapon_dmg= weapon.dmg_basestat,
                spell_name = "$",
                spell_dmg = "$"
            )
            
            if arm is not None:
                armor = Armor.query.filter_by(name=arm).first()
                if armor is None:
                    new_player.armor_name = "Natural Armor"
                    new_player.ac = 10 + (dex/5)
                    flash('Armor not found with class, error with database..', category='error')
                else:
                    new_player.ac = armor.ac_stat
                    new_player.armor_name = armor.name
            else:
                new_player.armor_name = "Natural Armor"
                new_player.ac = 10 + (dex/5)
            
            if int(lvl) == 20 and cinfo.extra_atk > 2:
                new_player.atk_count = 4
                new_player.weapon_dmg = new_player.weapon_dmg * 4
            elif int(lvl) > 10 and cinfo.extra_atk > 1:
                new_player.atk_count = 3
                new_player.weapon_dmg = new_player.weapon_dmg * 3
            elif int(lvl) > 4 and cinfo.extra_atk > 0:
                new_player.atk_count = 2
                new_player.weapon_dmg = new_player.weapon_dmg * 2
            
            if spe is not None:
                spell = Spell.query.filter_by(name=spe).first()
                if spell is None:
                    flash('Spell not found with class, error with database..', category='error')
                else:
                    new_player.spell_name = spell.name
                    new_player.spell_dmg = spell.dmg_basestat * new_player.atk_count
                    
            if wil is not None:
                ws = Wildshape.query.filter_by(name=spe).first()
                if ws is None:
                    flash('Wildshape not found with class, error with database..', category='error')
                else:
                    new_player.wildshape_name = ws.name
                    new_player.ac = ws.temp_ac
                    hp = hp + ws.temp_hp
                    if new_player.weapon_dmg < ws.dmg_stat:
                        new_player.weapon_name = "Beast Attack"
                        new_player.weapon_dmg = ws.dmg_stat
                    
            db.session.add(new_player)
            db.session.commit()
            flash('Player Created!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template("character.html", user=current_user, clist=Classtype.query.get(int(id)), lvl=int(lvl), name=name)


