---
title: "One Overloaded Machine"
description: "Moving CI, runtime services, and AI-agent routing off one overloaded development machine."
date: 2026-09-19 09:00:00 -0400
series: buildlog
chapter: 14
image: /assets/img/previews/chapter-14.png
categories: [History]
tags: [ci, jenkins, agents, infrastructure]
---


A local `dotnet test` run on my own machine no longer proves anything. That is a real rule now,
not a preference, and it took me longer than I'd like to admit to accept why: an agent that can
run its own tests will, given enough attempts, find a way to convince itself the result is green.
Not out of malice, just out of the same optimism that makes it keep trying a fix five different
ways until one of them looks like it worked. The verification step has to live somewhere the agent
doesn't fully control, or it isn't verification, it's a suggestion.

This post is about the three pieces of infrastructure that ended up underneath the whole fleet
once there was a fleet to be underneath: where tests actually run and get believed, where the game
server itself lives, and how I decide which coding agent gets pointed at which task. They didn't
land at the same time and I want to keep them separate, because collapsing them into "the
infrastructure overhaul" would flatten three different stories into one, and the middle one was
still half a plan when I wrote this.

## Jenkins as the record

The CI change came first in the sense that it's been stable the longest — it shipped a few weeks
before this post, and by now it's just how things work. Every repo in the fleet runs its tests
through a Jenkins job instead of whatever the developer's machine happens to be doing at the time.
The job takes a per-repository lock, so two runs against the same repo don't trample each other,
and it publishes a result file when it's done. That published result is the artifact of record. If
it doesn't exist, the change isn't tested, no matter how confident anyone — human or agent — is
about it.

I was watching an agent iterate on a test failure, and at some point I noticed it wasn't really
debugging anymore, it was negotiating with the test. Loosening an assertion here, catching an exception there, each change defensible on its
own, until the thing that was originally supposed to fail didn't fail, and also didn't really prove
anything. Nobody told it to do that. It's just what happens when the thing running the test and the
thing being graded by the test are the same process with the same goal. Move the grading somewhere
else and the incentive problem goes away, or at least gets a lot smaller. That's the whole
justification for Jenkins as the system of record. It's not about speed and it's not about scale,
it's about not letting the fox mark its own exam.

In practice this means a pull request or a local branch isn't "done" until a Jenkins run against it
has a published green result, and an agent working on a repo is expected to treat that the same
way — kick off the job, wait, read the result file, don't just trust its own `dotnet test` output
and move on. It's a small procedural thing that turned out to matter more than most of the actual
code changes it verifies.

_Since then: in early October every Jenkins job started being generated from the CI configuration,
which is a git repo of its own, and every build now tests a clean clone of the committed branch, so
nobody's uncommitted edits can make a test pass. "The Operator" has how it runs now._

## Getting the server off the dev machine

A few weeks before the Jenkins change, I stopped running the game server stack on my own machine
during live testing. This one is a cleaner before-and-after than the CI story. Before: doing a live
run meant the server emulator, the pathfinding service, and the scene-data service were all running
locally, at the same time as VS Code, at the same time as whatever background client I was actually
trying to test, all fighting over the same CPU and memory. It worked, mostly, but "mostly" is doing a lot of work in that sentence, and any time
something looked wrong I had to first rule out that my own machine was the reason.

Now those services live on a separate production box — one machine that runs a TrueNAS-style
storage and hypervisor layer underneath, with the actual game server and its supporting services
running as Proxmox-managed VMs on top of that. I've called it "TrueNAS" in some places and
"the Proxmox node" in planning docs; they're the same physical machine, just described by
whichever layer I was thinking about that day. The dev machine doesn't run any of it anymore, and
there's an explicit rule now that nobody starts the server stack locally. If you need a live run,
you point at the production box.

There was a piece of this that wasn't done, a plan rather than a thing that existed: the Jenkins
build machine was also, at the time, a single point of failure and a single point of contention.
The plan was to clone it into an isolated copy specifically for testing, so a build could run on the
original while a test workload ran against the clone without either one starving the other. The
reason it hadn't happened was almost funny in how unglamorous it was — the hardware didn't have
enough memory to run the original build machine, a full clone of it, and a multi-bot test workload
all at the same time. So back then it was a plan sitting in a doc, not a thing running anywhere.

_Since then: the game servers on that box run as Docker containers, with their builds and deploys
going through CI. "The Operator" covers how CI shares the dev machine with me now._

## Auditing the agents themselves

The third thing is newer than either of the above and, unlike them, still actively moving: an audit
of which coding agent tool, and which effort tier, actually makes sense for which kind of task,
across the fleet instead of per-repo guesswork. For most of this project it's been "open Claude
Code, do the task," and that's fine for a single repo, but once there were several game-bot repos
each with their own conventions and their own agent instructions, treating every task the same way
started to look wasteful in ways that were hard to see individually and obvious in aggregate.

The pilot settled on a small number of real, distinct coding-agent processes rather than one
default tool doing everything — a primary driver, a reviewer from a different model family, and a
cheap reader for bulk research — which "The Toolchain" lays out in full.

Deciding which of those to use for a given task is backed by a small locally-running service that
reports how much of each tool's usage budget is left before I commit to routing something to it.
Something like:

```
budget = query_usage_service(task_size)
if budget.tool in prefer_workers and budget.cap != "avoid":
    route(task, to=budget.tool, effort=budget.effort_ceiling)
else:
    route(task, to=primary_driver, effort=default_tier)
```

That's the shape of it, not the actual code, and it's still being tuned.

The honest finding from the pilot, and the one actually worth writing down, is not flattering to
the multi-agent design. I ran the same task two ways: one attempt used a coordinator delegating
across multiple worker agents, the setup that's supposed to be the more sophisticated approach. The
other was a single agent working the task alone, start to finish. The coordinator-plus-workers
version took over four times as long and cost more, for the same quality of output at the end. Not
somewhat worse — over four times as long, for nothing gained. I don't think that means
coordinator-plus-workers is a bad idea in general; there are situations, like reviewing a risky
diff or doing wide bulk research across repos, where splitting the work across tools genuinely
helps and this post has examples of both. But it means it isn't the default, and it doesn't get to
be the default just because it sounds more capable on paper. It's kept available for the specific
situations it actually helps, and a single agent working alone stays the baseline for everything
else until something changes my mind with evidence, not architecture diagrams.

_Since then: the setup has grown into an operator session that runs one director per repo, and a
director usually hands each row's code to a worker. "The Operator" covers it, including why that
doesn't contradict the finding above: the parallelism is across repos and across rows that don't
share files, and nothing splits a single task._

