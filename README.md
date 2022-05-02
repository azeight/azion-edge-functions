# Azion Edge Function docker action

Create or update an Edge Functions on Azion Edge Nodes.

The domain name is the key for decision to a create or update an Edge Function, then if the domain name is already on use by an Edge Function, the function will be updated.


## API Inputs

## `azion-auth`

**Required** Authentication method

Create your free account on Azion site https://azion.com to use this action.

For authentication you can use __Basic__ or __Token__ methods.

Details how to create your Token or generate a base64 for Basic method, please visit https://api.azion.com/#58ba6991-2fe6-415c-9f17-a44dc0bc8cd4. Token authorization ensure more secure method than Basic, tokens are valid up to 24 hours, generate other token if it's expired.

* For Basic method use in this input “Authorization: Basic <YOUR BASE64 HERE>” 
  * For example: “Authorization: Basic dXNlckdBabn1hiW46cGFzc3dvcmQK”
* For Token method use in this input "Authorization: TOKEN[YOUR TOKEN HERE]"
  * For example: "Authorization: TOKEN[455SAFafa#$sfdsf789aswas23casf3=]

## `config`

**Required** Configuration file with Azion Edge Functions details

In the __action.yaml__ file, you have the configuration example please fill with your own data:
* name: name of your Edge Function
* path: path and filename with the source code using __JavaScript__ language.
* domain: your domain, maybe a __CNAME__ record
* args: parameters for use in the edge function at runtime, the argument name and value of each argument used on the JavaScript code.
  * arg1 "first argument name" : "value of first argument"
  * arg2 "second argument name" : "value of second argument" 	
  * arg..N "N argument" : "value of N argument" 
* path_uri: the __URI__ path of your edge function
* active: boolean that control if your Edge Function is active or not, domain values (true|false). Your function is only accessible when it is active true.


## Outputs

## `domain`

__URI__ of the edge function deployed.

You could use this __URI__, ir necessary you can create a __CNAME__ at your __DNS__. For local use and testing, you can change your __/etc/hosts__ for your domain.


## Example usage on Github Action

File available

```
uses: actions/azion-edge-function@v1
with:
  azion-auth: "Authorization: TOKEN[455SAFafa#$sfdsf789aswas23casf3=]
  config: 'function1.yaml'
```

## Example of configuration file

Edit the __action.yaml__ file, containing the details of your edge functions at Azion.

Don't change the __edge_functions__ name, and name parameters but instead just complete with desired values. The exception is for args, when you need to change the arg names and arg values.
```
edge_functions:
  -
    path: "example/src/messages.js"
    domain: "www.yourdomain.com"
    name: "Function Hello World Azion"
    args: 
      arg1: "value1"
      arg2: "value2"
    path_uri: "/api/messages/"
    active: "true"
```

More details on [Azion site](www.azion.com)
