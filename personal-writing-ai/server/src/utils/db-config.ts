import mongoose from "mongoose";
import { DB_URI } from "../lib/constants.ts";

export async function connectDb() {
  try {
    if (!DB_URI) throw new Error("DB uri is required");
    await mongoose.connect(DB_URI);

    console.log("database connected");
  } catch (error) {
    console.log(error);
  }
}
