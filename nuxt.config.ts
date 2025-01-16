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
  ],
  runtimeConfig: {
    public: {
      CENTER_COORDINATES: process.env.NUXT_PUBLIC_CENTER_COORDINATES || [43.6044, 1.4444],
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
});
