// NOTE: these must be specified at build time
console.log(import.meta.env.VITE_SOME_KEY);
console.log(process.env.VITE_APP_BACKEND_URL);

const mode = import.meta.env.MODE;

let BACKEND_URL = "http://localhost:3000";

if (mode === "production") {
  BACKEND_URL = "https://communist-loise-collega-b748a8e9.koyeb.app";
}

export { BACKEND_URL };
