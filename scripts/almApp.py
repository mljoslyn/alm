# checkout submodules
def checkoutSubmodules():
	print("Pulling Submodules ")
	statementStatus  = subprocess.call('git submodule init', shell=True)
	if statementStatus == 1 :
		sys.exit("Error when init submodule ")
	statementStatus  = subprocess.call('git submodule update --init --remote', shell=True)
	if statementStatus == 1 :
		sys.exit("Error when updating submodules")

	return statementStatus


def buildProject(mavenCommand,projectDir):
	statementStatus  = subprocess.call(mavenCommand, shell=True)
	if statementStatus == 1 :
		sys.exit("Error building the project "+projectDir)

	return statementStatus



def deployProject(config, cfCommand, projectDir):
	print("****************** Running deployProject for ******************" + projectDir)
	print("Fast install set =" + config.fastinstall)
	print("artifactory repo=" + config.artifactoryrepo)
	print("artifactory user =" + config.artifactoryuser)
	print("artifactory pass =" + config.artifactorypass)
 	print ("Current Directory = " + os.getcwd())
 	print ("Project Directory = " + projectDir)

	artifactId=""
	version=""
  	artifactory=""
  	artifactoryrepo=""
	artifactoryuser=""
	artifactorypass=""
	if config.fastinstall == 'y' :
		print('mvnsettings=' + config.mvnsettings)
		print('mavenRepo=' + config.mavenRepo)
		print("Copying artifacts..")
		os.chdir(projectDir)
 		print ("Current Directory = " + os.getcwd())
		f = open("pom.xml", 'r')
		f1 = f.read()
		f.close()
		print("=============")
		artifactIdTemp=re.search(r'<artifactId[^>]*>([^<]+)</artifactId>', f1)
		if artifactIdTemp:
        		print(artifactIdTemp.group(1))
			artifactId=artifactIdTemp.group(1)
		else:
			sys.exit("Error getting artifactId from " + projectDir + "/pom.xml")
		versionTemp=re.search(r'<version[^>]*>([^<]+)</version>', f1)
		if versionTemp:
		        print(versionTemp.group(1))
			version=versionTemp.group(1)
		else:
			sys.exit("Error getting version from " + projectDir + "/pom.xml")
		print("ArtifactId derived from pom.xml = " + artifactId)
		print("Version derived from pom.xml" + version)
		os.chdir("..")
		f = open(config.mvnsettings, 'r')
		f1 = f.read()
		f.close()
		#print(f1)
		found = 0
		dom = parse(config.mvnsettings)
		serverlist = dom.getElementsByTagName("server")
		for aServer in  serverlist:
			artifactory1 = aServer.getElementsByTagName("id")[0].firstChild.data 
			artifactoryuser = aServer.getElementsByTagName("username")[0].firstChild.data
			artifactorypass = aServer.getElementsByTagName("password")[0].firstChild.data
        		print("server id === " + artifactory1)
			repolist = dom.getElementsByTagName("repository")
        		for aRepo in  repolist:
				artifactory2 = aRepo.getElementsByTagName("id")[0].firstChild.data 
				artifactoryrepo = aRepo.getElementsByTagName("url")[0].firstChild.data
				print("REPOSITORY INFO :" + artifactory2)
				if artifactory1 == artifactory2 :
					print("Artifactory derived from maven settings.xml ==== " + artifactory2)
					print("Artifactory url from maven settings.xml ==== " + artifactoryrepo)
					print("Artifactory user derived from maven settings.xml ==== " + artifactoryuser)
					#print("Artifactory pass derived from maven settings.xml ==== " + artifactorypass)
	 				print ("Current Directory = " + os.getcwd())
					os.chdir(projectDir)
					try:
						os.stat("target")
					except:
						os.mkdir("target")
					request = Request(artifactoryrepo + "/com/ge/predix/solsvc/" + projectDir + "/" + version + "/" + artifactId + "-" + version + ".jar")
					authString = artifactoryuser + ":" + artifactorypass
					base64string = base64.b64encode(bytearray(authString, 'UTF-8')).decode("ascii")
					request.add_header("Authorization", "Basic %s" % base64string)
					try:
        					print("Downloading....")
        					result = urlopen(request)
        					with open("target/" + artifactId + "-" + version + ".jar", "wb") as local_file:
            						local_file.write(result.read())
						print("Found in this repo:" + artifactory + " url: " + artifactoryrepo)
        					print("Downloading....DONE")
						print("============================")
						found = 1
						os.chdir("..")
						break
					except URLError as err:
					        e = sys.exc_info()[1]
					        print("Error: %s" % e)
						found = 0
						os.chdir("..")
						continue
					except HTTPError as err:
        					e = sys.exc_info()[1]
					        print("Error: %s" % e)
						found = 0
						os.chdir("..")
						continue
			if found == 1:
				break
		if found == 0:
			sys.exit("Error copying artifact "+projectDir)
		else:
			print("Deploying to CF...")
			pushStatus = cfPush(cfCommand, projectDir)
			print("Deployment to CF done.")
			return pushStatus

def cfPush(cfCommand, projectDir):
	print("Deploying project as  "+cfCommand + " projectDir=" + projectDir)
	statementStatus  = subprocess.call(cfCommand, shell=True)
	if statementStatus == 1 :
		sys.exit("Error deploying the project"+projectDir)

	return statementStatus

def deleteExistingApplications(config):
	deleteRequest = "cf delete -f -r " + config.predixbootAppName
	statementStatus  = subprocess.call(deleteRequest, shell=True)

	if statementStatus == 1 :
		print("Error deleting an application: " +deleteRequest)
	time.sleep(5)  # Delay for 5 seconds
	deleteRequest = "cf delete -f -r " +config.dataSeedAppName
	statementStatus  = subprocess.call(deleteRequest, shell=True)
	if statementStatus == 1 :
		print("Error deleting an application: " +deleteRequest)
	time.sleep(5)  # Delay for 5 seconds
	deleteRequest = "cf delete -f -r " +config.dataSourceAppName
	statementStatus  = subprocess.call(deleteRequest, shell=True)
	if statementStatus == 1 :
		print("Error deleting an application: " +deleteRequest)
	time.sleep(5)  # Delay for 5 seconds
	deleteRequest = "cf delete -f -r " +config.websocketAppName
	statementStatus  = subprocess.call(deleteRequest, shell=True)
	if statementStatus == 1 :
		print("Error deleting an application: " +deleteRequest)
	time.sleep(5)  # Delay for 5 seconds
	deleteRequest = "cf delete -f -r " +config.dataIngestionAppName
	statementStatus  = subprocess.call(deleteRequest, shell=True)
	if statementStatus == 1 :
		print("Error deleting an application: " +deleteRequest)
	time.sleep(5)  # Delay for 5 seconds
	deleteRequest = "cf delete -f -r " +config.machineSimulatorAppName
	statementStatus  = subprocess.call(deleteRequest, shell=True)
	if statementStatus == 1 :
		print("Error deleting an application: " +deleteRequest)
	time.sleep(5)  # Delay for 5 seconds
	deleteRequest = "cf delete -f -r " +config.uiAppName
	statementStatus  = subprocess.call(deleteRequest, shell=True)
	if statementStatus == 1 :
		print("Error deleting an application: " +deleteRequest)
	time.sleep(10)  # Delay for 10 seconds
	return statementStatus

def deleteExistingServices(config):
	print("Delete Services>? : "+config.allDeploy)
	if config.allDeploy in ('y','Y'):
		#delete UAA instance

		deleteRequest = "cf delete-service -f "
		statementStatus  = subprocess.call(deleteRequest+config.rmdUaaName, shell=True)
		if statementStatus == 1 :
			sys.exit("Error deleting an service instance: " +config.rmdUaaName)
		time.sleep(10)  # Delay
		statementStatus  = subprocess.call(deleteRequest+config.rmdAcsName, shell=True)
		if statementStatus == 1 :
			sys.exit("Error deleting an service instance: " +config.rmdAcsName)
		time.sleep(3)  # Delay
		statementStatus  = subprocess.call(deleteRequest+config.rmdPredixAssetName, shell=True)
		if statementStatus == 1 :
			sys.exit("Error deleting an service instance: " +config.rmdPredixAssetName)
		time.sleep(3)  # Delay
		statementStatus  = subprocess.call(deleteRequest+config.rmdPredixTimeseriesName, shell=True)
		if statementStatus == 1 :
			sys.exit("Error deleting an service instance: " +config.rmdPredixTimeseriesName)
		time.sleep(3)  # Delay
		statementStatus  = subprocess.call(deleteRequest+config.rmdPostgre, shell=True)
		if statementStatus == 1 :
			sys.exit("Error deleting an service instance: " +config.rmdPostgre)
		time.sleep(3)  # Delay
		statementStatus  = subprocess.call(deleteRequest+config.rmdRedis, shell=True)
		if statementStatus == 1 :
			sys.exit("Error deleting an service instance: " +config.rmdRedis)
		time.sleep(20)  # Delay
		return statementStatus

def createPredixUAASecurityService(config):
	if config.allDeploy in ('y','Y'):
		#create UAA instance
	    uaa_payload_filename = 'uaa_payload.json'
	    data = {}
	    data['adminClientSecret'] = config.uaaAdminSecret

	    with open(uaa_payload_filename, 'w') as outfile:
	        json.dump(data, outfile)
	        outfile.close()

		uaaJsonrequest = "cf cs "+config.predixUaaService+" "+config.predixUaaServicePlan +" "+config.rmdUaaName+ " -c " + os.getcwd()+'/'+uaa_payload_filename
		print(uaaJsonrequest)
		statementStatus  = subprocess.call(uaaJsonrequest, shell=True)
		if statementStatus == 1 :
			sys.exit("Error creating a uaa service instance")
		return statementStatus

def getVcapJsonForPredixBoot (config):
	predixBootEnv = subprocess.check_output(["cf", "env" ,config.predixbootAppName])
	systemProvidedVars=predixBootEnv.split('System-Provided:')[1].split('No user-defined env variables have been set')[0]
	config.formattedJson = "[" + systemProvidedVars.replace("\n","").replace("'","").replace("}{","},{") + "]"
	#print ("formattedJson=" + config.formattedJson)

def addUAAUser(config, userId , password, email,adminToken):
	createUserBody = {"userName":"","password":"","emails":[{"value":""}]}
	createUserBody["userName"] = userId
	createUserBody["password"] = password
	createUserBody["emails"][0]['value'] = email

	createUserBodyStr = json.dumps(createUserBody)
	print(createUserBodyStr)


	headers = ' -H "Authorization:'+adminToken+'\" -H \"Content-Type: application/json\" '
	createUserCurl = "curl -X POST '"+config.UAA_URI+"/Users' " +"-d '"+createUserBodyStr+"'"+headers
	print ("*****************")
	print ("Creating User command : "+createUserCurl)
	print ("*****************")

	clientResponse  = subprocess. check_output(createUserCurl, shell=True)
	statementStatusJson = json.loads(clientResponse)
	#print("print the json response is "+ clientResponse)
	if statementStatusJson.get('error'):
		statementStatus = statementStatusJson['error']
		statementStatusDesc = statementStatusJson['error_description']
	else :
		statementStatus = 'success'
		statementStatusDesc = statementStatusJson['id']

	if statementStatus == 'success' or  'scim_resource_already_exists' not in statementStatusDesc :
		print("User is UAA ")
	else :
		sys.exit("Error adding Users "+statementStatusDesc )




def deployAndBindUAAToPredixBoot(config):
	deployProject(config, 'cf push '+config.predixbootAppName+' -f '+'predix-microservice-cf-jsr/manifest.yml',config.predixbootJSRRepoName)
	statementStatus  = subprocess.call("cf bs "+config.predixbootAppName +" " + config.rmdUaaName , shell=True)
	if statementStatus == 1 :
			sys.exit("Error binding a uaa service instance to boot ")

	#statementStatus  = subprocess.call("cf restage "+config.predixbootAppName, shell=True)
	#if statementStatus == 1 :
	#		sys.exit("Error restaging a uaa service instance to boot")


def getUAAAdminToken(config):
	adminRealm = "admin:"+config.uaaAdminSecret
	adminRelmKey = base64.b64encode(adminRealm)
	#headers = {"Content-Type":"application/x-www-form-urlencoded", "Authorization":"Basic " + adminRelmKey}
	#jsonPostBody= "grant_type=client_credentials"

	headers = ' -H "Authorization: Basic '+adminRelmKey+'\" -H \"Content-Type: application/x-www-form-urlencoded\" '
	queryClientCreds= "grant_type=client_credentials"
	uaaAdminClientTokenCurl = "curl -X GET '"+config.uaaIssuerId+"?"+queryClientCreds+"'"+headers

	print ("*****************")
	print (" UAA Client GET client ADMIN token "+uaaAdminClientTokenCurl)
	print ("*****************")
	getAdminClientTokenResponse  = subprocess. check_output(uaaAdminClientTokenCurl, shell=True)
	getAdminClientTokenResponseJson = json.loads(getAdminClientTokenResponse)

  	print("Admin Token is "+getAdminClientTokenResponseJson['token_type']+" "+getAdminClientTokenResponseJson['access_token'])
  	return (getAdminClientTokenResponseJson['token_type']+" "+getAdminClientTokenResponseJson['access_token'])


def createClientIdAndAddUser(config):
	# setup the UAA login
	adminToken = processUAAClientId(config,config.UAA_URI+"/oauth/clients","POST")

	# Add users
	print("****************** Adding users ******************")
	addUAAUser(config, config.rmdUser1 , config.rmdUser1Pass, config.rmdUser1 + "@gegrctest.ge.com",adminToken)
	addUAAUser(config, config.rmdAdmin1 , config.rmdAdmin1Pass, config.rmdAdmin1 + "@gegrctest.com",adminToken)

def createBindPredixACSService(config, rmdAcsName):
	if config.allDeploy in ('y','Y'):
	    acs_payload_filename = 'acs_payload.json'
	    data = {}
	    data['trustedIssuerIds'] = config.uaaIssuerId
	    with open(acs_payload_filename, 'w') as outfile:
	        json.dump(data, outfile)
	        outfile.close()

		#create UAA instance
		acsJsonrequest = "cf cs "+config.predixAcsService+" "+config.predixAcsServicePlan +" "+rmdAcsName+ " -c "+ os.getcwd()+'/'+ acs_payload_filename
		print(acsJsonrequest)
		statementStatus  = subprocess.call(acsJsonrequest, shell=True)
		if statementStatus == 1 :
			sys.exit("Error creating a uaa service instance")

	statementStatus  = subprocess.call("cf bs "+config.predixbootAppName +" " + rmdAcsName , shell=True)
	if statementStatus == 1 :
			sys.exit("Error binding a uaa service instance to boot ")


	#statementStatus  = subprocess.call("cf restage "+config.predixbootAppName, shell=True)
	#if statementStatus == 1 :
	#		sys.exit("Error restaging a uaa service instance to boot")

	return statementStatus

def createGroup(config, adminToken,policyGrp):
	print("****************** Add Group ******************")
	createGroupBody = {"displayName":""}
	createGroupBody["displayName"] = policyGrp
	createGroupBodyStr = json.dumps(createGroupBody)

	headers = ' -H "Authorization:'+adminToken+'\" -H \"Content-Type: application/json\" '
	uaaGroupCurl = "curl -X POST '"+config.UAA_URI+"/Groups' -d '"+createGroupBodyStr+"'"+headers
	print ("*****************")
	print (" UAA Client Group Command"+uaaGroupCurl)
	print ("*****************")

	clientResponse  = subprocess. check_output(uaaGroupCurl, shell=True)
	statementStatusJson = json.loads(clientResponse)

	if statementStatusJson.get('error'):
		statementStatus = statementStatusJson['error']
		statementStatusDesc = statementStatusJson['error_description']
	else :
		statementStatus = 'success'
		statementStatusDesc = 'success'

	if statementStatus == 'success' or  'scim_resource_exists' not in statementStatusDesc :
		print("Success creating or reusing the Group")
	else :
		sys.exit("Error Processing Adding Group on UAA "+statementStatusDesc )

def getGroup(config, adminToken ,grpname):
	#check Get Group
	# https://9938f377-5b07-4677-a951-cfeb36858836.predix-uaa-sysint.grc-apps.svc.ice.ge.com/Groups?filter=displayName+eq+%22test%22&startIndex=1
	headers = ' -H "Authorization:'+adminToken+'\" -H \"Content-Type: application/json\" '
	uaaGroupCurl = 'curl -X GET "'+config.UAA_URI+'/Groups/?filter=displayName+eq+%22'+grpname+'%22&startIndex=1"'+headers
	print ("*****************")
	print (" UAA Client Group Command "+uaaGroupCurl)
	print ("*****************")
	getGroupResponse  = subprocess. check_output(uaaGroupCurl, shell=True)
	getGroupResponseJson = json.loads(getGroupResponse)
	groupFound = True
	statementStatus = 'success'

	if getGroupResponseJson.get('totalResults') <=0 :
		statementStatus = 'not found'
		groupFound = False

	print ("print Group "+str(groupFound) + "JSON "+getGroupResponse)

	return groupFound ,getGroupResponseJson

def getUserbyDisplayName(config, adminToken ,username):
	#check Get Group
	# get https://9938f377-5b07-4677-a951-cfeb36858836.predix-uaa-sysint.grc-apps.svc.ice.ge.com/Users?attributes=id%2CuserName&filter=userName+eq+%22rmd_admin_1%22&startIndex=1
	headers = ' -H "Authorization:'+adminToken+'\" -H \"Content-Type: application/json\" '
	uaaUserCurl = 'curl -X GET "'+config.UAA_URI+'/Users/?attributes=id%2CuserName&filter=userName+eq+%22'+username+'%22&startIndex=1"'+headers
	print ("*****************")
	print (" UAA Client User Command "+uaaUserCurl)
	print ("*****************")
	getUserResponse  = subprocess. check_output(uaaUserCurl, shell=True)
	getUserResponseJson = json.loads(getUserResponse)
	userFound = True
	statementStatus = 'success'

	if getUserResponseJson.get('totalResults') <= 0 :
		statementStatus = 'not found'
		userFound = False

	return userFound ,getUserResponseJson


def addAdminUserPolicyGroup(config, policyGrp,userName):

	adminToken = getUAAAdminToken(config)
	if not adminToken :
		sys.exit("Error getting admin token from the UAA instance ")

	#check Get Group
	groupFound,groupJson = getGroup(config, adminToken,policyGrp)

	if not groupFound :
		createGroup(config,adminToken,policyGrp)
		groupFound,groupJson = getGroup(config, adminToken,policyGrp)



	userFound,userJson = getUserbyDisplayName(config,adminToken,userName)

	if not userFound :
		sys.exit(" User is not found in the UAA - error adding member to the group")

	members = []
	if groupJson.get('resources') :
		grpName = groupJson['resources'][0]
		if grpName.get('members') :
			groupMeberList = grpName.get('members')
			for groupMeber in groupMeberList:
				members.insert(0 ,groupMeber['value'])

	members.insert(0, userJson['resources'][0]['id'])

	print (' Member to be updated for the Group ,'.join(members))

	#update Group
	groupId = groupJson['resources'][0]['id']
	updateGroupBody = { "meta": {}, "schemas": [],"members": [],"id": "","displayName": ""}
	updateGroupBody["meta"] = groupJson['resources'][0]['meta']
	updateGroupBody["members"] = members
	updateGroupBody["displayName"] = groupJson['resources'][0]['displayName']
	updateGroupBody["schemas"] = groupJson['resources'][0]['schemas']
	updateGroupBody["id"] = groupId

	updateGroupBodyStr = json.dumps(updateGroupBody)
	uuaGroupURL = config.UAA_URI + "/Groups/"+groupId

	headers = ' -H "Authorization:'+adminToken+'\" -H \"Content-Type: application/json\"  -H \"if-match: *\" -H \"accept: application/json\" '
	uaaGroupPutCurl = "curl -X  PUT '"+uuaGroupURL+"' -d '"+updateGroupBodyStr+"'"+headers
	print ("*****************")
	print (" UAA Client Command UAA group member add "+uaaGroupPutCurl)
	print ("*****************")

	clientResponse  = subprocess. check_output(uaaGroupPutCurl, shell=True)
	statementStatusJson = json.loads(clientResponse)

	if statementStatusJson.get('error'):
		statementStatus = statementStatusJson['error']
		statementStatusDesc = statementStatusJson['error_description']
	else :
		statementStatus = 'success'
		statementStatusDesc = 'success'

	if statementStatus == 'success' or  'Client already exists' not in statementStatusDesc :
		print ("User Successful adding " +userName + " to the group "+policyGrp)
	else :
		sys.exit("Error adding " +userName + " to the group "+policyGrp + " statementStatusDesc=" + statementStatusDesc )


def updateUserACS(config):
	addAdminUserPolicyGroup(config, "acs.policies.read",config.rmdAdmin1)
	addAdminUserPolicyGroup(config, "acs.policies.write",config.rmdAdmin1)
	addAdminUserPolicyGroup(config, "acs.attributes.read",config.rmdAdmin1)
	addAdminUserPolicyGroup(config, "acs.attributes.write",config.rmdAdmin1)

	addAdminUserPolicyGroup(config, "acs.policies.read",config.rmdUser1)
	addAdminUserPolicyGroup(config, "acs.attributes.read",config.rmdUser1)

def processUAAClientId (config,uuaClientURL,method):
	adminToken = getUAAAdminToken(config)
	if not adminToken :
		sys.exit("Error getting admin token from the UAA instance ")

	# create a client id
	print("****************** Creating client id ******************")
	print(config.clientScope)
	print(config.clientScopeList)

	createClientIdBody = {"client_id":"","client_secret":"","scope":[],"authorized_grant_types":[],"authorities":[],"autoapprove":["openid"]}
	createClientIdBody["client_id"] = config.rmdAppClientId
	createClientIdBody["client_secret"] = config.rmdAppSecret
	createClientIdBody["scope"] = config.clientScopeList
	createClientIdBody["authorized_grant_types"] = config.clientGrantType
	createClientIdBody["authorities"] = config.clientAuthoritiesList

	createClientIdBodyStr = json.dumps(createClientIdBody)

	headers = ' -H "Authorization:'+adminToken+'\" -H \"Content-Type: application/json\" '
	#uaaCreateClientCurl = 'curl -X '+method+' "'+uuaClientURL+'" -d "'+createClientIdBodyStr+'"'+headers
	uaaCreateClientCurl = "curl -X "+method+" '"+uuaClientURL+"' -d '"+createClientIdBodyStr+"'"+headers
	print ("*****************")
	print (" UAA Client Command"+uaaCreateClientCurl)
	print ("*****************")

	clientResponse  = subprocess. check_output(uaaCreateClientCurl, shell=True)
	statementStatusJson = json.loads(clientResponse)


	if statementStatusJson.get('error'):
		statementStatus = statementStatusJson['error']
		statementStatusDesc = statementStatusJson['error_description']
	else :
		statementStatus = 'success'
		statementStatusDesc = 'success'

	if statementStatus == 'success' or  'Client already exists' in statementStatusDesc :
		print("Success creating or reusing the Client Id")
	else :
		sys.exit("Error Processing ClientId on UAA "+statementStatusDesc )

	return adminToken


def updateClientIdAuthorities(config):
	processUAAClientId(config,config.UAA_URI+"/oauth/clients/"+config.rmdAppClientId,"PUT")

def getTokenFromUAA(config):
	url = config.uaaIssuerId
	oauthRelam = config.rmdAppClientId+":"+config.rmdAppSecret
	authKey = base64.b64encode(oauthRelam)
	print ( authKey)

	headers = ' -H "Authorization: Basic '+authKey+'\" -H \"Content-Type: application/x-www-form-urlencoded\" '
	queryClientCreds= "grant_type=client_credentials"

	uaaClientTokenCurl = "curl -X GET '"+config.uaaIssuerId+"?"+queryClientCreds+"'"+headers
	print ("*****************")
	print (" UAA Client GET client token "+uaaClientTokenCurl)
	print ("*****************")
	getClientTokenResponse  = subprocess. check_output(uaaClientTokenCurl, shell=True)
	getClientTokenResponseJson = json.loads(getClientTokenResponse)
	print("Client Token is "+getClientTokenResponseJson['token_type']+" "+getClientTokenResponseJson['access_token'])
	return (getClientTokenResponseJson['token_type']+" "+getClientTokenResponseJson['access_token'])

def createRefAppACSPolicyAndSubject(config,acs_zone_header):
	adminUserTOken = getTokenFromUAA(config)
	headers = ' -H "Authorization:'+adminUserTOken+'\" -H \"Content-Type: application/json\" '
	headers = headers + ' -H "Predix-Zone-Id:'+acs_zone_header+'"'
	acsPolicyCurl = 'curl -X PUT "'+config.ACS_URI+'/v1/policy-set/refapp-acs-policy" ' +'-d "@./acs/rmd_app_policy.json"'+headers
	#acsPolicyCurl = "curl -X PUT "+config.ACS_URI+"/v1/policy-set/refapp-acs-policy " +" -d @./acs/rmd_app_policy.json"+headers
	print ("Adding ACS policy "+acsPolicyCurl)
	statementStatus  = subprocess.call(acsPolicyCurl, shell=True)
	print(statementStatus)
	if statementStatus == 1 :
		sys.exit("Error creating ACS policy " )

	headers = ' -H "Authorization:'+adminUserTOken+'\" -H \"Content-Type: application/json\" '
	headers = headers + ' -H "Predix-Zone-Id:'+acs_zone_header+'"'

	acsSubjectCurl = 'curl -X PUT "'+config.ACS_URI+'/v1/subject/' + config.rmdAdmin1 + '"' + ' -d "@./acs/' + config.rmdAdmin1 + '_role_attribute.json"'+headers
	print ("Adding Subject "+acsSubjectCurl)
	statementStatus  = subprocess.call(acsSubjectCurl, shell=True)
	acsSubjectCurl = 'curl -X PUT "'+config.ACS_URI+'/v1/subject/' + config.rmdUser1 + '"' + ' -d "@./acs/"' + config.rmdUser1 + '"_role_attribute.json"'+headers
	print ("Adding Subject "+acsSubjectCurl)
	statementStatus  = subprocess.call(acsSubjectCurl, shell=True)

def createAsssetInstance(config,rmdPredixAssetName ,predixAssetName ):
	getPredixUAAConfigfromVcaps(config)
	asset_payload_filename = 'asset_payload.json'
	uaaList = [config.uaaIssuerId]
	data = {}
	data['trustedIssuerIds'] = uaaList
	with open(asset_payload_filename, 'w') as outfile:
		json.dump(data, outfile)
		print(data)
		outfile.close()

		assetJsonrequest = "cf cs "+predixAssetName+" "+config.predixAssetServicePlan +" "+rmdPredixAssetName+ " -c "+os.getcwd()+'/' +asset_payload_filename
		print ("Creating Service cmd "+assetJsonrequest)
		statementStatus  = subprocess.call(assetJsonrequest, shell=True)
		#if statementStatus == 1 :
			#sys.exit("Error creating a assset service instance")

def createTimeSeriesInstance(config,rmdPredixTimeSeriesName,predixTimeSeriesName):
    timeSeries_payload_filename = 'timeseries_payload.json'
    uaaList = [config.uaaIssuerId]
    data = {}
    data['trustedIssuerIds'] =uaaList
    with open(timeSeries_payload_filename, 'w') as outfile:
        json.dump(data, outfile)
        outfile.close()

	tsJsonrequest = "cf cs "+predixTimeSeriesName+" "+config.predixTimeSeriesServicePlan +" "+rmdPredixTimeSeriesName+ " -c "+os.getcwd()+'/'+timeSeries_payload_filename
	print ("Creating Service cmd "+tsJsonrequest)
	statementStatus  = subprocess.call(tsJsonrequest, shell=True)
	if statementStatus == 1 :
		sys.exit("Error creating a assset service instance")

def getPredixUAAConfigfromVcaps(config):
	if not hasattr(config,'uaaIssuerId') :
		getVcapJsonForPredixBoot(config)
		d = json.loads(config.formattedJson)
		config.uaaIssuerId =  d[0]['VCAP_SERVICES'][config.predixUaaService][0]['credentials']['issuerId']
		config.UAA_URI = d[0]['VCAP_SERVICES'][config.predixUaaService][0]['credentials']['uri']
		uaaZoneHttpHeaderName = d[0]['VCAP_SERVICES'][config.predixUaaService][0]['credentials']['zone']['http-header-name']
		uaaZoneHttpHeaderValue = d[0]['VCAP_SERVICES'][config.predixUaaService][0]['credentials']['zone']['http-header-value']
		print("****************** UAA configured As ******************")
		print ("\n uaaIssuerId = " + config.uaaIssuerId + "\n UAA_URI = " + config.UAA_URI + "\n "+uaaZoneHttpHeaderName+" = " +uaaZoneHttpHeaderValue+"\n")
		print("****************** ***************** ******************")


def getPredixACSConfigfromVcaps(config):
	if not hasattr(config,'ACS_URI') :
		getVcapJsonForPredixBoot(config)
		d = json.loads(config.formattedJson)
		config.ACS_URI = d[0]['VCAP_SERVICES'][config.predixAcsService][0]['credentials']['uri']
		config.acsPredixZoneHeaderName = d[0]['VCAP_SERVICES'][config.predixAcsService][0]['credentials']['zone']['http-header-name']
		config.acsPredixZoneHeaderValue = d[0]['VCAP_SERVICES'][config.predixAcsService][0]['credentials']['zone']['http-header-value']
		config.acsOauthScope = d[0]['VCAP_SERVICES'][config.predixAcsService][0]['credentials']['zone']['oauth-scope']


def bindService(applicationName , rmdServiceInstanceName):
	statementStatus  = subprocess.call("cf bs "+applicationName +" " + rmdServiceInstanceName , shell=True)
	if statementStatus == 1 :
		sys.exit("Error binding a "+rmdServiceInstanceName+" service instance to boot ")


def restageApplication(applicationName):
	statementStatus  = subprocess.call("cf restage "+applicationName, shell=True)
	if statementStatus == 1 :
		sys.exit("Error restaging a uaa service instance to boot")

def getAssetURLandZone(config):
	if not hasattr(config,'ASSET_ZONE') :
		assetUrl = ''
		assetZone =''
		d = json.loads(config.formattedJson)
		assetZone = d[0]['VCAP_SERVICES'][config.predixAssetService][0]['credentials']['instanceId']
		assetUrl = d[0]['VCAP_SERVICES'][config.predixAssetService][0]['credentials']['uri']
		config.ASSET_ZONE = assetZone
		config.ASSET_URI = assetUrl

def getTimeseriesURLandZone(config):
	if not hasattr(config,'TS_ZONE') :
		timeseriesUrl = ''
		timeseriesZone =''
		d = json.loads(config.formattedJson)
		timeseriesZone = d[0]['VCAP_SERVICES'][config.predixTimeSeriesService][0]['credentials']['query']['zone-http-header-value']
		timeseriesUrl = d[0]['VCAP_SERVICES'][config.predixTimeSeriesService][0]['credentials']['query']['uri']
		config.TS_ZONE = timeseriesZone
		config.TS_URI = timeseriesUrl

def getClientAuthoritiesforAssetAndTimeSeriesService(config):
	d = json.loads(config.formattedJson)

	config.assetScopes = config.predixAssetService+".zones."+d[0]['VCAP_SERVICES'][config.predixAssetService][0]['credentials']['instanceId']+".user"
	#get Ingest authorities
	tsInjest = d[0]['VCAP_SERVICES'][config.predixTimeSeriesService][0]['credentials']['ingest']
	config.timeSeriesInjestScopes = tsInjest['zone-token-scopes'][0] +"," + tsInjest['zone-token-scopes'][1]
	# get query authorities
	tsQuery = d[0]['VCAP_SERVICES'][config.predixTimeSeriesService][0]['credentials']['query']
	config.timeSeriesQueryScopes = tsQuery['zone-token-scopes'][0] +"," + tsQuery['zone-token-scopes'][1]
	config.clientAuthoritiesList.append(config.assetScopes)
	config.clientAuthoritiesList.append(config.timeSeriesInjestScopes)
	config.clientAuthoritiesList.append(config.timeSeriesQueryScopes)
	config.clientScopeList.append(config.assetScopes)
	config.clientScopeList.append(config.timeSeriesInjestScopes)
	config.clientScopeList.append(config.timeSeriesQueryScopes)

	print ("returning timeseries client zone scopes query -->"+config.timeSeriesQueryScopes + " timeSeriesInjestAuthorities -->"+config.timeSeriesInjestScopes )



def checkoutAndDeployUI(config, repoName,appDeploymentName):
	try:
		print ("deploying "+repoName)
		os.chdir(repoName)
		print ("Changed directory to "+os.getcwd())
		statementStatus  = subprocess.check_output("npm install",shell=True)
		statementStatus  = subprocess.check_output("bower install", shell=True)
		statementStatus  = subprocess.check_output("grunt dist", shell=True)
		configureManifest(config, ".")
		configureConnectServer(config,"./tasks/options/")
		cfPush('cf push '+appDeploymentName,config.projectDir)
	except:
		print ( 'having trouble with the github username pass?  try downloading the dependencies manually by running "npm install", "bower install", and "grunt dist" from the rmd-ref-app-ui dir.  Then go back to the root dir run "python scripts/installRefApp.py --continueFrom deployReferenceAppCreateUI"')
		print ()
		raise
	finally:
		os.chdir("..")


def configureManifest(config, manifestLocation):
	# create a backup
	if os.path.isfile(manifestLocation + "/manifest.yml"):
		shutil.copy(manifestLocation+"/manifest.yml", manifestLocation+"/manifest.yml.bak")
	# copy template as manifest
	shutil.copy(manifestLocation+"/manifest.yml.template", manifestLocation+"/manifest.yml")
	s = open(manifestLocation+"/manifest.yml").read()
	s = s.replace('${assetService}', config.rmdPredixAssetName)
	s = s.replace('${uaaService}', config.rmdUaaName)
	s = s.replace('${acsService}', config.rmdAcsName)
	s = s.replace('${oauthRestHost}', config.UAA_URI.replace('https://',''))
	s = s.replace('${clientId}', config.rmdAppClientId)
	s = s.replace('${secret}', config.rmdAppSecret)
	if hasattr(config,'ACS_URI') :
		s = s.replace('${acsURI}', config.ACS_URI)
	s = s.replace('${timeSeriesService}', config.rmdPredixTimeseriesName)
	s = s.replace('${acssubdomain}', 'rmdsubdomain')
	s = s.replace('${postgresqService}', config.rmdPostgre)
	if hasattr(config,'DATA_INGESTION_URL') :
		s = s.replace('${dataIngestionUrl}', config.DATA_INGESTION_URL)
	s = s.replace('${sessionService}', config.rmdRedis)
	s = s.replace('${UAA_SERVER_URL}', config.UAA_URI)
	if hasattr(config,'ASSET_URI') :
		s = s.replace('${ASSET_URL}', config.ASSET_URI)
		s = s.replace('${ASSET_ZONE}', config.ASSET_ZONE)
	if hasattr(config,'TS_URI') :
		s = s.replace('${TS_URL}', config.TS_URI.split('/api/')[0])
		s = s.replace('${TS_ZONE}', config.TS_ZONE)
	s = s.replace('${ENCODED_CLIENTID}', base64.b64encode(config.rmdAppClientId+":"+config.rmdAppSecret))
	if hasattr(config,'RMD_DATASOURCE_URL') :
		s = s.replace('${RMD_DATASOURCE_URL}', config.RMD_DATASOURCE_URL)
	if hasattr(config,'WEB_SOCKET_HOST') :
		s = s.replace('${WEB_SOCKET_HOST}', config.WEB_SOCKET_HOST)
		s = s.replace('${LIVE_DATA_WS_URL}', config.LIVE_DATA_WS_URL)
	f = open(manifestLocation+"/manifest.yml", 'w')
	f.write(s)
	f.close()
	with open(manifestLocation+'/manifest.yml', 'r') as fin:
		print (fin.read())

def configureConnectServer(config, fileLocation):
	# create a backup
	if os.path.isfile(fileLocation + "/connect.js"):
		shutil.copy(fileLocation+"/connect.js", fileLocation+"/connect.js.bak")
	# copy template as manifest
	shutil.copy(fileLocation+"/connect.js.template", fileLocation+"/connect.js")
	s = open(fileLocation+"/connect.js").read()
	s = s.replace('${clientId}', config.rmdAppClientId)
	s = s.replace('${secret}', config.rmdAppSecret)
	s = s.replace('${UAA_SERVER_URL}', config.UAA_URI)
	s = s.replace('${ASSET_URL}', config.ASSET_URI)
	s = s.replace('${ASSET_ZONE}', config.ASSET_ZONE)
	s = s.replace('${TS_URL}', config.TS_URI.split('/api/')[0])
	s = s.replace('${TS_ZONE}', config.TS_ZONE)
	s = s.replace('${ENCODED_CLIENTID}', base64.b64encode(config.rmdAppClientId+":"+config.rmdAppSecret))
	s = s.replace('${RMD_DATASOURCE_URL}', config.RMD_DATASOURCE_URL)
	s = s.replace('${LIVE_DATA_WS_URL}', config.LIVE_DATA_WS_URL)
	f = open(fileLocation+"/connect.js", 'w')
	f.write(s)
	f.close()
	with open(fileLocation+'/connect.js', 'r') as fin:
		print (fin.read())

def updateUAAUserGroups(config, serviceGroups):
	groups = serviceGroups.split(",")
	#print (groups)
	for group in groups:
		#print (group)
		addAdminUserPolicyGroup(config, group,config.rmdAdmin1Pass)
		addAdminUserPolicyGroup(config, group,config.rmdUser1Pass)

def findRedisService(config):
	#setup Redis
	result = []
	process = subprocess.Popen('cf m',
	    shell=True,
	    stdout=subprocess.PIPE,
	    stderr=subprocess.PIPE )
	for line in process.stdout:
	    result.append(line)
	errcode = process.returncode
	#print (errcode)
	search_redis = config.predixRedis
	for line in result:
		if(line.find(search_redis) > -1):
			#print(line)
			config.predixRedis = line.split()[0].strip()
			print ("Setting Redis config.predixRedis as "+ config.predixRedis)

#####################################################################################################
############################### main methods ###############################
#####################################################################################################

def buildReferenceApp(config):
	try:
		config.current='buildReferenceApp'
		print("Fast install set = " + config.fastinstall)
		if config.pullsubmodules == 'y':
			checkoutSubmodules()
			print("Build using maven setting : "+config.mvnsettings +" Maven Repo : "+config.mavenRepo)
		if config.fastinstall != 'y' :
			print("Compiling code...")
			if config.mavenRepo != "":
				os.removedirs(config.mavenRepo)
				#statementStatus  = subprocess.call("rm -rf "+config.mavenRepo, shell=True)
				if config.mvnsettings == "":
					statementStatus  = subprocess.call("mvn clean package -Dmaven.repo.local="+config.mavenRepo, shell=True)
				else:
					statementStatus  = subprocess.call("mvn clean package -s "+config.mvnsettings+" -Dmaven.repo.local="+config.mavenRepo, shell=True)
			else:
				 #statementStatus  = subprocess.call("rm -rf ~/.m2/repository/com/ge/predix/", shell=True)
				if config.mvnsettings == "":
				 	statementStatus  = subprocess.call("mvn clean package", shell=True)
				else:
				 	statementStatus  = subprocess.call("mvn clean package -s "+config.mvnsettings, shell=True)
		 	if statementStatus != 0:
				print("Maven build failed.")
				sys.exit(1);
		config.retryCount=0
	except:
		print traceback.print_exc()
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			buildReferenceApp(config)
		else :
			raise

def deployReferenceAppDelete(config):
	try:
		print("****************** Installing deployReferenceAppDelete ******************")
		config.current='deployReferenceAppDelete'
		# Deleting existing Applications and Services
		deleteExistingApplications(config)
		deleteExistingServices(config)
		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			time.sleep(10)  # Delay
			deployReferenceAppDelete(config)
		else :
			raise

def getAuthorities(config):
	if not hasattr(config,'clientAuthoritiesList') :
		config.clientAuthoritiesList = list(config.clientAuthorities)
		config.clientScopeList = list(config.clientScope)

def deployReferenceAppCreateUAA(config):
	try :
		print("****************** Running deployReferenceAppCreateUAA ******************")
		config.current='deployReferenceAppCreateUAA'
		# these two are modified by some other functions.
		getAuthorities(config)


		createPredixUAASecurityService(config)
		time.sleep(10)

		#Bind to Predix Boot
		deployAndBindUAAToPredixBoot(config)
		getPredixUAAConfigfromVcaps(config)

		if config.allDeploy in ('y','Y'):
			#Create Client Id and Users
			createClientIdAndAddUser(config)
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployReferenceAppCreateUAA(config)
		else :
			raise

def updateClientAuthoritiesACS(config):
	getPredixACSConfigfromVcaps(config)
	config.clientAuthoritiesList.append(config.acsOauthScope)
	config.clientScope.append(config.acsOauthScope)


def deployReferenceAppCreateACS(config):
	try :
		print("****************** Running deployReferenceAppCreateACS ******************")
		config.current='deployReferenceAppCreateACS'
		# acs integration
		getPredixUAAConfigfromVcaps(config)
		createBindPredixACSService(config,config.rmdAcsName)
		getPredixACSConfigfromVcaps(config)

		print("****************** ACS configured As ******************")
		print ("\n ACS_URI = " + config.ACS_URI + "\n "+config.acsPredixZoneHeaderName+"= " +config.acsPredixZoneHeaderValue)
		print (" ACS zone "+config.acsOauthScope)
		print("****************** ***************** ******************")

		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployReferenceAppCreateACS(config)
		else :
			raise

def updateClientAuthoritiesAssetAndTimeseries(config):
	getClientAuthoritiesforAssetAndTimeSeriesService(config)

def deployReferenceAppCreateAssetAndTimeseries(config):
	try:
		print("****************** Running deployReferenceAppCreateAssetAndTimeseries ******************")
		config.current='deployReferenceAppCreateAssetAndTimeseries'

		if config.allDeploy in ('y','Y'):
			# create a Asset Service
			print("****************** Predix Asset Timeseries ******************")
			createAsssetInstance(config,config.rmdPredixAssetName,config.predixAssetService)

			# create a Timeseries
			createTimeSeriesInstance(config,config.rmdPredixTimeseriesName,config.predixTimeSeriesService)

		bindService(config.predixbootAppName,config.rmdPredixAssetName)
		bindService(config.predixbootAppName,config.rmdPredixTimeseriesName)

		getVcapJsonForPredixBoot(config)
		getAssetURLandZone(config)
		getTimeseriesURLandZone(config)


		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployReferenceAppCreateAssetAndTimeseries(config)
		else :
			raise

def deployReferenceAppAddAuthorities(config):
	try:
		print("****************** Running deployReferenceAppAddAuthorities ******************")
		config.current='deployReferenceAppAddAuthorities'
		getPredixUAAConfigfromVcaps(config)
		getAuthorities(config)
		updateClientAuthoritiesACS(config)
		updateClientAuthoritiesAssetAndTimeseries(config)
		updateClientIdAuthorities(config)

		updateUserACS(config)
		updateUAAUserGroups(config, config.timeSeriesQueryScopes+","+config.timeSeriesInjestScopes+","+config.assetScopes+","+config.acsOauthScope)

		# setting up ACS policy and Subject
		createRefAppACSPolicyAndSubject(config, config.acsPredixZoneHeaderValue)

		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployReferenceAppAddAuthorities(config)
		else :
			raise

def getDataseedUrl(config):
	if not hasattr(config,'DATA_SEED_URL') :
		cfTarget= subprocess.check_output(["cf", "app",config.dataSeedAppName])
		print (cfTarget)
		config.DATA_SEED_URL="https://"+cfTarget.split('urls:')[1].strip().split('last uploaded:')[0].strip()
		print ('dataSeedAppName URL '+config.DATA_SEED_URL)


def deployReferenceAppCreateDataseed(config):
	try:
		print("****************** Running deployReferenceAppCreateDataseed ******************")
		config.current='deployReferenceAppCreateDataseed'
		getPredixUAAConfigfromVcaps(config)
		getPredixACSConfigfromVcaps(config)
		dataSeedRepoName = "data-seed-service"
		configureManifest(config, dataSeedRepoName)
		deployProject(config,'cf push '+config.dataSeedAppName+' -f '+dataSeedRepoName+'/manifest.yml',dataSeedRepoName)

		getDataseedUrl(config)
		#calling data loading on dataseedURl
		curlStatement = "curl -F \"username=${rmdAdmin1}\" -F \"password=${rmdAdmin1Pass}\" -F \"file=@./${dataSeedRepoName}/src/main/resources/rmdapp/AssetData.xls\" "
		curlStatement = curlStatement.replace('${rmdAdmin1}', config.rmdAdmin1)
		curlStatement = curlStatement.replace('${rmdAdmin1Pass}', config.rmdAdmin1Pass)
		curlStatement = curlStatement.replace('${dataSeedRepoName}', dataSeedRepoName)
		curlStatement = curlStatement+" "+config.DATA_SEED_URL+"/uploadAssetData"
		print (str(curlStatement))
		output= subprocess.check_output(curlStatement,shell=True)
		print ("output=" + output)
		if ( not output == "You successfully uploaded file!" ) :
			sys.exit('unable to upload Asset Data using curl in deployReferenceAppCreateDataseed, output=' + output + ' curl=' + curlStatement )

		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployReferenceAppCreateDataseed(config)
		else :
			raise

def getRMDDatasourceUrl(config):
	if not hasattr(config,'RMD_DATASOURCE_URL') :
		cfTarget= subprocess.check_output(["cf", "app",config.dataSourceAppName])
		print (cfTarget)
		config.RMD_DATASOURCE_URL="http://"+cfTarget.split('urls:')[1].strip().split('last uploaded:')[0].strip()
		print ('Data dataSourceAppName URL '+config.RMD_DATASOURCE_URL)

def deployReferenceAppCreateDatasource(config):
	try:
		print("****************** Running deployReferenceAppCreateDatasource ******************")
		config.current='deployReferenceAppCreateDatasource'
		getPredixUAAConfigfromVcaps(config)
		dataSourceRepoName = "rmd-datasource"
		configureManifest(config, dataSourceRepoName)
		deployProject(config, 'cf push '+config.dataSourceAppName+' -f '+dataSourceRepoName+'/manifest.yml',dataSourceRepoName)

		getRMDDatasourceUrl(config)


		#postgreJsonrequest = "cf cs "+config.predixPostgre+" "+config.predixPostgrePlan+" "+config.rmdPostgre
		#print ("Creating Postgre cmd "+postgreJsonrequest)
		#statementStatus  = subprocess.call(postgreJsonrequest, shell=True)

		#httpDatariverRepoName = "predix-http-datariver"
		#checkoutDeploytHttpRiver(httpDatariverRepoName,"",httpDataRiverAppName)

		#https://github.build.ge.com/adoption/predix-websocket-server.git
		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			time.sleep(10)  # Delay
			deployReferenceAppCreateDatasource(config)
		else :
			raise

def getWebsocketAppInfo(config):
	if not hasattr(config,'WEB_SOCKET_HOST') :
		print("****************** Running getWebsocketAppInfo ******************")
		cfTarget= subprocess.check_output(["cf", "app",config.websocketAppName])
		print (cfTarget)
		config.WEB_SOCKET_HOST=cfTarget.split('urls:')[1].strip().split('last uploaded:')[0].strip()
		print ('WS ingestion URL '+config.WEB_SOCKET_HOST)
		config.LIVE_DATA_WS_URL="wss://"+config.WEB_SOCKET_HOST+"/livestream"
		print ('LIVE_DATA_WS_URL '+config.LIVE_DATA_WS_URL)

def deployReferenceAppCreateWebsocketServer(config):
	try:
		config.current='deployReferenceAppCreateWebsocketServer'
		getPredixUAAConfigfromVcaps(config)
		websocketServerRepoName = "predix-websocket-server"
		configureManifest(config, websocketServerRepoName)
		deployProject(config, 'cf push '+config.websocketAppName+' -f '+websocketServerRepoName+'/manifest.yml',websocketServerRepoName)

		getWebsocketAppInfo(config)
		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployReferenceAppCreateWebsocketServer(config)
		else :
			raise


def deployReferenceAppCreateDataIngestion(config):
	try:
		print("****************** Running deployReferenceAppCreateDataIngestion ******************")
		config.current='deployReferenceAppCreateDataIngestion'
		getPredixUAAConfigfromVcaps(config)
		getWebsocketAppInfo(config)
		dataIngestionRepoName = "dataingestion-service"
		configureManifest(config, dataIngestionRepoName)
		deployProject(config, 'cf push '+config.dataIngestionAppName+' -f '+dataIngestionRepoName+'/manifest.yml',dataIngestionRepoName)


		cfTarget= subprocess.check_output(["cf", "app",config.dataIngestionAppName])
		print (cfTarget)
		config.DATA_INGESTION_URL="https://"+cfTarget.split('urls:')[1].strip().split('last uploaded:')[0].strip()
		print ('Data Ingestion URL '+config.DATA_INGESTION_URL)
		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployReferenceAppCreateDataIngestion(config)
		else :
			raise

def deployReferenceAppCreateMachineSimulator(config):
	try:
		print("****************** Running deployReferenceAppCreateMachineSimulator ******************")
		config.current='deployReferenceAppCreateMachineSimulator'
		getPredixUAAConfigfromVcaps(config)
		machineSimulatorRepoName = "machinedata-simulator"
		configureManifest(config, machineSimulatorRepoName)
		deployProject(config, 'cf push '+config.machineSimulatorAppName+' -f '+machineSimulatorRepoName+'/manifest.yml',machineSimulatorRepoName)
		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployReferenceAppCreateMachineSimulator(config)
		else :
			raise

def deployReferenceAppCreateUI(config):
	try:
		print("****************** Running deployReferenceAppCreateUI ******************")
		config.current='deployReferenceAppCreateUI'
		findRedisService(config)
		getPredixUAAConfigfromVcaps(config)
		getRMDDatasourceUrl(config)
		getWebsocketAppInfo(config)

		getVcapJsonForPredixBoot(config)
		getAssetURLandZone(config)
		getTimeseriesURLandZone(config)

		print("*********Create redis********************")
		redisJsonrequest = "cf cs "+config.predixRedis+" "+config.predixRedisPlan+" "+config.rmdRedis
		print ("Creating Redis cmd "+redisJsonrequest)
		statementStatus = subprocess.call(redisJsonrequest, shell=True)

		print("*********Deploying UI application********************")
		uiRepoName = "rmd-ref-app-ui"
		checkoutAndDeployUI(config, uiRepoName, config.uiAppName)

		print("********* DONE deploying UI application ********************")
		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployReferenceAppCreateUI(config)
		else :
			raise


def deployReferenceAppFinalPrep(config):
	try:
		print("****************** Running deployReferenceAppFinalPrep ******************")
		config.current='deployReferenceAppFinalPrep'

		getPredixUAAConfigfromVcaps(config)

		stopSimulatorRequest = "cf stop "+config.machineSimulatorAppName
		statementStatus  = subprocess.call(stopSimulatorRequest, shell=True)

		#restageApplication(config.predixbootAppName)
		#print("***********************Restage Predix Boot Completed**********************")
		config.retryCount=0
	except:
		print(traceback.print_exc())
		print()
		print ('Exception when running ' + config.current + '.  Retrying')
		config.retryCount = config.retryCount + 1
		if config.retryCount <= 1 :
			deployReferenceAppFinalPrep(config)
		else :
			raise

def sanityChecks(config):
	config.current='sanityChecks'
	# Sanity checks:
	jsonrequest = "cf apps | grep "+config.instanceAppender
	statementStatus  = subprocess.call(jsonrequest, shell=True)

	jsonrequest = "cf s | grep "+ config.instanceAppender
	statementStatus  = subprocess.call(jsonrequest, shell=True)

	cfTarget= subprocess.check_output(["cf", "app",config.uiAppName])
	print (cfTarget)
	config.uiUrl="https://"+cfTarget.split('urls:')[1].strip().split('last uploaded:')[0].strip()

	getDataseedUrl(config)
	getPredixUAAConfigfromVcaps(config)
	getVcapJsonForPredixBoot(config)
	getAssetURLandZone(config)
	getTimeseriesURLandZone(config)
	getPredixACSConfigfromVcaps(config)
	getDataseedUrl(config)
	getRMDDatasourceUrl(config)
	getWebsocketAppInfo(config)

	print ('uaaAdmin= ' + config.uaaAdminSecret)
	print ('clientId= ' + config.rmdAppClientId)
	print ('clientSecret= ' + config.rmdAppSecret)
	print ('rmdUser= ' + config.rmdUser1)
	print ('rmdUserPass= ' + config.rmdUser1Pass)
	print ('rmdAdmin= ' + config.rmdAdmin1)
	print ('rmdAdminPass= ' + config.rmdAdmin1Pass)
	print ('client basic auth= ' + base64.b64encode(config.rmdAppClientId+":"+config.rmdAppSecret))
	print ('UAA_SERVER_URL= ' + config.UAA_URI)
	print ('ASSET_URL= ' + config.ASSET_URI)
	print ('ASSET_ZONE= ' + config.ASSET_ZONE)
	print ('TS_URI= ' + config.TS_URI)
	print ('TS_ZONE= ' + config.TS_ZONE)
	print ('ACS_URI= ' + config.ACS_URI)
	print ('ACS_Zone_Id= ' + config.acsPredixZoneHeaderValue)
	print ('DATASOURCE= ' + config.RMD_DATASOURCE_URL)
	print ('WEBSOCKET_URL= ' + config.LIVE_DATA_WS_URL)
#######################################
# Begin Main script
#######################################
import subprocess
import sys
import traceback
import os
import json
import base64
import random
import string
import shutil
import time
import argparse
import re
import xml.dom.minidom
import base64
try:
	from urllib2 import Request, urlopen
	from urllib2 import URLError, HTTPError
except ImportError:
	from urllib.request import Request, urlopen
	from urllib.error import URLError, HTTPError


from xml.dom.minidom import parse
