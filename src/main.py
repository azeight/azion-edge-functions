#!/usr/local/bin/python3

import base64
import copy
from importlib.metadata import PathDistribution
from io import StringIO
import string
import json
import requests
import json
import yaml
import re
from datetime import datetime
import csv
import sys
from datetime import datetime, timedelta




#####################################################
## Classe de centralizacao de chamadas a API AZION ##
## Diego Barbosa Victoria - Azion                  ##
## Hackaton develop - 30/04/2022                   ##
#####################################################
class AzionAPI:
    def __init__(self, authentication):
        self._urlBase='https://api.azionapi.net'
        self._moduleApplicationAcceleration=False
        self._edgeAppID = 0;
        
        if ('Basic ' in authentication):
            self.createToken(authentication)
        else:
            self._token=authentication
            

    def getEdgeAppID(self):
        return self._edgeAppID;
    
    #################################
    ## Busca Token de autenticacao ##
    #################################
    def createToken(self,basic64):
        url = self._urlBase + "/tokens"
        
        payload="{\"query\":\"\",\"variables\":{}}"
        headers = {
            'Accept': 'application/json; version=3',
            'Authorization': '{basic64}'.format(basic64=basic64),
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        responseJson = response.json()
        self._token = responseJson.get('token')
    
    def _callGetMethod(self, path):

        url = self._urlBase + path

        payload = json.dumps({})
        headers = {
            'Accept': 'application/json; version=3',
            'Authorization': 'Token '+self._token,
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response

    def _callPostMethod(self, path, payload):
    
        url = self._urlBase + path

        headers = {
            'Accept': 'application/json; version=3',
            'Authorization': 'Token '+self._token,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.ok == False:
            raise Exception("\nERROR: "+response.text+"\nCALL: "+path+"\nPAYLOAD: "+payload)
        return response

    def _callPatchMethod(self, path, payload):
        
        url = self._urlBase + path

        headers = {
            'Accept': 'application/json; version=3',
            'Authorization': 'Token '+self._token,
            'Content-Type': 'application/json'
        }

        response = requests.request("PATCH", url, headers=headers, data=payload)
        if response.ok == False:
            raise Exception("\nERROR: "+response.text+"\nCALL: "+path+"\nPAYLOAD: "+payload)

        return response

    def _callPutMethod(self, path, payload):
        
        url = self._urlBase + path

        headers = {
            'Accept': 'application/json; version=3',
            'Authorization': 'Token '+self._token,
            'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        if response.ok == False:
            raise Exception("\nERROR: "+response.text+"\nCALL: "+path+"\nPAYLOAD: "+payload)

        return response

    def _callDeleteMethod(self, path, payload):
        
        url = self._urlBase + path

        headers = {
            'Accept': 'application/json; version=3',
            'Authorization': 'Token '+self._token,
            'Content-Type': 'application/json'
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)
        if response.ok == False:
            raise Exception("\nERROR: "+response.text+"\nCALL: "+path+"\nPAYLOAD: "+payload)

        return response

    #################################
    #### Busca dados do Dominio ####
    ################################ 
    def getDomain(self,cname):
        
        response = self._callGetMethod("/domains?page_size=100")
        responseJson = response.json()
        
        results=responseJson.get('results')

        out=0
        for reg in results:
            for regcname in reg['cnames']:
                if(regcname==cname):
                    out = reg
                    break
        return out

    ############################
    #### Cria novo Dominio ####
    ########################### 
    def createDomain(self,name, cnames, edgeAppId=False, cnameAccessOnly=False, isActive=True, environment='production'): 

        if(isinstance(cnames,str)):
            if "," in cnames:
                cnames = cnames.split(',')
            else:
                cnames = [cnames]
        
        payload = json.dumps({
            "name": name,
            "cname_access_only": False,
            "edge_application_id": edgeAppId,
            "is_active": isActive,
            "environment": environment
        })

        response = self._callPostMethod("/domains", payload)

        responseJson = response.json()
        
        results=responseJson.get('results')

        if cnames[0] != '':
            domainID=str(responseJson.get('results')['id'])

            payload = json.dumps({
                "cnames": cnames,
                "cname_access_only": cnameAccessOnly
            })

            response = self._callPatchMethod("/domains/"+domainID, payload)

            responseJson = response.json()
            
            results=responseJson.get('results')

        out=0
        if (len(results)>0):
            out = results
        
        return out

    #################################
    #### Busca dados de Edge App ####
    ################################ 
    def getEdgeApp(self,id): 
                
        response = self._callGetMethod("/edge_applications/" + str(id))

        responseJson = response.json()
        
        results=responseJson.get('results')

        out=0
        if (len(results)>0):
            out = results

        return out

    #####################################
    #### Criacao de Edge Application ####
    ##################################### 
    def createEdgeApp(self,cname,deliveryProto="http,https", httpPort=80, httpsPort=443, minimunTLS="",active=True, applicationAcceleration=False, caching=True, deviceDetection=False, 
                      edgeFirewall=False, edgeFunctions=True, imageOptimization=False, l2Caching=False, loadBalancer=False, rawLogs=False, waf=False,
                            originType="single_origin", address="to.remove.com", originProtoPolicy="preserve", hostHeader="${host}", 
                            browserCacheSettings="honor", browserCacheSettingsTTL=0,cdnCacheSettings="honor", cdnCacheSettingsTTL=0): 

        
        payload = json.dumps({
            "name": cname,
            "delivery_protocol": deliveryProto, 
            "origin_type": originType,
            "address": address,
            "origin_protocol_policy": originProtoPolicy,
            "host_header": hostHeader,
            "browser_cache_settings": browserCacheSettings,
            "browser_cache_settings_maximum_ttl": browserCacheSettingsTTL,
            "cdn_cache_settings": cdnCacheSettings,
            "cdn_cache_settings_maximum_ttl": cdnCacheSettingsTTL
        })
        
        response = self._callPostMethod("/edge_applications", payload)
        responseJson = response.json()

        edgeAppID=str(responseJson.get('results')['id'])
        edgeAppName=responseJson.get('results')['name']

        self._edgeAppID = edgeAppID
        

        ##PATCH (insere diferencas)

        payload = json.dumps({
            "http_port": httpPort,
            "https_port": httpsPort,
            "minimum_tls_version": minimunTLS,
            "active": active,
            "application_acceleration": applicationAcceleration,
            "caching": caching,
            "device_detection": deviceDetection,
            "edge_firewall": edgeFirewall,
            "edge_functions": edgeFunctions,
            "image_optimization": imageOptimization,
            "l2_caching": l2Caching,
            "load_balancer": loadBalancer,
            "raw_logs": rawLogs,
            "web_application_firewall": waf
        })

        response = self._callPatchMethod("/edge_applications/"+edgeAppID, payload)

        responseJson = response.json()
        
        results=responseJson.get('results')

        out=0
        if (len(results)>0):
            out = results
        
        return out


    ##################################
    #### Busca dados de Functions ####
    ##################################
    def getFunctions(self,name=''): 
        
        response = self._callGetMethod("/edge_functions?page_size=100")

        responseJson = response.json()
        
        results=responseJson.get('results')

        out=0
        if (len(results)>0):
            if(name!=''):
                for reg in results:
                    if(reg['name']==name):
                        out = reg
            #else:
            #    out = results

        return out

    #############################
    #### Criacao de Function ###
    ############################
    def createFunction(self, name, code, args, active, language='javascript', initiator='edge_application'):

        originData = {
                      "name": name,
                      "code": code,
                      "language": language,
                      "json_args": args,
                      "active": active
                    }
        payload = json.dumps( originData )

        response = self._callPostMethod("/edge_functions", payload)

        responseJson = response.json()
        
        results=responseJson.get('results')

        out=0
        if (len(results)>0):
            out = results
        
        return out

    #################################
    #### Atualizacao de Function ###
    ###############################
    def updateFunction(self, functionID, name, code, args, active, language='javascript', initiator='edge_application'):

        originData = {
                      "name": name,
                      "code": code,
                      "json_args": args,
                      "active": active
                    }
        payload = json.dumps( originData )

        response = self._callPutMethod("/edge_functions/" + str(functionID), payload)

        responseJson = response.json()
        
        results=responseJson.get('results')

        out=0
        if (len(results)>0):
            out = results
        
        return out

    #######################################
    #### Busca dados de App Functions ####
    ######################################
    def getAppFunctions(self,edgeAppID,name=''): 
                
        response = self._callGetMethod("/edge_applications/" + str(edgeAppID) + "/functions_instances?page_size=100")
        responseJson = response.json()
        
        results=responseJson.get('results')

        out=0
        if (len(results)>0):
            if(name!=''):
                for reg in results:
                    if(reg['name']==name):
                        out = reg
            #else:
            #    out = results

        return out

    ################################
    #### Criacao de App Function ###
    ################################
    def createAppFunction(self, name, edgeAppID, functionID, args):

        originData = {
          "name": name,
          "edge_function_id": functionID,
          "args": args
        }
        payload = json.dumps( originData )

        response = self._callPostMethod("/edge_applications/"+str(edgeAppID)+"/functions_instances", payload)

        responseJson = response.json()
        
        results=responseJson.get('results')

        out=0
        if (len(results)>0):
            out = results
        
        return out

    ###############################
    #### Busca dados de Rules ####
    ##############################
    def getRules(self,edgeAppID,name='',phase='request',targetDefault=False): 
        
        response = self._callGetMethod("/edge_applications/" + str(edgeAppID) + "/rules_engine/" + phase + "/rules?page_size=100")

        responseJson = response.json()
        
        results=responseJson.get('results')

        out=0
        if (len(results)>0):
            if(name!=''):
                for reg in results:
                    if(reg['name']==name and targetDefault==False):
                        out = reg
                    elif(reg['name']==name and targetDefault==True and reg['phase']=='default'):
                        out = reg
            else:
                if (targetDefault == True):
                    out = results
                else:
                    out=[]
                    for rule in results:
                        if rule['phase'] != 'default':
                            out.append(rule)

        return out

    #######################
    #### Altera Rules ####
    ######################
    def changeRules(self,edgeAppID,phase,ruleID,newRule): 

        payload = json.dumps( newRule )

        #headers = {
        #    'Accept': 'application/json; version=3',
        #    'Authorization': 'Token '+self._token,
        #    'Content-Type': 'application/json'
        #}

        #response = requests.request("PATCH", url, headers=headers, data=payload)
        response = self._callPatchMethod("/edge_applications/"+str(edgeAppID)+"/rules_engine/"+phase+"/rules/"+str(ruleID), payload)

        responseJson = response.json()
        
        results=responseJson.get('results')

        out=0
        if (len(results)>0):
            out = results
        
        return out

    #############################
    #### Criacao de Regra    ###
    ############################
    def createRule(self, name, edgeAppID, functionID, pathURI, phase='request'):

        originData = {
            "name": name,
            "phase": phase,
            "behaviors": [
                {
                    "name": "run_function",
                    "target": str(functionID)
                }
            ],
            "criteria": [
                [
                    {
                        "variable": "${uri}",
                        "operator": "is_equal",
                        "conditional": "if",
                        "input_value": pathURI
                    }
                ]
            ],
            "is_active": True
        }
        
        payload = json.dumps( originData )

        response = self._callPostMethod("/edge_applications/"+str(edgeAppID)+"/rules_engine/"+str(phase)+"/rules", payload)

        responseJson = response.json()
        
        results=responseJson.get('results')

        out=0
        if (len(results)>0):
            out = results
        
        return out



authentication = sys.argv[1]
yamlFile = sys.argv[2]

#with open(r'/Users/dv/Scripts/hackaton/config.yaml') as file:
with open(yamlFile) as file:
    content = yaml.full_load(file)

    for edgeFunctionRoot, funcList in content.items():
        for func in funcList:
            #print(func, ":", "")

            with open(func['path'],"r") as f:
                fileContent = f.read()

            cname       = func['domain']
            funcName    = func['name']
            code        = fileContent
            args        = func['args']
            funcActive  = func['active']
            pathURI     = func['path_uri']


            azion = AzionAPI(authentication)
            domain = azion.getDomain(cname)

            domainID = None
            edgeAppID = None

            if(domain != 0):
                domainID = domain['id']
                edgeAppID = domain['edge_application_id']
            else:
                edgeApp = azion.createEdgeApp( cname )
                if(edgeApp != 0):
                    domain = azion.createDomain(cname,cname,edgeApp['id'])
                    if(domain != 0):
                        domainID = domain['id']
                        edgeAppID = domain['edge_application_id']


            if (domain != 0 and edgeAppID != 0):
            
                function = azion.getFunctions(funcName)
                if(function!=0):
                    function = azion.updateFunction(function['id'], function['name'], code, args, funcActive)
                else:
                    function = azion.createFunction(funcName, code, args, funcActive)
                

                appFunction = azion.getAppFunctions(edgeAppID,funcName)
                if (appFunction == 0):
                    appFunction = azion.createAppFunction(funcName, edgeAppID, function['id'], args)

                rule = azion.getRules(edgeAppID,pathURI)
                if (rule == 0):
                    azion.createRule(pathURI, edgeAppID, appFunction['id'], pathURI)

                dt=datetime.today() + timedelta(minutes=5)
                whenExec = dt.strftime("%H:%M:%S")

                print("::set-output name=domain::https://"+domain['domain_name']+pathURI+"\n Access the url with your function after "+whenExec)

