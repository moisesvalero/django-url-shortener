/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./shortener/templates/**/*.html",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Space Grotesk", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
    },
  },
  plugins: [],
}
