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
            data = yaml.load(file,Loader=yaml.FullLoader)
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

class RunParser(object):

    def __init__(self):
        self.config = self.setup_flag_parser()

    def setup_flag_parser(self):
        parser = argparse.ArgumentParser(usage="project_sdk_examples.py --project_name name")

        parser.add_argument("--project_name",
                            type=str,
                            dest="project_name_",
                            default=None)

        args = parser.parse_args()

        return {"project_name":args.project_name_}


if __name__ == '__main__':
    project = project_sdk_examples()
    config = RunParser().config
    resp = project.create_project(project_name=config["project_name"])
    print("Project Created:{}".format(resp))
    # project.delete_project(project_id='g299z32')