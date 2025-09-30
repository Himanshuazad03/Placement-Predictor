/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./views/**/*.{ejs,html}",   // your EJS templates
    "./public/**/*.js"           // any client-side JS
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
