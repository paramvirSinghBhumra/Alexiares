#!flask/bin/python
from FlaskAPI.HANA_Backend import get_columnNames, True_View

from flask import Flask, jsonify
from flask import make_response

app = Flask(__name__)


###########################################
# ----------- Missions (Level 1)-----------
@app.route('/api/missions', methods=['GET'])
def return_all_missions():
    tv = True_View()
    json = tv.get_ALL("Mission")
    del tv

    return jsonify(json)

@app.route('/api/missions/<int:mission_id>', methods=['GET'])
def return_mission_info(mission_id):
    tv = True_View()
    json = tv.get_Specific("Mission", mission_id)
    del tv
    
    print(json)
    return jsonify(json)
###########################################





########################################
# ----------- Sites (Level 2)-----------
@app.route('/api/sites', methods=['GET'])
def return_all_sites():
    tv = True_View()
    json = tv.get_ALL("Site")
    del tv

    return jsonify(json)
    
@app.route('/api/sites/<int:site_id>', methods=['GET'])
#SITE AND MISSIONS ARE LINKED TOGETHER IN THE Mission_has_System table! MIGHT REORGANIZE
#return site <site_id> info.... as well as any 2nd/3rd order relationships with other assets 
def return_site_info(site_id):
    tv = True_View()
    json = tv.get_Specific("Site", site_id)
    del tv

    return jsonify(json)
########################################





##########################################
# ----------- Systems (Level 3)-----------
@app.route('/api/systems', methods=['GET'])
def return_all_systems():
    tv = True_View()
    json = tv.get_ALL("System")
    del tv

    return jsonify(json)

@app.route('/api/systems/<int:system_id>', methods=['GET'])
#return system <system_id> info.... as well as any 2nd/3rd order relationships with other assets 
def return_system_info(system_id):
    tv = True_View()
    json = tv.get_Specific("System", system_id)
    del tv

    return jsonify(json)
##########################################





#############################################
# ----------- Subsystems (Level 4)-----------
@app.route('/api/subsystems', methods=['GET'])
def return_all_subsystems():
    tv = True_View()
    json = tv.get_ALL("Subsystem")
    del tv

    return jsonify(json)

@app.route('/api/subsystems/<int:subsystem_id>', methods=['GET'])
#return subsystem <subsystem_id> info.... as well as any 2nd/3rd order relationships with other assets 
def return_subsystem_info(subsystem_id):
    tv = True_View()
    json = tv.get_Specific("Subsystem", subsystem_id)
    del tv
    
    print(json)
    return jsonify(json)
#############################################




# fixing bugs/etc
@app.route('/api/')
def err_msg():
    return make_response(jsonify({"msg":"Hi! Make sure you enter \'/api/<asset_name>\' or \'/api/<asset_name>/<asset_id>\' to make a valid API call"}))

@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def index(path):
    return make_response(jsonify({"error":"invalid API call. Try typing '/api' for more information"}), 401)



if __name__ == "__main__":
    app.run(debug=True, port=5000)
