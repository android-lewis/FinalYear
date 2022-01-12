module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: false,
  theme: {
    fontFamily: {
      'body': ['Poppins'],
    },
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
