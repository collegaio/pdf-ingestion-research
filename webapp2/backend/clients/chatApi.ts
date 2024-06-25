import axios from "axios";
import env from "../config/env";

const createChatAPIClient = () => {
  return axios.create({
    baseURL: env.CHAT_API_ENDPOINT,
    timeout: 120_000,
  });
};

const chatAPIClient = createChatAPIClient();

export const callChatAPI = async (
  message: string,
  history: { text: string; role: string }[]
) => {
  const response = await chatAPIClient.post<{ message: string }>("/chat", {
    message: message,
    chat_history: history,
  });

  return response.data.message;
};
