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
