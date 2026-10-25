# Batch runs and major compute

Standing instructions for planning, reviewing and running simulations, batch jobs, large data analyses, and anything that uses cloud or paid resources. Use this together with the [development workflow](development-workflow.md).

## The prompt (verbatim)

> Please review all planned simulations, batch jobs, or data analysis processes for performance, reliability, parallelism, total runtime, correctness, and cost. FOR ALL REVIEWS - USE SUBAGENTS AND RUN IN PARALLEL, striking a good balance between parallelism and short context length (which saves money), with adequate intelligence, context, and knowledge to perform effectively. Review code to optimize the use of parallelism and threads where possible. For any LLM or cloud invocations, review LLM parameters, settings, and limitations to ensure (a) experimental validity, (b) consistency with known good practices, (c) appropriately-sized limits, such as maximum context length (max_length), model type, version, and size, maximum prompt length, number(s) of iterations, and any other parameter, ensuring to balance experimental validity, statistical significance, and adequate performance with cost, speed, and total runtime. When invoking cloud services, optimize for parallelism, analyzing the total run stream for dependencies, and then within each group of independent jobs, running as many jobs in parallel as possible, up to the limits of local machine performance and resources (like RAM and CPU), internet bandwidth, cloud capacity, cloud budget, and monitoring for timeouts or other errors from cloud services. Before every significant run involving cloud or other paid resources, estimate the runtime, total number of requests, total number of tokens, and estimated total cost, and prompt me to review and approve these.
>
> Also rigorously review experimental design, including the design, selection, and permutation of input parameters, data sets, parameters, and experimental arms, reviewing both for excessive / superfluous processing which can be omitted, and also poorly designed / underpowered / low value / misaligned experimental arms which don't provide overall project value. For every change, before running major jobs, review the entire project end-to-end for alignment with the three evaluation criteria in https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25#guidelines and the three major research questions (and their subquestions) in https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25#resources, focusing on how we can achieve "5" ratings in all three guideline areas, and address the specific research questions, and interests, areas of focus, or research areas of the judges listed in this page, with an emphasis on judges involved with AI frontier labs or AI safety research organizations. For all reviews and discrete units of work, use fresh subagents, striking a good balance between parallelism and short context length (which saves money), with adequate intelligence, context, and knowledge to perform effectively.
>
> For batch runs, estimate the runtime of each major category or type of job, and each major set of runtime parameters. Run batch jobs in parallel, running the longest-run-time jobs first, and using a MSSQ (Multiple Server, Single Queue) architecture so that no single long-running job can block any other job, and that one thread doesn't block another one, and that as the batch completes, there are no single long-running jobs blocking other jobs.

## Checklist before any significant run

Run each review with its own fresh subagent, in parallel.

| Review | What to check |
|---|---|
| **Performance and parallelism** | Use of threads and processes; independent groups of jobs; local limits (CPU, RAM, bandwidth) and cloud limits (rate limits, concurrency, budget) |
| **Reliability** | Timeout and retry policy (retry infrastructure failures only, never rerun a behavioural outcome); checkpoint and resume; monitoring and alerts for cloud errors |
| **LLM and cloud parameters** | Model, version and size; temperature; max tokens and context length; prompt length; number of iterations and seeds. Check each for experimental validity, good practice and cost. |
| **Experimental design** | Parameters, datasets and arms. Remove superfluous processing. Flag arms that are underpowered, low-value or misaligned with the research questions. Check statistical power. |
| **Correctness** | Prompts render as intended. Run IDs are unique and resumable. Outputs are parsed and validated. A small pilot runs cleanly first. |
| **End-to-end alignment** | The sprint's three judging criteria (aim for 5s), its three research tracks and their sub-questions, and the interests of judges and mentors, especially those at frontier AI labs and AI safety organisations |

## Estimate, then ask for approval

Before any run that uses paid or cloud resources, give the user a table like this and **wait for approval**:

| Job type / parameter set | Jobs | Requests | Input tokens | Output tokens | Est. runtime (wall-clock at planned parallelism) | Est. cost |
|---|---|---|---|---|---|---|
| … | … | … | … | … | … | … |
| **Total** | | | | | | |

State your assumptions: tokens per request, latency, concurrency and price per token. Estimate separately for each major job type and each major set of runtime parameters.

## Scheduling: Multiple Server, Single Queue (MSSQ)

- **One shared queue, several workers.** All jobs go into one queue, and a pool of workers (threads, processes or cloud slots) takes the next job as soon as it becomes free. No job is ever tied to a particular worker.
- **Longest jobs first.** Order the queue by estimated runtime, longest first, so the batch doesn't end with one long job running while every other worker sits idle.
- **Respect dependencies.** Split the run into dependency groups. Within each group, run as many jobs in parallel as the local and cloud limits allow.
- **No blocking.** A slow or failing job must never block another worker. Use per-job timeouts and isolate failures.
- **Monitor the run.** Track throughput, error rates (timeouts, rate limits, connection errors) and cost so far, and alert when any of them drifts from the estimate.
