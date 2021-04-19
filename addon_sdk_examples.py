import argparse
import os
from rafaysdk.models.addon import Addon
from rafaysdk.models.publish_addon_request import PublishAddonRequest
from rafaysdk.api.addons_api import AddonsApi
from rafaysdk import Configuration, ApiClient
from rafaysdk.rest import ApiException
import yaml

from project_sdk_examples import project_sdk_examples


class addon_sdk_examples:

    def __init__(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(ROOT_DIR, 'user_config.yaml')
        with open(config_path) as file:
            data = yaml.safe_load(file)
        self.addon_sdk_instance = self.create_addon_sdk_instance(data['host'], data['api_key'])
        self.project = project_sdk_examples()

    def create_addon_sdk_instance(self, endpoint, apikey):
        """
        Creates Addon sdk instance
        :param endpoint:
        :param apikey:
        :return:
        """
        configuration = Configuration()
        configuration.host = endpoint
        configuration.api_key['X-RAFAY-API-KEYID'] = apikey
        self.addon_sdk_instance = AddonsApi(ApiClient(configuration))
        return self.addon_sdk_instance

    def create_yaml_addon(self, addon_name, project_name, namespace, payload, version):
        """
        Creates yaml type addon with version
        :param addon_name:
        :param project_id:
        :param namespace:
        :param payload:
        :param version:
        :return:
        """
        project_id = self.project.get_project_id(project_name=project_name)
        try:
            request = Addon(name=addon_name, namespace=namespace, type='NativeYaml')
            addon_response = self.addon_sdk_instance.create_addon(project_id, request)
            addon_resp = addon_response.to_dict()
            self.addon_sdk_instance.upload_payload_addon(id=addon_resp['id'], project_id=project_id,
                                                                            payload=payload)
            request = PublishAddonRequest(version=version)
            self.addon_sdk_instance.publish_addon(id=addon_resp['id'], project_id=project_id,
                                                                     body=request)
        except ApiException as e:
            print("Exception when calling AddonsApi->create_addon: %s\\n" % e)
        return {"addon_id":addon_resp['id'],"type":addon_resp['type'],"name":addon_resp['name']}

    def create_helm3_addon(self, addon_name, project_name, namespace, payload, values, version):
        """
        Creates Helm3 type addon with version
        :param addon_name:
        :param project_id:
        :param namespace:
        :param payload:
        :param version:
        :return:
        """
        project_id = self.project.get_project_id(project_name=project_name)
        try:
            request = Addon(name=addon_name, namespace=namespace, type='NativeHelm')
            addon_response = self.addon_sdk_instance.create_addon(project_id, request)
            addon_resp = addon_response.to_dict()
            print(addon_resp)
            self.addon_sdk_instance.upload_payload_addon(id=addon_resp['id'], project_id=project_id,
                                                                            payload=payload)
            self.addon_sdk_instance.upload_values_addon(id=addon_resp['id'], project_id=project_id,
                                                                          values=values)
            request = PublishAddonRequest(version=version)
            self.addon_sdk_instance.publish_addon(id=addon_resp['id'], project_id=project_id,
                                                                     body=request)
        except ApiException as e:
            print("Exception when calling AddonsApi->create_addon: %s\\n" % e)
        return {"addon_id":addon_resp['id'],"type":addon_resp['type'],"name":addon_resp['name']}

    def list_addons(self, project_name):

        """
        :param project_name:
        :return:
        """
        limit = 56  # int | Number of results to return per page (optional)
        offset = 56  # int | The base index of records to be returned in the results (optional)

        project_id = self.project.get_project_id(project_name=project_name)
        try:
            api_response = self.addon_sdk_instance.list_addons(project_id=project_id)
        except ApiException as e:
            print("Exception when calling AddonsApi->list_addons: %s\n" % e)

        return api_response.to_dict()['results']

    def get_addon_id(self, project_name, addon_name):
        """
        :param project_name:
        :param addon_name:
        :return:
        """
        results = self.list_addons(project_name)

        for addon in results:
            if addon_name == addon['name']:
                return addon['id']

    def get_addon(self, project_name, addon_name):
        """
        Get addon details
        :param project_name:
        :param addon_name:
        :return:
        """
        project_id = self.project.get_project_id(project_name=project_name)
        addon_id= self.get_addon_id(project_name,addon_name)
        try:
            response = self.addon_sdk_instance.get_addon(id=addon_id, project_id=project_id)
        except ApiException as e:
            print("Exception when calling AddonsApi->get_addon: %s\\n" % e)

        return response.to_dict()

    def delete_addon(self, project_name, addon_name):
        """
        Deletes Addon
        :param project_name:
        :param addon_name:
        :return:
        """

        project_id = self.project.get_project_id(project_name=project_name)
        addon_id = self.get_addon_id(project_name, addon_name)

        try:
            self.addon_sdk_instance.delete_addon(id=addon_id, project_id=project_id)
        except ApiException as e:
            print("Exception when calling AddonsApi->delete_addon: %s\n" % e)
            return False

        return True

class RunParser(object):

    def __init__(self):
        self.config = self.setup_flag_parser()

    def setup_flag_parser(self):
        parser = argparse.ArgumentParser(usage="addon_sdk_examples.py --action <get|delete|create|list> --addon_name addonname \
                                               --addon_type <NativeHelm|NativeYaml> --version version \
                                               --project_name projectname --namespace namespacename \
                                               --chart <path to the helm chart> --values <path to values file> \
                                               --yaml <path to yaml file>")

        parser.add_argument("--action",
                            type=str,
                            dest="action_",
                            default=None)

        parser.add_argument("--namespace",
                            type=str,
                            dest="namespace_",
                            default=None)

        parser.add_argument("--addon_name",
                            type=str,
                            dest="addon_name_",
                            default=None)

        parser.add_argument("--addon_type",
                            type=str,
                            dest="addon_type_",
                            default="NativeHelm")

        parser.add_argument("--version",
                            type=str,
                            dest="version_",
                            default=None)

        parser.add_argument("--project_name",
                            type=str,
                            dest="project_name_",
                            default=None)

        parser.add_argument("--chart",
                            type=str,
                            dest="chart_",
                            default=None)

        parser.add_argument("--values",
                            type=str,
                            dest="values_",
                            default=None)

        parser.add_argument("--yaml",
                            type=str,
                            dest="yaml_",
                            default=None)

        args = parser.parse_args()

        return {"action":args.action_,"namespace":args.namespace_,"addon_name":args.addon_name_,"version":args.version_,
                "project_name":args.project_name_,"chart":args.chart_,"values":args.values_,"yaml":args.yaml_,
                "addon_type": args.addon_type_}


if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    addon = addon_sdk_examples()
    config = RunParser().config
    if config["action"] == "get":
        resp = addon.get_addon(config["project_name"],config["addon_name"])
        print(resp)
    if config["action"] == "list":
        resp = addon.list_addons(config["project_name"])
        print(resp)
    if config["action"] == "delete":
        resp = addon.delete_addon(config["project_name"],config["addon_name"])
        print(resp)
    if config["action"] == "create":
        if config["addon_type"] == "NativeHelm":
            addon_resp = addon.create_helm3_addon(namespace=config["namespace"], addon_name=config["addon_name"],
                                                  payload=config["chart"], values=config["values"],
                                                 project_name=config["project_name"], version=config["version"])
            print("Addon created:{}".format(addon_resp))
        if config["addon_type"] == "NativeYaml":
            addon_resp = addon.create_yaml_addon(namespace=config["namespace"], addon_name=config["addon_name"],
                                                 payload=config["yaml"], project_name=config["project_name"],
                                                 version=config["version"])
            print("Addon created:{}".format(addon_resp))
