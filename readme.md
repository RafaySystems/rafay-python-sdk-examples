# Rafay Python SDK Examples
This repo provides how in generating python SDK and examples on how to manage multiple resources using SDK bindings.
##### Prerequisite(s) :
- Ensure to run on python3.8
- Installing Rafay SDK
  - Used Docker images to generate SDK in desired location
    ```
    docker run --rm -v /tmp:/tmp/ swaggerapi/swagger-codegen-cli generate -i https://app.rafay.dev/swagger-ui/rafay-swagger-specs.json -l python -o /tmp/SDKGEN -DpackageName=rafaysdk
    ```
  - After generating SDK install SDK using pip at the SDK path
    
    ```
    user~/tmp/SDKGEN% pip install . 
    ```
  - Ensure SDK is generated with name **`rafaysdk`**, as examples are referring sdk with this name
##### Configuration file : 
Configuration file `config.yaml` has two parameters 
1. console_url - Rafay controller URL 
2. api_key - Generated API key to be placed here. SDK uses this API Key to authenticate and Authorize SDK binding calls.
```yaml
console_url : 100  #100 concurrent sessions 
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
   python3 addon_sdk_examples.py --namespace sample-namespace --addon_name sample-addon --project_id pd270k4 --version v1
    ```
   - Output: 
   ```
   Addon created:{'addon_id': 'g29wek0', 'type': 'NativeYaml', 'name': 'sample-addon'}
   ```
3. `blueprint_example.py`:
     - Run below command with necessary runner arguments to a create blueprint
    ```
    python3 blueprint_sdk_examples.py --blueprint_name sample-blueprint --addons sample-addon sample-addon1 --project_id pd270k4 --version v1
    ```
    - Output: 
   ```
   Blueprint Created:{'name': 'sample-blueprint', 'id': 'dpkv0mn'}
   ```