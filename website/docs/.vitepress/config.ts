import { readFileSync } from 'node:fs'
import { join } from 'node:path'
import { defineConfig, type PageData } from 'vitepress'
import llmstxt from 'vitepress-plugin-llms'

// Published under https://docs.unlibra.com/tkinter-unblur/ as the GitHub
// Pages site of this repository (see .github/workflows/deploy-docs.yml).
const SITE_URL = 'https://docs.unlibra.com/tkinter-unblur/'

// FAQPage structured data built from the page's own "## Question" sections,
// so it always matches the text that readers see.
function faqPage(markdown: string) {
  const sections = markdown.replace(/^---\n[\s\S]*?\n---\n/, '').split(/^## /m).slice(1)
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: sections.map((section) => {
      const [question, ...answer] = section.split('\n')
      return {
        '@type': 'Question',
        name: toPlainText(question),
        acceptedAnswer: { '@type': 'Answer', text: toPlainText(answer.join('\n')) }
      }
    })
  }
}

const AUTHOR = { '@type': 'Person', name: 'unlibra', url: 'https://unlibra.com' }

function techArticle(pageData: PageData, url: string, description: string) {
  return {
    '@context': 'https://schema.org',
    '@type': 'TechArticle',
    headline: pageData.title,
    description,
    url,
    inLanguage: 'en',
    author: AUTHOR,
    isPartOf: { '@type': 'WebSite', name: 'tkinter-unblur', url: SITE_URL },
    ...(pageData.lastUpdated ? { dateModified: new Date(pageData.lastUpdated).toISOString() } : {})
  }
}

function toPlainText(markdown: string) {
  return markdown
    .replace(/```[^\n]*\n([\s\S]*?)```/g, '$1') // keep the code, drop the fences
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1') // keep the link text
    .replace(/[`*]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
}

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

  // Generates llms.txt, llms-full.txt and a Markdown copy of each page, for
  // coding agents and other LLM tools that read the docs.
  vite: {
    plugins: [
      llmstxt({
        domain: 'https://docs.unlibra.com',
        // The hint is hidden text on the home page, which search engines may
        // treat as cloaking. Pages still link to llms.txt in their <head>.
        injectLLMHint: false,
        // Unlike a hero-only landing page, the home page holds the
        // installation and usage instructions.
        excludeIndexPage: false
      })
    ]
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
          license: 'https://opensource.org/licenses/MIT',
          author: AUTHOR,
          sameAs: ['https://pypi.org/project/tkinter-unblur/']
        })
      ])
    } else {
      // Tells search engines and AI answer engines who wrote each page, what
      // it belongs to and when it last changed (lastUpdated is the date of
      // the page's last commit).
      head.push(['script', { type: 'application/ld+json' }, JSON.stringify(techArticle(pageData, url, description))])
    }

    if (pageData.relativePath === 'faq.md') {
      const markdown = readFileSync(join(siteConfig.srcDir, pageData.relativePath), 'utf-8')
      head.push(['script', { type: 'application/ld+json' }, JSON.stringify(faqPage(markdown))])
    }
  },

  head: [
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:site_name', content: 'tkinter-unblur' }],
    // The same OGP image as unlibra.com, for every site on docs.unlibra.com.
    ['meta', { property: 'og:image', content: 'https://unlibra.com/ogp.png' }],
    ['meta', { property: 'og:image:width', content: '1200' }],
    ['meta', { property: 'og:image:height', content: '630' }],
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
    // The shared unlibra icons, served from the root of docs.unlibra.com.
    ['link', { rel: 'icon', href: 'https://docs.unlibra.com/favicon.ico', sizes: '32x32' }],
    ['link', { rel: 'icon', type: 'image/svg+xml', href: 'https://docs.unlibra.com/favicon.svg' }],
    ['link', { rel: 'apple-touch-icon', href: 'https://docs.unlibra.com/apple-touch-icon.png' }],
  ],

  themeConfig: {
    // A full URL: a site path would get this site's base prepended.
    // alt: the brand, read before the site title in the link.
    logo: { src: 'https://docs.unlibra.com/brand/symbol.svg', alt: 'unlibra' },

    nav: [
      { text: 'Donate', link: 'https://unlibra.com/donate' },
      { text: 'PyPI', link: 'https://pypi.org/project/tkinter-unblur/' }
    ],

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
