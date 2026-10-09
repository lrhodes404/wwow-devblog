---
title: "The Pull Problem"
description: "Building the coordination a group pull actually needs — raid markers, threat gating, verified pull spots — on top of navmesh data finally trustworthy enough to bake them from."
date: 2026-09-15 09:00:00 -0400
series: buildlog
chapter: 10
categories: [History]
tags: [dungeoneering, group-ai, pathfinding, raid-markers]
---


Bots had been getting stuck in Ragefire Chasm since the very first five-bot group, for the navmesh
reasons covered back in "The StateManager," and I shelved dungeoneering rather than keep staring at
it.

That failure didn't get solved by grinding on it for years. Once the physics and scene-data work
from the last several posts gave the navmesh something honest to describe, the coordination side of
the dungeon problem turned out to be tractable in a few weeks. Whether the whole thing actually
clears end to end yet is a separate question, and I want to answer it honestly rather than let the
coordination win read as more than it is.

## The long gap

Dungeon-running then sat untouched for something like twenty months — not because I forgot about
it, it just wasn't on the list. That stretch covers most of the physics saga and the early
Claude-assisted work: getting the background client's collision and movement to actually match the
game client, then reverse-engineering the binary to stop guessing at it. None of that was framed as
"fixing dungeons." It was framed as fixing movement, full stop, and dungeoneering was one of the
things sitting downstream of it, waiting. That gap is worth naming instead of glossing over,
because it's the shape of the whole arc: the fix for a three-year-old failure was never a better
dungeon AI. It was making the ground underneath it trustworthy.

Once the physics work had landed enough to be usable, I restored the dungeoneering task from
wherever it had been sitting — a bare, mechanical restoration, followed a couple of weeks later by
a unit-test pass covering the ten or so key behaviors. That's the whole beat. It wasn't a rewrite
and it wasn't the moment anything got proven. It was just putting the piece back on the board so it
could be worked on again.

## Getting bots to agree on a pull

What actually changed happened in a dense stretch this summer, and it's mostly about coordination,
not raw pathing.

The first piece was getting bots to pay attention to raid markers — the icons a raid leader can
drop on the ground or slap onto a target. Bots went from treating markers as decoration to actually
reading party stats and marker assignments before deciding what to attack. That sounds small, but
it's the difference between five bots independently deciding what to attack and five bots agreeing
on a target because someone put a skull on it.

The second piece was threat-gated engagement. Plainly: a bot doesn't walk up and swing at whatever's
nearby. It waits until the tank has actually established threat on a target before committing to
it.

```
onCombatTick(bot, target):
    if bot.role != Tank and not target.threatEstablishedBy(tank):
        wait()
        return
    if bot.role == Tank and not tank.hasThreatOn(target):
        tank.buildThreat(target)
        return
    bot.engage(target)
```

That one rule is most of what makes a group fight look like a group fight instead of a scramble.
Without it you get exactly the kind of chaos that used to end with someone pulling an extra pack
and the whole group dying under an overhang they couldn't get out of anyway.

The technical heart of the work, and the part that actually closes the loop back to the original
failure, is a shift in how a pull gets planned in the first place. Instead of a bot wandering into a
room and hoping the geometry works out — which is exactly what was happening in 2023 — the game now
precomputes which specific spots in a dungeon are legal places to stand and pull enemies from,
derived directly from the navmesh. The same navmesh data that used to be the entire problem is now
trustworthy enough to bake pull regions out of, which is about as literal a callback to the original
failure as this project has produced.

```
bakeLegalPullRegions(navmesh, room):
    candidates = navmesh.sampleWalkablePolys(room)
    return candidates.filter(spot =>
        navmesh.hasPathTo(spot, room.exit) and
        not navmesh.isUnderOverhang(spot) and
        room.pullRadius(spot).clearOfAdjacentPacks()
    )
```

Alongside the baking step is something I've been calling a pull-spot oracle — a coordinator can
query it for a specific, navmesh-verified spot to send the puller to, instead of eyeballing a room's
centroid and hoping. One thing I want to flag rather than overclaim: the code orders visits to
multiple pull spots and objectives, but there's no formal traveling-salesman implementation in
here. It's ordered visitation, not a routing algorithm with a name, and I'm not going to call it
something fancier just because "TSP" is the word that comes to mind when you see a list of stops.

None of this landed as one clean piece and stayed put. A dead tank was forcing every follower to
walk all the way to its corpse before the group could re-form — fine for a single character, a bad
rule for a five-bot party standing in a room full of kobolds. A regression in the follower
waypoint cap crept back in from the pull-region work and needed its own fix. Neither of those is
glamorous. Both are the actual texture of getting a system like this to hold up under repeated runs
instead of one good take.

## Where this actually stands

![A bot at 1 HP out of 213 in Ragefire Chasm, mid-fight against Earthborer](/assets/img/posts/finally-clearing-rfc/wow-dungeoneering-2.png)
_The same Earthborer fight from the "Inheritance" post, one frame later — this is what a pull with
no threat-gating and no verified pull spot looked like from the inside. Nobody agreed on a target,
nobody built threat first, and the healer found out the hard way._

I want to be precise here instead of letting the coordination work read as a bigger win than it
is: RFC has not been cleared end to end yet. What exists now is the machinery a clean clear would
actually need — bots that agree on a target, a tank that reliably holds threat before anyone else
commits, and pulls planned from verified, navmesh-backed spots instead of guesses. Each of those
pieces works on its own and has been tested on its own. Stringing all of it together into one full
run of the instance, start to finish, without a human stepping in, hasn't happened yet.

That's a meaningfully different place than three years of "stuck under an overhang," and I don't
want to undersell it. But it's not the same as having cleared the dungeon, and I'd rather say that plainly now than have a future post quietly
correct it.
