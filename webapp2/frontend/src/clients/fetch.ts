import axios from "axios";

const createAPIClient = () => {
  return axios.create({
    baseURL: "http://localhost:3000",
    timeout: 120_000,
  });
};

export const apiClient = createAPIClient();

export const fetchJSON = async <T>(url: string) => {
  const response = await apiClient.get<T>(url);

  return response.data;
};
