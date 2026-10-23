// The custom fonts replace Inter, so skip bundling and preloading it.
import DefaultTheme from 'vitepress/theme-without-fonts'
import type { Theme } from 'vitepress'
import './custom.css'

export default {
  extends: DefaultTheme
} satisfies Theme
