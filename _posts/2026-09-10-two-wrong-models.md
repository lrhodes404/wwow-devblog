---
title: "Two Wrong Models"
description: "Two different approaches to collision and movement, tried one after another, both wrong in a way that took months each to actually prove."
date: 2026-09-10 09:00:00 -0400
series: buildlog
chapter: 5
categories: [History]
tags: [physics, collision, navmesh, vmap]
---


The navmesh-as-height-source stopgap from the last post worked fine on open ground and fell apart
the moment a bot walked under anything. Stand a background client on a hillside and ask the
navmesh how tall it should be, and the answer is right, because there's exactly one polygon under
its feet and exactly one floor. Send that same bot into Ragefire Chasm, where the path doubles back
under itself and a walkway passes directly over a lower room, and the question stops having one
answer. The mesh happily returns the height of the ledge six feet overhead, because as far as
Detour is concerned that ledge is also "the nearest walkable surface," and now the bot is standing
on a ceiling.

The reason is structural, not a bug: Detour's world model is a 2D graph with height annotations,
not a volume. It can tell you whether a polygon is walkable, but it has no concept of what's solid
above or below it, because it never needed one. So the first real attempt at fixing this didn't
touch the navmesh's connectivity at all. It tried to give the height query something better to
consult — the same collision geometry the real client uses, read straight from the map data instead
of baked into a walkable-polygon mesh.

## Reading the map data directly

VMaNGOS already parses this data — VMAP for static building and terrain-mesh collision, ADT for
outdoor heightmaps — for its own line-of-sight and spell-range checks. That code already existed,
was already tested, and answered exactly the question a background bot needed: given an X and Y
and a starting Z, is there solid geometry below this point, and where. Wiring a bot's height query
into that instead of the navmesh looked, at first, like it would simply make the overhang problem
go away, since VMAP has to know about ceilings or the server's own sightline checks would be wrong
too.

Getting a usable number out of it took a while — the lookup was close but not exact for weeks
before it was actually right. What turned it into something usable wasn't the lookup itself, it
was how a bot used it. Instead of asking for the height at one exact point and trusting the single
answer back, the background client started sweeping a capsule — the same shape used for the bot's
own collision — straight down through the map geometry from somewhere above its last known
position, and taking the first surface it hit as ground:

```
function findGroundZ(position, searchRadius):
    capsule = bot.collisionCapsule
    topZ = position.z + searchRadius
    bottomZ = position.z - searchRadius
    hit = sweepCapsuleDown(capsule, position.xy, topZ, bottomZ, vmapGeometry, adtGeometry)
    if hit.found:
        return hit.z
    return null  // fall back to navmesh height
```

This fixed the Ragefire Chasm case specifically — a bot in the lower room no longer had its Z
snapped up to the walkway above it, because the sweep found the nearer surface first — and for a
while the work that followed was tuning, not discovery: transport handling, replay calibration,
cliff rerouting, batching the queries so they didn't cost a full sweep every tick. Each of these
made some specific case better. None of them made the underlying idea more correct.

## Which surface counts as ground

![A debug console printing MOVEMENT: snapping to ground with old/new position, delta, and velocity, next to a character standing in the Valley of Trials](/assets/img/posts/the-downward-probe/wow-standing-on-vmap.png)
_The actual output the probe was producing on a walk through the Valley of Trials — old position,
new position, a Z delta, velocity, all snapped to whatever surface the sweep found first. Reading
these logs line by line is how the bugs below actually got found._

The problem the probe never solved, and structurally couldn't, is deciding which of several hits
is the one that matters. A downward sweep anywhere with real vertical complexity doesn't return one
surface, it returns a list — a cave floor, a tunnel ceiling above it, an overlapping piece of
decorative geometry, sometimes a second cave floor further down if the map has one dungeon stacked
under another. "Pick the first one," "pick the closest one," "pick the one inside some search
window above the bot's last position" — all of these sound reasonable, and all of them fail
somewhere, because the rule a real client actually uses isn't geometric at all. It's the client's
continuous physics state, carried frame to frame, which a single downward ray with no memory of
how the bot got there was never going to reconstruct.

In practice this showed up as a run of narrow, specific bugs that all traced back to the same root
cause: the search window preferring a cave surface over the correct one, the same ambiguity
showing up separately on the teleport path, a bot on an ordinary sloped ramp in the Valley of
Trials falling straight through the terrain because a slope makes "nearest surface below" far more
sensitive to exactly where the sweep starts than flat ground does. Each of these got its own fix,
and each fix worked for the case it targeted. None of them gave the probe a principled way to know,
in general, which surface under a bot a real client would actually be standing on — because the
information that decision needs (is this volume the inside of a building, or a cave beneath the
ground I'm on) isn't in the map data at all. It's a byproduct of the client's real physics state,
which is exactly the thing this whole approach was built to avoid needing.

The commit that said this out loud didn't come from a general audit. It came out of chasing one
specific case in Warsong Gulch, where a bot kept preferring the wrong ground surface no matter how
the search window was tuned. The conclusion was blunt: every knob available for adjusting how the
navmesh was baked, or how the probe searched it, was dead, because the problem was bake-independent.
No amount of rebaking the mesh or re-tuning the sweep was going to fix something that lived one
layer down — the probe could only ever be as good as its model of "what counts as ground," and that
model was a guess dressed up as geometry.

## Building a physics engine instead

That reframe pointed at the same conclusion from a different angle: stop trying to infer the right
surface from static collision data after the fact, and instead get the background client's own
model of movement close enough to the real client's that it wouldn't need to infer anything. This
wasn't a decision made in isolation — a second, larger effort had been running on a different
branch for most of this same stretch, in parallel with the map-reading work above: an attempt to
give the background client an actual physics engine, modeled on the game's own.

I built it from scratch, in C++, on the kind of character controller PhysX itself ships: a capsule
standing in for the character's body, swept through the world once per tick, its contacts
resolved, sliding along whatever it hit rather than stopping dead or tunneling through it. It's a
well-understood approach — every serious engine has some version of it — and it was the obvious
thing to reach for with a little 3D-engine background and no idea whether WoW's client actually
worked anything like it. I assumed it probably did, mostly because it's what anyone building a
character controller in the mid-2000s would have reached for, and because it was the model I knew
how to implement.

![Two characters fishing off the dock at Ratchet, with GM teleport and skill-up messages in the log](/assets/img/posts/physx-and-the-wall/wow-sphere-sweep.png)
_A capsule-sweep test dressed up as two bots fishing off a dock — the dock edge, the water line, and
a GM teleport back to a known position are exactly the kind of small, repeatable geometry you want
when checking whether a swept sphere resolves a contact correctly._

On paper, this is a clean way to turn "where do I want to go" into "where do I actually end up,"
without special-casing every kind of terrain. Running it against real Azeroth geometry — uneven
ground, doorframes, the lip of a staircase, the underside of an overhang — the model produced
behavior that was directionally right and specifically wrong: sliding along a wall instead of
stopping at it, stopping at a slope a real character would walk straight up, hanging for a frame at
a ledge edge where the real client would have already committed to the fall. None of these were
exotic. They were the ordinary cost of guessing at contact-resolution rules that had actually been
written down somewhere in a binary nobody had looked at yet.

## Calibrating against a client that never explains itself

With no way to ask the model whether it was right, the only option left was to ask the game
instead: run the real foreground client, record exactly what it does frame by frame — every
position, every flag, every velocity — and try to make the background client's physics reproduce
those same recordings from the same starting conditions. If the two capsules ended up in the same
place, the model was right for that frame. If they didn't, the recording showed roughly where the
divergence started.

That harness took real infrastructure to build — packet capture hooks on the foreground client, a
detour on its own message-processing function so the recorder could see movement packets before
they left the process, a fix for a Z-axis guard that had been quietly inflating recorded heights —
and it ran for months in parallel with the physics work it was meant to validate. Along the way I
also started running the recorded movement against VMaNGOS's own anticheat rules, the same checks
the server uses to flag a client for teleporting or speed-hacking. That one is worth pausing on,
because it's an unusual kind of validation: the goal was never to evade the server's cheat
detection, it was to use it as a free, independent second opinion on whether the model's output
looked like something a real client would actually have sent. If the anticheat would have flagged
it, the anticheat was right and the model was wrong.

![Two WoW clients and a VS Code window, with a Windows notification reading "Claude is asking you a question"](/assets/img/posts/physx-and-the-wall/wow-physics.png)
_The shape of a calibration session by this point — two clients running side by side for a
foreground/background comparison, a terminal running the parity tests, and an agent partway through
one of them, waiting on an answer before it kept going._

None of this, calibration included, is actually a way to know a model is correct. It's a way to
know when it's wrong. Every recording matched narrows the space of remaining error without ever
closing it, because there's always another terrain feature, another edge case not yet recorded,
where the two diverge again. You can get very good at guess-and-check without the guess ever being
the right shape — which is roughly what four months of this bought: a model that converged closer
and closer to the recordings without ever converging exactly, because it was, unknowingly, the
wrong shape of model entirely.

## The kill

The model eventually got a name — PhysX-CCT — on the same day it was killed. There was no gap
between writing the name down and deleting every reference to it, because naming it was the last
step of finally being able to say what was wrong with it in one sentence: WoW.exe is not a
PhysX-style three-pass swept-capsule controller. Every open-source implementation tried before
this one, and the one built here, assumed something roughly in that family — sweep, detect,
resolve, slide — because that's the standard shape of the problem in every engine that documents
how it solves it. That assumption is exactly why months of calibration against real recordings
produced a model that kept getting closer without ever arriving. The constants weren't imprecise.
The equation was wrong, and "closer" had been getting mistaken for "almost there."

The cleanup ran for weeks afterward — the dead collide-and-slide code came out, the capsule
primitive itself turned out to be close to whatever Blizzard was actually using for its bounding
volume, which says something about how much of that calibration time had gone toward compensating
for the collision model rather than the primitive shape. The last function with zero live callers
left anywhere in the solution came out some time later, on the same day, as it happened, that a
completely unrelated verification pass was quietly confirming a different, newer set of numbers
against the binary byte for byte — but that's a different post's story.

Two models, tried one after the other, both wrong for reasons that took months of real
infrastructure to prove. That's the honest shape of this stretch of the project: not a wall that
eventually gave way to the right technique, but two techniques that each looked reasonable, each
got a real hearing, and each turned out to be solving the wrong problem.
