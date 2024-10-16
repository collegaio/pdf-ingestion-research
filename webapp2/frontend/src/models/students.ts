export interface StudentResponse {
  id: string;
}

export interface Student {
  id: string;
  name: string | null;
  unweightedGPA: number | null;
  geographicPreferences: string[] | null;
  // schoolPreferences: string[] | null;
  // majorInterests: string[] | null;
  // classYear: number | null;
  // graduationYear: number | null;
}

export interface StudentUpdate {
  name?: string;
  unweightedGPA?: number;
  geographicPreferences?: string[];
}
