import { auth } from "@/auth";
import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";
import { getOrCreateDefaultUser } from "@/lib/user";

export async function GET() {
  const session = await auth();
  let userId = session?.user?.id;
  if (!userId) {
    const defaultUser = await getOrCreateDefaultUser();
    userId = defaultUser?.id || "default-user";
  }

  let notifications = await prisma.notification.findMany({
    where: { userId },
    orderBy: { createdAt: "desc" },
  });

  if (notifications.length === 0) {
    const seed = [
      {
        userId,
        title: "AutoML Pipeline Completed",
        message: "Gradient Boosting model achieved 94.2% accuracy on Sales Dataset.",
        type: "success",
      },
      {
        userId,
        title: "Resource Warning",
        message: "GPU usage exceeded 85% during feature scaling phase.",
        type: "warning",
      },
      {
        userId,
        title: "Inference Engine Connected",
        message: "Successfully connected to Ollama Local Llama-3 model.",
        type: "success",
      },
      {
        userId,
        title: "Security Event",
        message: "New active session established from Chrome / Windows 11.",
        type: "info",
      }
    ];
    
    await prisma.notification.createMany({ data: seed });
    
    notifications = await prisma.notification.findMany({
      where: { userId },
      orderBy: { createdAt: "desc" },
    });
  }

  return NextResponse.json({ status: "success", notifications });
}

export async function POST(req: Request) {
  const session = await auth();
  let userId = session?.user?.id;
  if (!userId) {
    const defaultUser = await getOrCreateDefaultUser();
    userId = defaultUser?.id || "default-user";
  }

  try {
    const { action, id } = await req.json();
    if (action === "read_all") {
      await prisma.notification.updateMany({
        where: { userId },
        data: { read: true },
      });
      return NextResponse.json({ status: "success" });
    } else if (action === "read" && id) {
      await prisma.notification.update({
        where: { id, userId },
        data: { read: true },
      });
      return NextResponse.json({ status: "success" });
    }
    return NextResponse.json({ error: "Invalid Action" }, { status: 400 });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
