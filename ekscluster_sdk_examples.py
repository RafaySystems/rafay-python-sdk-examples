import argparse
import os
import yaml
from rafaysdk.api.cluster_api import ClusterApi
from rafaysdk import Configuration, ApiClient
from rafaysdk.rest import ApiException
from rafaysdk.models.cluster_infra import ClusterInfra

from project_sdk_examples import project_sdk_examples
from cloud_credentials import cloud_credentials


class ekscluster_sdk_examples:
    def __init__(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(ROOT_DIR, 'user_config.yaml')
        with open(config_path) as file:
            data = yaml.safe_load(file)
        self.cluster_sdk_instance = self.create_cluster_sdk_instance(data['host'], data['api_key'])
        self.project = project_sdk_examples()
        self.cloud_credentials = cloud_credentials()

    def create_cluster_sdk_instance(self, endpoint, apikey):
        """
        Creates Cluster sdk instance
        :param endpoint:
        :param apikey:
        :return:
        """
        configuration = Configuration()
        configuration.host = endpoint
        configuration.api_key['X-RAFAY-API-KEYID'] = apikey
        self.cluster_sdk_instance = ClusterApi(ApiClient(configuration))
        return self.cluster_sdk_instance

    def provision_eks_cluster(self, cluster_name,cloud_provider_name,blueprint,project_name,config_path):
        """
        Provision EKS-AWS type of cluster with config
        :param cluster_name:
        :param cloud_provider:
        :param blueprint:
        :param project_name:
        :param config_path:
        :return:
        """
        with open(config_path) as file:
            data = yaml.safe_load(file)
        if "subnets" in data['vpc']:
            if "private" in data['vpc']['subnets']:
                private_subnets = []
                VPC_CIDR = ''
                for k, v in data['vpc']['subnets']['private'].items():
                    private_subnets.append(data['vpc']['subnets']['private'][k]['id'])
            if "public" in data['vpc']['subnets']:
                VPC_CIDR = ''
                public_subnets = []
                for k, v in data['vpc']['subnets']['public'].items():
                    public_subnets.append(data['vpc']['subnets']['public'][k]['id'])
        else:
            private_subnets = ''
            public_subnets = ''
            VPC_CIDR = data['vpc']['cidr']
        if "privateNetworking" in data['nodeGroups'][0]:
            node_networking = data['nodeGroups'][0]['privateNetworking']
        else:
            node_networking = "false"
        params = {
        "params": "{\"region\":\"aws/" + data['metadata']['region'] + "\",\"instance_type\":\"" + data['nodeGroups'][0]['instanceType'] + "\",\"version\":\"" + data['metadata']['version'] + "\",\"nodes\":" + str(data['nodeGroups'][0]['desiredCapacity']) + ","
                  "\"nodes_min\":" + str(data['nodeGroups'][0]['maxSize']) + ",\"nodes_max\":" + str(data['nodeGroups'][0]['minSize']) + ",\"node_volume_type\":\"" + data['nodeGroups'][0]['volumeType'] + "\",\"node_ami_family\":\"" + data['nodeGroups'][0]['amiFamily'] + "\", "
                  "\"vpc_nat_mode\":\"" + data['vpc']['nat']['gateway'] + "\",\"vpc_cidr\":\"" + VPC_CIDR + "\",\"enable_full_access_to_ecr\":true,"
                  "\"enable_asg_access\":true,\"managed\":false,\"node_private_networking\":" + str(node_networking).lower() +","
                  "\"cluster_endpoint_access_type\":\"private\", "
                  "\"private_access\":\"" + str(data['vpc']['clusterEndpoints']['privateAccess']).lower() + "\",\"public_access\":\"" + str(data['vpc']['clusterEndpoints']['publicAccess']).lower() + "\",\"nodegroup_name\":\"" + data['metadata']['name'] + "\","
                  "\"vpc_private_subnets\": [" + str(private_subnets)[1:-1].replace("'",'"') + "],\"vpc_public_subnets\": [" + str(public_subnets)[1:-1].replace("'",'"') + "]} "
        }
        project_id = self.project.get_project_id(project_name=project_name)
        cloud_provider_id= self.cloud_credentials.get_cloud_credential_id(project_name=project_name,provider_name=cloud_provider_name)
        data = ClusterInfra(name=cluster_name, cluster_type='aws-eks', cloud_provider=cloud_provider_name, provider_id=cloud_provider_id,
                                                cluster_provider_params=params,cluster_blueprint=blueprint,auto_create=True)

        api_response = self.cluster_sdk_instance.create_cluster(project_id, cluster_data=data)
        resp = api_response.to_dict()

        try:
            # Provision cluster
            self.cluster_sdk_instance.provision_cluster(project_id, resp['id'])
        except ApiException as e:
            print("Exception when calling ClusterApi->provision_cluster: %s\n" % e)

        return {"cluster_id":resp['id'],"cluster_type":resp['cluster_type'],"cluster_name":resp['name']}

    def list_clusters(self, project_name):

        """
        :param project_name:
        :return:
        """

        limit = 56  # int | Number of results to return per page (optional)
        offset = 56  # int | The base index of records to be returned in the results (optional)

        project_id = self.project.get_project_id(project_name=project_name)
        try:
            api_response = self.cluster_sdk_instance.list_clusters(project_id=project_id)
        except ApiException as e:
            print("Exception when calling ClusterApi->list_clusters: %s\n" % e)

        return api_response.to_dict()['results']

    def get_cluster_id(self, project_name, cluster_name):
        """
        :param project_name:
        :param cluster_name:
        :return:
        """
        results = self.list_clusters(project_name)

        for cluster in results:
            if cluster_name == cluster['name']:
                return cluster['id']

    def get_cluster(self, project_name, cluster_name):
        """
        Get cluster details
        :param project_name:
        :param cluster_name:
        :return:
        """
        project_id = self.project.get_project_id(project_name=project_name)
        cluster_id = self.get_cluster_id(project_name, cluster_name)
        try:
            response = self.cluster_sdk_instance.get_cluster(cluster_id=cluster_id, project_id=project_id)
        except ApiException as e:
            print("Exception when calling ClusterApi->get_cluster: %s\\n" % e)

        return response.to_dict()

    def get_cluster_status(self, project_name, cluster_name):
        """
        Get cluster status
        :param project_name:
        :param cluster_name:
        :return:
        """
        project_id = self.project.get_project_id(project_name=project_name)
        cluster_id = self.get_cluster_id(project_name, cluster_name)
        try:
            response = self.cluster_sdk_instance.get_cluster(cluster_id=cluster_id, project_id=project_id)
        except ApiException as e:
            print("Exception when calling ClusterApi->get_cluster_status: %s\\n" % e)

        return response.to_dict()['status']

    def get_cluster_provision_status(self, project_name, cluster_name):
        """
        Get cluster status
        :param project_name:
        :param cluster_name:
        :return:
        """
        project_id = self.project.get_project_id(project_name=project_name)
        cluster_id = self.get_cluster_id(project_name, cluster_name)
        try:
            response = self.cluster_sdk_instance.get_cluster(cluster_id=cluster_id, project_id=project_id)
        except ApiException as e:
            print("Exception when calling ClusterApi->get_cluster_provision_status: %s\\n" % e)

        return response.to_dict()['provision']['status']

    def delete_cluster(self,project_name,cluster_name):

        """
        Get cluster details
        :param project_name:
        :param cluster_name:
        :return:
        """

        project_id = self.project.get_project_id(project_name=project_name)
        cluster_id = self.get_cluster_id(project_name, cluster_name)
        try:
            # Delete cluster
            self.cluster_sdk_instance.delete_cluster(project_id, cluster_id)
        except ApiException as e:
            print("Exception when calling ClusterApi->delete_cluster: %s\n" % e)

        return True

class RunParser(object):

    def __init__(self):
        self.config = self.setup_flag_parser()

    def setup_flag_parser(self):
        parser = argparse.ArgumentParser(usage="ekscluster_sdk_examples.py --action <get|delete|create|list|status> --cluster_name <cluster-name> --project_name <project-name> --config_file <path-to-config-file> --cluster_blueprint <blueprint-name> --cloud_provider_id <cloud-provider-id> --cloud_provider_name <cloud-provider-name>")

        parser.add_argument("--action",
                            type=str,
                            dest="action_",
                            default=None)

        parser.add_argument("--cluster_name",
                            type=str,
                            dest="cluster_name_",
                            default=None)

        parser.add_argument("--cloud_provider_name",
                            type=str,
                            dest="cloud_provider_name_",
                            default=None)

        parser.add_argument("--cluster_blueprint",
                            type=str,
                            dest="cluster_blueprint_",
                            default=None)

        parser.add_argument("--project_name",
                            type=str,
                            dest="project_name_",
                            default=None)

        parser.add_argument("--config_file",
                            type=str,
                            dest="config_file_",
                            default=None)

        args = parser.parse_args()

        return {"action":args.action_,"cluster_name": args.cluster_name_, "cluster_blueprint": args.cluster_blueprint_,
                "project_name": args.project_name_,"cloud_provider_name":args.cloud_provider_name_,"config_file": args.config_file_}


if __name__ == '__main__':
    cluster = ekscluster_sdk_examples()
    config = RunParser().config
    if config["action"] == "get":
        resp = cluster.get_cluster(config["project_name"], config["cluster_name"])
        print(resp)
    if config["action"] == "list":
        resp = cluster.list_clusters(config["project_name"])
        print(resp)
    if config["action"] == "delete":
        resp = cluster.delete_cluster(config["project_name"], config["cluster_name"])
        print(resp)
    if config["action"] == "status":
        resp = cluster.get_cluster_status(config["project_name"], config["cluster_name"])
        print(resp)
    if config["action"] == "create":
        resp = cluster.provision_eks_cluster(cluster_name=config["cluster_name"],config_path=config["config_file"],cloud_provider_name=config["cloud_provider_name"],
                                        blueprint=config["cluster_blueprint"],project_name=config["project_name"])
        print("Cluster Created:{}".format(resp))