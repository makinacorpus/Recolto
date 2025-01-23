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
});
