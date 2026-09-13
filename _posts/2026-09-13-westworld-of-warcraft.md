---
title: "Westworld of Warcraft"
date: 2026-09-13 09:00:00 -0400
categories: [Origin]
tags: [wow, bots, origin]
pin: true
---

World of Warcraft was my first MMORPG. As a huge fan of Warcraft, and Blizzard in general, it was
inevitable that I would play the game. At one point, it was my motivating factor to move out of my
dad's house, as it was financially advantageous for me to live there while going to school. He
lived in the woods, so we only had satellite internet, and the 5s+ ping was never conducive to
multiplayer gaming. Most of my multiplayer experience at that point was LAN games, but I couldn't
do that for an MMO either.

So I moved out into an apartment with friends and shared an account with my brother, Jared. He had
a rogue he would play when he would visit, and we'd share resources as best we could. I had no clue
what I was doing and didn't even play on the same faction as my friends, because I wanted to play a
shaman and didn't know how the factions worked until I was too invested. This created a great
rivalry with my friends, as Jared and I were "The Horde Players" in our group, which resulted in a
few IRL "attacks" where an Alliance player would get IRL ambushed in their apartment so the Horde
player would have a fighting chance.

I chose the route of PvP with my shaman because I could hop in and out of games at work, and used a
priest my brother had leveled to actually raid in Molten Core and Zul'Gurub. I acquired my
Benediction but sadly have never defeated Ragnaros...

I was forced to move back in with my dad and had to put my WoW career on hold. I tried to play, but
the raiding guild quickly lost interest once they saw how my internet performed. I can't blame
them, but it was an experience that would prepare me for corporate life. I had taken on a new
position at work, so I couldn't play there anymore either. It wouldn't be until that job "forced"
me to move to a new city that I would be able to play again. Jared was conveniently going to school
in the same city, so we lived together with various folks and were able to get him a separate
account. At that point we had decided to really dive into the game: raiding and achieving
server-first progression, successful BG groups and Arena teams, max professions on multiple alts,
etc. This continued from the end of The Burning Crusade into Wrath of the Lich King.

It was about this time that I was laid off from the job that had brought me here and, having not
finished technical college, I was forced onto unemployment and was working part-time at a BBQ
restaurant I could walk to from the apartment. By this time, school was picking up for my brother,
and we had grown burnt out with guild drama. We left our raiding guild and took up life as
mercenaries, just enjoying PvP and keeping up with dailies.

It was around this time that I had decided to go back to school. I didn't want to continue with my
technical college career and wanted to go to the school my brother and friends were at, because it
seemed to be where lives were headed in a good direction. Even though I had failed my first
programming course in technical college, I still decided to change my major on the first day from
I.T. to Computer Science. At that point my most successful attempt at programming was editing the
Lua of a WoW mod so it would play specific audio files instead of the default ones in particular
zones. Losing my job and having most of my possessions destroyed put things in perspective, so I
decided to put some effort into this one. As it turns out, I really enjoyed and was good at
programming. And software development in general.

## Botting becomes the game

Around this time, Wrath of the Lich King was wrapping up. We had achieved server-first Ulduar and
Immortal achievements (server first!). My brother even participated in the smaller guild's
server-first Undying achievement. We had multiple alts that covered all professions, but no time to
really keep up with everything. Everyone is going to school full time, so who has the time to farm?
Weekly PvP wasn't viable, as you'd only have a few hours of playtime a week, and even then, the
college life had a lot to offer.

I decided that I wasn't too concerned with what happened to my account as I started to mull over
how to keep up with the game, and the choice was obvious: botting. I wasn't trying to grind to High
Warlord or dominate the Auction House, but I wanted to keep playing and enjoy the game when I had
the time.

This turned into its own game. The bot I used had an interface that let you write C# script for how
to control the bot's behavior. As a budding CS student, I ended up having as much fun working on
the bots as I did enjoying the fruits of their labor. I would monitor it while studying for other
classes and get tickled every time someone sent a whisper thanking it for helping them or telling
it "you're really good!". I became very proud of my Turing Test WoW bot, and it wasn't until
Cataclysm when I finally decided it was time to wrap it up...

Friends had me running their accounts as well, so we had a small "army" of 4 accounts full of
characters that could gather resources and work together in PvP. Eventually, THAT became the game
for me. It was more about resource management and optimization rather than playing the game as
intended. Spell rotations and placement were analyzed and optimized over days of farming. We had
everything we could need, but Cataclysm had left a lot to be desired and life had already changed
so much for myself and my friends. After "capping out" on what we could do, it was time to sign
off. Many more expansions would come out that I couldn't play, and the very brief time I spent
trying out other MMOs never gave me the same feeling the older WoW iterations did. I would dive
into Final Fantasy XIV, but after a falling out with the group I joined, I decided MMOs just
weren't for me. Too much time needed to invest, subscriptions needed to maintain servers and new
content, etc. I didn't want a second job, so I would swear off MMOs entirely.

## Ten years later

Fast-forward nearly 10 years and my brother and I are reminiscing. I'm not sure how it came up, but
I was streaming Warhammer Online: Return of Reckoning and was really enjoying that. I simply loved
the big player battles and city sieges. As was customary, I played a shaman, and I had the time to
farm a little for materials and spent most of my time on stream doing warband PUGs. I experimented
with a bot for WAR but never intended on using it, as the RoR gameplay loop didn't require it and,
for the most part, all parts were fun.

At this point I've been a software developer for quite some time. I was able to comprehend every
aspect of how the game and bots worked together, how cheat detection worked, how game clients
operated, packets, client-server ownership, etc., to the point that when my brother and I were
discussing it, I was challenged again to do the parts of the game I hadn't covered with my previous
bot experiments: dungeons and raiding. I thought it would be fun to find the old bot that I used to
use and see if I could use it to recreate the fun I had when I was writing behavior scripts and
feeling like I was really testing how my work would be interpreted by live unaware users.

I shopped around using various bots that were free before it dawned on me: you're a veteran
software engineer and this has been around for over a decade. Surely something already existed that
was more flexible, that could allow me to do what I wanted to. I finally stumbled upon
[Drew Kestell's write-ups](https://www.drewkestell.us/Article/6/Chapter/1) and it led me down a
rabbit hole of even clearer understanding of how the botting process worked. Most of it I already
understood, but to see it all laid out and to have the source code available was a huge step
forward for me. I immediately cloned the repo and made all kinds of adjustments and "enhancements"
so the bot operated exactly as I expected and did things that most bots hadn't been configured for.
Mainly to group and coordinate with each other. This is where the solution started to look like my
own. I needed something to manage the state of each bot so it knew what to do next.

I created the first StateManager that was able to launch individual clients (first `WoW.exe`, then
inject the DLL) and use a POC my brother had created that utilized Google protobuf to compress the
messages and create an exchange of information between each individual "bot" and the StateManager,
so each bot knew what to do next. Once a bot was launched, it would have just enough arguments to
know where to reach out to the StateManager and begin a heartbeat communication loop. As each bot's
state changes, the StateManager internal loop will go through and assign the next task if it
requires changing.

It did not take long to get 5 bots in a group together and using GM commands to set themselves up.
After a few months of working on the project, I found myself stalling, as the bots were successfully
entering RFC but unable to complete it. There seemed to be little errors with how it handled navmesh
generation (the default server method wasn't the best for units that had to actually adhere to the
physics of the game, as opposed to server-controlled units that didn't). The bots had a knack for
getting stuck, and I wasn't making a lot of progress with Detour/Recast in fixing them getting stuck
underneath overhangs or stuck in places that didn't have a path out. The project itself was stalling
even though I had made a lot of progress. I decided to shelve it for a while and come back to it.

## Westworld

Fast-forward again to ChatGPT and other LLMs emerging that were starting to redefine how software
engineering was handled. My brother and I immediately thought of the Warcraft bot project and how it
could help me overcome some of the challenges. It was clear that just the initial GitHub Copilot and
ChatGPT were already propelling me ahead. After a series of discussions with my brother about the
future of these, we quickly came upon our final idea: Westworld of Warcraft. A WoW server populated
by bots, where each bot would simulate a unique character with its own personality and could operate
and be so human-like that a real human playing with them would not be able to discern if someone was
on the other end of the keyboard, or if there was a keyboard at all.

The major hurdle to overcome at this point was scaling. We would never just be able to launch 3,000+
clients and have them be able to operate as we needed them to for our simulation. We would need a
lightweight client that could authenticate and exchange packets as well as follow the navmesh — a
client that would use far less resources and still be able to operate a character.

It didn't take too long standing up scaffolding that would use pre-existing libraries that could
handle the session-key generation as well as send the correct packets. At this point I am taking
server emulation code and putting it into ChatGPT so it can give me files to work with. There was a
lot of "uploading project documents/code files" then "generate new code attempt" and using that to
see what worked and repeating the process, but this time with output logs. This was enough to get a
character logged in outside of the official client and facing my character that was logged in
normally. I quickly piped in the chat packets to be used with my locally running Ollama instance and
was able to "communicate" with my Background Bot character.

I was writing a lot of code manually from here and, as I started working on movement, I hit my first
real wall. I knew very little about 3D engines and had only dabbled with engines like Unreal and
Unity. I tried using open-source code but what I implemented was clearly not compatible with the
Blizzard geometry, and the results varied. I was able to continue testing by having the background
client use the navmesh for what height to stand at, but that was still limited and didn't provide
the desired results, as simple as the solution sounded.

This meant I HAD to get the physics working. Collision and physics were going to be calculated in
the background client so it could operate like the original client as far as traversing terrain, but
also with behavior-relevant information like how large the interact distance is for a particular
unit/game object. So this meant that even if we had all of these things in place, we would still
need to scale the game assets so that each background client could get the necessary data it needed
to make decisions without needing to display anything or play any sounds. As I'm struggling to
implement all of this, Claude and Codex are emerging. I'm still utilizing Copilot and ChatGPT to
implement what I can, but there is still a lot of limitation with what it could generate at the
time and, as this was one of many hobbies (albeit the one I spent the most time on), I still had
other things I wanted to do and I was starting to lose hope that I would make any progress again.

## Enter Claude

By this point, I have a solution that contains multiple projects all covering various aspects of the
Westworld of Warcraft goal. Most are "spec'ed out", where every aspect of what the codebase did was
documented, and what was missing or expected to be implemented. I'm finding myself wanting to do
other activities as I feel like I'm spinning my wheels with countless attempts to isolate the
collision and physics.

All that would change when my brother would message me and tell me he had tried the new "Claude
Code" and that it would be able to get me past my next hurdle. I started using it and knew it was
good, but even after countless upgrades and refactors, I still wasn't able to get past the
physics/collision/movement controls problem I had been encountering. Claude along with Codex were
working wonders on the repo, but any time I turned my attention to fixing movement, it would still
stall. No amount of frame-by-frame analysis was cracking the code, until another realization: the
old bots were built by decompiling the engine and reading memory values. So why not have the agent
dump the `WoW.exe` binary and reverse-engineer it?

Sure enough, it was able to use Python and decompile major sections of the `WoW.exe` binary and was
not only able to reverse-engineer all of the physics and movement code, it was also able to refine
the packet lifecycle so that the clients' behaviors match 1 for 1. After some time ironing out all
of the previous bad solutions and jank code I wrote/generated, I was able to get the solution to
where it was measuring things properly and had the test frameworks as I described them.

I had separated out the BotRunner logic and a lot of the Background client code into unit tests,
while live runs were performed against a locally running WoW server emulator. This is still time
costly, as it requires booting at least one FG client and logging in so that a person can observe
what's going on just in case. I considered how accurate the background client was and decided we
could spend some time working on a world-server unit test where we use server code behavior in our
unit tests, so it can emulate the server world (or at least certain encounters) on a frame-by-frame
basis, so we can make sure the bots perform exactly as requested. For now, this still requires a
human-in-the-loop to verify at various small milestones, but the solution is leaps and bounds ahead
of where it was and it continues to accelerate to being a working solution.

---

> **On scope.** Everything described here runs on a private, self-hosted server using a legacy
> 1.12.1 client. The botting I did on live realms was roughly fifteen years ago, on an expansion
> that no longer exists, with an account long since gone. Westworld of Warcraft is not that: there
> is no one to gain an advantage over, because there is no one else on the server. More on the
> scope and the credits on the [about page]({{ site.baseurl }}/about/).
{: .prompt-info }
