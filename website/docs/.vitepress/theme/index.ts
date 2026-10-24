// The custom fonts replace Inter, so skip bundling and preloading it.
import DefaultTheme from 'vitepress/theme-without-fonts'
import type { Theme } from 'vitepress'
// Served from this site (no third-party font server), in unicode-range
// slices: a page loads only the slices of the characters it shows.
// Noto Sans, not Noto Sans JP: the pages are in English (the Japanese in
// code samples is in the mono font), and its 8 rules keep the stylesheet
// small where Noto Sans JP's 124 made most of it.
import '@fontsource-variable/noto-sans'
import '@fontsource-variable/geist-mono'
import './custom.css'

export default {
  extends: DefaultTheme
} satisfies Theme
