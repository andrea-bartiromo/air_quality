export default defineNuxtConfig({
  pages: true,                 // forza l'uso della cartella "pages/"
  srcDir: '.',                 // radice = questa cartella
  dir: { pages: 'pages' },     // posizione esplicita delle pagine
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:5001/api'
    }
  }
})
