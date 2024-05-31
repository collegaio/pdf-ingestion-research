import axios from "axios";

const createAPIClient = () => {
  return axios.create({
    timeout: 30_000,
  });
};

export const apiClient = createAPIClient();

export const fetchJSON = async <T>(url: string) => {
  const response = await apiClient.get<T>(url);

  return response.data;
};
