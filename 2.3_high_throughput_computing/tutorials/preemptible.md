# High-Throughput + Many-Task Computing

- [Batch job arrays](arrays.md)
- [Batch job dependencies](dependencies.md)
- [Batch job bundling](bundling.md)
- [Preemptible batch jobs](preemptible.md)

## Preemptible batch jobs

Preemptible batch jobs behave the same as regular batch jobs, but they
may be cancelled (or terminated) by the scheduler at anytime in order to
reclaim the compute resources they were provided and redistrbute those
resources to run a higher priority job. However, if your workloads are
fault-tolerant and can withstand such interruptions, then running your
jobs in a preemptible queue or partition can reduce your total compute
costs over the lifetime of a project.

Expanse has two (non-refundabled) preemptible partitions that provide 
you with a 20% service unit (SU) discount. 
- **preempt**
- **gpu-preempt**

#

Back to Start - [High-Throughput + Many-Task Computing](../README.md)
