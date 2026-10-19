import { defineConfig } from 'vitepress'

// Published under https://docs.unlibra.com/tkinter-unblur/ as the GitHub
// Pages site of this repository (see .github/workflows/deploy-docs.yml).
export default defineConfig({
  lang: 'en',
  title: 'tkinter-unblur',
  description: 'Fix blurry Tkinter applications on Windows 10/11 high-DPI displays',
  base: '/tkinter-unblur/',
  cleanUrls: true,

  sitemap: {
    hostname: 'https://docs.unlibra.com/tkinter-unblur/'
  },

  head: [
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
