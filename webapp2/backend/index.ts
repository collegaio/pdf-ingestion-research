import cors from "@fastify/cors";
import fastifyRequestContext from "@fastify/request-context";
import { TypeBoxTypeProvider } from "@fastify/type-provider-typebox";
// import { Profile } from "@prisma/client";
// import { User } from "@supabase/supabase-js";
import fastify from "fastify";
import env from "./config/env";
// import { PORT } from "./config/keys";
// import ideasController from "./controllers/ideas.controller";
// import locationsController from "./controllers/locations.controller";
// import missionsController from "./controllers/missions.controller";
// import photosController from "./controllers/photos.controller";
// import profilesController from "./controllers/profiles.controller";
// import pushNotificationsTokenController from "./controllers/pushNotificationTokens.controller";
import conversationsController from "./routes/conversations.controller";
import studentsController from "./routes/students.controller";
import { BackendError } from "./models/error.model";
// import { prisma } from "./repositories/prisma";

const server = fastify({
  logger: true,
}).withTypeProvider<TypeBoxTypeProvider>();

server.setErrorHandler((error, request, reply) => {
  if (error instanceof BackendError) {
    const backendError = error as BackendError;
    // Log error
    // this.log.error(error);
    console.error(backendError.error);
    // Send error response
    reply.status(backendError.code).send(backendError.message);
  } else {
    // fastify will use parent error handler to handle this
    reply.send(error);
  }
});

server.get("/ping", async (request, reply) => {
  return "pong\n";
});

server.register(fastifyRequestContext, {
  defaultStoreValues: {
    authUser: null,
    profile: null,
    isAdmin: false,
  },
});

server.register(cors);
server.register(conversationsController, { prefix: "/conversations" });
server.register(studentsController, { prefix: "/students" });
// server.register(photosController, { prefix: "/photos" });
// server.register(locationsController, { prefix: "/locations" });
// server.register(missionsController, { prefix: "/missions" });
// server.register(ideasController, { prefix: "/ideas" });
// server.register(pushNotificationsTokenController, {
//   prefix: "/pushNotificationTokens",
// });

// server.addHook("onClose", async () => {
//   await prisma.$disconnect();
// });

server.listen({ port: env.PORT, host: "0.0.0.0" }, (err, address) => {
  if (err) {
    console.error(err);
    process.exit(1);
  }
  console.log(`Server listening at ${address}`);
});
