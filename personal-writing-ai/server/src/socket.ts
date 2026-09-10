import { type Server } from "socket.io";
import { messageFormat } from "./utils/message.tsx";
import { runConversation } from "./utils/ollama.ts";

const bot = { name: "T-AI" };

export function listen(io: Server) {
  io.on("connection", async (socket) => {
    socket.on("joinRoom", ({ room }) => {
      socket.join(room);
    });

    socket.on("chatMessage", async (msg) => {
      // return console.log(msg.file);
      io.to("chat").emit("typing", messageFormat(bot.name));

      const response = await runConversation(msg?.text, [msg.file]);

      if (response.error) {
        io.to("chat").emit("message", messageFormat(bot.name, response.error));
      } else {
        io.to("chat").emit(
          "message",
          messageFormat(bot.name, response?.result),
        );
      }

      io.to(msg.room).emit("stopTyping", messageFormat(bot.name));
    });
  });
}
