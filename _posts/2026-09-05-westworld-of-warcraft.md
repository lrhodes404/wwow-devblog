---
title: "Lore"
description: "How fifteen years of playing, botting, and walking away from World of Warcraft turned into the reason this project exists."
date: 2026-09-05 09:00:00 -0400
series: buildlog
chapter: 1
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
I was streaming Warhammer Online: Return of Reckoning and was really enjoying that. I loved
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
forward for me.

I immediately cloned the repo.

That was September 2023. Everything after it — the coordination layer, the headless client, two
years stuck on collision, and eventually pointing a coding agent at the game's own binary — is what
this blog is about.

---

> **On scope.** Everything on this blog runs on a private, self-hosted server using a legacy
> 1.12.1 client. The botting described above was roughly fifteen years ago, on an expansion that no
> longer exists, with an account long since gone. Westworld of Warcraft is not that: there is no
> one to gain an advantage over, because there is no one else on the server. More on the scope and
> the credits on the [about page]({{ site.baseurl }}/about/).
{: .prompt-info }

