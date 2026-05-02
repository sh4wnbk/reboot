# Session Resume Card - Video Demo Script

## [TITLE SLIDE - 5 seconds]
**On screen:** Team name + "Session Resume Card"

"Hi, I'm [name] and this is Session Resume Card."

---

## [PROBLEM - 25 seconds]
**On screen:** Developer staring at screen, looking confused

"You know that feeling when you open your IDE after lunch, or the next morning, and you just... stare at the screen? You remember you were working on something important, but what was it exactly? Where were you in the code? What were you about to do next?

Most developers spend 15 to 20 minutes every time they context-switch just trying to remember where they left off. That's time we're never getting back."

---

## [SOLUTION - 10 seconds]
**On screen:** Session Resume Card logo/name

"Session Resume Card fixes that. It reads your Bob IDE session history and gives you a compact summary — exactly where you were, what you were doing, and what to do next."

---

## [LIVE DEMO - 2 minutes]
**On screen:** Bob IDE interface

"Let me show you how it works. Here I am in Bob IDE — I've been working on adding a new feature to my app. I've had a conversation with Bob, made some code changes, ran some tests. Now I need to take a break.

**[Click through Bob IDE]**

Before I close this session, I go to Views, More Actions, History. I select my task and click the Export icon. Bob saves my entire session as a markdown file.

**[Show exported file]**

This file has everything — my original request, Bob's responses, all the code changes, even the terminal output. It's complete, but it's also... a lot. If I come back tomorrow and try to read through all of this, I'm back to square one.

**[Open terminal]**

So instead, I run Session Resume Card. I just type:

`.\run.ps1 --export session.md --format structured`

**[Show command running]**

The tool sends my session to watsonx.ai — specifically the llama-3-3-70b-instruct model — and asks it to create what we call a Restoration String.

**[Show output appearing]**

And here it is. Look at this — it's broken down into clear sections: where I was in the project, what I accomplished in that session, what I was about to do next, and even the specific files I was working with.

**[Scroll through output]**

This is everything I need. When I start my next Bob session, I just paste this in and say 'continue from here.' No more staring at the screen. No more trying to piece together what I was doing. I'm back in flow state immediately."

---

## [IMPACT - 25 seconds]
**On screen:** bob_sessions folder, screenshots

"Here's the meta part — we built this tool entirely using Bob IDE and watsonx.ai. Every session during development was exported and fed back into Session Resume Card itself. The bob_sessions folder in our repo has all the proof.

We used Bobcoins efficiently by focusing on structured prompts and only processing what we needed. The result? We're saving 15-20 minutes every time we context-switch. For a developer who switches contexts 3-4 times a day, that's over an hour saved daily."

---

## [CLOSE - 10 seconds]
**On screen:** #watsonxHackathon, GitHub repo link

"Session Resume Card — because your brain shouldn't be your only backup. Built with Bob IDE and watsonx.ai for the watsonx Hackathon. Check out the repo and try it yourself."

---

**Total estimated time: 2 minutes 55 seconds**