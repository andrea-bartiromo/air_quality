export default defineNuxtConfig({
  pages: true,
  srcDir: '.',
  dir: { pages: 'pages' },
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:5001/api'
    }
  }
})
