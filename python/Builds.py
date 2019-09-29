
import sys
import jenkins
from time import sleep

from config import server as serv
from config import credentials as user
from config import job_names_build as build
from config import job_names_deploy as deploy

server = jenkins.Jenkins(url=serv.url , username=user.username, password=user.password)

def report():
	next_build_number = server.get_job_info(build.report)['nextBuildNumber']
	output = server.build_job(build.report)
	print("Building report with queue number: % 2d" %(output))  
	is_build_ok = check_build_process(next_build_number , build.report)
	if is_build_ok:
		print("Report has been built successfully")
		next_build_number = server.get_job_info(deploy.report)['nextBuildNumber']
		output = server.build_job(deploy.report)
		print("Deploying report with queue number: % 2d" %(output))
		is_deploy_ok = check_build_process(next_build_number , deploy.report)
		if is_deploy_ok:
			print("Report has been deployed successfully")
		
		else:
			print("Report has not been deployed successfully")
	
	else:
		print("Report has not been built successfully")

	
def check_build_process(build_number , build_name):
	is_building = True
	is_success = False
	errors = 0
	while is_building:
		try:
			#Waiting a few seconds until job starts
			sleep(10)
			build_info = server.get_build_info(build_name , build_number)
			is_building = build_info['building']
			if not is_building:
				is_success = build_info['result'] == "SUCCESS"
		
		except Exception as ex:
			print("Job not started yet")
			print("Trying again...")
			#Avoid infinite loop
			errors += 1
			if errors == 9:
				print("Could not start job: " + build_name)
				break
				
	return is_success			


def switch(arg):
    switcher = {
        "report" : report
    }
    return switcher.get(arg, lambda: print("Invalid argument"))    


if __name__ == "__main__":
    func = switch(sys.argv[1])
    func()
