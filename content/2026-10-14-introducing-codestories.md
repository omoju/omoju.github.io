Title: Where Comprehension Goes: Introducing CodeStories
Date: 2026-10-14
Category: Blog
Tags: ai, developer-tools, comprehension, research
Slug: introducing-codestories
Description: I built stories of codebases, pinned to real lines and run like tests. My preregistered rule said kill. I read it as ship, and published both.
Status: draft

<figure>
  <a href="https://omojumiller.com/comprehension/stories/bench/rich/">
    <img src="{static}/images/codestories/rich-codestory.jpg"
         alt="The CodeStory for Textualize/rich, titled What Actually Reaches the Terminal: Two Strings and a Table Through Rich. A premise paragraph sits above three columns: on the left, a control flow diagram of the traced run with boxes for calls and diamonds for decisions; in the middle, Chapter 1, The World the Data Enters, in prose; on the right, the source of rich/console.py with lines 505 to 522 highlighted.">
  </a>
  <figcaption>Figure 1: CodeStory of the Textualize/rich Python repository on GitHub.</figcaption>
</figure>

CodeStory is an application that follows the journey of data through a codebase based on one real traced run, with claims pinned to lines, a proof per chapter, and it fails like a test. I designed it to start by giving you, the reader, somewhere to stand before the code starts. This choice helps the reader orient themselves, and gives them a place to enter the code.

Each story is presented with its control flow diagram that explicitly traces the data through an intended run of the codebase, a narrative story of the codebase in chapters, and the places in the code where the reader can map the prose to code. In Figure 1, you can see the story for Textualize/rich: [What Actually Reaches the Terminal](https://omojumiller.com/comprehension/stories/bench/rich/index.html). This codebase was one I wasn’t familiar with at all. I was able to follow it, and understand how it works. What made the experience good for me was being able to click on each thing in the control flow diagram, and then jump into where that was in the code base. In my mind, I could follow the intended-use data through the system. And I could start building the mental models I needed to understand the code.

Now, let’s get into how I got here. Remember that essay I wrote on [luxury products and software](https://omojumiller.com/2026/08/14/what-is-luxury-and-what-has-that-got-to-do-with-software/)? I ended it like so:

> “Am not quite sure where the new location for comprehension is, perhaps its reading diffs, but after a while, they are just boring, and hard to force yourself to read a giant migration PR with all its diffs. There has to be a new place. And that has now become my quest.” - Omoju

I started on that quest by doing two-week sprints. Inspired by Angus Fletcher’s *Primal Intelligence*, which argues that human intelligence runs on narrative, for the first sprint, I asked myself what it would feel like to read the story of a codebase. Instead of documentation, what if I imagined myself as a piece of data that had to go on this journey through a codebase. Would such a story hold my attention? Would such a story actually teach me about the codebase? Would I be able to answer questions about the codebase, and when things didn’t make sense, would I be able to tell? All that was going to be my first experiment: go build a CodeStory and find out.

For this prototype, I had two hypotheses that I wanted to test. The first, H1, is that the CodeStory machinery (claims pinned to lines, proofs and so on) would lead to more accurate sentences when compared to generated documentation, Cognition’s DeepWiki. The second, H2, the riskier hypothesis, tested comprehension, and on this one the result showed that a reader with a CodeStory understood the code better than a reader with DeepWiki. I expected the checking to make the stories more accurate than generated docs. It didn’t. What made the difference was the story.

To make sure that I could stand behind my findings, I wrote a preregistration rule to either ship, pivot, or kill the prototype based on those two hypotheses. Based on the results, the rule said kill; my own read, recorded before any number existed, said ship, and both are published. The thing that mattered most from this sprint came after the experiment, when a friend pointed the same machinery at a pull request.

**What I built**

A CodeStory is made of a premise, a reader chosen per story (owner, maintainer, user), a plot that is based on a real run, a protagonist (the main input), chapters sized by the journey, claims pinned to exact lines at a pinned commit, a proof per chapter, reader callouts, and a reading page. Every claim is checked against a commit, and every proof is run, and a chapter that fails its proof goes back to the model with the verdict, at most twice. To test out my idea, I focused on Python, picked ten common repos, and generated CodeStories for each repo. All chapters passed after at most two repairs, and the ten stories cost about $65 to write. One of the ten, itsdangerous, was used to build the pipeline, so it doesn’t count. The comparison is on the other nine.

**How I decided to judge it**

I needed a way to know whether CodeStories are good. As the builder, the reader, and the judge of this prototype, I needed a way to make sure that I wasn’t lying to myself. So I created a [preregistration](https://github.com/omoju/comprehension/blob/2c653907ca0ef7a67b8e9b08d5f7ed337858539f/PREREGISTRATION.md). I set the kill rule in advance, and recorded my own verdict before I looked at any metrics, so that I couldn’t go and create more reruns to get a better number.

To test the effectiveness of the approach, I used Cognition’s DeepWiki (generated wiki documentation, organised by the code’s structure, with links to source files). I picked DeepWiki because it is gaining traction, and it ranks near the top in exploring an unfamiliar codebase.

The two hypotheses, as preregistered:

**H1: Accountability.** CodeStories contain far fewer claims that contradict the code than DeepWiki pages.

**H2: Comprehension.** A reader given a CodeStory answers questions about the code at least as well as a reader given DeepWiki on general questions, and clearly better on questions about the intended-use path.

H1 is the core claim, while H2 is the riskier, newer claim. If you want the full mechanics, here are the two walk-throughs, [H1](https://omojumiller.com/comprehension/eval/explainer/h1.html), [H2](https://omojumiller.com/comprehension/eval/explainer/index.html).

| Outcome | Condition |
| :- | :- |
| Ship | H1: story contradiction density ≤ ½ of DeepWiki's, and general questions: story ≥ DeepWiki − 5 points, and path questions: story ≥ DeepWiki + 10 points. |
| Pivot | H1 holds, H2 does not: the checking works but the story form doesn't help. Next: apply the checking machinery to changes, i.e. stories of how a pull request changes the data's path. |
| Kill | H1 does not hold. |

One model did almost everything. Claude Opus 5, called through the API with no tools, no fine-tuning and no memory between calls, wrote the stories, rewrote both arms into checkable claims, wrote the quiz questions from the code and one traced run (never from either document), read each document and answered the questions, graded the answers against the keys, and judged the sampled claims against the source. Each of those roles was a fresh conversation that knew nothing of the others. Two things were not Claude: TypeSafe’s Jev (served on Cloudflare), which re-scored every verdict and also ran inside the pipeline as a paragraph check; and the other judge was me: I hand-checked 20 of the judged claims blind.

**What happened**

Each arm’s text (the CodeStory and the DeepWiki wiki for the same repository) was rewritten into atomic claims. Forty were sampled per repository per arm with a fixed random seed. This gave 360 story claims and 360 DeepWiki claims.

On accuracy, a CodeStory is no more accurate than DeepWiki's pages. The difference between them came down to three sentences. For the CodeStory arm, 10 sentences out of 360 were contradicted, while 7 of DeepWiki's were. Three sentences in 360 is noise, and the interval says so (95% interval on the ratio 0.55–4.86, which includes 1, where the two are equal).

The rule, though, wasn't written on the count. It was written on a rate: contradicted claims per 1,000 words, and on that rate the story came out worse, 0.71 to 0.54. The reason is not more mistakes. A story packs more checkable claims into every thousand words than a wiki does, so the same share of wrong claims comes out as more wrong per word. What this means is that DeepWiki is accurate at the sentence level.

On comprehension, given a CodeStory, a reader model was able to answer general code owner-style questions better than one given the DeepWiki wiki for the same repository, 76 to 56 points. Now, if the reader got path-based questions, questions about the traced run itself, CodeStory bested DeepWiki by 35 points: 98 vs 63. There are two caveats I need to point out here. First, there might be a bias: the model that wrote the stories was also the reader, and there is a chance that a reader likes their own prose. Second, the general questions were all on core modules the trace passed through.

The first time the judge ran, it said ship.

| judging pass | story unverifiable | DeepWiki unverifiable | story / 1k words | DeepWiki / 1k words | rule said |
| :- | :- | :- | :- | :- | :- |
| first | 243 / 360 | 137 / 360 | 0.07 | 0.69 | ship |
| second | 10 / 360 | 49 / 360 | 0.71 | 0.54 | kill |

**What the story got wrong**

From the story:

- **tqdm** · “The first thing `tqdm.__new__` does is `with cls.get_lock():`.” The judge: the first statement is `instance = object.__new__(cls)`; the lock is acquired afterwards.
- **rich** · “`Text.wrap` calls `divide_line(str(line), width, fold=True)` for each line.” The judge: `fold` is `wrap_overflow == "fold"`, not always `True`, and only in the non-`no_wrap` branch.

From DeepWiki:

- **requests** · “`Response.ok` is `True` if `status_code` is between 200 and 299.” The judge: `ok` is `True` for any status below 400, including 3xx.
- **markupsafe** · “The publish workflow is triggered on push of tags and on `workflow_dispatch`.” The judge: tags only; there is no `workflow_dispatch` trigger.

All seventeen, with the judge’s reason and the lines, are on [the accuracy explainer](https://omojumiller.com/comprehension/eval/explainer/h1.html).

The story’s errors are small misstatements of mechanism in otherwise accurate paragraphs. On the other hand, DeepWiki’s errors include two about CI workflow files and one about line numbers, the sort of claim a story never makes. The two are wrong about different things.

**The judge was the hard part**

On the first run, the verdict was **ship** because the judge was blind on large repositories and labelled what it couldn’t see as “unverifiable.” The judge reads the repo as a block of files that has to fit a budget. That block led with the README and docs, and in large repos that budget ran out before the source: for Textualize/rich, the judge saw 1 of about 80 modules.

I fixed this by putting the source files first, then the rest of the package, then the docs. The judge re-ran on the same claims; nothing else was re-run. Unverifiable counts as not contradicted, so a judge that can’t see the code flatters whichever arm it can’t check; both passes are published. The most important lesson from this experiment is to make sure to test the instrument on the hard case, and pay attention to the column that shows what the judge actually saw.

**Why I still read it as ship**

Once I got everything working correctly, I tested out a story myself to see if it made sense. I explored Textualize/rich’s story, [*What Actually Reaches the Terminal: Two Strings and a Table Through Rich*](https://omojumiller.com/comprehension/stories/bench/rich/).

I also noticed something else. As I explored the stories, something that had been foggy started to become clear to me. A codebase is a graph; often you don’t even know where to start. What a CodeStory does is scaffold you into the code by giving you first a premise.

It took me a while to realize why this act felt somewhat familiar; then I had an aha moment: “Oh, this is basically like a user story.” User stories come from product design; they say who wants what, and why, before anyone describes how it’s built. For example: as a developer, I want one GET to come back as a Response. A user story doesn’t describe the architecture; it tells you what the architecture is for, and only then do you go and look at it. Each chapter’s proof is the acceptance test that says the story is done. DeepWiki is the other kind of document, the architecture overview organised by module; it is accurate and complete, but it doesn’t tell you where to start.

User stories were never a correctness tool; nobody writes them to reduce bugs. They exist so that when you read the code you already know what it is supposed to be doing. H1 asked whether the story form made the sentences more accurate than DeepWiki’s, and it did not. H2 asked whether a reader with the premise understood the code better, and they did, by 20 points on general questions and 35 points on the path. The premise did what user stories do. Further, with everything that I now know, CodeStories are basically reverse-engineered user stories.

**Then a friend pointed it at a pull request**

Throughout building this prototype I would bounce ideas off of a friend. At some point, when I got the first few stories out, I sent them to him. He read them, and said, “You know what I really need? To see if this can work on a pull request.” Hmm, I thought. So I said, why not. I gave him access to the repository, he opened the pull requests himself, and the first change story was created. It was tested on a massive PR that had been sitting there. We both got online and did a walkthrough of the feature. The first thing I noticed was that, instead of feeling overwhelmed and not even knowing where to start with the PR, with a change story you know where to start. There is the premise, there is a clear path you can walk to know what changed, and then reason about the change.

**What’s next**

The part of this problem that is actually on fire is not understanding a library you chose to read; it is reviewing a pull request you didn’t write. So the first thing added after the decision was the pivot my own rule named: the same machinery telling the story of a change. It runs the PR’s own tests before and after, follows the same data through both versions, and makes each chapter’s proof one of the PR’s own test files, run before the change and after it: it has to fail before and pass after, so a proof can’t just restate the code. That exists today. It has run on a public pull request (unjs/ufo #313) and on three in a private TypeScript codebase: fifteen chapters, every proof right on both sides.

Applications are next, and they change the shape of the problem. A library has one intended use you can run offline. An application has a database, a queue, a clock and twenty user journeys, and its tests go flaky the moment they touch any of those. I don’t intend to make test suites reliable; I intend to make one run reproducible. Trace one user story, record everything that crosses a boundary (the queries and their rows, the HTTP out and back, the time, the randomness), and let the proofs replay the recording instead of the world. A recorded run can’t be flaky; it can only go stale, and stale is what the drift check is for. The story then says plainly what the run touched and what it didn’t, which is the one thing a reviewer most needs and never gets.

This is not a new fixation for me. Fimio pinned a run of a repository to a container and a manifest of everything it depended on, down to the driver version. It worked, and it was pulling me toward running infrastructure, which I didn’t want to spend the next decade on, so I wound it down and returned the cash. What I wanted from Fimio was the other half: not the frozen environment, but what the run did inside it. That is CodeStories. For applications I need both halves, and this time the environment half is CI’s job, not mine. CI is where someone has already made the application run, with the fixtures, the dummy database and the toolchain for every language in the repository. The story becomes a check on the pull request, next to the tests and the coverage. That is also the honest answer on languages: Python and TypeScript have tracers today; the rest get the skeleton of the run from the telemetry applications already emit, and line-level tracing only where it earns its keep.

Cycle 2 gets its own preregistration: the judge that caught all ten errors moves inside the pipeline, so accuracy is tested with the sentence read; the comprehension questions reach beyond the traced path; and the comparison controls for length. The rule gets written before the result, again. Everything, including the parts that went wrong, is at [github.com/omoju/comprehension](http://github.com/omoju/comprehension).

Onwards.

Where to look:

- The repository, <https://github.com/omoju/comprehension>
- The project home, <https://omojumiller.com/comprehension/>
- The stories gallery, <https://omojumiller.com/comprehension/stories/>
- The eval/results, <https://omojumiller.com/comprehension/eval/results.html>
- The explainers:
    - <https://omojumiller.com/comprehension/eval/explainer/>
    - <https://omojumiller.com/comprehension/eval/explainer/h1.html>
