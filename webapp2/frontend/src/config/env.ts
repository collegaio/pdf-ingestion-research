// NOTE: these must be specified at build time
console.log(process.env.VITE_APP_BACKEND_URL);
export const BACKEND_URL =
  process.env.VITE_APP_BACKEND_URL || "http://localhost:3000";
