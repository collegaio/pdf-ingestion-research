import axios from "axios";
import { env } from "~/env";

const createChatAPIClient = () => {
  return axios.create({
    baseURL: env.CHAT_API_ENDPOINT,
    timeout: 30_000,
  });
};

const chatAPIClient = createChatAPIClient();

export const callChatAPI = async (message: string, history: string[]) => {
  const response = await chatAPIClient.post<{ message: string }>("/chat", {
    message: message,
    chat_history: history,
  });

  return response.data.message;
};
