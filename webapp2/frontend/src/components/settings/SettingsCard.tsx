import { useEffect, useState } from "react";
import { AlertCircle, X } from "lucide-react";
import { useForm } from "react-hook-form";
import useSWR from "swr";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogClose,
  DialogFooter,
} from "@/components/ui/dialog";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
} from "@/components/ui/form";

import { Student } from "../../models/students";
import { ErrorResponse } from "../../models/errors";
import { fetchJSON } from "../../clients/fetch";
import { updateStudent } from "../../actions/students";
import { Alert, AlertDescription, AlertTitle } from "../ui/alert";

interface SettingsCardFormValues {
  name?: string;
  unweightedGPA?: number;
  geographicPreferences?: string[];
}

interface SettingsCardProps {
  studentId: string;
  onClose: () => void;
}

const SettingsCard = ({ studentId, onClose }: SettingsCardProps) => {
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const form = useForm<SettingsCardFormValues>();
  const {
    data: studentResponse,
    isLoading: isLoadingStudent,
    error: getStudentError,
    mutate: mutateStudent,
  } = useSWR<Student, ErrorResponse>(`/students/${studentId}`, fetchJSON);

  // Set error message if error fetching student
  useEffect(() => {
    if (getStudentError) {
      setErrorMessage(getStudentError.error);
    }
  }, [getStudentError]);

  // Set form values to student values
  useEffect(() => {
    if (studentResponse) {
      form.reset({
        name: studentResponse.name || undefined,
        unweightedGPA: studentResponse.unweightedGPA || undefined,
        geographicPreferences:
          studentResponse.geographicPreferences || undefined,
      });
    }
  }, [studentResponse, form]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    const { name, unweightedGPA, geographicPreferences } = form.getValues();

    const updateFn = async () => {
      const updatedStudent = await updateStudent(studentId, {
        name,
        unweightedGPA: unweightedGPA,
        geographicPreferences,
      });

      return updatedStudent;
    };

    try {
      const optimisticStudent: Student = {
        ...(studentResponse ? studentResponse : { id: studentId }),
        name: name || null,
        unweightedGPA: unweightedGPA || null,
        geographicPreferences: geographicPreferences || [],
      };

      const options = {
        optimisticData: optimisticStudent,
      };

      await mutateStudent(updateFn(), options);
      onClose();
    } catch (error) {
      console.error("Failed to update student:", error);
      setErrorMessage("Failed to update profile. Please try again.");
    }
  };

  return (
    <DialogContent className="">
      <DialogHeader className="flex flex-row items-center justify-between px-4 pt-4">
        <DialogTitle className="text-xl">Profile</DialogTitle>
        <DialogClose className="rounded-sm opacity-70 ring-offset-white transition-opacity hover:opacity-100 disabled:pointer-events-none data-[state=open]:bg-stone-100 data-[state=open]:text-stone-500 dark:ring-offset-stone-950 dark:focus:ring-stone-300 dark:data-[state=open]:bg-stone-800 dark:data-[state=open]:text-stone-400">
          <X className="h-4 w-4" />
          <span className="sr-only">Close</span>
        </DialogClose>
      </DialogHeader>

      <hr className="w-full border-t border-gray-200" />

      <div className="px-4 pb-4">
        {errorMessage && (
          <Alert
            variant="destructive"
            className="mb-4 flex items-center justify-between"
          >
            <div className="flex items-center">
              <AlertCircle className="mr-2 h-4 w-4" />
              <div>
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>{errorMessage}</AlertDescription>
              </div>
            </div>
            <button
              onClick={() => setErrorMessage(null)}
              className="text-sm font-semibold hover:text-red-700"
            >
              Dismiss
            </button>
          </Alert>
        )}

        {isLoadingStudent ? (
          <div className="flex min-h-40 items-center justify-center">
            <span className="loading loading-spinner loading-lg"></span>
          </div>
        ) : (
          <>
            <div className="space-y-4 pb-4">
              <Form {...form}>
                <FormField
                  control={form.control}
                  name="name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Name</FormLabel>
                      <FormControl>
                        <Input placeholder="Enter your name" {...field} />
                      </FormControl>
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="unweightedGPA"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Unweighted GPA</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="Enter your unweighted GPA"
                          {...field}
                        />
                      </FormControl>
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="geographicPreferences"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Location Preferences</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="Enter a location preference and press Enter"
                          onKeyDown={(e) => {
                            if (e.key === "Enter") {
                              e.preventDefault();
                              const input = e.target as HTMLInputElement;
                              const newPreference = input.value.trim();
                              if (newPreference) {
                                const currentPreferences = field.value || [];
                                field.onChange([
                                  ...currentPreferences,
                                  newPreference,
                                ]);
                                input.value = "";
                              }
                            }
                          }}
                        />
                      </FormControl>
                      <div className="mt-2 flex flex-wrap gap-2">
                        {field.value &&
                          field.value.map((preference, index) => (
                            <Badge
                              key={index}
                              variant="outline"
                              className="px-2 py-1"
                            >
                              {preference}
                              <button
                                className="ml-2 text-xs"
                                onClick={() => {
                                  const currentPreferences = field.value || [];
                                  currentPreferences.splice(index, 1);
                                  field.onChange(currentPreferences);
                                }}
                              >
                                ×
                              </button>
                            </Badge>
                          ))}
                      </div>
                    </FormItem>
                  )}
                />
              </Form>
            </div>

            <DialogFooter>
              <Button type="submit" onClick={handleSubmit}>
                Save changes
              </Button>
            </DialogFooter>
          </>
        )}
      </div>
    </DialogContent>
  );
};

export default SettingsCard;
