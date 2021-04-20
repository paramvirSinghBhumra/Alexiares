#!flask/bin/python
from HANA_Backend import get_columnNames, True_View

from flask import Flask, jsonify
from flask import make_response

web = Flask(__name__)



@web.route('/')
def index():
    return make_response(jsonify({"msg":"Hi! Make sure you enter \'/api/<asset_name>\' to make a valid API call"}))
    
@web.route('/api/')
def err_msg():
    return make_response(jsonify({"error":"invalid API call"}), 401)

@web.route('/api/sites', methods=['GET'])
def return_all_sites():
    tv = True_View()
    json = tv.get_ALL("Site")
    del tv

    return jsonify(json)
    
@web.route('/api/sites/<int:site_id>', methods=['GET'])
#return site <site_id> info.... as well as any 2nd/3rd order relationships with other assets 
def return_site_info(site_id):
    return make_response(jsonify({"error":"page under construction"}), 401)


@web.route('/api/systems', methods=['GET'])
def return_all_systems():
    tv = True_View()
    json = tv.get_ALL("System")
    del tv

    return jsonify(json)

@web.route('/api/systems/<int:system_id>', methods=['GET'])
#return system <system_id> info.... as well as any 2nd/3rd order relationships with other assets 
def return_system_info(system_id):
    return make_response(jsonify({"error":"page under construction"}), 401)


@web.route('/api/subsystems', methods=['GET'])
def return_all_subsystems():
    tv = True_View()
    json = tv.get_ALL("Subsystem")
    del tv

    return jsonify(json)

@web.route('/api/subsystems/<int:subsystem_id>', methods=['GET'])
#return subsystem <subsystem_id> info.... as well as any 2nd/3rd order relationships with other assets 
def return_subsystem_info(subsystem_id):
    return make_response(jsonify({"error":"page under construction"}), 401)


if __name__ == "__main__":
    web.run(debug=True)