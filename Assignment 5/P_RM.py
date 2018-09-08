"""
Partitionned EDF using PartitionedScheduler.
"""
from simso.core.Scheduler import SchedulerInfo
from simso.utils import PartitionedScheduler
from simso.schedulers import scheduler

@scheduler("simso.schedulers.P_RM")
class P_RM(PartitionedScheduler):
    def init(self):
        PartitionedScheduler.init(
            self, SchedulerInfo("simso.schedulers.RM_mono"))

    def packer(self):
        # First Fit
        cpus = [[cpu, 0] for cpu in self.processors]
        
        n = [0] * len(cpus)
        for task in self.task_list:
           
            j = 0
            # Find the processor with the lowest load.
            for i, c in enumerate(cpus):
                Urm = (n[i]+1.0) * ((pow(2.0, 1/(n[i]+1.0))) - 1.0)
                u = (c[1] + (task.wcet / task.period))
                
                if u < Urm:
                    j = i
                    break

            n[j] = n[j] + 1
            

            # Affect it to the task.
            self.affect_task_to_processor(task, cpus[j][0])

            # Update utilization.
            cpus[j][1] += float(task.wcet) / task.period
        return True
