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

  let members = await prisma.workspaceMember.findMany({
    where: { userId },
    include: {
      workspace: {
        include: {
          members: {
            include: {
              user: {
                select: {
                  id: true,
                  name: true,
                  email: true,
                  image: true,
                  role: true,
                }
              }
            }
          }
        }
      }
    }
  });

  let workspaces = members.map(m => ({
    id: m.workspace.id,
    name: m.workspace.name,
    type: m.workspace.type,
    ownerId: m.workspace.ownerId,
    userRole: m.role,
    members: m.workspace.members.map(member => ({
      id: member.id,
      userId: member.user.id,
      name: member.user.name || "Team Member",
      email: member.user.email,
      image: member.user.image,
      role: member.role,
    })),
  }));

  if (workspaces.length === 0) {
    const personal = await prisma.workspace.create({
      data: {
        name: "Personal Workspace",
        type: "PERSONAL",
        ownerId: userId,
      }
    });

    await prisma.workspaceMember.create({
      data: {
        workspaceId: personal.id,
        userId,
        role: "ADMIN"
      }
    });

    const team = await prisma.workspace.create({
      data: {
        name: "Data Intelligence Team",
        type: "TEAM",
        ownerId: userId,
      }
    });

    await prisma.workspaceMember.create({
      data: {
        workspaceId: team.id,
        userId,
        role: "ADMIN"
      }
    });

    try {
      const colleague = await prisma.user.create({
        data: {
          name: "Sarah Chen",
          email: "sarah.chen@agentix.com",
          role: "USER"
        }
      });
      await prisma.workspaceMember.create({
        data: {
          workspaceId: team.id,
          userId: colleague.id,
          role: "EDITOR"
        }
      });
      
      const viewer = await prisma.user.create({
        data: {
          name: "Marcus Aurelius",
          email: "marcus@agentix.com",
          role: "USER"
        }
      });
      await prisma.workspaceMember.create({
        data: {
          workspaceId: team.id,
          userId: viewer.id,
          role: "VIEWER"
        }
      });
    } catch (e) {
      console.warn("Could not seed demo team members", e);
    }

    members = await prisma.workspaceMember.findMany({
      where: { userId },
      include: {
        workspace: {
          include: {
            members: {
              include: {
                user: {
                  select: {
                    id: true,
                    name: true,
                    email: true,
                    image: true,
                    role: true,
                  }
                }
              }
            }
          }
        }
      }
    });

    workspaces = members.map(m => ({
      id: m.workspace.id,
      name: m.workspace.name,
      type: m.workspace.type,
      ownerId: m.workspace.ownerId,
      userRole: m.role,
      members: m.workspace.members.map(member => ({
        id: member.id,
        userId: member.user.id,
        name: member.user.name || "Team Member",
        email: member.user.email,
        image: member.user.image,
        role: member.role,
      })),
    }));
  }

  return NextResponse.json({ status: "success", workspaces });
}

export async function POST(req: Request) {
  const session = await auth();
  let userId = session?.user?.id;
  if (!userId) {
    const defaultUser = await getOrCreateDefaultUser();
    userId = defaultUser?.id || "default-user";
  }

  try {
    const body = await req.json();
    const { action, name, type, workspaceId, email, role, memberId } = body;

    if (action === "create") {
      const workspace = await prisma.workspace.create({
        data: {
          name,
          type: type || "TEAM",
          ownerId: userId,
        }
      });
      await prisma.workspaceMember.create({
        data: {
          workspaceId: workspace.id,
          userId,
          role: "ADMIN"
        }
      });
      return NextResponse.json({ status: "success", workspace });
    }

    if (action === "add_member") {
      let user = await prisma.user.findUnique({ where: { email } });
      if (!user) {
        user = await prisma.user.create({
          data: {
            email,
            name: email.split("@")[0],
            role: "USER"
          }
        });
      }

      const existing = await prisma.workspaceMember.findUnique({
        where: {
          workspaceId_userId: {
            workspaceId,
            userId: user.id
          }
        }
      });

      if (existing) {
        return NextResponse.json({ error: "User is already a member" }, { status: 400 });
      }

      const member = await prisma.workspaceMember.create({
        data: {
          workspaceId,
          userId: user.id,
          role: role || "VIEWER"
        }
      });

      return NextResponse.json({ status: "success", member });
    }

    if (action === "update_role") {
      const updated = await prisma.workspaceMember.update({
        where: { id: memberId },
        data: { role }
      });
      return NextResponse.json({ status: "success", member: updated });
    }

    if (action === "remove_member") {
      await prisma.workspaceMember.delete({
        where: { id: memberId }
      });
      return NextResponse.json({ status: "success" });
    }

    return NextResponse.json({ error: "Invalid action" }, { status: 400 });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
