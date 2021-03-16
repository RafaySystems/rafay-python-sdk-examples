# Rafay Python SDK Examples
This repo provides how in generating python SDK and examples on how to manage multiple resources using SDK bindings.
##### Prerequisite(s) :
- Ensure to run on python3.8
- Installing Rafay SDK
  - Ensure SDK is generated with name **`rafaysdk`**, as examples are referring sdk with this name
  - Used Docker images to generate SDK in desired location
    ```
    docker run --rm -v /tmp:/tmp/ swaggerapi/swagger-codegen-cli generate -i https://console.rafay.dev/swagger-ui/rafay-swagger-specs.json -l python -o /tmp/SDKGEN -DpackageName=rafaysdk
    ```
  - After generating SDK install SDK using pip at the SDK path
    
    ```
    cd /tmp/SDKGEN
    user~/tmp/SDKGEN% pip install .
    ```
- Clone this repo and install requirements
   ```
   git clone https://github.com/RafaySystems/rafay-python-sdk-examples.git
   cd rafay-python-sdk-examples
   pip install -r requirements.txt
   ```

##### Configuration file :
Configuration file `user_config.yaml` has two parameters
1. console_url - Rafay controller URL 
2. api_key - Generated API key to be placed here. SDK uses this API Key to authenticate and Authorize SDK binding calls.
```yaml
host : "https://console.rafay.dev"
api_key: <api_key generated from your rafay organziation>
```
#### Running
1. `project_sdk_examples.py`:
     - Run below command with necessary runner arguments to a create project
    ```
   python3 project_sdk_examples.py --project_name sample_project
    ```
    - Output: 
   ```
   Project Created:{'project_id': 'pd270k4', 'name': 'sample_project'}
   ```
2. `addon_sdk_examples.py`:
    - Run below command with necessary runner arguments to create addon
    ```
   python3 addon_sdk_examples.py --namespace sample-namespace --addon_name sample-addon --project_name sample_project --version v1
    ```
   - Output: 
   ```
   Addon created:{'addon_id': 'g29wek0', 'type': 'NativeYaml', 'name': 'sample-addon'}
   ```
3. `blueprint_example.py`:
     - Run below command with necessary runner arguments to a create blueprint
    ```
    python3 blueprint_sdk_examples.py --blueprint_name sample-blueprint --addons sample-addon sample-addon1 --project_name sample_project --version v1
    ```
    - Output: 
   ```
   Blueprint Created:{'name': 'sample-blueprint', 'id': 'dpkv0mn'}
   ```
4. `ekscluster_sdk_examples.py`:
     - Run below command with necessary runner arguments to a provision EKS-Cluster
       
    -   Sample EKS Config File for --config_file argument
    ```yaml
    apiVersion: rafay.io/v1alpha5
    kind: ClusterConfig
    metadata:
      name: demo-eks
      region: us-west-1
      version: "1.18"
    nodeGroups:
    - amiFamily: AmazonLinux2
      desiredCapacity: 1
      iam:
        withAddonPolicies:
          autoScaler: true
          imageBuilder: true
      instanceType: t3.xlarge
      maxSize: 1
      minSize: 1
      name: ankur-ng
      volumeSize: 70
      volumeType: gp2
    vpc:
      cidr: 192.168.0.0/16
      clusterEndpoints:
        privateAccess: true
        publicAccess: false
      nat:
        gateway: Single
    ```
    ```
    python3 ekscluster_sdk_examples.py --cluster_name demo-eks --project_name defaultproject --config_file ./eks-config.yaml --cluster_blueprint default --cloud_provider_id gkj3nzm --cloud_provider_name dev-credential
    ```
    - Output: 
   ```
   Cluster Created:{'cluster_id': 'j2q4p8k', 'cluster_type': 'aws-eks', 'cluster_name': 'demo-eks-test'}
   ```