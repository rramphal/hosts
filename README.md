# `hosts`

Instead of point to other people's lists and trusting them implicitly, this script downloads, validates, concatenates, deduplicates, and formats them all into a single file.
It also removes any whitelisted domains.

In `data/`, there are three folders (`blacklists`, `whitelists`, and `sources`) and `localhost.txt`.
`blacklists` and `whitelists` have text files with domains listed in the hosts format (not regex, etc.).
`sources` are lists of URLs that must first be downloaded and then treated as black/white-lists.
`localhost.txt` are the loopback / localhost domains.

## Lists

Name         | URL                                                                      | Description
------------ | ------------------------------------------------------------------------ | -----------
`blacklist`  | https://raw.githubusercontent.com/rramphal/hosts/master/lists/blacklist  | sourced blacklists + custom blacklists
**`hosts`**  | **https://raw.githubusercontent.com/rramphal/hosts/master/lists/hosts**  | `localhost.txt` + `blacklist` - `whitelist`

### Breaking Functionality

There are some domains that should not be blocked at the network level, but rather at the discretion of the user at the client level.
Blocking them at the network could break key functionality of some sites.
Instead, they could be blocked using a browser extension (for example, as a custom filter list within [uBlock Origin](https://github.com/gorhill/uBlock)).

#### Stripe

On April 21, 2020, [Michael Lynch](https://mtlynch.io/stripe-recording-its-customers/) reported that Stripe was silently recording user behavior on websites.
Categorically blocking Stripe would break payment functionality across many legitimate sites.
Stripe uses this tracking to drive the machine learning system that contributes to fraud prevention.
That said, this is only important when users are going to actually pay using Stripe.
If users are just browsing, there is no reason anyone needs to be tracking them.
Since Stripe has no way of knowing what users' intentions are, it's best left up to the users themselves to enable Stripe when relevant.
For that reason, there are some Stripe domains listed under `data/whitelist/ecommerce.txt`.

## Updating

1. `pip3 install -r requirements.txt`
1. Update relevant file in `/data` or create a new file with the `.txt` extension.
1. Run `python3 generate.py` to generate lists.

### Guidelines

* When listing domains in `/data/blacklists` or `/data/whitelists`, only list the domain itself.
* `www.` is prepended to custom lists domains automatically, but NOT to the sourced lists.
* Commented lines begin with `#`.

### Github Action

This repo contains a Github action that automatically updates the lists periodically and on push.

## Roadmap

* [x] Concatenate user blacklists
* [x] Concatenate user whitelists
* [x] Import external lists from source URLs
* [x] Automatically update lists periodically and on push
* [ ] Support DNSCrypt/regex domain formats
