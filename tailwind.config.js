/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./chat/templates/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark", "cupcake"],
  },
};

