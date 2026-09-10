import http from "http";
import { Server } from "socket.io";
import { connectDb } from "./utils/db-config.tsx";
import { PORT } from "./lib/constants.ts";
import { listen } from "./socket.ts";
const httpServer = http.createServer();

const io = new Server(httpServer, {
  cors: {
    origin: "http://localhost:5173",
  },
});

async function startServer() {
  await connectDb();

  httpServer.listen(PORT, () => {
    console.log(`Personal AI Server is live on port: ${PORT}`);
  });

  listen(io);
}

startServer();
