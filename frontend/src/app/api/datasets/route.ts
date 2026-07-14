import { auth } from "@/auth";
import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";
import { getOrCreateDefaultUser } from "@/lib/user";

export async function POST(req: Request) {
  const session = await auth();
  let userId = session?.user?.id;
  if (!userId) {
    const defaultUser = await getOrCreateDefaultUser();
    userId = defaultUser?.id || "default-user";
  }

  try {
    const { name, sizeBytes, rowCount, colCount, storageUrl, status } = await req.json();

    if (!name) {
      return NextResponse.json({ error: "Missing dataset name" }, { status: 400 });
    }

    // Check if the dataset already exists under this user
    let dataset = await prisma.dataset.findFirst({
      where: { userId, name }
    });

    if (dataset) {
      // Update existing dataset
      dataset = await prisma.dataset.update({
        where: { id: dataset.id },
        data: {
          sizeBytes: sizeBytes || dataset.sizeBytes,
          rowCount: rowCount !== undefined ? rowCount : dataset.rowCount,
          colCount: colCount !== undefined ? colCount : dataset.colCount,
          storageUrl: storageUrl || dataset.storageUrl,
          status: status || dataset.status || "UPLOADED",
        }
      });
    } else {
      // Create new dataset record
      dataset = await prisma.dataset.create({
        data: {
          userId,
          name,
          sizeBytes: sizeBytes || 0,
          rowCount: rowCount || 0,
          colCount: colCount || 0,
          storageUrl: storageUrl || "local",
          status: status || "UPLOADED",
        }
      });
    }

    // Get the next version number
    const lastVersion = await prisma.datasetVersion.findFirst({
      where: { datasetId: dataset.id },
      orderBy: { version: "desc" }
    });
    const nextVersion = lastVersion ? lastVersion.version + 1 : 1;

    // Create the version record
    const datasetVersion = await prisma.datasetVersion.create({
      data: {
        datasetId: dataset.id,
        version: nextVersion,
        name: name,
        sizeBytes: sizeBytes || 0,
        rowCount: rowCount || 0,
        colCount: colCount || 0,
        storageUrl: storageUrl || "local",
        changeSummary: nextVersion === 1 ? "Initial Upload" : `Uploaded Version ${nextVersion}`,
      }
    });

    // Log this activity
    await prisma.activityLog.create({
      data: {
        userId,
        action: "DATASET_UPLOAD",
        metadata: {
          datasetId: dataset.id,
          datasetName: name,
          version: nextVersion,
          rowCount: rowCount,
          sizeBytes: sizeBytes,
        }
      }
    });

    return NextResponse.json({
      status: "success",
      dataset,
      version: datasetVersion,
    });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
