import argparse
import os
import simplejson
import json
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.OperatingSystem import OperatingSystem
from rafaysdk.models.addon import Addon
from rafaysdk.models.publish_addon_request import PublishAddonRequest
from rafaysdk.api.addons_api import AddonsApi
from rafaysdk import Configuration, ApiClient
from rafaysdk.rest import ApiException
import yaml


class addon_sdk_examples:

    def __init__(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(ROOT_DIR, 'user_config.yaml')
        with open(config_path) as file:
            data = yaml.load(file,Loader=yaml.FullLoader)
        self.addon_sdk_instance = self.create_addon_sdk_instance(data['host'], data['api_key'])

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

    def create_yaml_addon(self, addon_name, project_id, namespace, payload, version):
        """
        Creates yaml type addon with version
        :param addon_name:
        :param project_id:
        :param namespace:
        :param payload:
        :param version:
        :return:
        """
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

    def create_helm3_addon(self, addon_name, project_id, namespace, payload, values, version):
        """
        Creates Helm3 type addon with version
        :param addon_name:
        :param project_id:
        :param namespace:
        :param payload:
        :param version:
        :return:
        """
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

    def get_addon(self, project_id, addon_id):
        """
        Get addon details
        :param project_id:
        :param addon_id:
        :return:
        """

        try:
            response = self.addon_sdk_instance.get_addon(id=addon_id, project_id=project_id)
        except ApiException as e:
            print("Exception when calling AddonsApi->get_addon: %s\\n" % e)

        return response.to_dict()

    def delete_addon(self, project_id, addon_id):
        """
        Deletes Addon
        :param project_id:
        :param addon_id:
        :return:
        """
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
        # not specifying a suite is supported in testrunner, we have a default here so that tests can be run without args
        parser = argparse.ArgumentParser(usage="addon_sdk_examples.py --namespace namespacename --addon_name addonname --version version --project_id id")

        parser.add_argument("--namespace",
                            type=str,
                            dest="namespace_",
                            default=None)

        parser.add_argument("--addon_name",
                            type=str,
                            dest="addon_name_",
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

        return {"namespace":args.namespace_,"addon_name":args.addon_name_,"version":args.version_,"project_id":args.project_id_}


if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    yaml_payload = os.path.join(ROOT_DIR, 'config/addon-nginx.yaml')
    helm_payload = os.path.join(ROOT_DIR, 'config/chartmuseum.tgz')
    helm_values = os.path.join(ROOT_DIR, 'config/chartmuseum-values.yaml')
    addon = addon_sdk_examples()
    config = RunParser().config
    addon_resp = addon.create_yaml_addon(namespace=config['namespace'], addon_name=config['addon_name'], payload=yaml_payload,
                                       project_id=config['project_id'],version=config['version'])
    print("Addon created:{}".format(addon_resp))
    # # addon.delete_addon(project_id='w2l5xqk',addon_id=addon_id)
    # addon_id = addon.create_helm3_addon(namespace='elk-ns', addon_name='addon2', payload=helm_payload,values=helm_values, project_id='w2l5xqk',version='v1')
    # # addon.delete_addon(project_id='w2l5xqk',addon_id=addon_id)