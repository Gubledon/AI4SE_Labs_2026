# Task 1 Report

All three frameworks come from the list at https://frompting.com/frameworks. I left out ROSES and zero-shot, as the assignment asks.

The problem in Task 2 is text-to-SQL. There are 156 questions about restaurants, and each one has to become a SQLite query that returns exactly the right rows. Most questions follow a handful of templates (a city or region, a food type, a street, a minimum rating, or "the best" place). Many are also padded with nonsense about picnics and pancakes that the model has to ignore. I wanted three frameworks that steer the model in different ways, so the comparison in Task 2 tells me something.

## CO-STAR

Source: https://frompting.com/frameworks/co-star

CO-STAR splits a prompt into Context, Objective, Style, Tone, Audience and Response. I picked it because it is the most common general-purpose framework on the site, and because it has a slot for the audience and the response format. My audience here is an evaluation script that runs whatever SQL comes back, so it helps to say that outright. The prompt spells out every rule in plain words and asks for one line of SQL and nothing else.

I expect it to be the fastest of the three, since the answer is short. Accuracy should be good on the common questions. I'm less sure about the odd ones, like the questions about a city called "unknown", because the model never sees a finished query.

## Chain of Thought

Source: https://frompting.com/frameworks/cot

Chain of Thought makes the model reason in steps before it answers. My prompt walks it through four of them. First it cuts the question down to the actual request, then it pulls out the city, street, food type and rating. Next it turns each of those into a condition, and only then writes the query. It also has to list its assumptions and read the query back to check it.

I chose it because two parts of this task really are reasoning: getting rid of the filler text and splitting the request into pieces. The site says CoT is a poor fit for simple lookups and for output that a program has to parse. Both apply here, and that's part of why I want to test it. I expect it to handle the long, noisy questions best. It will also be clearly the slowest, because every answer comes with its working.

## Few-Shot

Source: https://frompting.com/frameworks/few-shot

Few-shot gives the model worked examples to copy. My prompt has seven question and SQL pairs, one for each type of question in the dataset. I made the examples up, so none of the test questions appear in the prompt.

The questions are very repetitive, and the site recommends few-shot for exactly that kind of pattern-following work. A complete example query also shows things that are awkward to describe in words, like the subquery for "best" or how to escape an apostrophe in a name. I think this one will score highest on accuracy. The risk is that the model copies a value from an example instead of the question, or gets stuck on a question type the examples don't cover.

All three prompts get the same database schema and must return the query inside `<sql>` tags. The only real difference between them is the framework.
