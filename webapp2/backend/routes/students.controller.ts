import { Type, TypeBoxTypeProvider } from "@fastify/type-provider-typebox";
import { FastifyError, FastifyInstance, FastifyServerOptions } from "fastify";

import {
  createStudentProfile,
  getStudentProfileByID,
  updateStudentProfile,
} from "../services/students.service";
import {
  convertStudent,
  StudentProfileParamsSchema,
  StudentProfileSchema,
  UpdateStudentProfileSchema,
} from "../models/student.model";
import { ErrorSchema, NotFoundError } from "../models/error.model";

const router = (
  fastify: FastifyInstance,
  opts: FastifyServerOptions,
  done: (err?: FastifyError) => void
) => {
  fastify.withTypeProvider<TypeBoxTypeProvider>().post(
    "/",
    {
      schema: {
        response: {
          201: StudentProfileSchema,
        },
      },
    },
    async (_, response) => {
      const student = await createStudentProfile();

      return response.status(201).send(convertStudent(student));
    }
  );

  fastify.withTypeProvider<TypeBoxTypeProvider>().get(
    "/:studentId",
    {
      schema: {
        params: StudentProfileParamsSchema,
        response: {
          200: StudentProfileSchema,
        },
      },
    },
    async (request, response) => {
      console.log("get student:", request.params);
      const studentId = request.params.studentId;
      const student = await getStudentProfileByID(studentId);

      if (!student) {
        throw new NotFoundError("Student not found");
      }

      return response.send(convertStudent(student));
    }
  );

  fastify.withTypeProvider<TypeBoxTypeProvider>().put(
    "/:studentId",
    {
      schema: {
        params: StudentProfileParamsSchema,
        body: UpdateStudentProfileSchema,
        response: {
          200: StudentProfileSchema,
        },
      },
    },

    async (request, response) => {
      const studentId = request.params.studentId;
      const student = await updateStudentProfile(studentId, request.body);

      return response.send(convertStudent(student));
    }
  );

  done();
};

export default router;
