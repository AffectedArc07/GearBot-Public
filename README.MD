# GearBot Public Release

This is a public release of the code compiler and general coder utility bot found in the Paradise discord.

## The code! Its terrible

Yes it is. This project has been hacked together with various snippets since 2019, hence why some of the python is god awful, and so is the rest of the project. It included:

- Hardcoded secrets [now removed]
- Shell scripts hardcoded to work on my server and only my server
- No inbuilt management of BYOND versions
- A ton of copypaste everywhere (look how many cogs have the header for the `misc.py` cog)
- Various styles of string interpolation, or none at all
- General hackyness to make things syncronous
- A proprietary rust executable that could read `.dmb` bytecode to disassemble. This has been removed for reasons.
- A complete lack of source for the DMI function, which no one ever uses. Oops.

## Why publicise it?

A few reasons.

1. It's been in use in the discord for a while and I should really make it public.
2. Some improvements could be made even if this repo isn't the live repo.
3. I finally upgraded from a 2020 build of discord.py to the latest, and commands now take like **8 seconds** to execute and I have no idea why.
4. It's a good showcase of how we all started off terrible. You are free to cry at this source and laugh at how bad things used to be, and how this is **still** somehow in use.

## LICENSE

None lol. You should **NOT** use this. No instructions are provided. This is source to merely cringe at and/or hopefully oxidise (aka - convert to rust). I am open to monetary offers if you wish to take this up - ping me in coderbus for details. *Yes I know `Wrench` exists and is written in rust, I just want to host a para specific one with a few extra commands and a format we are all already used to.*
