import argparse
import os
import simplejson
import json
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.OperatingSystem import OperatingSystem
from rafaysdk.models.project import Project
from rafaysdk.models.publish_addon_request import PublishAddonRequest
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
        self.project_sdk_instance = self.create_project_sdk_instance(data['console_url'], data['api_key'])

    def create_project_sdk_instance(self, endpoint, apikey):
        """
        Creates partner user's organziation sdk instance
        :param endpoint:
        :param apikey:
        :param api_secret:
        :return:
        """
        configuration = Configuration()
        configuration.host = endpoint
        configuration.api_key['X-RAFAY-API-KEYID'] = apikey
        self.project_sdk_instance = ProjectsApi(ApiClient(configuration))
        return self.project_sdk_instance

    def create_project(self, project_name):
        """
        Creates yaml type addon with version
        :param addon_name:
        :param project_id:
        :param namespace:
        :param payload:
        :param version:
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
        :param project_id:
        :param addon_id:
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
        # not specifying a suite is supported in testrunner, we have a default here so that tests can be run without args
        parser = argparse.ArgumentParser()

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