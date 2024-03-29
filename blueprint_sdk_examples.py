import argparse
import os
import yaml
from rafaysdk.api.blueprints_api import BlueprintsApi
from rafaysdk.models.v2_rafay_meta import V2RafayMeta
from rafaysdk.models.v2_snapshot_ref import V2SnapshotRef
from rafaysdk.models.v2_blueprint_spec import V2BlueprintSpec
from rafaysdk.models.v2_publish_blueprint_request import V2PublishBlueprintRequest
from rafaysdk import Configuration, ApiClient
from rafaysdk.models.v2_blueprint import V2Blueprint
from rafaysdk.rest import ApiException

from project_sdk_examples import project_sdk_examples


class bluprint_sdk_examples:

    def __init__(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(ROOT_DIR, 'user_config.yaml')
        with open(config_path) as file:
            data = yaml.safe_load(file)
            self.blueprint_sdk_instance = self.create_blueprint_sdk_instance(data['host'], data['api_key'])
        self.project = project_sdk_examples()

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

    def create_blueprint(self, blueprint_name, project_name, version, psp_policy='cluster-scoped',
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
        project_id = self.project.get_project_id(project_name=project_name)
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


    def list_blueprints(self, project_name):
        """
        List all existing blueprints
        :param project_id:
        :return:
        """

        project_id = self.project.get_project_id(project_name=project_name)
        try:
            response = self.blueprint_sdk_instance.get_blueprints(project_id=project_id, limit=1000)
        except ApiException as e:
            print("Exception when calling blueprintsApi->list_blueprint: %s\\n" % e)

        return response.to_dict()['items']

    def get_blueprint_id(self, project_name, blueprint_name):
        """
        :param project_name:
        :return:
        """
        results = self.list_blueprints(project_name)

        for blueprint in results:
            if blueprint_name == blueprint['metadata']['name']:
                return blueprint['metadata']['id']

    def delete_blueprint(self, project_name, blueprint_name):
        """
        Delete blueprint with ID
        :param project_name:
        :param blueprint_name:
        :return:
        """
        project_id = self.project.get_project_id(project_name=project_name)
        blueprint_id = self.get_blueprint_id(project_name, blueprint_name)
        try:
            self.blueprint_sdk_instance.delete_blueprint(blueprint_id=blueprint_id, project_id=project_id)
        except ApiException as e:
            print("Exception when calling blueprintsApi->delete_blueprint: %s\n" % e)
            return False

        return True

    def get_blueprint(self, project_name, blueprint_name):
        """
        Get blueprint details
        :param project_name:
        :param blueprint_name:
        :return:
        """

        project_id = self.project.get_project_id(project_name=project_name)
        blueprint_id = self.get_blueprint_id(project_name, blueprint_name)
        try:
            response = self.blueprint_sdk_instance.get_blueprint_id(blueprint_id=blueprint_id, project_id=project_id)
        except ApiException as e:
            print("Exception when calling blueprintsApi->get_blueprint: %s\\n" % e)

        return response.to_dict()

class RunParser(object):

    def __init__(self):
        self.config = self.setup_flag_parser()

    def setup_flag_parser(self):
        parser = argparse.ArgumentParser(usage="blueprint_sdk_examples.py --action <get|delete|create|list> \
                                               --blueprint_name blueprint_name --addons addon1 addon2 --version version \
                                               --project_name project_name")

        parser.add_argument("--action",
                            type=str,
                            dest="action_",
                            default=None)

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

        parser.add_argument("--project_name",
                            type=str,
                            dest="project_name_",
                            default=None)

        args = parser.parse_args()

        return {"action":args.action_,"blueprint_name": args.blueprint_name_, "addons": args.addons_, "version": args.version_,
                "project_name": args.project_name_}


if __name__ == '__main__':
    blueprint = bluprint_sdk_examples()
    config = RunParser().config
    if config["action"] == "get":
        resp = blueprint.get_blueprint(config["project_name"], config["blueprint_name"])
        print(resp)
    if config["action"] == "list":
        resp = blueprint.list_blueprints(config["project_name"])
        print(resp)
    if config["action"] == "delete":
        resp = blueprint.delete_blueprint(config["project_name"], config["blueprint_name"])
        print(resp)
    if config["action"] == "create":
        resp = blueprint.create_blueprint(blueprint_name=config["blueprint_name"], addonlist=config["addons"],
                                      project_name=config['project_name'], version=config['version'])
        print("Blueprint Created:{}".format(resp))
