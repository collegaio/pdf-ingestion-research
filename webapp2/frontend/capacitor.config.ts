import { CapacitorConfig } from "@capacitor/cli";

const config: CapacitorConfig = {
  appId: "com.collega.app",
  appName: "Collega",
  webDir: "dist",
  plugins: {
    Keyboard: {
      resize: "native",
      // "style": "DARK",
      // resizeOnFullScreen: true,
    },
  },
  server: {
    androidScheme: "https",
    url: "http://localhost:5173",
  },
};

export default config;
