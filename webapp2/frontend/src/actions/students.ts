import { apiClient } from "../clients/fetch";
import { StudentResponse } from "../models/students";

export const createStudent = async () => {
  const response = await apiClient.post<StudentResponse>(`/students`);

  return response.data;
};
