import argparse
import os
from rafaysdk.models.project import Project
from rafaysdk.api.projects_api import ProjectsApi
from rafaysdk import Configuration, ApiClient
from rafaysdk.rest import ApiException
import yaml


class project_sdk_examples:

    def __init__(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(ROOT_DIR, 'user_config.yaml')
        with open(config_path) as file:
            data = yaml.safe_load(file)
        self.project_sdk_instance = self.create_project_sdk_instance(data['host'], data['api_key'])

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

    def create_project(self, project_name):
        """
        Creates Project
        :param project_name:
        :return:
        """
        data = Project(name=project_name,description='New project')
        try:
            api_response = self.project_sdk_instance.create_project(data=data)
            api_response = api_response.to_dict()
        except ApiException as e:
            print("Exception when calling ProjectsApi->create_project: %s\n" % e)

        return {"project_id":api_response['id'],"name":api_response['name']}

    def list_projects(self):

        limit = 56  # int | Number of results to return per page (optional)
        offset = 56  # int | The base index of records to be returned in the results (optional)

        try:
            api_response = self.project_sdk_instance.list_projects()
        except ApiException as e:
            print("Exception when calling ProjectsApi->list_projects: %s\n" % e)

        return api_response.to_dict()['results']


    def delete_project(self, project_id):
        """
        Delete Project
        :param project_id:
        :return:
        """
        try:
            self.project_sdk_instance.delete_project(id=project_id)
        except ApiException as e:
            print("Exception when calling ProjectsApi->delete_project: %s\\n" % e)
            return False

        return True

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

class RunParser(object):

    def __init__(self):
        self.config = self.setup_flag_parser()

    def setup_flag_parser(self):
        parser = argparse.ArgumentParser(usage="project_sdk_examples.py --action <get|delete|create> --project_name name")

        parser.add_argument("--action",
                            type=str,
                            dest="action_",
                            default=None)

        parser.add_argument("--project_name",
                            type=str,
                            dest="project_name_",
                            default=None)

        args = parser.parse_args()

        return {"action":args.action_, "project_name":args.project_name_}


if __name__ == '__main__':
    project = project_sdk_examples()
    config = RunParser().config
    if config["action"] == "get":
        resp = project.get_project_id(config["project_name"])
        print(resp)
    if config["action"] == "delete":
        project_id=project.get_project_id(config["project_name"])
        resp=project.delete_project(project_id=project_id)
        print(resp)
    if config["action"] == "create":
        resp = project.create_project(project_name=config["project_name"])
        print("Project Created:{}".format(resp))
