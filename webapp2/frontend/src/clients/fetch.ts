import axios from "axios";
import { BACKEND_URL } from "../config/env";

const createAPIClient = () => {
  return axios.create({
    baseURL: BACKEND_URL,
    timeout: 120_000,
  });
};

export const apiClient = createAPIClient();

export const fetchJSON = async <T>(url: string) => {
  const response = await apiClient.get<T>(url);

  return response.data;
};
