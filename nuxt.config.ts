// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  // devtools: { enabled: true },
  css: ["~/assets/css/main.css"],
  modules: [
    "@nuxt/content",
    "@nuxt/ui",
    [
      "@nuxtjs/google-fonts",
      {
        outputDir: "assets",
        families: {
          Montserrat: [400, 500, 600, 700],
        },
      },
    ],
    "@nuxtjs/i18n",
  ],
  runtimeConfig: {
    public: {
      CENTER_COORDINATES: process.env.NUXT_PUBLIC_CENTER_COORDINATES || [ 46.77373, 2.230225 ],
      ZOOM: process.env.NUXT_PUBLIC_ZOOM || 6,
    }
  },
  content: {
    documentDriven: true,
    experimental: {
      clientDB: true
    }
  },
  colorMode: {
    preference: 'light'
  },
  nitro: {
    preset: "service-worker",
    // prerender: {
    //   routes: ["/"],
    //   ignore: ['/blog/**', '/app', ]
    // },
  },
  i18n: {
    locales: [
      {
        code: 'fr-FR',
        file: 'fr-FR.json',
        name: "Français",
      },
      {
        code: 'en-US',
        file: 'en-US.json',
        name: "English"
      }
    ],
    lazy: true,
    defaultLocale: 'fr-FR',
  },
});
