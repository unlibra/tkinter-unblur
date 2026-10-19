# Website

This website is built using [VitePress](https://vitepress.dev/). The pages are in `docs/`, and the config and theme are in `docs/.vitepress/`.

## Installation

```bash
pnpm install
```

## Local Development

```bash
pnpm dev
```

This command starts a local development server. Most changes are reflected live without having to restart the server.

## Build

```bash
pnpm build
```

This command generates static content into the `docs/.vitepress/dist` directory. `pnpm preview` serves the built site locally.

## Deployment

Pushing changes under `website/` to `main` builds the site and deploys it to GitHub Pages with GitHub Actions.
