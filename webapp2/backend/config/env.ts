import dotenv from "dotenv";

dotenv.config({
  path: ".env",
});

export default {
  NODE_ENV: "development",
  DATABASE_URL: process.env.DATABASE_URL,
  CHAT_API_ENDPOINT: process.env.CHAT_API_ENDPOINT,
  PORT: process.env.PORT ? parseInt(process.env.PORT) : 3000,
};

// export const DATABASE_URL: z.string().url(),
// export const NODE_ENV: z
//       .enum(["development", "test", "production"])
//       .default("development"),
//     CHAT_API_ENDPOINT: z.string(),
//   },
