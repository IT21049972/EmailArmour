/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.js'],
  theme: {
    extend: {
      colors: {
        primary: {
          100: '#3B7197',
          200: '#4A8DB7',
        },
        secondary: {
          100: '#74BDE0',
          200: '#A1E1FA',
        },
      },
    },
  },
  plugins: [],
};
