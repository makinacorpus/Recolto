// .vitepress/theme/index.js
import DefaultTheme from 'vitepress/theme'
import { h } from 'vue'
import './custom.css'
import MakinaCorpusHorizontal from './components/MakinaCorpusHorizontal.vue'
import MakinaCorpusSquare from './components/MakinaCorpusSquare.vue'

export default {
  extends: DefaultTheme,
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'aside-bottom': () => h(MakinaCorpusSquare),
      'home-features-after': () => h(MakinaCorpusHorizontal),
    })
  },
}