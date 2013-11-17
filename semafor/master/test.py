from semafor.master.worker import tasks

#print tasks.create_instances.delay(2)

print tasks.semafor_parse.delay([], n_instances=3)
