import { Static, Type } from "@fastify/type-provider-typebox";
import type { StudentProfile as PrismaStudentProfile } from "@prisma/client";

// student profile
export const StudentProfileSchema = Type.Object({
  id: Type.String(),
  name: Type.Union([Type.String(), Type.Null()]),
  gender: Type.Union([Type.String(), Type.Null()]),
  geographicPreferences: Type.Union([Type.Array(Type.String()), Type.Null()]),
  schoolPreferences: Type.Union([Type.Array(Type.String()), Type.Null()]),
  majorInterests: Type.Union([Type.Array(Type.String()), Type.Null()]),
  classYear: Type.Union([Type.Number(), Type.Null()]),
  graduationYear: Type.Union([Type.Number(), Type.Null()]),
  unweightedGPA: Type.Union([Type.Number(), Type.Null()]),
  weightedGPA: Type.Union([Type.Number(), Type.Null()]),
});

export type StudentProfile = Static<typeof StudentProfileSchema>;

export const convertStudent = (
  student: PrismaStudentProfile
): StudentProfile => {
  const convertedStudent: StudentProfile = {
    id: student.id,
    name: student.name || "",
    gender: student.gender || "",
    geographicPreferences: student.geographic_preferences,
    schoolPreferences: student.school_preferences,
    majorInterests: student.major_interests,
    classYear: student.class_year || 0,
    graduationYear: student.graduation_year || 0,
    unweightedGPA: student.unweighted_gpa || 0,
    weightedGPA: student.weighted_gpa || 0,
  };

  return convertedStudent;
};

// Requests
export const StudentProfileParamsSchema = Type.Object({
  studentId: Type.String(),
});

export const UpdateStudentProfileSchema = Type.Partial(
  Type.Pick(StudentProfileSchema, [
    "name",
    "gender",
    "geographicPreferences",
    "schoolPreferences",
    "majorInterests",
    "classYear",
    "graduationYear",
    "unweightedGPA",
    "weightedGPA",
  ])
);

export type UpdateStudentProfile = Static<typeof UpdateStudentProfileSchema>;
