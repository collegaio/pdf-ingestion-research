-- CreateTable
CREATE TABLE "student_profiles" (
    "id" TEXT NOT NULL,
    "name" TEXT,
    "gender" TEXT,
    "geographic_preferences" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "school_preferences" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "major_interests" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "class_year" INTEGER,
    "graduation_year" INTEGER,
    "unweighted_gpa" DOUBLE PRECISION,
    "weighted_gpa" DOUBLE PRECISION,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "student_profiles_pkey" PRIMARY KEY ("id")
);
