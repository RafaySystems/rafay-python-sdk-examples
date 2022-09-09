import argparse
import os
from rafaysdk.models.namespace import Namespace
from rafaysdk.api.namespaces_api import NamespacesApi
from rafaysdk import Configuration, ApiClient
from rafaysdk.rest import ApiException
import yaml

from project_sdk_examples import project_sdk_examples


class namespace_sdk_examples:

    def __init__(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(ROOT_DIR, 'user_config.yaml')
        with open(config_path) as file:
            data = yaml.safe_load(file)
        self.namespace_sdk_instance = self.create_namespace_sdk_instance(data['host'], data['api_key'])
        self.project = project_sdk_examples()

    def create_namespace_sdk_instance(self, endpoint, apikey):
        """
        Creates Namespace sdk instance
        :param endpoint:
        :param apikey:
        :return:
        """
        configuration = Configuration()
        configuration.host = endpoint
        configuration.api_key['X-RAFAY-API-KEYID'] = apikey
        self.namespce_sdk_instance = NamespacesApi(ApiClient(configuration))
        return self.namespce_sdk_instance

    def create_namespace(self, project_name, namespace):
        """
        Creates Namespace
        :param project_name:
        :param namespace:
        :return:
        """
        project_id = self.project.get_project_id(project_name=project_name)
        try:
            request = Namespace(api_version="config.rafay.dev/v2" , kind="Namespace",metadata={"name":namespace,"urlScope":"project/kog1dn2"},spec={"metadata":{"name":namespace},"spec":{"namespaceMeta":{"name":namespace}},"type":"RafayWizard"})
            ns_response = self.namespce_sdk_instance.create_namespace(project_id, request)
            ns_resp = ns_response.to_dict()

        except ApiException as e:
            print("Exception when calling NamespacesApi->create_namespace: %s\\n" % e)
        return {"namespace_id":ns_resp["metadata"]["id"],"name":ns_resp["metadata"]["name"]}


    def list_namespaces(self, project_name):

        """
        :param project_name:
        :return:
        """
        limit = 56  # int | Number of results to return per page (optional)
        offset = 56  # int | The base index of records to be returned in the results (optional)

        project_id = self.project.get_project_id(project_name=project_name)
        try:
            api_response = self.namespce_sdk_instance.list_namespaces(project_id=project_id)
        except ApiException as e:
            print("Exception when calling NamespacesApi->list_namespaces: %s\n" % e)

        return api_response.to_dict()['results']

    def get_namespace_id(self, project_name, namespace_name):
        """
        :param project_name:
        :return:
        """
        results = self.list_namespaces(project_name)

        for namespace in results:
            if namespace_name == namespace['name']:
                return namespace['id']

    def get_namespace(self, project_name, namespace_name):
        """
        Get namespace details
        :param project_name:
        :param namespace_name:
        :return:
        """
        project_id = self.project.get_project_id(project_name=project_name)
        namespace_id= self.get_namespace_id(project_name,namespace_name)
        try:
            response = self.namespce_sdk_instance.get_namespace(id=namespace_id, project_id=project_id)
        except ApiException as e:
            print("Exception when calling NamespacesApi->get_namespace: %s\\n" % e)

        return response.to_dict()

    def delete_namespace(self, project_name, namespace_name):
        """
        Deletes Namespace
        :param project_name:
        :param namespace_name:
        :return:
        """

        project_id = self.project.get_project_id(project_name=project_name)
        namespace_id = self.get_namespace_id(project_name, namespace_name)

        try:
            self.namespace_sdk_instance.delete_namespace(id=namespace_id, project_id=project_id)
        except ApiException as e:
            print("Exception when calling NamespacesApi->delete_namespace: %s\n" % e)
            return False

        return True

class RunParser(object):

    def __init__(self):
        self.config = self.setup_flag_parser()

    def setup_flag_parser(self):
        parser = argparse.ArgumentParser(usage="namespace_sdk_examples.py --action <get|delete|create|list> \
                                        --namespace_name namespace --project_name projectname")

        parser.add_argument("--action",
                            type=str,
                            dest="action_",
                            default=None)

        parser.add_argument("--namespace",
                            type=str,
                            dest="namespace_",
                            default=None)

        parser.add_argument("--project_name",
                            type=str,
                            dest="project_name_",
                            default=None)

        args = parser.parse_args()

        return {"action":args.action_,"namespace_name":args.namespace_,"project_name":args.project_name_}

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    namespace = namespace_sdk_examples()
    config = RunParser().config
    if config["action"] == "get":
        resp = namespace.get_namespace(config["project_name"],config["namespace_name"])
        print(resp)
    if config["action"] == "list":
        resp = namespace.list_namespaces(config["project_name"])
        print(resp)
    if config["action"] == "delete":
        resp = namespace.delete_namespace(config["project_name"],config["namespace_name"])
        print(resp)
    if config["action"] == "create":
        resp = namespace.create_namespace(project_name=config["project_name"], namespace=config["namespace_name"])
        print("Namespace created:{}".format(resp))
