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
  studentId: string,
  message: string,
  history: { text: string; role: string }[]
) => {
  // TODO: add student_id
  const response = await chatAPIClient.post<{ message: string }>("/chat", {
    student_id: studentId,
    message: message,
    chat_history: history,
  });

  return response.data.message;
};
