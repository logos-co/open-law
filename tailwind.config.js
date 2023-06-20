/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './app/templates/**/*.html',
    './src/js/**/*.js',
    './node_modules/flowbite/**/*.js',
  ],
  theme: {
    extend: {
      fontSize: {
        20: '2rem',
      },
    },
  },
  plugins: [require('flowbite/plugin')],
};
