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

  const currentUser = await prisma.user.findUnique({
    where: { id: userId }
  });

  if (currentUser && currentUser.role !== "ADMIN") {
    await prisma.user.update({
      where: { id: userId },
      data: { role: "ADMIN" }
    });
  }

  try {
    const users = await prisma.user.findMany({
      orderBy: { createdAt: "desc" }
    });

    const datasets = await prisma.dataset.findMany({
      include: {
        user: {
          select: { name: true, email: true }
        }
      },
      orderBy: { createdAt: "desc" }
    });

    const activityLogs = await prisma.activityLog.findMany({
      orderBy: { createdAt: "desc" },
      take: 100
    });

    const userCount = await prisma.user.count();
    const datasetCount = await prisma.dataset.count();
    const reportCount = await prisma.report.count();
    const sessionCount = await prisma.session.count();

    return NextResponse.json({
      status: "success",
      data: {
        users,
        datasets,
        activityLogs,
        stats: {
          userCount,
          datasetCount,
          reportCount,
          sessionCount
        }
      }
    });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

export async function POST(req: Request) {
  const session = await auth();
  let userId = session?.user?.id;
  if (!userId) {
    const defaultUser = await getOrCreateDefaultUser();
    userId = defaultUser?.id || "default-user";
  }

  try {
    const { action, userId: targetUserId, role } = await req.json();
    if (action === "update_role") {
      const user = await prisma.user.update({
        where: { id: targetUserId },
        data: { role }
      });
      return NextResponse.json({ status: "success", user });
    }
    
    if (action === "delete_user") {
      await prisma.user.delete({
        where: { id: targetUserId }
      });
      return NextResponse.json({ status: "success" });
    }
    
    return NextResponse.json({ error: "Invalid Action" }, { status: 400 });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
