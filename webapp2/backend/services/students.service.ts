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
  update: UpdateStudentProfile
) => {
  const studentProfile = await db.studentProfile.update({
    where: { id },
    data: {
      name: update.name,
      gender: update.gender,
      geographic_preferences: update.geographicPreferences ?? [],
      school_preferences: update.schoolPreferences ?? [],
      major_interests: update.majorInterests ?? [],
      class_year: update.classYear,
      graduation_year: update.graduationYear,
      unweighted_gpa: update.unweightedGPA,
      weighted_gpa: update.weightedGPA,
    },
  });

  return studentProfile;
};
