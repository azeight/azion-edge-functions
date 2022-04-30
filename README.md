# Azion Edge Function docker action

Create or update an Edge Functions on Azion Edge Nodes.

## Inputs

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

**Required** Configuration file with Edge Functions details

In the yaml file, you have the configuration example please fill with your own data:
* name: name of your Edge Function
* path: path and filename with the source code using JavaScript language.
* domain: your domain, maybe a CNAME record
* args: parameters for use in the edge function at runtime, the argument name and value of each argument used on the JavaScript code.
  * arg1 "first argument name" : "value of first argument"
  * arg2 "second argument name" : "value of second argument" 	
  * arg..N "N argument" : "value of N argument" 
* path_uri: URI path of your edge function
* active: boolean that control if your Edge Function is active or not, domain values (true|false). Your function is only accessible when it is active true.


## Outputs

## `domain`

URI of the edge function deployed.

You could use this URI, ir necessary you can create a CNAME at your DNS. For local use and testing, you can change your /etc/hosts for your domain.


## Example usage on Github Action

```
uses: actions/azion-edge-function@v1
with:
  azion-auth: "Authorization: TOKEN[455SAFafa#$sfdsf789aswas23casf3=]
  config: 'function1.yaml'
```

## Example of configuration file

A YAML format file, containing the details of your edge function at Azion.

Not change the edge_functions name, and name of parameters, just fill the values. The exception is for args, when you need to change the arg names and arg values.
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

