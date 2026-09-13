---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
---

**Westworld of Warcraft** is a simulation platform. It turns a private World of Warcraft server
into a world populated by autonomous characters — bots that quest, fight, travel, group up, and
run dungeons without anyone at the keyboard. The goal is the one the HBO show implies: characters
behaved well enough that a human playing alongside them could not tell which ones were people.

This blog is the development log. It covers three things, usually at the same time:

- **The bots.** How a character decides what to do, how that decision decomposes into something a
  game client can actually execute, and how far that is from looking human.
- **The client.** Driving a 2006 game you have no source for — process injection and memory reads
  on one side, a from-scratch protocol and physics implementation on the other, and the work of
  keeping the two honest with each other.
- **The process.** The project is built with coding agents, and that changed both how fast it
  moves and what kinds of mistakes it makes.

## Scope, stated up front

This runs on a **private, self-hosted server** using a **legacy 1.12.1 client**, and only there.

It does not work against modern retail World of Warcraft, and nothing here is written to help
anyone try. The techniques are specific to a twenty-year-old binary on a server that is not
Blizzard's. The anti-cheat system in that old client is disabled during injection for the simple
reason that both the client and the server belong to me.

Nobody is competing with these bots for anything. There is no economy to distort, no ladder to
climb, and no other players to disadvantage. They exist to be watched and studied.

The project is a hobby and a research platform, and it is unfinished. The posts here say so.

## Credit

The foundation is [BloogBot](https://www.drewkestell.us/Article/6/Chapter/1) by **Drew Kestell**,
whose write-ups laid out the whole approach with source available. This project began as a fork of
that work and owes it a great deal.

**Jared Rhodes** built the inter-process communication layer the whole architecture still rests on,
and **Seth Rhodes** has contributed along the way.

It also stands on [VMaNGOS](https://github.com/vmangos/core) and the
[Recast & Detour](https://github.com/recastnavigation/recastnavigation) navigation libraries.

## Contact

Lamar Rhodes — [github.com/lrhodes404](https://github.com/lrhodes404)
