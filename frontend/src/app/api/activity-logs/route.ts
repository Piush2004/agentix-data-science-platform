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

  let logs = await prisma.activityLog.findMany({
    where: { userId },
    orderBy: { createdAt: "desc" },
    take: 50,
  });

  if (logs.length === 0) {
    const seed = [
      {
        userId,
        action: "USER_LOGIN",
        metadata: { ip: "127.0.0.1", device: "Chrome / Windows 11", status: "SUCCESS" },
      },
      {
        userId,
        action: "DATASET_UPLOAD",
        metadata: { datasetName: "Sales Data", rowCount: 1500, sizeBytes: 250482 },
      },
      {
        userId,
        action: "DATASET_CLEAN",
        metadata: { datasetName: "Sales Data", rowsRemoved: 14, missingImputed: 128 },
      },
      {
        userId,
        action: "MODEL_TRAIN",
        metadata: { datasetName: "Sales Data", modelType: "Gradient Boosting", accuracy: 0.942 },
      },
      {
        userId,
        action: "REPORT_GENERATE",
        metadata: { reportTitle: "Sales Performance Quarterly Report", format: "PDF" },
      }
    ];

    await prisma.activityLog.createMany({ data: seed });

    logs = await prisma.activityLog.findMany({
      where: { userId },
      orderBy: { createdAt: "desc" },
      take: 50,
    });
  }

  return NextResponse.json({ status: "success", logs });
}

export async function POST(req: Request) {
  const session = await auth();
  let userId = session?.user?.id;
  if (!userId) {
    const defaultUser = await getOrCreateDefaultUser();
    userId = defaultUser?.id || "default-user";
  }

  try {
    const { action, metadata } = await req.json();
    const log = await prisma.activityLog.create({
      data: {
        userId,
        action,
        metadata: metadata || {},
      },
    });
    return NextResponse.json({ status: "success", log });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
