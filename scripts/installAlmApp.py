#######################################
# Begin Main script
#######################################
import sys
import almAppConfig as config
import almApp
import traceback


print ('environment : '+config.environment)
print ('continueFrom=' + config.continueFrom)
print ('only=' + config.only)
print("****************** Installing ALM Application ******************")
try:

	config.retryCount=0
	if config.only not in (''):
		if config.only in ('buildALMApp'):
			almApp.buildALMApp(config)
		if config.only in ('deployALMAppDelete'):
			almApp.deployALMAppDelete(config)
		if config.only in ('deployALMAppCreateUAA'):
			almApp.deployALMAppCreateUAA(config)
		if config.only in ('deployALMAppCreateACS'):
			almApp.deployALMAppCreateACS(config)
			almApp.deployALMAppCreateAssetAndTimeseries(config)
			almApp.deployALMAppFinalPrep(config)
		if config.only in ('deployALMAppCreateAssetAndTimeseries'):
			almApp.deployALMAppCreateAssetAndTimeseries(config)
			almApp.deployALMAppFinalPrep(config)
		if config.only in ('deployALMAppAddAuthorities'):
			almApp.deployALMAppAddAuthorities(config)
		if config.only in ('deployALMAppCreateDataseed'):
			almApp.deployALMAppCreateDataseed(config)
		if config.only in ('deployALMAppCreateDatasource'):
			almApp.deployALMAppCreateDatasource(config)
		if config.only in ('deployALMAppCreateWebsocketServer'):
			almApp.deployALMAppCreateWebsocketServer(config)
		if config.only in ('deployALMAppCreateDataIngestion'):
			almApp.deployALMAppCreateDataIngestion(config)
		if config.only in ('deployALMAppCreateMachineSimulator'):
			almApp.deployALMAppCreateMachineSimulator(config)
		if config.only in ('deployALMAppCreateUI'):
			almApp.deployALMAppCreateUI(config)
		if config.only in ('deployALMAppFinalPrep'):
			almApp.deployALMAppFinalPrep(config)
	

		almApp.sanityChecks(config)
	else :
		if config.continueFrom in ('all'):
			almApp.buildALMApp(config)
			almApp.deployALMAppDelete(config)
			almApp.deployALMAppCreateUAA(config)
			almApp.deployALMAppCreateACS(config)
			almApp.deployALMAppCreateAssetAndTimeseries(config)
			almApp.deployALMAppAddAuthorities(config)
			almApp.deployALMAppCreateDataseed(config)
			almApp.deployALMAppCreateDatasource(config)
			almApp.deployALMAppCreateWebsocketServer(config)
			almApp.deployALMAppCreateDataIngestion(config)
			almApp.deployALMAppCreateMachineSimulator(config)
			almApp.deployALMAppCreateUI(config)
			almApp.deployALMAppFinalPrep(config)
			almApp.sanityChecks(config)

		if config.continueFrom in ('continue','buildALMApp'):
			config.continueFrom = 'continue'
			almApp.buildALMApp(config)
		if config.continueFrom in ('continue','deployALMAppDelete'):
			config.continueFrom = 'continue'
			almApp.deployALMAppDelete(config)
		if config.continueFrom in ('continue','deployALMAppCreateUAA'):
			config.continueFrom = 'continue'
			almApp.deployALMAppCreateUAA(config)
		if config.continueFrom in ('continue','deployALMAppCreateACS'):
			config.continueFrom = 'continue'
			almApp.deployALMAppCreateACS(config)
		if config.continueFrom in ('continue','deployALMAppCreateAssetAndTimeseries'):
			config.continueFrom = 'continue'
			almApp.deployALMAppCreateAssetAndTimeseries(config)
		if config.continueFrom in ('continue','deployALMAppAddAuthorities'):
			config.continueFrom = 'continue'
			almApp.deployALMAppAddAuthorities(config)
		if config.continueFrom in ('continue','deployALMAppCreateDataseed'):
			config.continueFrom = 'continue'
			almApp.deployALMAppCreateDataseed(config)
		if config.continueFrom in ('continue','deployALMAppCreateDatasource'):
			config.continueFrom = 'continue'
			almApp.deployALMAppCreateDatasource(config)
		if config.continueFrom in ('continue','deployALMAppCreateWebsocketServer'):
			config.continueFrom = 'continue'
			almApp.deployALMAppCreateWebsocketServer(config)
		if config.continueFrom in ('continue','deployALMAppCreateDataIngestion'):
			config.continueFrom = 'continue'
			almApp.deployALMAppCreateDataIngestion(config)
		if config.continueFrom in ('continue','deployALMAppCreateMachineSimulator'):
			config.continueFrom = 'continue'
			almApp.deployALMAppCreateMachineSimulator(config)
		if config.continueFrom in ('continue','deployALMAppCreateUI'):
			config.continueFrom = 'continue'
			almApp.deployALMAppCreateUI(config)
		if config.continueFrom in ('continue','deployALMAppFinalPrep'):
			config.continueFrom = 'continue'
			almApp.deployALMAppFinalPrep(config)
		
	almApp.sanityChecks(config)

	print("*******************************************")
	print("**************** SUCCESS!! ****************")
	print("*******************************************")
	print ('Visit your live ALM App in the browser: '+ config.uiUrl)
	print ('(Optional) Visit the DataSeedService to load asset data in to the Predix ALM App: '+config.DATA_SEED_URL)
	print ('(Optional) Start the machine data simulator with this command: cf start ' + config.machineSimulatorAppName)
	print ('(Optional) See the accounts and passwords of your ref app at the bottom of the file scripts/almAppConfig.py')
except:
	print()
	print traceback.print_exc()
	print()
	if config.only in (''):
		print ('Exception when running ' + config.current + '.  After repairing the problem, use "--continueFrom ' + config.current + '" switch to resume the install') 
	print
	sys.exit(2)


