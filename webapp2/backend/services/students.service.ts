import { db } from "../clients/db";
import { UpdateStudentProfile } from "../models/student.model";

// create student profile
export const createStudentProfile = async () => {
  const studentProfile = await db.studentProfile.create({
    data: {},
  });

  return studentProfile;
};

// get student profile
export const getStudentProfileByID = async (id: string) => {
  const studentProfile = await db.studentProfile.findUnique({
    where: { id },
  });

  return studentProfile;
};

// update student profile
export const updateStudentProfile = async (
  id: string,
  data: UpdateStudentProfile
) => {
  const studentProfile = await db.studentProfile.update({
    where: { id },
    data,
  });

  return studentProfile;
};
