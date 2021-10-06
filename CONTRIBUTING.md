# How to Contribute to Code Thesaurus

Hello! I'm glad you're reading this because Code Thesaurus can always use more help adding language data, fixing site bugs, working on documentation, and more!

## Code of Conduct

We as members, contributors, and leaders pledge to make participation in our community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

We pledge to act and interact in ways that contribute to an open, welcoming, diverse, inclusive, and healthy community.

You agree to follow our Code of Conduct while working on the project and/or being a part of any related communities. You can read that [here](https://github.com/codethesaurus/codethesaur.us/blob/main/CODE_OF_CONDUCT.md).

## Hacktoberfest

Code Thesaurus grew out of [@geekygirlsarah](https://twitter.com/geekygirlsarah) building it over Hacktoberfests 2018, 2019, and 2020. She's a strong encourager of working on Hacktoberfest, and so this is a project that has opted in!

Read on to learn how to take on issues or thesaurus data files to contribute!

## Check Out the Project

Head over to https://codethesaur.us to see how the site currently works. 

You can also head over to the [documentation site](https://docs.codethesaur.us) and read about how the site is designed and developed and how the core thesaurus files are created.

Some of the types of work we need here include:
* Working on site features or bugs filed as [Issues](https://github.com/codethesaurus/codethesaur.us/issues) on the project
* Adding programming language information to the thesaurus data files (see any issue tagged "ct-language-data")
* Adding new programming languages (those may not have issues but you're encouraged to add them)
* Working on documentation (see [the documentation repo](https://github.com/codethesaurus/docs/issues) for those issues, or just propose some changes!)

## Claiming An Issue

If you wish to claim a GitHub issue, please review the full issue as I try to make them as detailed as possible. If you wish to claim it, leave a comment indicating so. I can then officially add you as the assignee.

If I add you as an assignee, you'll have a week or so to either create a PR, or add comments indicating any updates. If I don't hear from you in a week, I'll try to check in. If I don't hear from you after about two weeks, you'll be unassigned.

If you're unassigned, you're always welcome to leave another comment to get added back again.

Read below about our Issue to PR process.

## Thesaurus Data Updates

The ultimate goal of Code Thesaurus is to provide the _best_ polyglot developer reference tool to any and all developers, regardless of language they code in. To that end, we'll need contributions not just on the website but to the actual thesaurus data files.

These won't have issues. Instead, they're openly designed to allow people to add new features to a language or to easily add a new language to the system.

Please read over the [documentation site](https://docs.codethesaur.us) to learn about how the thesaurus system works. Then feel free to work on adding or correcting a data set!

If you wish to officially claim a new lanuage not listed, please file a [New Issue](https://github.com/codethesaurus/codethesaur.us/issues/new/choose), add in the language and concept you plan to work on, and then I'll assign you to that.

## Reporting Bugs or Issues

Did you find a bug? Great! Make sure it's not already reported on our [Issues Page](https://github.com/codethesaurus/codethesaur.us/issues) page. If it's not, please open up a [New Issue](https://github.com/codethesaurus/codethesaur.us/issues/new/choose) and add it so I can look it over.

Please make your issue as detailed as possible! Add in the page or URL it happened at, what you were doing when the error occurred, or any other details important to the issue. I may contact you to try to get more details if I can't replicate it.

## From Issue to PR

Think you can tackle an issue? Great! 

1. First, fork the repo so you have your own copy of it
1. Create a new branch. You can name it whatever you want, but I'd recommend something descriptive, like `issue-123-fix-string-exception`
1. Make your changes! I suggest committing early and often.
1. Make sure you test the changes. Check out how to run the project on the [`README.md`](README.md) page.
1. If you can test the changes and they work reliably, then create a new pull request. Be sure to either add `Fixes #1234` or `Closes #1234` so GitHub can link your issue number automatically.
1. The CI/CD system should run tests (if applicable) and spin up a sample deploy of the app. 
1. I'll review it and leave any comments for things that may need to change. Changes aren't intended because your code is bad but more a consideration towards how it may work with other parts of the project or ways the user might interact with it.
1. Finally, we'll merge it in! 

Note: Due to the prolific spam at this year's Hacktoberfest, your PR may get marked as invalid or spam if it appears to not follow the request on the issue or appears to just be trying to get easy PRs for the shirt. If it's mistakenly marked as invalid/spam, please reach out so I can correct it.

## Adding New Features

I have a large roadmap for this project and will be adding lots of new features in the near future. For now, the present focus is on adding lots of language data into the site.

If you strongly believe there should be a new feature or something is really lacking on the site, you are welcome to add an [Issue](https://github.com/codethesaurus/codethesaur.us/issues/new/choose) and I'll consider it. 

## Adding or Revising Documentation

I want Code Thesaurus to be easy-to-use for anyone regardless of their experience label. That requires good documentation of many facets of the project. I will very much welcome any additional changes or suggestions on what to change or how to evolve the documentation so it's helpful for people to understand the technical side of the site.

## What About Cosmetic Patches?

Issues marked with a `frontend` tag are open to having the cosmetic changes fixed. If there are typos or other issues, you are welcome to try to correct those. However, frivolous PRs for unnecessary changes may be marked as invalid or spam.

## Have Questions or Problems?

Please feel free to reach out! You can:

* Tweet [@codethesaurus](https://twitter.com/codethesaurus) or [@geekygirlsarah](https://twitter.com/geekygirlsarah)
* Email [coreteam@codethesaur.us](mailto:coreteam@codethesaur.us)
* Add comments onto issues if they are specific to that issue

## Happy Hacking!
