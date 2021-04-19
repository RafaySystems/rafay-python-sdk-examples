import argparse
import os
from rafaysdk.models.project import Project
from rafaysdk.api.projects_api import ProjectsApi
from rafaysdk import Configuration, ApiClient
from rafaysdk.rest import ApiException
import requests
import yaml


class cloud_credentials:

    def __init__(self):
        data=self.get_config()
        self.project_sdk_instance = self.create_project_sdk_instance(data['host'], data['api_key'])

    def get_config(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(ROOT_DIR, 'user_config.yaml')
        with open(config_path) as file:
            data = yaml.safe_load(file)
        return data

    def create_project_sdk_instance(self, endpoint, apikey):
        """
        Creates projects sdk instance
        :param endpoint:
        :param apikey:
        :return:
        """
        configuration = Configuration()
        configuration.host = endpoint
        configuration.api_key['X-RAFAY-API-KEYID'] = apikey
        self.project_sdk_instance = ProjectsApi(ApiClient(configuration))
        return self.project_sdk_instance

    def list_projects(self):

        limit = 56  # int | Number of results to return per page (optional)
        offset = 56  # int | The base index of records to be returned in the results (optional)

        try:
            api_response = self.project_sdk_instance.list_projects()
        except ApiException as e:
            print("Exception when calling ProjectsApi->list_projects: %s\n" % e)

        return api_response.to_dict()['results']


    def get_project_id(self,project_name):
        """
        :param project_name:
        :return:
        """
        results = self.list_projects()

        for project in results:
            if project_name == project['name']:
                return project['id']

        return None

    def get_all_cloud_credentials(self, project_name, log=True):
        """
        :param project_name:
        :return:
        """
        project_id = self.get_project_id(project_name)
        data = self.get_config()
        provider_endpoint=data['host']+"/edge/v1/projects/"+project_id+"/providers/?limit=50&ofset=0"
        r = requests.get(provider_endpoint, headers={'X-RAFAY-API-KEYID': data['api_key']})
        if log == True:
            for result in r.json()['results']:
                print("provider_name: {}, provider_id: {}".format(result['name'], result['ID']))
        return r.json()['results']

    def get_cloud_credentials(self, project_name, provider_name):
        """
        :param project_name:
        :param provider_name:
        :return:
        """
        providers=self.get_all_cloud_credentials(project_name=project_name,log=False)
        for provider in providers:
            if provider['name'] == provider_name:
                print("provider_name: {}, provider_id: {}".format(provider['name'],provider['ID']))
                return provider['name'], provider['ID']

    def get_cloud_credential_id(self, project_name, provider_name):
        """
        :param project_name:
        :param provider_name:
        :return:
        """
        providers = self.get_all_cloud_credentials(project_name=project_name, log=False)
        for provider in providers:
            if provider['name'] == provider_name:
                return provider['ID']

class RunParser(object):

    def __init__(self):
        self.config = self.setup_flag_parser()

    def setup_flag_parser(self):
        parser = argparse.ArgumentParser(usage="cloud_credentials.py --project_name name --provider_name provider")

        parser.add_argument("--action",
                            type=str,
                            dest="action_",
                            default=None)

        parser.add_argument("--provider_name",
                            type=str,
                            dest="provider_name_",
                            default=None)

        parser.add_argument("--project_name",
                            type=str,
                            dest="project_name_",
                            default=None)

        args = parser.parse_args()

        return {"action":args.action_,"project_name":args.project_name_, "provider_name":args.provider_name_}


if __name__ == '__main__':
    providers = cloud_credentials()
    config = RunParser().config
    if config["action"] == "get":
        resp = providers.get_cloud_credentials(project_name=config["project_name"],
                                               provider_name=config["provider_name"])
        print(resp)
    if config["action"] == "list":
        resp = providers.get_all_cloud_credentials(project_name=config["project_name"], log=True)
    #if config["provider_name"]:
    #    resp = providers.get_cloud_credentials(project_name=config["project_name"],provider_name=config["provider_name"])
    #else:
    #    resp = providers.get_all_cloud_credentials(project_name=config["project_name"],log=True)
