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
     - Run below command with to a create project
    ```
   python3 project_sdk_examples.py --action create --project_name sampleproject
    ```
    - Output: 
   ```
   Project Created:{'project_id': 'pd270k4', 'name': 'sampleproject'}
   ```
2. `namespace_sdk_examples.py`:
    - Run below command to create namespace
    ```
    python3 namespace.py --action create --project sampleproject --namespace demo
    ```
   - Output:
   ```
   Namespace created:{'namespace_id': 'j2qqyz2', 'name': 'demo'}
   ```

3. `addon_sdk_examples.py`:
    - Run below command to create addon
    ```
    python3 addon.py --action create --project_name sampleproject --addon_name demo1 --addon_type NativeHelm --version v1 --namespace demo --chart config/chartmuseum.tgz --values config/chartmuseum-values.yaml
    ```
   - Output: 
   ```
   Addon created:{'addon_id': 'g29wek0', 'type': 'NativeHelm', 'name': 'demo1'}
   ```

4. `blueprint_sdk_examples.py`:
     - Run below command to a create blueprint
    ```
    python3 blueprint_sdk_examples.py --action create --project_name sampleproject --blueprint_name demo --version v1 --addons demo1
    ```
    - Output: 
   ```
   Blueprint Created:{'name': 'demo', 'id': 'dpkv0mn'}
   ```

5. `ekscluster_sdk_examples.py`:
    - Run below command to a provision EKS-Cluster
       
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
    python3 ekscluster_sdk_examples.py --action create --cluster_name demo-eks --cloud_provider_name aws-dev --cluster_blueprint demo --project_name sampleproject --config_file ./eks-config.yaml
    ```
    - Output: 
   ```
   Cluster Created:{'cluster_id': 'j2q4p8k', 'cluster_type': 'aws-eks', 'cluster_name': 'demo-eks'}
   ```

   - To get the status of an EKS-Cluster:
   ```
   python3 ekscluster_sdk_examples.py --action status --project_name sampleproject --cluster_name demo-eks
   ```