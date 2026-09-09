/** @type {import('tailwindcss').Config} */
module.exports = {
  // Tailwind scans these files for class names. The page scripts are inline, so
  // classes toggled at runtime (bg-[#0f172a]/95, backdrop-blur-md, bg-white/20,
  // opacity-100, ...) are picked up from the same files. If a script is ever
  // moved to an external .js file, add it here or those classes will be purged.
  content: ['./*.html'],
  theme: {
    extend: {
      colors: {
        navy: '#0f172a',
        gold: '#c2a67a',
      },
    },
  },
  plugins: [],
};
