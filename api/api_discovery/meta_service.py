from flask import request, jsonify
import logging

app_logger = logging.getLogger("api_logic_server_app")

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators ):
    pass

    @app.route('/meta_service', methods=['GET'])
    def meta_service():
        """        
        Illustrates:
        * Use standard Flask, here for non-database endpoints.

        Test it with:
        
                http://localhost:5656/hello_newer_service?user=ApiLogicServer
                
        """
        result = []
        from api.api_discovery.ontimize_api import getMetaData
        md = getMetaData()
        for r in md['resources']:
            attrs = []
            for attr in md["resources"][r]['attributes']:
                print(attr['attr'].columns[0].name)
                attrs.append({"name": attr['name'], "type": attr['type'],"nullable":attr['attr'].columns[0].nullable,"primary_key": attr['attr'].columns[0].primary_key}) # "nullable": attr.attr.nullable, "primary_key": attr.attr.primary_key
            #md["resources"][r]['attributes'][0]['attr'].columns[0].primary_key | nullable |table | type
            #md["resources"][r]['model']
            entity = {"entity": r, "attributes": attrs}
            result.append(entity)
        print(result)
        return jsonify(result)