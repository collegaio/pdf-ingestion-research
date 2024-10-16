import { apiClient } from "../clients/fetch";
import { Student, StudentResponse, StudentUpdate } from "../models/students";

export const createStudent = async () => {
  const response = await apiClient.post<StudentResponse>(`/students`);

  return response.data;
};

export const updateStudent = async (studentId: string, student: StudentUpdate) => {
  const response = await apiClient.put<Student>(`/students/${studentId}`, student);

  return response.data;
};
