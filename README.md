# `hosts`

My completely subjective list of domains to block.

## Lists

Name                          | URL
----------------------------- | ---
**`hosts`**                   | **https://raw.githubusercontent.com/rramphal/hosts/master/lists/blacklist**
`toggleable`                  | https://raw.githubusercontent.com/rramphal/hosts/master/lists/toggleable
`hosts-all` (not recommended) | https://raw.githubusercontent.com/rramphal/hosts/master/lists/all

NOTE: This repo assumes [Steven Black](https://github.com/StevenBlack)'s [fakenews-gambling](https://github.com/StevenBlack/hosts/tree/master/alternates/fakenews-gambling) `hosts` file as a base.

### What is the `toggleable` list?

There are some domains that should not be blocked at the network level, but rather at the discretion of the user at the client level.
Blocking them at the network could break key functionality of some sites.
Instead, they could be blocked using a browser extension (for example, as a custom filter list within [uBlock Origin](https://github.com/gorhill/uBlock)).

#### Case Study

An example of a domain that is toggleable is `m.stripe.com`.
On April 21, 2020, [Michael Lynch](https://mtlynch.io/stripe-recording-its-customers/) reported that Stripe was silently recording user behavior on websites.
Categorically blocking Stripe would break payment functionality across many legitimate sites.
Stripe uses this tracking to drive the machine learning system that contributes to fraud prevention.
That said, this is only important when users are going to actually pay using Stripe.
If users are just browsing, there is no reason anyone needs to be tracking them.
Since Stripe has no way of knowing what users' intentions are, it's best left up to the users themselves to enable Stripe when relevant.

## Updating

1. Update relevant file in `/data` or create a new file with the `.txt` extension.
2. Run `node generate.js` to generate lists.

### Guidelines

* `www.` is prepended to all domains automatically.
* Each file in `/data` must have a descriptive comment that starts with `#` as the first line of the file.
* Each file in `/data` must end with a blank line.
* When listing domains, only list the domain itself.
