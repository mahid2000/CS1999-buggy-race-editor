from typing import DefaultDict
from flask import Flask, render_template, request, jsonify
import sqlite3 as sql

from flask.json import htmlsafe_dumps

LEGAL_VAL =  160

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "https://rhul.buggyrace.net"

#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM buggies")
        record = cur.fetchone();     
        return render_template("buggy-form.html", buggy = None)
    elif request.method == 'POST':
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM buggies")
        record = cur.fetchone();  
        # request the data values and put them into their respective variables       
        msg=""
        msg2 = ""
        qty_wheels = request.form['qty_wheels'].strip()
        primary_motive_power = request.form['primary_motive_power']
        primary_motive_power_units = request.form['primary_motive_power_units']
        auxiliary_motive_power = request.form['auxiliary_motive_power']
        auxiliary_motive_power_units = request.form['auxiliary_motive_power_units']
        hamster_booster = request.form['hamster_booster']          
        flag_color = request.form['flag_color']
        flag_pattern = request.form['flag_pattern']
        flag_color_secondary = request.form['flag_color_secondary']    
        tyres = request.form['tyres']
        qty_tyres = request.form['qty_tyres']                                         
        armour = request.form['armour']                   
        attack = request.form['attack']                      
        qty_attacks = request.form['qty_attacks']
        try:
            fireproof = request.form['fireproof']
        except:
            fireproof = "False"
        try:
            insulated = request.form['insulated']
        except:
            insulated = "False"
        try:
            antibiotic = request.form['antibiotic']
        except:
            antibiotic = "False"
        try:
            banging = request.form['banging']
        except:
            banging = "False"
        algo = request.form['algo'] 
        buggy_id = request.form['id'] 
           
        error = ""
        # Validate if the inputs follow the rules, and if they dont then give an error message
        if qty_wheels.isdigit() == False or int(qty_wheels) < 4 or (int(qty_wheels) % 2) != 0 :
            msg += f'{qty_wheels} is not a valid quantity!!....Your buggy needs to have a EVEN NUMBER of wheels...at least 4 of them!!'
            error += 't'
        else:
            error += 'f'
        if primary_motive_power == 'fusion' or primary_motive_power == 'wind' or primary_motive_power == 'solar' or primary_motive_power == 'thermo':
            if int(primary_motive_power_units) != 1:
                msg += ' You can only have one non-consumable power source!'
                error += 't'
        else:
            error += 'f'
        if int(primary_motive_power_units) < 1:
            msg += ' You have no power!!!'
            error += 't'
        else:
            error += 'f'           
        if auxiliary_motive_power == 'fusion' or auxiliary_motive_power == 'wind' or auxiliary_motive_power == 'solar' or auxiliary_motive_power == 'thermo':
            if int(auxiliary_motive_power_units) != 1:
                msg += ' You can only have one non-consumable auxiliary power source!'
                error += 't'
        else:
            error += 'f'    
        if int(hamster_booster) < 0:
            error += 't'
            msg += ' Please input a valid quantity of Hamster Boosters!!'
        else:
            error += 'f'
        if primary_motive_power == 'hamster' and int(primary_motive_power_units) > 0:
            msg += ' Hamster Boosters are only effective on Hamsters!!!'
            error += 't'
        else:
            error += 'f'
        if auxiliary_motive_power == 'hamster' and int(auxiliary_motive_power_units) > 0:
            msg += ' Hamster Boosters are only effective on Hamsters!!!'
            error += 't'
        else:
            error += 'f'          
        if flag_pattern != 'plain' and flag_color == flag_color_secondary:
            error += 't'
            msg += 'You cant have two of the same colours unless its a PLAIN flag !!!'
        else:
            error += 'f'
        if qty_tyres < qty_wheels:
            error += 't'
            msg += ' You cant drive without tyres!!...They can get puntured so its good to have spares...'
        else:
            error += 'f'
        if algo == 'buggy':
            error = 't'
            msg += ' Your Operating System seems to be buggy.... please update it!!!'
        else:
            error += 'f'

        # Add up the cost and mass of the buggy
        cost = 0
        mass = 0

        if primary_motive_power == 'petrol' :
            cost += 4 * int(primary_motive_power_units)
            mass += 2 * int(primary_motive_power_units)
        elif primary_motive_power == 'fusion' :
            cost += 400 * int(primary_motive_power_units)
            mass += 100 * int(primary_motive_power_units)
        elif primary_motive_power == 'steam' :
            cost += 3 * int(primary_motive_power_units)
            mass += 4 * int(primary_motive_power_units)
        elif primary_motive_power == 'bio' :
            cost += 5 * int(primary_motive_power_units)
            mass += 2 * int(primary_motive_power_units)
        elif primary_motive_power == 'electric' :
            cost += 20 * int(primary_motive_power_units)
            mass += 20 * int(primary_motive_power_units)
        elif primary_motive_power == 'rocket' :
            cost += 16 * int(primary_motive_power_units)
            mass += 2 * int(primary_motive_power_units)
        elif primary_motive_power == 'hamster' :
            cost += 3 * int(primary_motive_power_units)
            mass += 1 * int(primary_motive_power_units)
        elif primary_motive_power == 'thermo' :
            cost += 300 * int(primary_motive_power_units)
            mass += 100 * int(primary_motive_power_units)
        elif primary_motive_power == 'solar' :
            cost += 40 * int(primary_motive_power_units)
            mass += 30 * int(primary_motive_power_units)
        elif primary_motive_power == 'wind' :
            cost += 20 * int(primary_motive_power_units)
            mass += 30 * int(primary_motive_power_units)

        if auxiliary_motive_power == 'petrol' :
            cost += 4 * int(auxiliary_motive_power_units)
            mass += 2 * int(auxiliary_motive_power_units)
        elif auxiliary_motive_power == 'fusion' :
            cost += 400 * int(auxiliary_motive_power_units)
            mass += 100 * int(auxiliary_motive_power_units)
        elif auxiliary_motive_power == 'steam' :
            cost += 3 * int(auxiliary_motive_power_units)
            mass += 4 * int(auxiliary_motive_power_units)
        elif auxiliary_motive_power == 'bio' :
            cost += 5 * int(auxiliary_motive_power_units)
            mass += 2 * int(auxiliary_motive_power_units)
        elif auxiliary_motive_power == 'electric' :
            cost += 20 * int(auxiliary_motive_power_units)
            mass += 20 * int(auxiliary_motive_power_units)
        elif auxiliary_motive_power == 'rocket' :
            cost += 16 * int(auxiliary_motive_power_units)
            mass += 2 * int(auxiliary_motive_power_units)
        elif primary_motive_power == 'hamster' :
            cost += 3 * int(auxiliary_motive_power_units)
            mass += 1 * int(auxiliary_motive_power_units)
        elif auxiliary_motive_power == 'thermo' :
            cost += 300 * int(auxiliary_motive_power_units)
            mass += 100 * int(auxiliary_motive_power_units)
        elif auxiliary_motive_power == 'solar' :
            cost += 40 * int(auxiliary_motive_power_units)
            mass += 30 * int(auxiliary_motive_power_units)
        elif auxiliary_motive_power == 'wind' :
            cost += 20 * int(auxiliary_motive_power_units)
            mass += 30 * int(auxiliary_motive_power_units)

        if int(hamster_booster) > 0:
            cost += 5 * int(hamster_booster)
        
        if tyres == 'knobbly' :
            cost += 15 * int(qty_tyres)
            mass += 20 * int(qty_tyres)
        elif tyres == 'slick' :
            cost += 10 * int(qty_tyres)
            mass += 14 * int(qty_tyres)
        elif tyres == 'steelband' :
            cost += 20 * int(qty_tyres)
            mass += 28 * int(qty_tyres)
        elif tyres == 'reactive' :
            cost += 40 * int(qty_tyres)
            mass += 20 * int(qty_tyres)
        elif tyres == 'maglev' :
            cost += 50 * int(qty_tyres)
            mass += 30 * int(qty_tyres)

        if armour == 'wood' :
            cost += 40 
            mass += 100
            if int(qty_wheels) > 4 :
                cost += 4 * (int(qty_wheels) - 4)
                mass += 10 * (int(qty_wheels) - 4)
        elif armour == 'aluminum' :
            cost += 200 
            mass += 50
            if int(qty_wheels) > 4 :
                cost += 20 * (int(qty_wheels) - 4) 
                mass += 5 * (int(qty_wheels) - 4)
        elif armour == 'thinsteel' :
            cost += 100 
            mass += 200
            if int(qty_wheels) > 4 :
                cost += 10 * (int(qty_wheels) - 4)
                mass += 20 * (int(qty_wheels) - 4)
        elif armour == 'thicksteel' :
            cost += 200 
            mass += 400
            if int(qty_wheels) > 4 :
                cost += 20 * (int(qty_wheels) - 4)
                mass += 40 * (int(qty_wheels) - 4)
        elif armour == 'titanium' :
            cost += 290 
            mass += 300
            if int(qty_wheels) > 4 :
                cost += 29 * (int(qty_wheels) - 4)
                mass += 30 * (int(qty_wheels) - 4)

        if attack == 'spike' :
            cost += 5 * int(qty_attacks)
            mass += 10 * int(qty_attacks)
        elif attack == 'flame' :
            cost += 20 * int(qty_attacks)
            mass += 12 * int(qty_attacks)
        elif attack == 'charge' :
            cost += 28 * int(qty_attacks)
            mass += 25 * int(qty_attacks)
        elif attack == 'biohazard' :
            cost += 30 * int(qty_attacks)
            mass += 10 * int(qty_attacks)

        if cost > LEGAL_VAL: 
            msg2 += 'This Buggy costs too much!!!! You have a £200 budget!!!!'
        else:
            error += 'f'


        # Check for errors... If there are errors, redo get fourm and send error message else try update Buggy Database
        for ch in error:
            if ch == 't' :
                return render_template("buggy-form.html", msg  = msg, buggy = record)
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                if buggy_id:
                    cur.execute(
                        "UPDATE buggies SET qty_wheels=?, power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, hamster_booster=?, flag_color=?, flag_pattern=?, flag_color_secondary=?, tyres=?, qty_tyres=?, armour=?, attack=?, qty_attacks=?, fireproof=?, insulated=?, antibiotic=?, banging=?, algo=?, cost=?, mass=? WHERE id=?",
                        (qty_wheels, primary_motive_power, primary_motive_power_units, auxiliary_motive_power, auxiliary_motive_power_units, hamster_booster, flag_color, flag_pattern, flag_color_secondary, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, cost, mass,  buggy_id)
                    )
                else:
                    cur.execute(
                        "INSERT INTO buggies (qty_wheels, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, flag_color, flag_pattern, flag_color_secondary, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, cost, mass) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (qty_wheels, primary_motive_power, primary_motive_power_units, auxiliary_motive_power, auxiliary_motive_power_units, hamster_booster, flag_color, flag_pattern, flag_color_secondary, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, cost, mass)
                    )
                con.commit()
                msg = "Record successfully saved"
        except:
            # If bugggy not succesfuly updated, send error message
            con.rollback() 
            msg = "error in update operation"
        finally:
            con.close()
        return render_template("updated.html", msg = msg, price = cost, weight = mass, price_error = msg2, error_msg = error)


#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    records = cur.fetchall(); 
    return render_template("buggy.html", buggies = records)

#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
#------------------------------------------------------------
@app.route('/edit/<buggy_id>')
def edit_buggy(buggy_id):
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=?", (buggy_id))
    record = cur.fetchone(); 
    return render_template("buggy-form.html", buggy = record)

@app.route('/delete/<buggy_id>')
def delete_buggy(buggy_id):
    con = sql.connect(DATABASE_FILE)
    con2 = sql.connect(DATABASE_FILE)
    con2.row_factory = sql.Row
    con.row_factory = sql.Row
    cur = con.cursor()  
    cur.execute("DELETE FROM buggies WHERE id=?", (buggy_id))
    cur2 = con2.cursor()
    cur2.execute("SELECT * FROM buggies WHERE id=?", (buggy_id))
    records = cur2.fetchall()
    record = cur.fetchone()

    con.commit()
    return render_template("buggy.html",buggies = records, rm="True", buggy = record)

#------------------------------------------------------------
# You probably don't need to edit this... unless you want  to ;)
#
# get JSON from current record
#  This reads the buggy record from the database, turns it
#  into JSON format (excluding any empty values), and returns
#  it. There's no .html template here because it's *only* returning
#  the data, so in effect jsonify() is rendering the data.
#------------------------------------------------------------
@app.route('/json')
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    buggies = cur.fetchall()
    return jsonify(list((dict(buggy) for buggy in buggies)))

@app.route('/poster')
def poster():
    return render_template("poster.html")


# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")

