# Westworld of Warcraft — Dev Blog

Source for the development blog at
**[lrhodes404.github.io/wwow-devblog](https://lrhodes404.github.io/wwow-devblog)**.

Built with [Jekyll](https://jekyllrb.com/) and the
[Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) theme. GitHub Actions builds and
deploys the site on every push to `main` — there is nothing to build locally.

## Writing a post

Add a file to `_posts/` named `YYYY-MM-DD-slug.md`:

```markdown
---
title: "Post title"
date: 2026-09-13 10:00:00 -0400
categories: [Origin]
tags: [wow, bots, reverse-engineering]
---

Body goes here.
```

Commit and push. The build takes about a minute; progress is in the Actions tab.

A post dated in the future will not publish until that date passes.

## License

Content © Lamar Rhodes. The Chirpy theme is MIT licensed; see [LICENSE](LICENSE).
