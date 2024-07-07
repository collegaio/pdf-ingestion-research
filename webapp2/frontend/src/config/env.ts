// NOTE: these must be specified at build time
console.log("mode:", import.meta.env.MODE);

const mode = import.meta.env.MODE;

let BACKEND_URL = "http://localhost:3000";

if (mode === "production") {
  BACKEND_URL = "https://communist-loise-collega-b748a8e9.koyeb.app";
}

export { BACKEND_URL };
