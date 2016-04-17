import os
import subprocess
import sys, getopt
import re

def checkRequirements():
    try:
        cfTarget = subprocess.check_output(["cf", "target"])
        print (cfTarget)
        user = cfTarget.split('User:')[1].split('Org:')[0]
        org = cfTarget.split('Org:')[1].split('Space:')[0]
        space = cfTarget.split('Space')[1]
        print("cf login detected")
        return (user.strip(), org, space)
    except subprocess.CalledProcessError as e:
        sys.exit("Please login to CF.")

#global org
#global space
#global user
global instanceAppender
global BASE_DIR
global BASE_PREDIX_DIR
global rmdUaaName
global rmdAcsName
global rmdPredixAssetName
global rmdPredixTimeseriesName
global rmdPostgre
global rmdRedis
global predixbootAppName
global dataSeedAppName
global dataSourceAppName
#global httpDataRiverAppName
global dataIngestionAppName
global machineSimulatorAppName
global uiAppName
global websocketAppName
global predixUaaService
global predixAcsService
global predixAssetService
global predixTimeSeriesService
global predixPostgre
global predixRedis
global predixUaaServicePlan
global predixAcsServicePlan
global predixAssetServicePlan
global predixTimeSeriesServicePlan
global predixPostgrePlan
global predixRedisPlan
global rmdAppClientId
global rmdAppSecret
global uaaAdminSecret
global clientAuthorities
global clientScope
global projectDir
global predixProject
global rmdUser1
global rmdUser1Pass
global environment
global mvnsettings
global pullsubmodules
global mavenRepo
global allDeploy
global continueFrom
global artifactoryrepo
global artifactoryuser
global artifactorypass

try:
    #set defaults
    instanceAppender = ""
    #mvnsettings = "~/.m2/settings.xml"
    from os.path import expanduser
    homeDir = expanduser("~")

    mvnsettings=homeDir + "/.m2/settings.xml"

    #mvnsettings = ""
    pullsubmodules = 'y'
    mavenRepo = ""
    environment = "PROD"
    allDeploy = "y"
    continueFrom = "all"    
    only = ""
    fastinstall = 'y'
    artifactoryrepo = ""
    artifactoryuser = ""
    artifactorypass = "" 
    #override with arguments
    opts, args = getopt.getopt(sys.argv[1:],"e:i:s:p:r:a:v:c:o:f:x:y:z:",["environment=","instanceAppender=","mvnsettings=","pullsubmodules=","mavenrepo=","allDeploy=","continueFrom=","only=", "fastinstall=", "artifactoryrepo=", "artifactoryuser=", "artifactorypass="])
except getopt.GetoptError:
    print 'Exception when parsing : '+sys.argv[0]+' -e (R2/PROD) -i <Instance appender> -s <mvnsettings>'
    sys.exit(2)
for opt, arg in opts:
    print ('opt=' + opt + ' arg=' + arg)
    if opt == '-h':
        print sys.argv[0]+' -e (R2/PROD) -g <Github User> -i <Instance appender> -s <Maven settings file>'
        sys.exit()
    elif opt in ("-i", "--instanceappender"):
        instanceAppender = arg
    elif opt in ("-e", "--environment"):
        environment = arg
    elif opt in ("-s", "--mvnsettings"):
        mvnsettings = arg
    elif opt in ("-p","--pullsubmodules"):
        pullsubmodules = arg
    elif opt in ("-r","--mavenrepo"):
        mavenRepo = arg
    elif opt in ("-a","--alldeploy"):
        allDeploy = arg
    elif opt in ("-v","--verbose"):
        verbose = true;
    elif opt in ("-c","--continueFrom"):
        continueFrom = arg;
    elif opt in ("-o","--only"):
        only = arg;
    elif opt in ("-f","--fastinstall"):
        fastinstall = arg;
    elif opt in ("-x","--artifactoryrepo"):
        artifactoryrepo = arg;
    elif opt in ("-y","--artifactoryuser"):
        artifactoryuser = arg;
    elif opt in ("-z","--artifactorypass"):
        artifactorypass = arg;

#if mvnsettings == "":
#        print sys.argv[0]+' -e (R2/PROD) -g <Github User> -i <Instance appender> -s <Maven settings file>'
#        print 'Maven settings file is a mandatory argument.'
#        sys.exit()

# check check login
user, org, space = checkRequirements()
if len(instanceAppender) == 0:
    instanceAppender = user.strip().split("@")[0].replace('.', '_')
print ('using Appender', instanceAppender)

# check or create a directory for Reference application
BASE_DIR = os.getcwd()
BASE_PREDIX_DIR = "PredixApps"

# Reference App Service Instance Names
rmdUaaName = "rmd_uaa_"+instanceAppender
rmdAcsName = "rmd_acs_"+instanceAppender
rmdPredixAssetName = "rmd_asset_"+instanceAppender
rmdPredixTimeseriesName = "rmd_time_series_"+instanceAppender
rmdPostgre = "rmd_postgre_"+instanceAppender
rmdRedis = "rmd_redis_"+instanceAppender

#Repo Name
predixbootJSRRepoName = "predix-microservice-cf-jsr"

# Predix Application Names
print ('instanceAppender=' + instanceAppender)
predixbootAppName = "predix-microservice-cf-jsr_"+instanceAppender
dataSeedAppName = "data_seed_"+instanceAppender
dataSourceAppName = "rmd_datasource_"+instanceAppender
httpDataRiverAppName = "http_datariver_"+instanceAppender
dataIngestionAppName = "dataingestion_service_"+instanceAppender
machineSimulatorAppName = "machinedata_simulator_"+instanceAppender
uiAppName = 'rmd_ref_app_ui_'+instanceAppender
websocketAppName = "websocket_service_"+instanceAppender

if environment == 'PROD':
    # Predix Service Instance Name for VPC
    predixUaaService = "predix-uaa"
    predixAcsService = "predix-acs"
    predixAssetService = "predix-asset"
    predixTimeSeriesService = "predix-timeseries"
    predixPostgre = "postgres"
    predixRedis = "redis"

    predixUaaServicePlan = "Tiered"
    predixAcsServicePlan = "Tiered"
    predixAssetServicePlan = "Tiered"
    predixTimeSeriesServicePlan = "Bronze"
    predixPostgrePlan = "shared"
    predixRedisPlan = "shared-vm"
    artifactoryrepo = "https://artifactory.predix.io/artifactory/PREDIX-EXT"
else :
    # Predix Service Instance Name for sysint
    predixUaaService = "predix-uaa-sysint"
    predixAcsService = "predix-acs-sysint"
    predixAssetService = "predix-asset-sysint"
    predixTimeSeriesService = "predix-timeseries-sysint"
    predixPostgre = "rdpg"
    predixRedis = "p-redis"

    predixUaaServicePlan = "free"
    predixAcsServicePlan = "free"
    predixAssetServicePlan = "Beta"
    predixTimeSeriesServicePlan = "Beta"
    predixPostgrePlan = "Free"
    predixRedisPlan = "shared-vm"

#Reference application client id
rmdAppClientId = "mvp3_ref_app"
rmdAppSecret = "mvp3ref@pp"
#UAA Admin Account
uaaAdminSecret = "rmd_uaa_secret"
clientGrantType = ["authorization_code","client_credentials","refresh_token","password"]
clientAuthorities = ["openid","acs.policies.read","acs.policies.write","acs.attributes.read","acs.attributes.write","uaa.resource","uaa.none"]
clientScope = ["uaa.none","openid","acs.policies.read","acs.policies.write","acs.attributes.read","acs.attributes.write"]

projectDir = "predix-microservice-templates"
predixProject = projectDir+".git"
#UAA User account for logging in to RMD Ref App
rmdUser1 = "rmd_user_1"
rmdUser1Pass = "RMD_user_1"
#Admin User that is allowed to add asset data
rmdAdmin1 = "rmd_admin_1"
rmdAdmin1Pass = "RMD_admin_1"
