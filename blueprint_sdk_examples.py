import argparse
import os
import simplejson
import json

import yaml
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.OperatingSystem import OperatingSystem
from rafaysdk.api.blueprints_api import BlueprintsApi
from rafaysdk.models.v2_rafay_meta import V2RafayMeta
from rafaysdk.models.v2_snapshot_ref import V2SnapshotRef
from rafaysdk.models.v2_blueprint_spec import V2BlueprintSpec
from rafaysdk.models.v2_publish_blueprint_request import V2PublishBlueprintRequest
from rafaysdk import Configuration, ApiClient
from rafaysdk.models.v2_blueprint import V2Blueprint
from rafaysdk.rest import ApiException


class bluprint_sdk_examples:

    def __init__(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(ROOT_DIR, 'user_config.yaml')
        with open(config_path) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.blueprint_sdk_instance = self.create_blueprint_sdk_instance(data['host'], data['api_key'])

    def create_blueprint_sdk_instance(self, endpoint, apikey):
        """
        Creates Blueprint sdk instance
        :param endpoint:
        :param apikey:
        :return:
        """
        configuration = Configuration()
        configuration.host = endpoint
        configuration.api_key['X-RAFAY-API-KEYID'] = apikey
        self.blueprint_sdk_instance = BlueprintsApi(ApiClient(configuration))
        return self.blueprint_sdk_instance

    def create_blueprint(self, blueprint_name, project_id, version, psp_policy='cluster-scoped',
                         addonlist=None, excludeDefaultaddons=None):
        """
        Create blueprint
        :param excludeDefaultaddons:
        :param addonlist:
        :param blueprint_name:
        :param project_id:
        :param psp_policy:
        :param blueprintlist:
        :return:
        """
        try:
            # Option to add psp policy
            labels = {
                "rafay.dev/pspPolicyType": "cluster-scoped"
            }
            if psp_policy == 'namespace-scoped':
                labels["rafay.dev/pspPolicyType"] = "namespace-scoped"
            metadata = V2RafayMeta(name=blueprint_name, labels=labels)
            # add blueprints to blueprint
            custom_components = []
            if addonlist is not None:
                for addon in addonlist:
                    snap = V2SnapshotRef(name=addon)
                    custom_components.append(snap)
            else:
                custom_components = None
            excluded_system_components = []
            if excludeDefaultaddons is not None:
                for default in excludeDefaultaddons:
                    snap = V2SnapshotRef(name=default)
                    excluded_system_components.append(snap)
            else:
                excluded_system_components = None
            spec = V2BlueprintSpec(custom_components=custom_components,
                                   excluded_system_components=excluded_system_components)
            request = V2Blueprint(metadata=metadata, spec=spec)
            api_response = self.blueprint_sdk_instance.create_blueprint(project_id, request)
            api_response = api_response.to_dict()
            request = V2PublishBlueprintRequest(snapshot_display_name=version)
            self.blueprint_sdk_instance.publish_blueprint(project_id, api_response['metadata']['id'], request)
        except ApiException as e:
            print("Exception when calling blueprintsApi->create_blueprint: %s\\n" % e)

        return {"name": api_response['metadata']['name'], "id": api_response['metadata']['id']}

    def get_blueprint(self, project_id, blueprint_id):
        """
        Get blueprint details
        :param project_id:
        :param blueprint_id:
        :return:
        """
        try:
            response = self.blueprint_sdk_instance.get_blueprint_id(blueprint_id=blueprint_id, project_id=project_id)
        except ApiException as e:
            print("Exception when calling blueprintsApi->get_blueprint: %s\\n" % e)

        return response.to_dict()

    def get_all_blueprints(self, project_id):
        """
        List all existing blueprints
        :param project_id:
        :return:
        """
        try:
            response = self.blueprint_sdk_instance.get_blueprints(project_id=project_id, limit=1000)
        except ApiException as e:
            print("Exception when calling blueprintsApi->list_blueprint: %s\\n" % e)

        return response.to_dict()

    def delete_blueprint(self, project_id, blueprint_id):
        """
        Delete blueprint with ID
        :param project_id:
        :param blueprint_id:
        :return:
        """
        try:
            self.blueprint_sdk_instance.delete_blueprint(blueprint_id=blueprint_id, project_id=project_id)
        except ApiException as e:
            print("Exception when calling blueprintsApi->delete_blueprint: %s\n" % e)
            return False

        return True


class RunParser(object):

    def __init__(self):
        self.config = self.setup_flag_parser()

    def setup_flag_parser(self):
        # not specifying a suite is supported in testrunner, we have a default here so that tests can be run without args
        parser = argparse.ArgumentParser(usage="blueprint_sdk_examples.py --blueprint_name blueprint_name --addons addon1 addon2 --version version --project_id id")

        parser.add_argument("--blueprint_name",
                            type=str,
                            dest="blueprint_name_",
                            default=None)

        parser.add_argument("--addons",
                            nargs="*",
                            type=str,
                            dest="addons_",
                            default=None)

        parser.add_argument("--version",
                            type=str,
                            dest="version_",
                            default=None)

        parser.add_argument("--project_id",
                            type=str,
                            dest="project_id_",
                            default=None)

        args = parser.parse_args()

        return {"blueprint_name": args.blueprint_name_, "addons": args.addons_, "version": args.version_,
                "project_id": args.project_id_}


if __name__ == '__main__':
    blueprint = bluprint_sdk_examples()
    config = RunParser().config
    resp = blueprint.create_blueprint(blueprint_name=config["blueprint_name"], addonlist=config["addons"],
                                      project_id=config['project_id'], version=config['version'])
    print("Blueprint Created:{}".format(resp))
    # print(blueprint.delete_blueprint(project_id='w2l5xqk',blueprint_id='pkzjp0m'))
