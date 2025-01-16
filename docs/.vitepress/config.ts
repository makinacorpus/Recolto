import { defineConfig } from 'vitepress'
import { generateSidebar } from 'vitepress-sidebar'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  lang: 'fr',
  title: "Documentation Recolt'Ô",
  description: '',
  srcDir: "content",
  base: "/",
  metaChunk: false,
  head: [
    ['link', {
      rel: 'icon',
      href: "/favicon.ico"
    }],
    ['meta', {
      property: 'og:image',
      content: 'https://raw.githubusercontent.com/makinacorpus/DbToolsBundle/main/docs/content/public/meta.png'
    }]
  ],
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    logo: '/logo.svg',
    nav: [
      { text: 'Accueil', link: '/' },
    ],
    editLink: {
      pattern: 'https://github.com/makinacorpus/recolto/blob/main/docs/content/:path',
      text: 'Modifier cette page sur Github'
    },
    docFooter: {
      prev: 'Page précédente',
      next: 'Page suivante'
    },
    outlineTitle: 'Sur cette page',
    lastUpdated: {
      text: 'Dernière mise à jour',
      formatOptions: {
        dateStyle: 'short'
      }
    },
    search: {
      provider: 'local'
    },
    footer: {
      message: 'Publié sous la licence MIT.',
      copyright: 'Copyright © 2024-aujourd\'hui <a href="https://makina-corpus.com/territoires">Makina Corpus Territoire</a>'
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/makinacorpus/recolto' }
    ],
    sidebar: generateSidebar({
      documentRootPath: 'content',
      // scanStartPath: null,
      // resolvePath: null,
      rootGroupText: 'Contenu',
      // rootGroupLink: 'https://github.com/jooy2',
      // rootGroupCollapsed: false,
      useTitleFromFileHeading: true,
      useTitleFromFrontmatter: true,
      // hyphenToSpace: true,
      // underscoreToSpace: true,
      collapsed: false,
      // collapseDepth: 2,
      sortMenusByFrontmatterOrder: true,
      // sortMenusOrderByDescending: true,
      // sortByFileName: ['first.md', 'second', 'third.md'],
      // excludeFiles: ['first.md', 'secret.md'],
      // excludeFolders: ['secret-folder'],
      // includeDotFiles: false,
      // includeRootIndexFile: false,
      // includeFolderIndexFile: true,
      // includeEmptyFolder: false,
      // convertSameNameSubFileToGroupIndexPage: false,
      // useFolderLinkAsIndexPage: false,
      // folderLinkNotIncludesFileName: false
    })
  }
})
