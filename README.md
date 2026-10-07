# fj-blanco.github.io

Personal research site built with Jekyll and hosted on GitHub Pages.

Pages and technical notes are written in Markdown. The shared HTML shell lives in
`_layouts/default.html`, and the site metadata is configured in `_config.yml`.

## Local development

Ruby and Bundler are required. Install the gems locally to the repository and
start the development server with live reload:

```sh
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll serve --livereload
```

The local site is available at <http://127.0.0.1:4000>.

## Research

The homepage links to `/research/`, with a catalogue and full reading pages for eight working papers. Each manuscript includes a visible work-in-progress notice, its AI disclosure, figures, and links to LaTeX, Markdown, references, and supporting code. Mathematical notation uses MathJax.

The research pages and downloads are synchronized from the research source collection. Update the authoritative manuscripts and regenerate the pages together. The catalogue is in `_data/research.json`; `_layouts/paper.html` supplies the paper header and source links. Compiled manuscript PDFs, ZIP archives, and private validation records are not included.
