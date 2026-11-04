# The check

The check reads one file holding exactly the text that will be sent: the email body or the chat message, with no subject line. It returns one of three tiers and an exit code, and lists every hit with its line.

```
check FILE --to ADDRESS_OR_NAME --channel email --save-draft
check - --to ADDRESS_OR_NAME --channel dm        (reads the draft from standard input)
```

## BLOCK (exit 2)

Any hit on the firm's hard rules. No pass is written. Hard rules are the things the owner has ruled out for good. A typical set:

- punctuation the owner never uses, such as a long dash;
- banned words and stock phrases, and filler transitions;
- announcement phrases of the "we're excited to" kind;
- internal labels left in a draft, such as a revision number;
- contrast shapes that define a thing by what it is not, in any punctuation: "It's not X. It's Y.", "a X, not a Y", "Not X. Y."

Each hit is listed with its line. Rewrite the sentence. Swapping the punctuation keeps the shape, and the shape is what was banned.

## FLAG (exit 1)

Things the owner might write, but has not yet:

- **Words and two-word phrases the owner has never written.** Names, web addresses, numbers and a short stoplist of common words are ignored.
- **Length.** A draft more than 1.5 times the median length of the owner's messages to this recipient. With too few messages to that person, the median for that kind of recipient is used, then the channel.
- **Swaps.** Any phrase the owner has replaced twice or more, shown with the owner's replacement.
- **Filler intensifiers,** allowed only in a warm social line.
- **A spaced short dash.**

A FLAG still writes a pass. Read each line and change what is not the owner's. A term the other person used in the thread can stay.

## PASS (exit 0)

None of the above.

## The pass file

On PASS or FLAG the check writes a pass named by a hash of the normalised text: markup stripped, curly quotes straightened, whitespace collapsed, letters lowercased. So a change in spacing or quote style keeps the pass, and a changed word loses it. Passes older than seven days are removed.

`--save-draft` also keeps the draft for the nightly match against what was sent.

## The gate

A hook runs before every send tool call. It refuses:

- a mail send, reply, forward or draft, or a chat send or scheduled send, whose exact text has no pass from the last 60 minutes;
- a browser click whose summary says send, post, publish, reply, submit or share, when no draft at all has passed in the last 30 minutes.

Messages only to the owner pass. Nothing else is stopped. Any error inside the hook lets the call through, so the gate can never break a turn. A refusal means the draft goes back to the examples.
