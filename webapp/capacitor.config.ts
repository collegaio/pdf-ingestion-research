import type { CapacitorConfig } from "@capacitor/cli";

const config: CapacitorConfig = {
  appId: "com.collega.app",
  appName: "collega",
  // webDir: 'public',
  loggingBehavior: "debug",
  webDir: ".next/standalone/.next/server/app",
  plugins: {
    SplashScreen: {
      launchShowDuration: 0,
    },
  },
  server: {
    androidScheme: "https",
    hostname: "localhost:3000",
  },
  android: {
    loggingBehavior: "debug",
    webContentsDebuggingEnabled: true,
  },
};

export default config;
