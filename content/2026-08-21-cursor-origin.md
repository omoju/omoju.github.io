Title: Notes on Origin
Date: 2026-08-28
Category: Blog
Tags: ai, developer-tools, software-engineering
Slug: on-origin
Description: Cursor shipped Origin, but GitHub's moat was never the git server. The next war is custody.

About two weeks ago I read a beautiful technical essay on the history of git and its evolution written by Vicent Martí aka [@vmg](https://x.com/vmg/status/2089763058721730990?s=20), one of the few people on earth qualified to do that subject justice. @vmg spent ten years at GitHub (GH) building its git infrastructure. Today he's at SpaceX (Cursor), building Origin, a large scale git hosting service, the logical competitor to GH. But go look at his GH profile, [libgit2](https://github.com/libgit2/libgit2) is _still_ pinned there. His bio still reads "Previously: @github (this website, yo)." The man is building the thing that's meant to replace GH, and his entire record still lives on the incumbent.

That detail is the whole story of this essay. The ability to build the git server walked out the door with him. The social graph did not. When SpaceX (Cursor) shipped Origin, it gave me the final push to write down something I've been circling since Fimio: using GH as an object to think with, as Papert would say, to work out what the coding platform war actually looks like in the agent era.

**The New Loop**

First, my product wish. I want a product that is a marriage of GH and AWS. I want one seamless experience from intent to prod, and I think SpaceX is the only company that can build it; a true vertically integrated developer experience around tooling. My desire for this came from working on the two separate halves of that marriage. At Fimio, we built a platform that was like Vercel but for Python ML load backends. You can see the demo below.

<figure>
  <div class="video-embed">
    <iframe src="https://player.vimeo.com/video/1222256645?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
            allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share"
            referrerpolicy="strict-origin-when-cross-origin"
            title="Building a FastAPI chatbot with LlamaIndex on Fimio"></iframe>
  </div>
  <figcaption>Building a FastAPI chatbot with LlamaIndex on Fimio, from repo to a live
  deployment. 8 min 6 sec.</figcaption>
</figure>

Instead of hosting the deployment forever, I made the decision to keep it live for an hour (we built Fimio as a testing platform). Why? I didn't want the product creep: I was building the solution for "but it worked on my machine, and now it's broken in prod," and at that time, I wasn't interested in Fimio becoming a neo cloud. The code-build-deploy loop for an agentic era is a chance to own the entire surface under one banner and make trivial what used to be tedious.

**The Moat**

Now let's get to the meat and potatoes of GH, aka demystify its moat. Lets remember that GH was built as a "social coding platform." So it's 2 things: 1, a social network for developers, and 2, a collaborative code hosting platform. 
All the devs that you admire are there, the most important projects are there, which means the eyeballs that matter are also there. The collaborative tools around code make it stick. Codeowners, branch protection, issues, actions, packages, code scanning, all those nit-picky Role-Based-Access-Control (RBAC) configs that make life possible for enterprise repos. Without these features, GH is just a git server in the cloud. Case in point, @vmg, he left and went to build a new git server, but he could not take his social graph with him.

Together, these features create a formidable workflow gravity that keeps sucking developers in and yields enterprise trust. GH is already entrenched in the workflows of most companies. Even new employees don't have to onboard, they come with their own GH handles, all the company needs to do is just add that handle to their org, and boom, the new employee is ready to go and inherits the security and compliance structure of the enterprise. We are talking about a compliance officer's dream, good enough for banks and governments.


The final boss level moat of GH is the fact that it is the home of open source and enjoys 2 different monopoly mechanics. First, the most important open source projects are hosted on GH, and second, in 2020, GH acquired npm; the default package registry for JavaScript/Node.JS, which underpins most of the internet's frontend, and a significant portion of backends as well. Every time an `npm install` happens, that's pulling from GH. That open source dominance has GH being both the best real estate on the internet, and being unavoidable infrastructure via npm. And oh by the way, about 96% of all enterprise code is based on open source. Go ahead and marinate on that for a lil' bit. As we would say in Yoruba, "bàbá ńlá" network effects.

**The Next War Is Custody**

Alas, all is not lost for anyone that wants to take on GH. There is no disputing, GH has won the war on distribution. The next war is for custody. In this new codegen era, what matters is knowing exactly who, or what, touched a change at every step from prompt to production. Maintaining a chain of custody is the **key unlock** to provenance. This is the thing we were reaching for at Fimio, where we answered the CI/CD half of the problem by making every single thing a SHA and storing it. In this codegen era, provenance is going to matter more than distribution. If you solve provenance, you have a shot at winning.

Origin has already built most of the machinery for this without calling it that. In [their write-up of how they built it](https://cursor.com/blog/git-at-any-scale), they keep full provenance data for every push and every repack, with a write-ahead log in S3 as the source of truth; every state the repository has ever been in, durable and replayable. That is a ledger. But look at what the ledger records. This is provenance of repository state, not of authorship. In the entire post, the only appearance of the word author is the byline. Custody, attribution, identity: not once. And unlike everyone else playing in this game, SpaceX can do something most of the others can't. If they invest deeply into being a neo cloud, they can create that unbroken chain from intent to prod.

**The status economy is the sleeping giant aka humans need to brag**

One final note for Origin, even if they manage to thread the needle from intent to prod, they will still not be home free for they need to address the issue of the **status economy**. OG GH was invented in the era where coding was humans writing for other humans. And in that transmission, we passed along way more than syntax. Without knowing it, we passed along status, judgment, and standard. And out of that emerged reputation. Below you can see a realtime visualization of all these metrics.

<figure>
  <div class="video-embed">
    <iframe src="https://player.vimeo.com/video/951284486?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
            allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share"
            referrerpolicy="strict-origin-when-cross-origin"
            title="GitHub — Gitmos Data Visualization"></iframe>
  </div>
  <figcaption>Gitmos, a realtime visualization of GitHub social graph.</figcaption>
</figure>

*An aside, because I earned it: I shipped this while at GH, and it is something I am proud of. How it came to be is a post for another day.*

Back to the matter at hand.

Now here is the kicker, every authorship metric in software is about to die. All those commits, green squares, PR counts and so on, all of them measure developer velocity, and agents make velocity infinite; which devalues the status of those metrics. Infinite things can't carry status. What survives is anything that measures the scarcity that remains: what depends on you, what you maintain, what you decided, what you refused to merge. Status in software is undergoing a migration from proof-of-output to proof-of-judgment, and no platform has built the instruments for it yet.

This is wildly important because **status** is one of the three legs holding up open source alongside learning and corporate sponsorship. And the leg the agent age breaks first is reputation-as-hiring-signal: when employers stop reading GitHub profiles because code is cheap, the strongest private incentive to do public work evaporates. That mechanism is not hypothetical; it is how @vmg got hired. He picked up [libgit2](https://github.com/libgit2/libgit2) through Google Summer of Code, and GH contracted him off the strength of that public work. Whoever builds the credential that replaces it captures the motivation flow of an entire profession. And that credential needs to be a legible, gaming-resistant record of judgment that employers actually trust.

Open source is drowning in contributions: maintainers are burning out under floods of plausible agent-generated PRs and slop vulnerability reports. The scarce resource is not code, it's **[stewardship](https://omojumiller.com/2026/08/14/what-is-luxury-and-what-has-that-got-to-do-with-software/)** aka review, maintenance, governance, and taste. A platform that makes human judgment legible and status-bearing isn't just building bragging rights; it's building the economic layer that keeps the commons alive when judgment is the bottleneck.

This puts GH in a tight spot and exposes a weakness that a challenger like Origin can leverage. A new platform can mint a new status currency without having to worry about demonetizing its existing status currency.

However, a status economy needs spectators. Bragging requires a public square; which is why the open questions I find most interesting about Origin are as follows:

- The GitHub-sync wedge is right, but sync-with-GitHub-as-source-of-truth is a dangerous resting place. What's the forcing function that flips source of truth? Detaching from GitHub is already possible, so why is it buried instead of easy to find?  
- Why aren't my public GitHub orgs and repos public by default on Cursor?   
- PR-shaped review is a human-era artifact. How far does the PR survive?  
- And the one I'd stay up at night on: Origin in paid-only beta has no free tier, no open source commons, no audience. GH became the home of open source by subsidizing it for free, forever. If the next generation of builders forms their muscle memory on GH's free tier, that final boss moat simply grows itself back within five years. The status economy is Origin's biggest clean-slate advantage, and it has nowhere to live until there's a public square to put it in.

The next billion builders are arriving. The platforms deciding what counts as custody and what counts as status are deciding how that arrival goes. Origin is one of the few places where those decisions are live, which is why I will be watching closely.  