import { defineConfig } from 'vitepress'

// Published under https://docs.unlibra.com/tkinter-unblur/ as the GitHub
// Pages site of this repository (see .github/workflows/deploy-docs.yml).
const SITE_URL = 'https://docs.unlibra.com/tkinter-unblur/'

export default defineConfig({
  lang: 'en',
  title: 'tkinter-unblur',
  description: 'Fix blurry Tkinter applications on Windows 10/11 high-DPI displays',
  base: '/tkinter-unblur/',
  cleanUrls: true,
  // Also feeds <lastmod> in the sitemap; the deploy workflow fetches the full
  // git history for it.
  lastUpdated: true,

  sitemap: {
    hostname: SITE_URL
  },

  transformPageData(pageData, { siteConfig }) {
    // Matches the URLs cleanUrls serves: "foo/index.md" -> "foo/", "foo.md" -> "foo".
    const url = SITE_URL + pageData.relativePath.replace(/(^|\/)index\.md$/, '$1').replace(/\.md$/, '')
    const description = pageData.frontmatter.description ?? siteConfig.site.description
    const head = (pageData.frontmatter.head ??= [])
    head.push(
      ['link', { rel: 'canonical', href: url }],
      ['meta', { property: 'og:url', content: url }],
      ['meta', { property: 'og:title', content: pageData.title }],
      ['meta', { property: 'og:description', content: description }]
    )

    if (pageData.relativePath === 'index.md') {
      head.push([
        'script',
        { type: 'application/ld+json' },
        JSON.stringify({
          '@context': 'https://schema.org',
          '@type': 'SoftwareSourceCode',
          name: 'tkinter-unblur',
          description,
          url: SITE_URL,
          codeRepository: 'https://github.com/unlibra/tkinter-unblur',
          programmingLanguage: 'Python',
          runtimePlatform: 'Windows',
          license: 'https://opensource.org/licenses/MIT'
        })
      ])
    }
  },

  head: [
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:site_name', content: 'tkinter-unblur' }],
    ['meta', { name: 'twitter:card', content: 'summary' }],
    // The shared unlibra symbol, served from the root of docs.unlibra.com.
    ['link', { rel: 'icon', type: 'image/svg+xml', href: 'https://docs.unlibra.com/brand/symbol.svg' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
    [
      'link',
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400..700&family=Noto+Sans+JP:wght@400..700&display=swap'
      }
    ]
  ],

  themeConfig: {
    // A full URL: a site path would get this site's base prepended.
    logo: 'https://docs.unlibra.com/brand/symbol.svg',

    nav: [{ text: 'PyPI', link: 'https://pypi.org/project/tkinter-unblur/' }],

    socialLinks: [{ icon: 'github', link: 'https://github.com/unlibra/tkinter-unblur' }],

    sidebar: [
      {
        items: [
          { text: 'Introduction', link: '/' },
          { text: 'Why Tkinter Looks Blurry', link: '/why-blurry' },
          { text: 'Compared to ctypes', link: '/vs-ctypes' },
          { text: 'FAQ', link: '/faq' },
          { text: 'API Reference', link: '/api' }
        ]
      }
    ],

    search: {
      provider: 'local'
    },

    outline: [2, 3],

    editLink: {
      pattern: 'https://github.com/unlibra/tkinter-unblur/edit/main/website/docs/:path'
    }
  }
})
