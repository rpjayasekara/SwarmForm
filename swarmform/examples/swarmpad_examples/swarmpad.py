# from swarmform import SwarmPad
# from fireworks import Firework, ScriptTask, FWorker
# from fireworks.core.rocket_launcher import launch_rocket
#
# if __name__ == "__main__":
# 	# set up the SwarmPad and reset it
# 	swarmpad = SwarmPad()
# 	swarmpad.reset('', require_password=False)
# 	#
# 	# # create the Firework consisting of a custom "Addition" task
# 	# firework = Firework(ScriptTask.from_str('echo "hello"'))
# 	#
# 	# # store workflow
# 	# swarmpad.add_sf(firework)
# 	#
# 	# # Retrieve SwarmFlow from the SwarmPad and print
# 	# sf = swarmpad.get_sf_by_id(1)
# 	# print(sf.to_db_dict())
# 	#
# 	# sf = swarmpad.get_sf_by_name('Unnamed FW')
# 	# print(sf.to_db_dict())
# 	#
# 	# # Run the swarmFlow
# 	# launch_rocket(swarmpad, FWorker())

from swarmform import SwarmPad, WorkflowGenerator


def main():
	# set up the LaunchPad and reset it
	swarmpad = SwarmPad()
	swarmpad.reset('', require_password=False)
	workflow_dax = "/Users/randika/Documents/WorkflowSim-1.0/config/dax/Montage_100.xml"
	dax_swarmflow = WorkflowGenerator.generate_workflow(workflow_dax)
	swarmpad.add_sf(dax_swarmflow)


if __name__ == "__main__":
	main()