# Comment Voice

Comments explain *why*, not *what*. Assume the reader can already read Python.
A comment earns its place by adding judgment, context, or a caveat the code
itself can not carry.

## Write like this

- First person when a judgment call was involved:
  "I am asserting on the response body here, not just the status code, because
  a 200 can still hide a validation failure that only shows in the payload."
- Hedge honestly when not fully sure why something is the way it is:
  "Not entirely sure why this wait is 2 seconds rather than the default,
  it predates this test, leaving it as is rather than guessing at a change."
- Plain declarative sentences for anything that is just a fact, no performance
  needed: "Token is fetched once per session, not per test, since login is not
  what this suite is testing."

## Never write like this

- No emojis, anywhere, including in commit messages and docstrings.
- No AI-stock phrasing: "This function handles the edge case where...",
  "Note: it is important to...", "This ensures that...". If you catch yourself
  writing "ensures that", ask what you actually mean and say that instead.
- No comments that just restate the line below them ("# loop through users"
  above "for user in users:").
- No exclamation marks. No "simply" or "just" when describing something that
  was not simple, that is a tell, not a description.

## Before / after

Generic AI comment (avoid):
    # This function handles the validation of the user is email address
    # to ensure data integrity throughout the system.
    def validate_email(email):

In your voice (target):
    # Checking format only here, not deliverability, since the signup flow
    # confirms via email anyway and a stricter check here just slows things down.
    def validate_email(email):
