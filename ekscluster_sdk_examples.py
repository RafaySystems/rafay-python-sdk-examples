import argparse
import os
import yaml
from rafaysdk.api.cluster_api import ClusterApi
from rafaysdk import Configuration, ApiClient
from rafaysdk.rest import ApiException
from rafaysdk.models.cluster_infra import ClusterInfra

from project_sdk_examples import project_sdk_examples


class ekscluster_sdk_examples:
    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(ROOT_DIR, '../rafay-python-sdk-examples/user_config.yaml')
        with open(config_path) as file:
            data = yaml.load(file)
        self.cluster_sdk_instance = self.create_cluster_sdk_instance(data['host'], data['api_key'])
        self.project = project_sdk_examples()

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

    def provision_eks_cluster(self, cluster_name,cloud_provider_name,cloud_provider_id,blueprint,project_name,config_path):
        """
        Provision EKS-AWS type of cluster with config
        :param cluster_name:
        :param cloud_provider:
        :param cloud_provider_id:
        :param blueprint:
        :param project_id:
        :param config_path:
        :return:
        """
        with open(config_path) as file:
            data = yaml.load(file)
        params = {
        "params": "{\"region\":\"aws/" + data['metadata']['region'] + "\",\"instance_type\":\"" + data['nodeGroups'][0]['instanceType'] + "\",\"version\":\"" + data['metadata']['version'] + "\",\"nodes\":" + str(data['nodeGroups'][0]['desiredCapacity']) + ","
                  "\"nodes_min\":" + str(data['nodeGroups'][0]['maxSize']) + ",\"nodes_max\":" + str(data['nodeGroups'][0]['minSize']) + ",\"node_volume_type\":\"" + data['nodeGroups'][0]['volumeType'] + "\",\"node_ami_family\":\"" + data['nodeGroups'][0]['amiFamily'] + "\", "
                  "\"vpc_nat_mode\":\"" + data['vpc']['nat']['gateway'] + "\",\"vpc_cidr\":\"" + data['vpc']['cidr'] + "\",\"enable_full_access_to_ecr\":true,"
                  "\"enable_asg_access\":true,\"managed\":false,\"node_private_networking\":false,"
                  "\"cluster_endpoint_access_type\":\"private\", "
                  "\"private_access\":\"" + str(data['vpc']['clusterEndpoints']['privateAccess']).lower() + "\",\"public_access\":\"" + str(data['vpc']['clusterEndpoints']['publicAccess']).lower() + "\",\"nodegroup_name\":\"" + data['metadata']['name'] + "\","
                  "\"vpc_private_subnets\":[],\"vpc_public_subnets\":[]} "
        }
        project_id = self.project.get_project_id(project_name=project_name)
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


    def delete_cluster(self,project_id,cluster_id):
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
        parser = argparse.ArgumentParser(usage="ekscluster_sdk_examples.py --cluster_name <cluster-name> --project_name <project-name> --config_file <path-to-config-file> --cluster_blueprint <blueprint-name> --cloud_provider_id <cloud-provider-id> --cloud_provider_name <cloud-provider-name>")

        parser.add_argument("--cluster_name",
                            type=str,
                            dest="cluster_name_",
                            default=None)

        parser.add_argument("--cloud_provider_name",
                            nargs="*",
                            type=str,
                            dest="cloud_provider_name_",
                            default=None)

        parser.add_argument("--cloud_provider_id",
                            type=str,
                            dest="cloud_provider_id_",
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

        return {"cluster_name": args.cluster_name_, "cloud_provider_id": args.cloud_provider_id_, "cluster_blueprint": args.cluster_blueprint_,
                "project_name": args.project_name_,"cloud_provider_name":args.cloud_provider_name_,"config_file": args.config_file_}


if __name__ == '__main__':
    cluster = ekscluster_sdk_examples()
    config = RunParser().config
    resp = cluster.provision_eks_cluster(cluster_name=config["cluster_name"],config_path=config["config_file"],cloud_provider_name=config["cloud_provider_name"],
                                        cloud_provider_id=config["cloud_provider_id"],blueprint=config["cluster_blueprint"],project_name=config["project_name"])
    print("Cluster Created:{}".format(resp))
    # print(cluster.provision_cluster('rx28oml','7w2lnkp'))